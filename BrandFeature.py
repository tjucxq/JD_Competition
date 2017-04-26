#coding=utf-8
import sys
import re
import csv
import feature_encoding

#input: user_id	 sku_id	 time	model_id	type	cate	brand

#parameter:
#           time1 : "2017-4-3 15:17:00"
#           time2 : "2017-4-1 9:53:00"
#           filename: 输入文件
#           outfile： 特征输出文件
def B_1_11_Features(time1, time2, filename, outfile):
    #Brand 第一个特征, 该品牌中6种行为交互的商品数（1d,3d,10d）
    F1_brand_1day = {}  # {bid: {actionID: set(sku_id) }}
    F1_brand_3day = {}
    F1_brand_10day = {}

    #Brand 第二个特征, 该品牌的6种行为平均用户数（1d,2d-3d,4d-10d）
    F2_brand_1day = {} # {bid: {actionId: set(user_id) }}
    F2_brand_3day = {}
    F2_brand_10day = {}

    #Brand 第三个特征, 该品牌的6种行为平均次数（1d,2d-3d,4d-10d）
    F3_brand_1day = {}  # {bid: {actionId: 次数}}
    F3_brand_3day = {}
    F3_brand_10day = {}

    F4_brand = 0.0
    F5_brand = 0.0
    F6_brand = 0.0
    F7_brand = 0.0

    #Brand 第八个特征，同cate的品牌中该品牌浏览次数的排名
    F8_brand = {} # {cate: {bid: 浏览次数}}
    # Brand 第九个特征，同cate的品牌中该品牌浏览人数的排名
    F9_brand = {} #{cate : {bid: set(uid)}}
    # Brand 第十个特征，同cate的品牌中该品牌购买次数的排名
    F10_brand = {} #{cate : {bid: 购买次数}}
    # Brand 第十一个特征，同cate的品牌中该品牌购买人数的排名
    F11_brand = {}  # {cate : {bid: 购买次数}}

    b_set = set()
    input = file(filename, "r")
    read = csv.reader(input)
    for line in read:
        if read.line_num == 1:
            continue
        uid = line[0]
        sku_id = line[1]
        t = line[2]
        mode = line[3]
        actionId = line[4]
        cate = line[5]
        bid = cate+"+"+line[6]

        b_set.add(bid)
        if t < time2:
            continue
        res, deta_day, deta_hour, deta = feature_encoding.deta_time(time1,t)

        if not F1_brand_1day.has_key(bid):
            F1_brand_1day[bid] = {}
            F1_brand_3day[bid] = {}
            F1_brand_10day[bid] = {}
            F2_brand_1day[bid] = {}
            F2_brand_3day[bid] = {}
            F2_brand_10day[bid] = {}
            F3_brand_1day[bid] = {}
            F3_brand_3day[bid] = {}
            F3_brand_10day[bid] = {}
        if not F1_brand_1day[bid].has_key(actionId):
            F1_brand_1day[bid][actionId] = set()
            F1_brand_3day[bid][actionId] = set()
            F1_brand_10day[bid][actionId] = set()
            F2_brand_1day[bid][actionId] = set()
            F2_brand_3day[bid][actionId] = set()
            F2_brand_10day[bid][actionId] = set()
            F3_brand_1day[bid][actionId] = 0
            F3_brand_3day[bid][actionId] = 0
            F3_brand_10day[bid][actionId] = 0

        if deta < 1.0:
            F1_brand_1day[bid][actionId].add(sku_id)
            F1_brand_3day[bid][actionId].add(sku_id)
            F1_brand_10day[bid][actionId].add(sku_id)
            F2_brand_1day[bid][actionId].add(uid)
            F3_brand_1day[bid][actionId] += 1
        elif deta < 3.0:

            F1_brand_3day[bid][actionId].add(sku_id)
            F1_brand_10day[bid][actionId].add(sku_id)
            F2_brand_3day[bid][actionId].add(uid)
            F3_brand_3day[bid][actionId] += 1
        elif deta < 10.0:
            F1_brand_10day[bid][actionId].add(sku_id)
            F2_brand_10day[bid][actionId].add(uid)
            F3_brand_10day[bid][actionId] += 1

        if not F8_brand.has_key(cate):
            F8_brand[cate] = {}
            F9_brand[cate] = {}
            F10_brand[cate] = {}
            F11_brand[cate] = {}
        if not F8_brand[cate].has_key(bid):
            F8_brand[cate][bid] = 0
            F9_brand[cate][bid] = set()
            F10_brand[cate][bid] = 0
            F11_brand[cate][bid] = set()
        if actionId == "1":
            F8_brand[cate][bid] += 1
            F9_brand[cate][bid].add(uid)
        elif actionId == "4":
            F10_brand[cate][bid] += 1
            F11_brand[cate][bid].add(uid)
    input.close()

    cate = ["11", "4", "5", "6", "7", "8", "9", "10"]
    F8_brand_rank = {}
    F9_brand_rank = {}
    F10_brand_rank = {}
    F11_brand_rank = {}
    default_rank = 10000
    for c in cate:
        F8_brand_sorted = sorted(F8_brand[c].items(), key=lambda e:e[1], reverse=True)
        pre = -1
        rank = 0
        for ele in F8_brand_sorted:
            bid = ele[0]
            num = ele[1]
            if pre != num:
                rank += 1
                F8_brand_rank[bid] = rank
                pre = num
            else:
                F8_brand_rank[bid] = rank
        F9_brand_sorted = sorted(F9_brand[c].items(), key=lambda e:len(e[1]), reverse=True)
        pre = -1
        rank = 0
        for ele in F9_brand_sorted:
            bid = ele[0]
            num = len(ele[1])
            if pre != num:
                rank += 1
                F9_brand_rank[bid] = rank
            else:
                F9_brand_rank[bid] = rank
        F10_brand_sorted = sorted(F10_brand[c].items(), key=lambda e:e[1], reverse=True)
        pre = -1
        rank = 0
        for ele in F10_brand_sorted:
            bid = ele[0]
            num = ele[1]
            if pre != num:
                rank += 1
                F10_brand_rank[bid] = rank
            else:
                F10_brand_rank[bid] = rank
        F11_brand_sorted = sorted(F11_brand[c].items(), key=lambda e:len(e[1]), reverse=True)
        pre = -1
        rank = 0
        for ele in F11_brand_sorted:
            bid = ele[0]
            num = len(ele[1])
            if pre != num :
                rank += 1
                F11_brand_rank[bid] = rank
            else:
                F11_brand_rank[bid] = rank

    f_name = ["cat","brand", "b_f1_1day_action1", "b_f1_1day_action2", "b_f1_1day_action3", "b_f1_1day_action4", "b_f1_1day_action5", "b_f1_1day_action6",
              "b_f1_3day_action1", "b_f1_3day_action2", "b_f1_3day_action3", "b_f1_3day_action4", "b_f1_3day_action5", "b_f1_3day_action6",
              "b_f1_10day_action1", "b_f1_10day_action2", "b_f1_10day_action3", "b_f1_10day_action4", "b_f1_10day_action5", "b_f1_10day_action6",
              "b_f2_1day_action1", "b_f2_1day_action2", "b_f2_1day_action3", "b_f2_1day_action4", "b_f2_1day_action5", "b_f2_1day_action6",
              "b_f2_3day_action1", "b_f2_3day_action2", "b_f2_3day_action3", "b_f2_3day_action4", "b_f2_3day_action5", "b_f2_3day_action6",
              "b_f2_10day_action1", "b_f2_10day_action2", "b_f2_10day_action3", "b_f2_10day_action4", "b_f2_10day_action5", "b_f2_10day_action6",
              "b_f3_1day_action1", "b_f3_1day_action2", "b_f3_1day_action3", "b_f3_1day_action4", "b_f3_1day_action5", "b_f3_1day_action6",
              "b_f3_3day_action1", "b_f3_3day_action2", "b_f3_3day_action3", "b_f3_3day_action4", "b_f3_3day_action5", "b_f3_3day_action6",
              "b_f3_10day_action1", "b_f3_10day_action2", "b_f3_10day_action3", "b_f3_10day_action4", "b_f3_10day_action5", "b_f3_10day_action6",
              "b_f4", "b_f5", "b_f6", "b_f7", "b_f8", "b_f9", "b_f10", "b_f11"]

    out = file(outfile,"wb")
    write = csv.writer(out)
    write.writerow(f_name)
    actionList = ["1", "2", "3", "4", "5", "6"]
    for bid in b_set:
        lst = bid.split("+")
        for action in actionList:
            if F1_brand_1day[bid].has_key(action):
                lst.append(str(len(F1_brand_1day[bid][action])))
            else:
                lst.append("0")
        for action in actionList:
            if F1_brand_3day[bid].has_key(action):
                lst.append(str(len(F1_brand_3day[bid][action])))
            else:
                lst.append("0")
        for action in actionList:
            if F1_brand_10day[bid].has_key(action):
                lst.append(str(len(F1_brand_10day[bid][action])))
            else:
                lst.append("0")

        for action in actionList:
            if F2_brand_1day[bid].has_key(action):
                lst.append(str(len(F2_brand_1day[bid][action])))
            else:
                lst.append("0.00")
        for action in actionList:
            if F2_brand_3day[bid].has_key(action):
                lst.append(str(round(len(F2_brand_3day[bid][action])/2.0, 2)))
            else:
                lst.append("0.00")
        for action in actionList:
            if F2_brand_10day[bid].has_key(action):
                lst.append(str(round(len(F2_brand_10day[bid][action])/7.0, 2)))
            else:
                lst.append("0")

        for action in actionList:
            if F3_brand_1day[bid].has_key(action):
                lst.append(str(F3_brand_1day[bid][action]))
            else:
                lst.append("0.00")
        for action in actionList:
            if F3_brand_3day[bid].has_key(action):
                lst.append(str(round(F3_brand_3day[bid][action]/2.0, 2)))
            else:
                lst.append("0.00")
        for action in actionList:
            if F3_brand_10day[bid].has_key(action):
                lst.append(str(round(F3_brand_10day[bid][action]/7.0, 2)))
            else:
                lst.append("0")

        if not F1_brand_10day[bid].has_key("4"):
            lst.append("0.00")
            lst.append("0.00")
        else:
            buySku = len(F1_brand_10day[bid]["4"])
            seeNum = 0.1
            if F1_brand_10day[bid].has_key("1"):
                seeNum = len(F1_brand_10day[bid]["1"])
            if seeNum == 0:
                seeNum = 0.1

            castNum = 0.1
            if F1_brand_10day[bid].has_key("2"):
                castNum = len(F1_brand_10day[bid]["2"])
            if castNum == 0:
                castNum = 0.1
            lst.append(str(round(buySku*1.0/seeNum, 2)))
            lst.append(str(round(buySku*1.0/castNum, 2)))

        if not F3_brand_1day[bid].has_key("4"):
            lst.append("0.00")
            lst.append("0.00")
        else:
            buyNum = F3_brand_1day[bid]["4"]+F3_brand_3day[bid]["4"]+F3_brand_10day[bid]["4"]
            seeNum = 0.1
            if F3_brand_1day[bid].has_key("1"):
                seeNum = F3_brand_1day[bid]["1"] + F3_brand_3day[bid]["1"] + F3_brand_10day[bid]["1"]
            if seeNum == 0:
                seeNum = 0.1

            castNum = 0.1
            if F3_brand_1day[bid].has_key("2"):
                castNum = F3_brand_1day[bid]["2"] + F3_brand_3day[bid]["2"] + F3_brand_10day[bid]["2"]
            if castNum == 0:
                castNum = 0.1
            lst.append(str(round(buyNum*1.0/seeNum, 2)))
            lst.append(str(round(buyNum*1.0/castNum, 2)))

        if F8_brand_rank.has_key(bid):
            lst.append(str(F8_brand_rank[bid]))
        else:
            lst.append(str(default_rank))
        if F9_brand_rank.has_key(bid):
            lst.append(str(F9_brand_rank[bid]))
        else:
            lst.append(str(default_rank))
        if F10_brand_rank.has_key(bid):
            lst.append(str(F10_brand_rank[bid]))
        else:
            lst.append(str(default_rank))
        if F11_brand_rank.has_key((bid)):
            lst.append(str(F11_brand_rank[bid]))
        else:
            lst.append(str(default_rank))

        write.writerow(lst)
    out.close()

