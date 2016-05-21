#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error


bufferCaseNum = 1000000
eta = 0.01
lamb = 1E-6
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

'''
if len(sys.argv) == 5:
    print 'Usage: train.yzx.base.txt train.yzx.bid.txt train.yzx.imp.txt train.yzx.lose.txt'
    exit(-1)
'''

for round in range(0, trainRounds):
    # train for this round
    #print 'Round:', trainRounds
    fi = open(sys.argv[1], 'r')  # train.yzx.base.txt
    lineNum = 0
    trainData = []
    for line in fi:
        lineNum = (lineNum + 1) % bufferCaseNum
        trainData.append(ints(line.replace(":1", "").split()))
        if lineNum == 0:
            for data in trainData:
                clk = data[0]
                mp = data[1]
                fsid = 2 # feature start id
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
            clk = data[0]
            mp = data[1]
            fsid = 2 # feature start id
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

    '''
    # test for this round
    y = []
    yp = []
    fi = open(sys.argv[3], 'r')
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
    '''

# # output the prediction of train.yzx.base
# fi = open(sys.argv[1], 'r')
# fo = open(sys.argv[2], 'w')
#
# for line in fi:
#     data = ints(line.replace(":1", "").split())
#     pred = 0.0
#     for i in range(1, len(data)):
#         feat = data[i]
#         if feat in featWeight:
#             pred += featWeight[feat]
#     pred = sigmoid(pred)
#     fo.write('%d\t%d\t%.6f\n' % (data[0], data[1], pred))
# print 'pctr train finished'
# fo.close()
# fi.close()

original_ecpc = 0.  # original eCPC from train.yzx.base.txt
total_cost_train = 0

# read in train.yzx.base for original_ecpc
fi = open(sys.argv[1], 'r') # train.yzx.base.txt
first = True
imp_num = 0
clk_num = 0
for line in fi:
    s = line.strip().split()
    click = int(s[0])  # y
    cost = int(s[1])  # z
    imp_num += 1
    clk_num += click
    total_cost_train += cost
fi.close()
original_ecpc = total_cost_train * 1.0 / clk_num


# output the prediction of train.yzx.bid.txt
fi = open(sys.argv[2], 'r')   # train.yzx.bid.txt
fo1 = open(sys.argv[3], 'w')  # train.yzx.imp.txt
fo2 = open(sys.argv[4], 'w')  # train.yzx.lose.txt

for line in fi:
    data = ints(line.replace(":1", "").split())
    pred = 0.0
    mp = int(data[1])
    for i in range(2, len(data)):
        feat = data[i]
        if feat in featWeight:
            pred += featWeight[feat]
    pred = sigmoid(pred)
    bid = int(original_ecpc * pred)
    if bid > mp:
        fo1.write(line)
    else:
        s = line.strip().split()
        nl = ' '.join(["0"]+[str(bid)]+s[2:])
        fo2.write(nl + '\n')
print 'lr_max_cpc bid finished'
fo1.close()
fo2.close()
fi.close()



