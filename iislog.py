import sys
import os
import argparse
import datetime
from sqlalchemy import  *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import label
from  iisLogDetail import  IIsLogDetail
import amiTools

class IIsLog():
    def __init__(self,argv):
       self.argv=argv

    def checkParams(self):
        parser=argparse.ArgumentParser()
        parser.add_argument('-d',dest="dir", action='store',help='directory')
        parser.add_argument('-c',dest="conn" ,action='store',help='ConnName')
        parser.add_argument('-e',dest="ext" ,action='store',help='file ext',default=".log")
        opts=parser.parse_args(self.argv)
        if (opts.dir==None or opts.ext==None or opts.conn==None ):
             print parser.print_help()
             return  False
        self.dir=opts.dir
        self.ext=opts.ext
        self.conn=opts.conn
        return True

    def checkDir(self):
        f1=os.path.exists(self.dir)
        if  f1 is False:
           print  self.dir+" dir not  exists!"

    def initConn(self):
       connString = amiTools.GetMsSqlConnStringByAmiConnName(self.conn)
       engine = create_engine(connString, echo=False)
       dbSession = sessionmaker(bind=engine)
       self.session = dbSession()


    def run(self):
        #****************************
        chk=self.checkParams()
        if chk==False:
           return
        #****************************
        if  self.checkDir() is False:
           return
        self.initConn()
        for root, dirs, files in os.walk(self.dir):
            for name in files:
               if name.endswith(self.ext)==True:
                  fullName=os.path.join(root,name)
                  #print  fullName
                  iisLogDetail=IIsLogDetail(self.session, fullName)
                  iisLogDetail.run()
                  self.session.commit()
        self.session.close()

if __name__=="__main__":
   # print  sys.argv[1:]
   d1=datetime.datetime.now()
   iisLog=IIsLog(sys.argv[1:])
   iisLog.run()
   d2=datetime.datetime.now()
   print  d2-d1


