#coding=utf-8

import csv

if __name__ == "__main__":
    predictFile = open("final_result.csv","r") #预测文件
    labelFile = open("final_result_2.csv","r") #标签文件

    predictReader = csv.reader(predictFile)
    labelReader = csv.reader(labelFile)

    labelMap = {} # key:uid  value: ser(sku_id)  标签结果

    #加载真集结果
    labelNum = 0  #真集个数
    for item in labelReader:
        uid = item[0]
        if labelReader.line_num == 1:
            continue
        labelNum += 1
        if labelMap.has_key(uid):
            labelMap[uid].add(item[1])
        else:
            labelMap[uid] = set()
            labelMap[uid].add(item[1])

    trueUser = 0   #预测对的用户
    trueSku = 0    #预测对的用户-商品
    predictNum = 0  #预测结果集个数

    #加载预测结果
    for item in predictReader:
        uid = item[0]
        sku = item[1]
        if predictReader.line_num == 1:
            continue
        predictNum += 1
        if labelMap.has_key(uid):
            trueUser += 1
            if sku in labelMap[uid]:
                trueSku += 1

    print "真集结果的个数为："+str(labelNum)+ " 预测结果的个数为："+str(predictNum)

    f11_precise = trueUser*1.0/predictNum
    f11_recall = trueUser*1.0/labelNum
    f11 = 6*f11_precise*f11_recall/(5*f11_recall + f11_precise)
    print "f11 is : "+str(f11)+"  f11_precise is : "+str(f11_precise)+"  f12_recall is : "+str(f11_recall)+\
          "  预测对的用户有："+str(trueUser)

    f12_precise = trueSku*1.0/predictNum
    f12_recall = trueSku*1.0/labelNum
    f12 = 5*f12_precise*f12_recall/(2*f12_recall + 3*f12_precise)
    print "f12 is : "+str(f12)+"  f12_precise is : "+str(f12_precise)+"  f12_recall is : "+str(f12_recall)+\
        "  预测对的用户-商品对有："+str(trueSku)

    f = 0.4*f11 + 0.6*f12
    print "f is : "+str(f)