import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib


def load_data(train_file, test_file):
    print 'start loading file...'
    train_x = []
    train_y = []
    test_x = []
    uid_cid = []
    with open(train_file) as f_train:
        f_train.readline()
        for line in f_train.readlines():
            feature = line.strip().split(',')
            train_x.append(feature[2:-1])
            train_y.append(feature[-1])
    with open(test_file) as f_test:
        f_test.readline()
        for line in f_test.readlines():
            feature = line.strip().split(',')
            uid_cid.append(feature[:2])
            test_x.append(feature[2:])
    print 'finish loading file...'
    trainx = np.array(train_x, np.float)
    trainy = np.array(train_y, np.float)
    testx = np.array(test_x, np.float)
    return trainx, trainy, testx, uid_cid


def gbdt(train_x, train_y, test_x, uid_cid):
    print 'start training...'
    clf = GradientBoostingClassifier(learning_rate=0.05,n_estimators=300,max_depth=7,max_features=0.6,min_samples_leaf=128,max_leaf_nodes=128,subsample=0.6,verbose=1)
    clf.fit_transform(train_x, train_y)
    print 'finish training...'
    joblib.dump(clf,'model/gbdt_model.m')
    print 'start predicting...'
    predict_y = clf.predict_proba(test_x)
    print clf.classes_
    print clf.feature_importances_ 
    print 'finish predicting...'
    return predict_y


def write_file(result_list, uid_cid, result_file):
    print 'start writing...'
    f_out = open(result_file, 'w')
    f_out.write('user_id,cate,prob1\n')
    for i in range(len(result_list)):
        result = '{},{},{}\n'.format(uid_cid[i][0], uid_cid[i][1], result_list[i][1])
        f_out.write(result)
    f_out.close()
    print 'finish writing...'

if __name__ == '__main__':
    train_file = 'F12\\2.15_4.10_uc_ui_i_sample.csv'
    test_file = 'F12\\4.6_4.15_uc_ui_i.csv'
    result_file = 'F12\\model_result.csv'
    train_x, train_y, test_x, uid_cid = load_data(train_file, test_file)
    print train_x.shape
    print train_y.shape
    print test_x.shape
    print len(uid_cid)
    result_list = gbdt(train_x, train_y, test_x, uid_cid)
    write_file(result_list, uid_cid, result_file)

