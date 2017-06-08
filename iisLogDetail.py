import sys
import argparse
from datetime import  datetime,timedelta
from sqlalchemy import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import label
from iislogmod import IIsLogMod
import amiTools


class IIsLogDetail():
    def __init__(self,session,logName):
       self.session=session
       self.logName=logName

    def run(self):
      with open(self.logName) as fp:
        for  fileLine in fp:
           if  fileLine[0]=="#":
               if  fileLine[1:5]=="Date":
                  iislogMod=IIsLogMod()
                  self.setDateObj(iislogMod,fileLine)
               else:
                   continue
           else:
              iislogMod=IIsLogMod()
              self.setObj(iislogMod,fileLine)
           self.session.add(iislogMod)

    def strToBeijingDate(self,strDate):
        strDate=strDate.strip()
        d1=datetime.strptime(strDate,"%Y-%m-%d %H:%M:%S")
        d2=d1+timedelta(hours=8)
        return  d2


    def setDateObj(self,iislogMod,fileLine):
         lines=fileLine.split(" ")
         iislogMod.log_file_name=self.logName
         iislogMod.str_date=lines[1]
         iislogMod.str_time=lines[2]
         iislogMod.cs_method="#Log init"
         strDate=lines[1]+" "+lines[2]
         beijingtime=self.strToBeijingDate(strDate)
         iislogMod.beijing_time=beijingtime

    def setObj(self,iislogMod,fileLine):
           lines=fileLine.split(" ")
           iislogMod.log_file_name=self.logName
           iislogMod.str_date=lines[0]
           iislogMod.str_time=lines[1]
           strDate=lines[0]+" "+lines[1]
           beijingtime=self.strToBeijingDate(strDate)
           iislogMod.beijing_time=beijingtime
           iislogMod.s_ip=lines[2]
           iislogMod.cs_method=lines[3]
           iislogMod.cs_uri_stem=lines[4]
           iislogMod.cs_uri_query=lines[5]
           iislogMod.s_port=lines[6]
           iislogMod.cs_username=lines[7]
           iislogMod.c_ip=lines[8]
           iislogMod.cs_User_Agent=lines[9]
           iislogModcs_Refer=lines[10]
           iislogMod.sc_status=lines[11]
           iislogMod.sc_substatus=lines[12]
           iislogMod.sc_win32_status=lines[13]
           iislogMod.time_taken=int(lines[14])

if  __name__=="__main__":
    connString = amiTools.GetMsSqlConnStringByAmiConnName("weblog")
    engine = create_engine(connString, echo=False)
    dbSession = sessionmaker(bind=engine)
    session = dbSession()
    iisLogDetail= IIsLogDetail(session,"c:/uniqserver/web1/ready.log")
    iisLogDetail.run()
    session.commit()
    session.close()

