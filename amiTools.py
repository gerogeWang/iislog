# -*- encoding=utf-8 -*-…
# Create by QiQi on 2015/02/13
import  os
import shutil
import codecs
import glob
import datetime
import _winreg
from sqlalchemy import  *
import base64

#reload(sys)
#sys.setdefaultencoding('gbk')


##  expect 是 排除的 目录
def copyTree(src,dst,expect):
    z1=os.listdir(src)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if  type(expect) is list and  item.lower() in  [  x.lower() for x in expect  ]:
                continue;
            else:
                if os.path.exists(d)==False:
                    os.mkdir(d)
                copyTree(s,d,expect)
        else:
            shutil.copy2(s, d)



# Get parent dir
def getParentDir(dir):
   if  len(dir)==0:
      return  ""
   a=dir.split('\\')
   return  a[-1]

##  Create by QiQi on 2015/02/13  返回 按日期 命名的目录名 的下一个
def getDateDir(parentDir):
    now=datetime.datetime.now().strftime("%Y%m%d")
    sourceDir=os.path.join(parentDir,now+"*")
    a= [os.path.basename(x) for x in glob.glob(sourceDir)]
    i=len(a)+1
    while  True:
        dirName=now+"_"+str(i).zfill(2)
        if  dirName in a:
            i=i+1
        else:
            return  os.path.join(parentDir,dirName)

##
def CheckIsProgramKey(line):
      s=line.split(" ")
      for s1 in s:
         s2=s1.split("=")
         if len(s2)>1:
            skey=s2[0].strip()
            svalue=s2[1].strip()
            if (svalue.lower()=='"programkey"' or svalue.lower()=="'programkey'") and skey.lower()=="key":
                return True
      return False


def GetNowVersion(line):
     s=line.split(" ")
     for s1 in s:
        s2=s1.split("=")
        if len(s2)>1:
           skey=s2[0].strip()
           svalue=s2[1].strip()
           if skey.lower()=="value":
               svalue=svalue.replace('"',"")
               return svalue
     return ""

def CreateNewVersion(line):
     svalue=GetNowVersion(line)
     if svalue=="":
       return svalue
     vers=svalue.split(".")
     if len(vers)==1:
         return svalue+".001"
     else:
        if vers[-1].isdigit():
           vers[-1]=str(int(vers[-1])+1).zfill(3)
           return ".".join(vers)
        else:
           return svalue+".001"
     return  ""


def UpgradeWebConfig(fileName,isOverWrite):
    if os.path.exists(fileName)==False:
        return;
    f1=codecs.open(fileName,'r',encoding='utf8')
    result=[]
    oldVer=""
    newVer=""
    find=False
    for  line in f1.readlines():
        if CheckIsProgramKey(line):   ##  if find
            oldVer=GetNowVersion(line)
            newVer=CreateNewVersion(line)
            if oldVer!="" and newVer!="":
                line=line.replace(oldVer,newVer)
                find=True
        result.append(line)
    f1.close()
    if isOverWrite and find:
        shutil.copy2(fileName,fileName+".bak")
        f2=codecs.open(fileName,'w',encoding='utf8')
        f2.writelines(result)
        f2.close()
    return find,oldVer,newVer

def GetFileNum(dir,fileName,ext):
    #fileName, fileExtension = os.path.splitext(fileName)
    if ext!=None:
        fileName=fileName+"*."+ext
    else:
        fileName=fileName+"*.*"
    filePath=os.path.join(dir,fileName)
    list=glob.glob(filePath)
    return  len(list)

def GetTotalPackPre(cfType):
    return  cfType+"_total_"

def GetAjaxFilePre(cfType):
    return  cfType+"_Ajax_"

def GetWebFilePre(cfType):
    return  cfType+"_Web_"

def CheckDirCanWrite(dir):
    fileName=os.path.join(dir,"_temp_002002.test")
    try:
       filehandle = open(fileName,"w")
       filehandle.close()
    except Exception,e:
       return False
    else:
       os.remove(fileName)
    return True

