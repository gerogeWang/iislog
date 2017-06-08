from datetime import datetime,timedelta

str1="2017-05-11 00:00:00"

d1=datetime.strptime(str1,"%Y-%m-%d %H:%M:%S")
d2=d1+timedelta(hours=8)

print d2





