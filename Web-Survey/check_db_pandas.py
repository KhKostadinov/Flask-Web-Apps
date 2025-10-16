import pandas as pd
import sqlalchemy as q
import logging
import numpy as np
# ===========================
# Extract data from db
# ===========================
engine = q.create_engine('sqlite:///survey_data.db',echo=False)
df = pd.read_sql_table("srv1",engine)
# print(df[["record_id","status"]])

# ===========================
# Status check
# status = 1 => Complete
# status = 2 => Screened
# ===========================
df["err"] = ~df["status"].isin([1,2])
logging.basicConfig(level=logging.INFO,filename="dv_reports/DP.log",filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Check status: ")
if len(df[df["err"] == True]) > 0:
    df["err_detailed"] = df["err"].replace(True,"Accepted values: 1/2, recorded value: 0")
    df_status = df.loc[df["err"].eq(True),["record_id","status","err_detailed"]]
    err = "\nErrors in punching status: \n"
    err += df_status.to_string()
    err += "\n"
    logging.error(err)
else:
    logging.info("0 error records")

def error_logger(title: str, main_df: pd.DataFrame, err_message: str, var_list: list):
    logging.info(title)
    if len(main_df[main_df["err"] == True]) > 0:
        df_err = main_df.loc[df["err"].eq(True), var_list]
        err = "\n" + err_message + "\n"
        err += df_err.to_string()
        err += "\n"
        logging.error(err)
    else:
        logging.info("0 error records")


# ===========================
# Screener check
# Screening conditions: Age not in 18-99 , "None of the above" selected at Q3.
# ===========================

df["err"] = False
df["err_detailed"] = "False"
df.loc[~(df['q1'].between(18,99)) & (df["status"] != 2),'err'] = True
df.loc[~(df['q1'].between(18,99)) & (df["status"] != 2),'err_detailed'] = "Out of age range but not screened"
# print(df[["record_id","status","q1","Q3_0_99","err",'err_detailed']])
error_logger("Q1 term point: ",df,"Age out of allowed range",["record_id","status","q1","err","err_detailed"])

df["err"] = False
df["err_detailed"] = "False"
df.loc[(df['Q3_0_99'].eq(1)) & (df["status"] != 2),'err'] = True
df.loc[(df['Q3_0_99'].eq(1)) & (df["status"] != 2),'err_detailed'] = "None selected at Q3 but not screened"
# print(df[["record_id","status","q1","Q3_0_99","err",'err_detailed']])
error_logger("Q3 term point: ",df,"NotA selected but not screened:",["record_id","status","Q3_0_99","err","err_detailed"])

# ===========================
# Completes check
# ===========================
df = df[df["status"] == 1]
logging.info("#==================== CHECK OF QUALIFYING RESPONDENTS ====================#")
# print(df_completes)
#Q1 - Age 18-99
df["err"] = False
df["err_detailed"] = "False"
df.loc[~(df['q1'].between(18,99)), 'err'] = True
df.loc[~(df['q1'].between(18,99)), 'err_detailed'] = "Out of age range"
error_logger("Q1 ",df,"Age out of allowed range",["record_id","status","q1","err","err_detailed"])
#Q2 - codes 1-8 + 99
df["err"] = False
df["err_detailed"] = "False"
df.loc[~(df['q2'].isin([1,2,3,4,5,6,7,8,99])), 'err'] = True
df.loc[~(df['q2'].isin([1,2,3,4,5,6,7,8,99])), 'err_detailed'] = "Code not allowed/missing data"
error_logger("Q2 ",df,"Code not allowed",["record_id","status","q2","err","err_detailed"])
#Q3 - multi + exclusive - closed part
df["err"] = False
df["err_detailed"] = "False"
df['cnt1'] = df[df[['Q3_0_1','Q3_0_2','Q3_0_3','Q3_0_4','Q3_0_5','Q3_0_6','Q3_0_7','Q3_0_99']] == 1].count(axis=1)
df['cnt2'] = df[df[['Q3_0_1','Q3_0_2','Q3_0_3','Q3_0_4','Q3_0_5','Q3_0_6','Q3_0_7','Q3_0_99']].isin([0,1])].count(axis=1)
df.loc[df['cnt1'] == 0, 'err'] = True
df.loc[df['cnt1'] == 0, 'err_detailed'] = "0 selected"
df.loc[df['cnt2'] != 8, 'err'] = True
df.loc[df['cnt2'] != 8, 'err_detailed'] = "Something hidden"
df.loc[df['Q3_0_99'] != 0, 'err'] = True
df.loc[df['Q3_0_99'] != 0, 'err_detailed'] = "Exclusive selected"
error_logger("Q3 ",df,"Multiple choice errors",["record_id","status","cnt1","cnt2",'Q3_0_99',"err","err_detailed"])
#Q3 - multi + exclusive - open ended part
df["err"] = False
df["err_detailed"] = "False"
df.loc[(df['Q3_0_7'] == 1) & (df['Q3_1'].isnull()), 'err'] = True
df.loc[(df['Q3_0_7'] == 1) & (df['Q3_1'].isnull()), 'err_detailed'] = "Missing data"
df.loc[(df['Q3_0_7'] != 1) & (df['Q3_1'].notnull()), 'err'] = True
df.loc[(df['Q3_0_7'] != 1) & (df['Q3_1'].notnull()), 'err_detailed'] = "Extra data"
error_logger("Q3 OE",df,"Semi-OE errors",["record_id","status","Q3_0_7",'Q3_1',"err","err_detailed"])

#Q3_2 - grid masked by previous question
df["err"] = False
df["err_detailed"] = "False"

mask = ['Q3_0_1','Q3_0_2','Q3_0_3','Q3_0_4','Q3_0_5','Q3_0_6','Q3_0_7']
masked = ['Q3_2_1','Q3_2_2','Q3_2_3','Q3_2_4','Q3_2_5','Q3_2_6','Q3_2_7']
for q3,q3_2 in zip(mask, masked):
    df.loc[(df[q3] == 1) & ~(df[q3_2].isin([1,2,3,4,5,6,7,8,9,10])), 'err'] = True
    df.loc[(df[q3] == 1) & ~(df[q3_2].isin([1,2,3,4,5,6,7,8,9,10])), 'err_detailed'] = f"Missing data at {q3_2}"
    df.loc[(df[q3] != 1) & (df[q3_2].notnull()), 'err'] = True
    df.loc[(df[q3] != 1) & (df[q3_2].notnull()), 'err_detailed'] = f"Extra data at {q3_2}"

error_logger("Q3_2",df,"Q3_2 masked",["record_id","status","err",'Q3_0_6','Q3_0_7','Q3_2_6','Q3_2_7',"err_detailed"])