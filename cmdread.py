import  sys
import argparse

if  __name__=="__main__":
    param=sys.argv[1:]

    parser=argparse.ArgumentParser()

    #parser.add_argument('-s','--s', action='store',help='simple value',default="abc")
    parser.add_argument('-s',dest="file", action='store',help='simple value',default="abc")
    parser.add_argument('-v','--v',action='store',help='haha')

    opts=parser.parse_args(param)

    if(opts.file==None or  opts.v==None ):
        print  parser.print_help()
    else:
       print  opts.file
       print  opts.v

   # print  type(opts)
   # print  opts







