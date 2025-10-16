from csv import reader
from os import chdir
from lib.schema import QDetails

# chdir("..")
data = open("datamap.csv", "r")
variables = next(reader(data, delimiter=','))
data_status = 'valid'

def screener_check(screening_point, data):
    global variables, data_status

    if screening_point == "q1":
        if data["q1"] not in range(18, 100) and data["status"] != 2:
            data_status = 'invalid'
        elif data["q1"] not in range(18, 100):
            for i in variables[variables.index("q1")+1:]:
                if data[i] != None:
                    data_status = 'invalid'
                    break
    elif screening_point == "Q3_0_99":
        if data["Q3_0_99"] == 1 and data["status"] != 2:
            data_status = 'invalid'
        elif data["Q3_0_99"] == 1:
            for i in variables[variables.index("Q3_0_99")+1:]:
                if data[i] != None:
                    data_status = 'invalid'
                    break
    return data_status

def complete_check(check_point, data):
    global variables, data_status
    Q3cnt = 0
    q2opts = QDetails()
    q2opts.get_xml("qre.xml", "Q2")
    q3map = ["Q3_0_1", "Q3_0_2", "Q3_0_3", "Q3_0_4", "Q3_0_5", "Q3_0_6", "Q3_0_7"]
    q32map = ["Q3_2_1", "Q3_2_2", "Q3_2_3", "Q3_2_4", "Q3_2_5", "Q3_2_6", "Q3_2_7"]
    if check_point == "q1" and data["status"] == 1:
        if data["q1"] not in range(18, 100):
            data_status = 'invalid'
        else:
            data_status = 'valid'
    elif check_point == "q2" and data["status"] == 1:
        if str(data["q2"]) not in q2opts.option_ids:
            data_status = 'invalid'
        else:
            data_status = 'valid'
    elif check_point == "q3" and data["status"] == 1:
        if data["Q3_0_99"] == 1:
            data_status = 'invalid'
        elif data["Q3_0_99"] != 1:
            for i in q3map:
                if data[i] not in [0, 1]:
                    data_status = 'invalid'
                    break
                elif data[i] == 1:
                    Q3cnt += 1
            if Q3cnt == 0:
                data_status = 'invalid'
        else:
            data_status = 'valid'

    elif check_point == "q3_1" and data["status"] == 1:
        if data["Q3_0_7"] == 1 and data["Q3_1"] == "":
           data_status = 'invalid'
        elif data["Q3_0_7"] != 1 and data["Q3_1"] != "":
           data_status = 'invalid'
        else:
            data_status = 'valid'

    elif check_point == "q3_2" and data["status"] == 1:
        for x, y in zip(q3map, q32map):
            if data[x] == 1 and data[y] not in range(1, 11):
                data_status = 'invalid'
            elif data[x] != 1 and data[y] != None:
                data_status = 'invalid'
    else:
        pass
    return data_status

data.close()
