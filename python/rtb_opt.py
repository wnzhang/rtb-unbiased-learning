#!/usr/bin/python
import sys
import random
import math

random.seed(10)

def bidding_const(bid):
    return bid

def bidding_rand(upper):
    return int(random.random() * upper)

def bidding_mcpc(ecpc, pctr):
    return int(ecpc * pctr)

def bidding_lin(pctr, base_ctr, base_bid):
    return int(pctr * base_bid / base_ctr)


# budgetProportion clk cnv bid imp budget spend para
def simulate_one_bidding_strategy_with_parameter(wyzps, tcost, proportion, algo, para):
    budget = int(tcost / proportion * b_p) # intialise the budget
    cost = 0
    clks = 0
    bids = 0
    imps = 0
    for wyzp in wyzps:
        bid = 0
        pctr = wyzp[3]
        winprice = wyzp[2]
        clk = wyzp[1]
        weight = wyzp[0]

        if algo == "const":
            bid = bidding_const(para)
        elif algo == "rand":
            bid = bidding_rand(para)
        elif algo == "mcpc":
            bid = bidding_mcpc(original_ecpc, pctr)
        elif algo == "lin":
            bid = bidding_lin(pctr, original_ctr, para)
        else:
            print 'wrong bidding strategy name'
            sys.exit(-1)

        bids += 1 * weight
        if bid > winprice:
            imps += 1 * weight
            clks += clk * weight
            cost += winprice * weight
        if cost > budget:
            break

    if proportion not in prop_algo_optimal_perf:
        prop_algo_optimal_perf[proportion] = {}
        prop_algo_optimal_para[proportion] = {}
    if algo not in prop_algo_optimal_perf[proportion]:
        prop_algo_optimal_perf[proportion][algo] = -1
    if clks > prop_algo_optimal_perf[proportion][algo]:
        prop_algo_optimal_perf[proportion][algo] = clks
        prop_algo_optimal_para[proportion][algo] = para

    #return '%d\t%d\t%d\t%d\t%.3f\t%d\t%d\t%.3f\t%s\t%d' \
    #       % (proportion, clks, bids, imps, imps * 1.0 / bids, budget, cost, cost * 1.0 / budget, algo, para)

    return '{proportion:>4}\t{clicks:>5}\t{bids:>8}\t{impressions:>8}\t{winrate:>6}\t{budget:>8}\t{spend:>8}\t' \
           '{ratio:>6}\t{algorithm:>6}\t{parameter:>8}'.format(
            proportion = proportion,
            clicks = int(clks),
            bids = int(bids),
            impressions = int(imps),
            winrate = '%.4f' % (imps * 1.0 / bids),
            budget = int(budget),
            spend = int(cost),
            ratio = '%.4f' % (cost * 1.0 / budget),
            algorithm = algo,
            parameter = para
        )

def simulate_one_bidding_strategy(cases, tcost, proportion, algo, writer):
    paras = algo_paras[algo]
    for para in paras:
        res = simulate_one_bidding_strategy_with_parameter(cases, tcost, proportion, algo, para)
        #print res
        writer.write(res + '\n')

'''
if len(sys.argv) == 6:
    print 'Usage: python rtb_opt.py train.(win).yzx.txt test.yzx.txt rtb.result.txt'
    exit(-1)
'''

wyzps_train = []          # winrate, clk and price and pctr for train
wyzps_test = []           # winrate, clk and price and pctr for test
total_cost_train = 0     # total original cost during the train data
total_cost_test = 0      # total original cost during the test data
original_ecpc = 0.       # original eCPC from train data
original_ctr = 0.        # original ctr from train data

# read in train data for original_ecpc and original_ctr
fi = open(sys.argv[1], 'r') # train.wyzp.xxxx.txt
ws = 0
num = 0
for line in fi:
    s = line.strip().split('\t')
    ws += 1. / float(s[0])
    num += 1
