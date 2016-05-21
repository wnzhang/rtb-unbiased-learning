#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from information_gain import get_relative_information_gain
from information_gain import get_cross_entropy

print 'Calculate auc and rmse ce score for', ((sys.argv[2]).split('/'))[-1], 'based on', ((sys.argv[1]).split('/'))[-1]
eta = 0.02 # 0.01
lamb = 1E-6 #1e-7
featWeight = {}
trainRounds = 40
random.seed(10)
initWeight = 0.01
importance_pow = 1. # 0.1
results = []
print '(eta, lamb, importance power):', eta, lamb, importance_pow

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

'''
if len(sys.argv) == 5:
    print 'Usage: train.yzx.base.txt train.yzx.bid.txt train.yzx.imp.txt train.yzx.lose.txt'
    exit(-1)
'''

ws = 1.0
summ = 0.
num = 0
ws = 0.
fi = open(sys.argv[1], 'r')
for line in fi:
    s = line.strip().split()
    num += 1
    summ += 1.0 / float(s[0])
fi.close()
ws = num * 1.0 / (summ * 1.0)

# read in data
trainData = []
fi = open(sys.argv[1], 'r')
for line in fi:
    trainData.append(fints(line.replace(":1", "").split()))
fi.close()

testData = []
fi = open(sys.argv[2], 'r')
for line in fi:
    testData.append(fints(line.replace(":1", "").split()))
fi.close()

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
        importance = math.pow(ws / w, importance_pow)
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
    print str(((sys.argv[1]).split('/'))[-2]) + ' ' + str(((sys.argv[1]).split('/'))[-1]) + '\t' + str(round) + \
          '\t' + str(auc) + '\t' + str(rmse) + '\t' + str(ce)
    results.append([auc, rmse, ce])

best_result = [0.0, 0.0, 1.] #1E9]
bst_auc = [0., 0., 0.]
for i in results:
    if i[0] > bst_auc[0]:
        bst_auc[0] = i[0]
        bst_auc[1] = i[1]
        bst_auc[2] = i[2]
for i in results:
    if i[2] < best_result[2]: # ce: the smaller the better
        best_result[0] = i[0]
        best_result[1] = i[1]
        best_result[2] = i[2]
fo = open(sys.argv[3], 'w')
#fo.write(str(best_result[0]) + '\t' + str(best_result[1]) + '\t' + str(best_result[2]) + '\n')
fo.close()

fo = open(sys.argv[4], 'w')
#for i in range(len(results)):
    #fo.write('%d\t%.6f\t%.6f\t%.6f\n' % (i + 1, results[i][0], results[i][1], results[i][2]))
fo.close()
print 'Best auc, rmse with best ce score:', str(best_result[0]), str(best_result[1]), str(best_result[2])
#print 'Best rmse ce with best auc score:', str(bst_auc[0]), str(bst_auc[1]), str(bst_auc[2])
print 'Finished creating files:', ((sys.argv[3]).split('/'))[-1], ((sys.argv[4]).split('/'))[-1]
print '-------------------'
