from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///survey_data.db', echo=True)
meta = MetaData()
Base = declarative_base()

class Record(Base): # create datamap for the given survey
    __tablename__ = "srv1"
    record_id =Column(Integer, primary_key=True)
    status = Column(Integer)
    q1 = Column(Integer)
    q2 = Column(Integer)
    Q3_0_1 = Column(Integer)
    Q3_0_2 = Column(Integer)
    Q3_0_3 = Column(Integer)
    Q3_0_4 = Column(Integer)
    Q3_0_5 = Column(Integer)
    Q3_0_6 = Column(Integer)
    Q3_0_7 = Column(Integer)
    Q3_0_99 = Column(Integer)
    Q3_1 = Column(String)
    Q3_2_1 = Column(Integer)
    Q3_2_2 = Column(Integer)
    Q3_2_3 = Column(Integer)
    Q3_2_4 = Column(Integer)
    Q3_2_5 = Column(Integer)
    Q3_2_6 = Column(Integer)
    Q3_2_7 = Column(Integer)


# create the table itself
def create_tab():
    global meta, engine
    meta.create_all(engine)



# add new record;
def add_record(rec_data):
    # global engine, srv1
    Session = sessionmaker(bind=engine)
    session = Session()

    record = Record(status=rec_data["status"],
                               q1=rec_data["q1"],
                               q2=rec_data["q2"],
                               Q3_0_1=rec_data["Q3_0_1"],
                               Q3_0_2=rec_data["Q3_0_2"],
                               Q3_0_3=rec_data["Q3_0_3"],
                               Q3_0_4=rec_data["Q3_0_4"],
                               Q3_0_5=rec_data["Q3_0_5"],
                               Q3_0_6=rec_data["Q3_0_6"],
                               Q3_0_7=rec_data["Q3_0_7"],
                               Q3_0_99=rec_data["Q3_0_99"],
                               Q3_1=rec_data["Q3_1"],
                               Q3_2_1=rec_data["Q3_2_1"],
                               Q3_2_2=rec_data["Q3_2_2"],
                               Q3_2_3=rec_data["Q3_2_3"],
                               Q3_2_4=rec_data["Q3_2_4"],
                               Q3_2_5=rec_data["Q3_2_5"],
                               Q3_2_6=rec_data["Q3_2_6"],
                               Q3_2_7=rec_data["Q3_2_7"])
    session.add(record)
    session.commit()
