#coding=utf-8
from sklearn.ensemble import RandomForestClassifier
import csv

if __name__ == "__main__":
    trainX = []
    trainY = []

    validX = []
    validY = []

    clf = RandomForestClassifier(n_estimators=400, criterion='gini', max_depth=60, min_samples_split=10,
                                 min_samples_leaf=2, min_weight_fraction_leaf=0.0, max_features=0.8,
                                 max_leaf_nodes=None, min_impurity_split=1e-07, bootstrap=True, oob_score=False,
                                 n_jobs=8, random_state=None, verbose=0, warm_start=False, class_weight={1:2})

    trainFile = open("uc_u_2.15_4.8_train_1_10.csv","r")
    reader1 = csv.reader(trainFile)
    for line in reader1:
        trainX.append([float(ele) for ele in line[2:-1]])
        trainY.append(int(line[-1]))
    trainFile.close()
    print trainX[0]
    print "--------start training----------"
    clf.fit(trainX,trainY)
    print "--------training is down--------"
    validFile = open("uc_u_features_4.1_4.10.csv","r")
    reader1 = csv.reader(validFile)
    for line in reader1:
        if reader1.line_num == 1:
            continue
        validX.append([float(ele) for ele in line[2:-1]])
        validY.append(int(line[-1]))
    validFile.close()

    predictY = clf.predict_proba(validX)

    outputFile = open("uc_u_features_4.1_4.10_predicted.csv","w")
    write = csv.writer(outputFile)
    write.writerow(["user_id","sku_id"])
    for i in range(len(validX)):
        write.writerow([validX[i][0],str(predictY[i])])
    outputFile.close()