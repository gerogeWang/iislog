import sys
import datetime
from sqlalchemy import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import label
import amiTools


reload(sys)
sys.setdefaultencoding('gbk')

BaseModel = declarative_base()

class IIsLogMod(BaseModel):
    __tablename__ = 'iis_log'
    Id=Column(Integer,autoincrement=True,primary_key=True)

    log_file_name=Column(String(100))
    beijing_time=Column(DateTime)
    str_date=Column(String(32))
    str_time=Column(String(32))
    s_ip=Column(String(50))
    cs_method=Column(String(100))
    cs_uri_stem=Column(String(1000))
    cs_uri_query=Column(String(1000))
    s_port=Column(String(100))
    cs_username=Column(String(100))
    c_ip=Column(String(100))
    cs_User_Agent=Column(String(200))
    cs_Refer=Column(String(200))
    sc_status=Column(String(50))
    sc_substatus=Column(String(50))
    sc_win32_status=Column(String(50))
    time_taken=Column(Integer)
    operate_time=Column(DateTime)



if __name__=="__main__":
    connString = amiTools.GetMsSqlConnStringByAmiConnName("weblog")

    # engine = create_engine(connString,echo=False)
    engine = create_engine(connString, echo=False)
    dbSession = sessionmaker(bind=engine)
    session = dbSession()

    iisLogMod=IIsLogMod()
    iisLogMod.str_date="1995" 
    iisLogMod.str_time="11:20:00"
    session.add(iisLogMod)
    session.commit()








