#!/usr/bin/python
import sys
import random
import math
import operator

bufferCaseNum = 1000000
eta = 0.01
lamb = 1E-4
featWeight = {}
trainRounds = 2
random.seed(10)
initWeight = 0.05
importance_pow = 1
#file_list = ["imp", "uimp", "kimp", "bid"]

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

def win_prob(bid, winfun):
    if bid in winfun:
        return winfun[bid]
    for key in sorted(winfun):
        if bid <= key:
            return winfun[key]
    return 1.

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

for j in range(2, 6):
    print 'for file', ((sys.argv[j]).split('/'))[-1]
    zw_dict = {}
    fi = open(sys.argv[j], 'r') # read imp/uimp/kimp/bid for w z
    for line in fi:
        s = line.strip().split()
        w = float(s[0])
        z = int(s[2])
        zw_dict[z] = w
    fi.close()

    for round in range(0, trainRounds):
        # train for this round
        #print 'Round:', trainRounds
        fi = open(sys.argv[1], 'r')  # read base for y z x
        lineNum = 0
        trainData = []
        for line in fi:
            lineNum = (lineNum + 1) % bufferCaseNum
            trainData.append(fints(line.replace(":1", "").split()))
            if lineNum == 0:
                for data in trainData:
                    clk = data[1]
                    mp = data[2]
                    w = win_prob(mp, zw_dict)
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
                trainData = []

        if len(trainData) > 0:
            for data in trainData:
                clk = data[1]
                mp = data[2]
                w = win_prob(mp, zw_dict)
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
                #print str(importance)
                for i in range(fsid, len(data)):
                    feat = data[i]
                    featWeight[feat] = featWeight[feat] * (1 - (eta * importance) * lamb) + (eta * importance) * (clk - pred)
        fi.close()

    fi = open(sys.argv[j], 'r') # read imp/uimp/kimp/bid for w y z x
    fo = open(sys.argv[j+5], 'w') # write to wyzp file
    for line in fi:
        data = ints(line.replace(":1", "").split())
        s = line.strip().split()
        pred = 0.0
        for i in range(3, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        nl = '\t'.join(s[0:3] + [str(pred)])
        fo.write(nl +'\n')
    fi.close()
    fo.close()

