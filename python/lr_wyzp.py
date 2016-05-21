#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error


bufferCaseNum = 1000000
eta = 0.01
lamb = 1E-6 # 1E-7 for all   1E-6 for others
featWeight = {}
trainRounds = 10
random.seed(10)
initWeight = 0.05

def nextInitWeight():
    return (random.random() - 0.5) * initWeight

def ints(s):
    res = []
    for ss in s:
        res.append(int(ss))
    return res

def sigmoid(p):
    return 1.0 / (1.0 + math.exp(-p))

adv = '2997'
if len(sys.argv) > 1:
    adv = sys.argv[1]

data_folder = '../../make-ipinyou-data/{}/'.format(adv)
base_train_file = data_folder + 'train.wyzx.base.txt'
validation_file = data_folder + 'test.yzx.txt'
test_output_file = data_folder + 'test.wyzp.txt'


for round in range(0, trainRounds):
    # train for this round
    # print 'Round:', trainRounds
    fi = open(base_train_file, 'r')  # train.yzx.base.txt
    lineNum = 0
    trainData = []
    for line in fi:
        lineNum = (lineNum + 1) % bufferCaseNum
        trainData.append(ints(line.replace(":1", "").split()))
        if lineNum == 0:
            for data in trainData:
                w = data[0]
                clk = data[1]
                mp = data[2]
                fsid = 3 # feature start id
                # predict
                pred = 0.0
                for i in range(fsid, len(data)):
                    feat = data[i]
                    if feat not in featWeight:
                        featWeight[feat] = nextInitWeight()
                    pred += featWeight[feat]
                pred = sigmoid(pred)
                # start to update weight
                # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ] 
                for i in range(fsid, len(data)):
                    feat = data[i]
                    featWeight[feat] = featWeight[feat] * (1 - lamb) + eta * (clk - pred)
            trainData = []

    if len(trainData) > 0:
        for data in trainData:
            w = data[0]
            clk = data[1]
            mp = data[2]
            fsid = 3 # feature start id
            # predict
            pred = 0.0
            for i in range(fsid, len(data)):
                feat = data[i]
                if feat not in featWeight:
                    featWeight[feat] = nextInitWeight()
                pred += featWeight[feat]
            pred = sigmoid(pred)
            # start to update weight
            # w_i = w_i + learning_rate * [ (y - p) * x_i - lamb * w_i ]
            for i in range(fsid, len(data)):
                feat = data[i]
                featWeight[feat] = featWeight[feat] * (1 - lamb) + eta * (clk - pred)
    fi.close()

    # test for this round
    y = []
    yp = []
    fi = open(validation_file, 'r')
    for line in fi:
        data = ints(line.replace(":1", "").split())
        clk = data[0]
        mp = data[1]
        fsid = 2 # feature start id
        pred = 0.0
        for i in range(fsid, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        y.append(clk)
        yp.append(pred)
    fi.close()
    auc = roc_auc_score(y, yp)
    rmse = math.sqrt(mean_squared_error(y, yp))
    print str(round) + '\t' + str(auc) + '\t' + str(rmse)


# lr training done. now make predictions and write the files

# test.wyzp.txt
fi = open(validation_file, 'r')
fo = open(test_output_file, 'w')
print 'processing {} and output to {}'.format(validation_file, test_output_file)
for line in fi:
    data = ints(line.replace(":1", "").split())
    clk = data[0]
    mp = data[1]
    fsid = 2 # feature start id
    pred = 0.0
    for i in range(fsid, len(data)):
        feat = data[i]
        if feat in featWeight:
            pred += featWeight[feat]
    pred = sigmoid(pred)
    fo.write('1\t%d\t%d\t%.8f\n' % (clk, mp, pred))

fi.close()
fo.close()


# train.wyzp.xxxx.txt
settings = ['imp', 'uimp', 'kimp', 'bid']
for setting in settings:
    input_file = data_folder + 'train.wyzx.{}.txt'.format(setting)
    output_file = data_folder + 'train.wyzp.{}.txt'.format(setting)
    print 'processing {} and output to {}'.format(input_file, output_file)
    fi = open(input_file, 'r')
    fo = open(output_file, 'w')
    for line in fi:
        w = line[0:line.index('\t')]
        data = ints(line.replace(":1", "").split()[1:])
        clk = data[0]
        mp = data[1]
        fsid = 2 # feature start id
        pred = 0.0
        for i in range(fsid, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        fo.write('%s\t%d\t%d\t%.8f\n' % (w, clk, mp, pred))
    fi.close()
    fo.close()
