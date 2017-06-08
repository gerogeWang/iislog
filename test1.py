import glob
import os
import os.path

#dirList = glob.glob
#print glob.glob("c:/uniqServer/*.log")

for root, dirs, files in os.walk("c:/uniqServer"):
   for name in files:
       if name.endswith(".log")==True:
           print "log !"
       print root + '/' + name



