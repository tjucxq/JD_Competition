#coding=utf-8
#########################################################################
#   Copyright (C) 2013 All rights reserved.
#
#########################################################################
#!/usr/bin/python
# please add your code here!
import re;
import sys;
import time;
import random;


def PrintUsage():
    sys.stderr.write("program [IN]startindex[IN]endindex[IN]count[IN]save_index_file \n");
    sys.exit(1);

if(__name__=="__main__"):
    if(len(sys.argv)!=5):
        PrintUsage();
    starttime=time.clock();
    keyfile=str(sys.argv[4]);
    start=int(sys.argv[1]);
    end=int(sys.argv[2]);
    count=int(sys.argv[3]);
    mydict={};
    while(len(mydict)<count):
        cand=random.randint(start,end);
        mydict[cand]=0;
    fid=open(keyfile,"w");
    for key in mydict.keys():
        fid.write("%d\n"%key);
    fid.close();
    endtime=time.clock();
    interval=endtime-starttime;
    sys.stderr.write("%s has finished congratulations!\n"%str(sys.argv[0]));
    sys.stderr.write("time elapse:%f\n"%interval);