if __name__ == "__main__":
    # print feature_encoding.deta_time("2017-02-06 00:00:00", "2017-02-05 00:00:00")
    # B_1_11_Features("2016-02-25 00:00:00", "2016-02-15 00:00:00", "extract_feature/2.15_2.24_feature.csv",
    #                 "extract_feature/b_feature_2.15_2.24.csv")
    B_1_11_Features("2016-02-27 00:00:00", "2016-02-17 00:00:00", "extract_feature/2.17_2.26_feature.csv",
                    "extract_feature/b_feature_2.17_2.26.csv")
    B_1_11_Features("2016-02-29 00:00:00", "2016-02-19 00:00:00", "extract_feature/2.19_2.28_feature.csv",
                    "extract_feature/b_feature_2.19_2.28.csv")
    B_1_11_Features("2016-03-02 00:00:00", "2016-02-21 00:00:00", "extract_feature/2.21_3.1_feature.csv",
                    "extract_feature/b_feature_2.21_3.1.csv")
    B_1_11_Features("2016-03-04 00:00:00", "2016-02-23 00:00:00", "extract_feature/2.23_3.3_feature.csv",
                    "extract_feature/b_feature_2.23_3.3.csv")
    B_1_11_Features("2016-03-06 00:00:00", "2016-02-25 00:00:00", "extract_feature/2.25_3.5_feature.csv",
                    "extract_feature/b_feature_2.25_3.5.csv")
    B_1_11_Features("2016-03-08 00:00:00", "2016-02-27 00:00:00", "extract_feature/2.27_3.7_feature.csv",
                    "extract_feature/b_feature_2.27_3.7.csv")
    B_1_11_Features("2016-03-28 00:00:00", "2016-03-18 00:00:00", "extract_feature/3.18_3.27_feature.csv",
                    "extract_feature/b_feature_3.18_3.27.csv")
    B_1_11_Features("2016-03-30 00:00:00", "2016-03-20 00:00:00", "extract_feature/3.20_3.29_feature.csv",
                    "extract_feature/b_feature_3.20_3.29.csv")
    B_1_11_Features("2016-04-01 00:00:00", "2016-03-22 00:00:00", "extract_feature/3.22_3.31_feature.csv",
                    "extract_feature/b_feature_3.22_3.31.csv")
    B_1_11_Features("2016-04-03 00:00:00", "2016-03-24 00:00:00", "extract_feature/3.24_4.2_feature.csv",
                    "extract_feature/b_feature_3.24_4.2.csv")
    B_1_11_Features("2016-04-05 00:00:00", "2016-03-26 00:00:00", "extract_feature/3.26_4.4_feature.csv",
                    "extract_feature/b_feature_3.26_4.4.csv")
    B_1_11_Features("2016-04-07 00:00:00", "2016-03-28 00:00:00", "extract_feature/3.28_4.6_feature.csv",
                    "extract_feature/b_feature_3.28_4.6.csv")
    B_1_11_Features("2016-04-09 00:00:00", "2016-03-30 00:00:00", "extract_feature/3.30_4.8_feature.csv",
                    "extract_feature/b_feature_3.30_4.8.csv")
    B_1_11_Features("2016-04-11 00:00:00", "2016-04-01 00:00:00", "extract_feature/4.1_4.10_feature.csv",
                    "extract_feature/b_feature_4.1_4.10.csv")
    B_1_11_Features("2016-04-16 00:00:00", "2016-04-06 00:00:00", "extract_feature/4.6_4.15_feature.csv",
                    "extract_feature/b_feature_4.6_4.15.csv")