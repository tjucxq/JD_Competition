# -*- coding: utf-8 -*-
_author_ = 'Haozijie'
import datetime
###该函数用于计算时间差,对行为时间进行编码###
##parameter :
#           time1 : "2017-4-3 15:17:00"
#           time2 : "2017-4-1 9:53:00"
#retrun :
#           res : 时间差，2h,6h,12h,1d,3d,5d,7d,10d
#           deta_day ： 时间差，天数
#           deta_hour : 时间差，小时
#           deta : 时间差，天数（精确到小数点后）
def deta_time(time1,time2):
    time1s = time1.split(" ")
    time2s = time2.split(" ")
    day1 = time1s[0].split("-")
    day2 = time2s[0].split("-")
    hour1 = time1s[1].split(":")
    hour2 = time2s[1].split(":")
    d1 = datetime.datetime(int(day1[0]), int(day1[1]), int(day1[2]), int(hour1[0]), int(hour1[1]),int(hour1[2]))
    d2 = datetime.datetime(int(day2[0]), int(day2[1]), int(day2[2]), int(hour2[0]), int(hour2[1]),int(hour2[2]))
    deta_day = int((d1 - d2).days)
    deta_hour = float((d1 - d2).seconds)/3600
    deta = str((float(deta_day*86400)+float((d1 - d2).seconds))/86400)[:9]   ###之前是9
    res = ""
    if deta_day == 0:
        if deta_hour <= 2:
            res = '2h'
        elif deta_hour <=6:
            res = '6h'
        elif deta_hour <=12:
            res = '12h'
        else:
            res = '1d'
    elif deta_day <= 2:
        res = '3d'
    elif deta_day <= 4:
        res = '5d'
    elif deta_day <= 6:
        res = '7d'
    else:
        res = '10d'

    return res,deta_day,deta_hour,float(deta)