def CheckRegConn(connName):
   regStr=r"SOFTWARE\\AmiSoft\\Connection\\"+connName
   try:
     aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
     aKey = _winreg.OpenKey(aReg, regStr,0,(_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
   except Exception,e:
       raise  Exception("Reg ="+regStr+"  can't open ")




def GetAmiRegValue(connName,keyName):
   aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
   regStr=r"SOFTWARE\\AmiSoft\\Connection\\"+connName
   aKey = _winreg.OpenKey(aReg, regStr,0,(_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
   #_winreg.OpenKey(aReg, regStr,0,(_winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
   strVal=_winreg.QueryValueEx(aKey, keyName)
   _winreg.CloseKey(aKey)
   str=strVal[0]
   if  keyName.lower()=="connstring" and str.lower().find("password")==-1:
       str=base64.decodestring(str)
   return str



#connString=mssql+pyodbc://sw:Thinkpad2010@10.10.10.21\sql2008R2CN/g2cn
def GetMsSqlConnStringByAmiConnName(connName):
    connString=GetAmiRegValue(connName,"connstring")
    if len(connString)>0:
        password=GetConnStrVal(connString,"password")
        userId=GetConnStrVal(connString,"UserID")
        serverName=GetConnStrVal(connString,"DataSource")  #Initial Catalog
        dbName=GetConnStrVal(connString,"InitialCatalog")  #InitialCatalog
        if password=="":
            raise Exception("amiTools.GetMsSqlConnString() password not found form string" )   # must in
        if userId=="":
            userId=GetConnStrVal(connString,"User")    # add USer
            if userId=="":
               raise Exception("amiTools.GetMsSqlConnString() user Id not found form string" )   # must in
        if serverName=="":
            serverName=GetConnStrVal(connString,"server")  #Initial Catalog
            if serverName=="":
               raise Exception("amiTools.GetMsSqlConnString() Data Source not found form string" )   # must in
        if dbName=="":
            dbName=GetConnStrVal(connString,"database")  #InitialCatalog
            if dbName=="":
               raise Exception("amiTools.GetMsSqlConnString() Initial Catalog not found form string" )   # must in
        #pyConnString="mssql+pyodbc://%s:%s@%s/%s" % (userId,password,serverName,dbName)
        pyConnString=GetMsSqlConnString(userId,password,serverName,dbName)
        return  pyConnString
    return  ""

def GetConnDbInfo(connName):
    connString=GetAmiRegValue(connName,"connstring")
    if len(connString)>0:
        password=GetConnStrVal(connString,"password")
        userId=GetConnStrVal(connString,"UserID")
        serverName=GetConnStrVal(connString,"DataSource")  #Initial Catalog
        dbName=GetConnStrVal(connString,"InitialCatalog")  #InitialCatalog
        return userId,password,serverName,dbName
    return "","","",""

def TestCreateEngine(connName):
    connString=GetMsSqlConnStringByAmiConnName(connName)
    db = create_engine(connString)
    conn = db.connect()
    #some simple data operations
    conn.close()
    db.dispose()


def GetMsSqlConnString(userId,password,serverName,dbName):
      pyConnString="mssql+pyodbc://%s:%s@%s/%s" % (userId,password,serverName,dbName)
      return  pyConnString


def GetConnStrVal(connStr,key):
    list=connStr.split(";")
    for str in list:
        str=str.replace(" ","")
        list11=str.split("=")
        if len(list11)>=2 and  list11[0].strip().lower()==key.lower():
            val=list11[1].strip()
            return  val
    return ""

def GetParentDir(dir):
    if  len(dir)==0:
       return  ""
    a=dir.split('\\')
    return  a[-1]

def GetSecondDir(rootDir,currDir):
    r=rootDir.split('\\')
    a=currDir.split('\\')
    rootLen=len(r)
    if len(a)<=len(r):
        return  ""
    return  a[rootLen]

def RemoveOldLog(recentDay):
    filePath="Ami*.log"
    list=glob.glob(filePath)
    now=datetime.datetime.now()
    for fileName in list:
        if len(fileName)>=12:
           year=fileName[4:8]
           month=fileName[8:10]
           day=fileName[10:12]
           try:
               strDatetime="%s/%s/%s" % (year,month,day)
               fileDatetime= datetime.datetime.strptime(strDatetime,"%Y/%m/%d")
               if  (now-fileDatetime).days>recentDay:
                  os.remove(fileName)
           except Exception,e:
               print "amiTools. RemoveOldLog err, file="+fileName



if __name__=="__main__":
    #copyTree("c:\\0328","c:\\0329",['adidas'])
    #s=getDateDir("d:\swp")
    #s2=s
    #print GetNowVersion('    <add key="ProgramKey" value="G2V1.3509" />')
    #print CreateNewVersion('    <add key="ProgramKey" value="G2V1.3509" />')
    #print  CheckIsProgramKey('    <add key="ParogramKey" value="G2V1.3509" />')
    #print  UpgradeWebConfig("web.config",True)
    #print  GetFileNum("C:\\0328","detail2014111","csv")
    #print GetAmiRegValue("OmsMng","connstring")
    #print GetMsSqlConnStringByAmiConnName("OmsMng")
    #c1=TestCreateEngine("testMng")
    #print "ok"
    #c2=c1
    #c3=c2
    RemoveOldLog(2)

# test 123
#test  789  
#test 