fi.close()
rate = num / ws

imp_num_train = 0
clk_num_train = 0
fi = open(sys.argv[1], 'r')
for line in fi:
    s = line.strip().split('\t')
    w = 1. / float(s[0]) * rate
    y = int(s[1])
    z = int(s[2])
    p = float(s[3])
    imp_num_train += 1 * w
    clk_num_train += y * w
    total_cost_train += z * w
    wyzps_train.append((w, y, z, p))
fi.close()

original_ecpc = total_cost_train * 1. / clk_num_train
original_ctr = clk_num_train * 1. / imp_num_train
rate_train = total_cost_train * 1. / imp_num_train
#print 'Train B/N:', rate_train

# read in test data
imp_num_test = 0
fi = open(sys.argv[2], 'r') # test.wyzp.txt
for line in fi:
    s = line.strip().split('\t')
    w = float(s[0])
    y = int(s[1])
    z = int(s[2])
    p = float(s[3])
    wyzps_test.append((w, y, z, p))
    imp_num_test += 1 * w # weight is always 1 here actually
    total_cost_test += z * w  # weight is always 1 here actually
    #if len(wyzps_test) >= num:
    #    break
fi.close()
rate_test = total_cost_test * 1. / imp_num_test
#print 'Test B/N:', rate_test
#print 'Test total cost:', total_cost_test

# parameters setting for each bidding strategy
b_p = rate_test / rate_train
print 'bp:', b_p
budget_proportions = [64, 32, 16, 8, 4, 2] # , 1, 0.5, 0.25] # , 32, 8]
const_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 301, 10)
rand_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 501, 10)
mcpc_paras = [1]
#lin_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 400, 10) + range(400, 800, 50)
lin_paras = range(1, 50, 1) + range(50, 100, 2) + range(100, 500, 5) + range(500, 1000, 10)

#algo_paras = {"const":const_paras, "rand":rand_paras, "mcpc":mcpc_paras, "lin":lin_paras}
algo_paras = {"lin":lin_paras}
prop_algo_optimal_para = {}
prop_algo_optimal_perf = {}

# initalisation finished
# rock!

# train
#print '\ntrain\n'
fo = open(sys.argv[3], 'w')  # rtb.train.results.txt
#header = "proportion\tclicks\tbids\timpressions\tbudget\tspend\tstrategy\tparameter"
header = "prop\tclks\tbids\timps\tbudget\tspend\talgo\tpara"
fo.write(header + "\n")
#print header
for proportion in budget_proportions:
    for algo in algo_paras:
        simulate_one_bidding_strategy(wyzps_train, total_cost_train, proportion, algo, fo)
fo.close()


# test
#print '\ntest\n'
b_p = 1
fo = open(sys.argv[4], 'w')  # rtb.test.results.txt
#header = "prop\tclks\tbids\timps\twinr\tbudget\tspend\tratio\talgo\tpara"
header = '{proportion:>4}\t{clicks:>5}\t{bids:>8}\t{impressions:>8}\t{winrate:>6}\t{budget:>8}\t{spend:>8}\t' \
           '{ratio:>6}\t{algorithm:>6}\t{parameter:>8}'.format(
            proportion = 'prop',
            clicks = 'clks',
            bids = 'bids',
            impressions = 'imps',
            winrate = 'winr',
            budget = 'budget',
            spend = 'spend',
            ratio = 'ratio',
            algorithm = 'algo',
            parameter = 'para'
        )
fo.write(header + "\n")
print header
for proportion in budget_proportions:
    for algo in prop_algo_optimal_para[proportion]:
        res = simulate_one_bidding_strategy_with_parameter(wyzps_test, total_cost_test, proportion,
                                                           algo, prop_algo_optimal_para[proportion][algo])
        fo.write(res + '\n')
        print res
fo.close()

#print prop_algo_optimal_para
#print prop_algo_optimal_perf