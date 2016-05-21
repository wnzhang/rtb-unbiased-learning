#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from information_gain import get_relative_information_gain
from information_gain import get_cross_entropy


def nextInitWeight():
    return (random.random() - 0.5) * initWeight

def ints(s):
    res = []
    for ss in s:
        res.append(float(ss))
    return res

def fints(s):
    res = []
    res.append(float(s[0]))
    for i in range(1, len(s)):
        res.append(int(s[i]))
    return res

def sigmoid(p):
    return 1.0 / (1.0 + math.exp(-p))



total_results_file = '../results/ce_total_para_loop.txt'
train_file = '../../make-ipinyou-data/all/train.wyzx.bid.txt'
test_file = '../../make-ipinyou-data/all/test.yzx.txt'

# read in data
trainData = []
fi = open(train_file, 'r')
for line in fi:
    trainData.append(fints(line.replace(":1", "").split()))
fi.close()

testData = []
fi = open(test_file, 'r')
for line in fi:
    testData.append(fints(line.replace(":1", "").split()))
fi.close()

fo = open(total_results_file, 'w')

etas = [1E-3, 5E-3, 8E-3, 1E-2, 3E-2, 5E-2, 8E-2, 0.1, 0.2]
lambs = [1E-9, 1E-8, 1E-7, 1E-6, 1E-5, 1E-4, 1E-3]

for eta in etas:
    for lamb in lambs:
        print 'eta:', eta, '  lambda:', lamb
        featWeight = {}
        trainRounds = 40
        random.seed(10)
        initWeight = 0.01
        results = []

        for round in range(0, trainRounds):
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
                importance = 1
                for i in range(fsid, len(data)):
                    feat = data[i]
                    featWeight[feat] = featWeight[feat] * (1 - (eta * importance) * lamb) + (eta * importance) * (clk - pred)

            # test for this round
            y = []
            yp = []
            for data in testData:
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
            auc = 0.
            rmse = 0.
            ce = get_cross_entropy(y, yp)
            print str(round) + '\t' + str(auc) + '\t' + str(rmse) + '\t' + str(ce) + '\t' + str(eta) + '\t' + str(lamb)
            results.append([auc, rmse, ce])

        best_result = [0.0, 0.0, 1.] #1E9]
        bst_auc = [0., 0., 0.]
        for i in results:
            if i[2] < best_result[2]: # ce: the smaller the better
                best_result[0] = i[0]
                best_result[1] = i[1]
                best_result[2] = i[2]
        fo.write(str(eta) + '\t' + str(lamb) + '\t' + str(best_result[2]) + '\n')
        fo.flush()

        print 'Best auc, rmse with best ce score:', str(best_result[0]), str(best_result[1]), str(best_result[2])
        print '-------------------'

fo.close()
