#coding=utf-8
#合并 u_features_*.csv 和 u_basic_features_*.csv

import sys
import os
import csv

fileList1 = os.listdir("u_features")
fileList2 = os.listdir("uc")

files1 = sorted(fileList1)
files2 = sorted(fileList2)
for f in range(len(files1)):
    a = open("u_features/"+files1[f],"r")
    reader1 = csv.reader(a)
    b = open("uc/"+files2[f],"r")
    reader2 = csv.reader(b)
    c = open("uc_u/uc_u_features_"+files2[f][:-7]+".csv","w")
    write = csv.writer(c)
    head1 = []
    head2 = []
    user_map = {}
    for line in reader1:
        if reader1.line_num == 1:
            head1 = line
            continue
        user_map[line[0]] = line[1:]

    for line in reader2:
        if reader2.line_num == 1:
            head2 = line
            write.writerow(head2[:-1]+head1[1:]+[head2[-1]])
            continue
        uid = line[0]
        if user_map.has_key(uid):
            write.writerow(line[:-1]+user_map[uid]+[line[-1]])
    a.close()
    b.close()
    c.close()


