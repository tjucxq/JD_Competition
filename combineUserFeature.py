#coding=utf-8
#合并 u_features_*.csv 和 u_basic_features_*.csv

import sys
import os

fileList1 = os.listdir("u_features")
for f in fileList1:
    print f