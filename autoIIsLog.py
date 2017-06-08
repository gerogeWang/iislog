import  os
import glob
import sys
import ConfigParser
import datetime
from sqlalchemy import  *
import amiTools

reload(sys)
sys.setdefaultencoding('gbk')

class AutoIIsLog:
    def __init__(self):
       self.genSection="gen"
       self.configFileName="autiIIsLog.config"
       self.pathList=[]
       self.ReadConfig()

    def initSection(self):
        connString = amiTools.GetMsSqlConnStringByAmiConnName("weblog")
        engine = create_engine(connString, echo=False)
        dbSession = sessionmaker(bind=engine)
        self.session = dbSession()



    def ReadConfig(self):
        if  os.path.exists(self.configFileName)==False:
            raise Exception( "config file=%s  not found  " % self.configFileName )
        cf = ConfigParser.RawConfigParser()
        cf.optionxform = str
        cf.read(self.configFileName)
        if  cf.has_option(self.genSection,"logSectionList")==False:
            raise Exception( "config file=%s logSectionList option  not exists!" % self.configFileName )
        self.logSections=cf.get(self.genSection,"logSectionList").split(",")
        self.dbConn=cf.get(self.genSection,"dbConn")
        self.cf=cf
        pathdict=[]
        for  section in  self.logSections:
           if  self.cf.has_option(section,"logPath")==False:
               raise Exception( "Section =%s logPath  option not exists!" % (section) )
           logPath=self.cf.get(section,"logPath")
           if os.path.exists(logPath)==False:
               raise Exception( "Path =%s not exits! " % (logPath) )
           if  pathdict[logPath]!=None:   #  if  path  exist  then  pass
               continue
           pathdict[logPath]=1
           dict={}
           dict["name"]=section
           dict["path"]=logPath
           self.pathList.add(dict)

    def  run(self):

        for  dictPath  in  self.pathList:
            serverName=dictPath["name"]
            serverPath=dictPath["path"]
            keyName=serverName+"_"+serverPath





