#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error

print 'lr_mcpc bid on', ((sys.argv[2]).split('/'))[-1]
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

def get_bid_landscape(mps):
    upper = 301
    init_val = 1
    mp_num = 0
    mp_dict = {}
    for i in range(0, upper):
        mp_dict[i] = init_val
        mp_num += init_val
    winfun = {}
    for mp in mps:
        if mp in mp_dict:
            mp_dict[mp] += 1
            mp_num += 1
        else:
            mp_dict[mp] = init_val
            mp_num += init_val
    #mp_num_tmp = max (mp_dict.keys()[0] - 1, 1)
    mp_num_tmp = 1
    #for key in mp_dict.keys():
    for key in range(0, upper):
        w = (mp_num_tmp * 1.0) / (mp_num * 1.0)
        mp_num_tmp += mp_dict[key]
        winfun[key] = w
    #print mp_num
    #print winfun
    #print mp_dict
    #exit()
    return winfun

def win_prob(bid):
    if bid in winfun:
        return winfun[bid]
    for key in sorted(winfun):
        if bid <= key:
            return winfun[key]
    return 1.

def test():
    y = []
    yp = []
    fi = open(sys.argv[1], 'r')
    for line in fi:
        data = ints(line.replace(":1", "").split())
        clk = data[1]
        mp = data[2]
        fsid = 3 # feature start id
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

original_ecpc = 0.  # original eCPC from train.yzx.base.txt
total_cost_train = 0

# read in train.yzx.base for original_ecpc
fi = open(sys.argv[1], 'r') # train.yzx.base.txt
first = True
imp_num = 0
clk_num = 0
for line in fi:
    s = line.strip().split()
    click = int(s[1])  # y
    cost = int(s[2])  # z
    imp_num += 1
    clk_num += click
    total_cost_train += cost
fi.close()
original_ecpc = total_cost_train * 1.0 / clk_num
print 'Finish loading', ((sys.argv[1]).split('/'))[-1]

for round in range(0, trainRounds):
    # train for this round
    print 'Round:', round
    fi = open(sys.argv[1], 'r')  # train.wyzx.base.txt
    lineNum = 0
    trainData = []
    for line in fi:
        lineNum = (lineNum + 1) % bufferCaseNum
        trainData.append(ints(line.replace(":1", "").split()))
        if lineNum == 0:
            for data in trainData:
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
    #test()


#adv_bid_discount = {'1458':4, '2259':2, '2261':3, '2821':4, '2997':4, '3358':4, '3386':4, '3427':4, '3476':4, 'all':4}
adv_bid_discount = {'1458':4, '2259':4, '2261':4, '2821':4, '2997':4, '3358':4, '3386':4, '3427':4, '3476':4, 'all':4}
discount = 4
for adv in adv_bid_discount:
    if adv in sys.argv[1]:
        discount = adv_bid_discount[adv]

win_num = 0
bid_num = 0
bid_max = 300
fi = open(sys.argv[2], 'r')   # train.wyzx.bid.txt
fo1 = open(sys.argv[3], 'w')  # train.wyzx.imp.txt
fo2 = open(sys.argv[4], 'w')  # train.wyb.imp.txt
fo3 = open(sys.argv[5], 'w')  # train.wyb.lose.txt
print 'Begin to bid'
for line in fi:
    data = ints(line.replace(":1", "").split())
    pred = 0.0
    mp = int(data[2])
    for i in range(3, len(data)):
        feat = data[i]
        if feat in featWeight:
            pred += featWeight[feat]
    pred = sigmoid(pred)
    bid = int(min(original_ecpc * pred / discount, bid_max))
    bid_num += 1
    if bid > mp:
        win_num += 1
        fo1.write(line)
        #w = win_prob(bid)
        s = line.strip().split()
        nl = '\t'.join(["1"] + [str(s[1])] + [str(bid)])
        fo2.write(nl + '\n')

    else:
        nl = '\t'.join(["0"] + ["0"] + [str(bid)])
        fo3.write(nl + '\n')
print 'lr_mcpc bid finished. Win ration:', float(win_num) / float(bid_num)
fo1.close()
fo2.close()
fo3.close()
fi.close()

mps = []
winfun = {}
# read in train.wyzx.imp for mps and win function
fi = open(sys.argv[3], 'r') # train.wyzx.imp.txt
for line in fi:
    s = line.strip().split()
    cost = int(s[2])  # z
    mps.append(cost)
fi.close()
winfun = get_bid_landscape(mps)

# output win prob
adv = 'null'
for a in ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']:
    if a in sys.argv[3]:
        adv = a
        break
win_prob_file = '../results/win-prob/{}.uimp.winprob.txt'.format(adv)
print 'output win prob to ' + win_prob_file
fof = open(win_prob_file, 'w')
for bid in range(302):
    fof.write('%d\t%.8f\n' % (bid, win_prob(bid)))
fof.close()

# read in train.wyzx.imp for to calculate w
fi1 = open(sys.argv[3], 'r') # train.wyzx.imp.txt
fi2= open(sys.argv[4], 'r') # train.wyb.imp.txt
fo = open(sys.argv[6], 'w') # train.wyzx.uimp.txt
for line1 in fi1:
    line2 = fi2.readline()
    s1 = line1.strip().split()
    s2 = line2.strip().split()
    bid = int(s2[2])
    w = win_prob(bid)
    nl = '\t'.join([str(w)] + s1[1:])
    fo.write(nl + '\n')
fi1.close()
fi2.close()
fo.close()
print 'Finished creating files:', ((sys.argv[3]).split('/'))[-1], ((sys.argv[4]).split('/'))[-1], ((sys.argv[5]).split('/'))[-1], ((sys.argv[6]).split('/'))[-1]
print '-------------------'
