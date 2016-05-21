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
def simulate_one_bidding_strategy_with_parameter(yzps, tcost, proportion, algo, para):
    budget = int(tcost / proportion) # intialise the budget
    cost = 0
    clks = 0
    bids = 0
    imps = 0
    for yzp in yzps:
        bid = 0
        pctr = yzp[2]
        winprice = yzp[1]
        clk = yzp[0]
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
        bids += 1
        if bid > yzp[1]:
            imps += 1
            clks += clk
            cost += winprice
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

    return '%d\t%d\t%d\t%d\t%.3f\t%d\t%d\t%.3f\t%s\t%d' \
           % (proportion, clks, bids, imps, imps * 1.0 / bids, budget, cost, cost * 1.0 / budget, algo, para)
    # return str(proportion) + '\t' + str(clks) + '\t' + str(bids) + '\t' + \
    #     str(imps) + '\t' + str(budget) + '\t' + str(cost) + '\t' + + '\t' + algo + '\t' + str(para)

def simulate_one_bidding_strategy(cases, tcost, proportion, algo, writer):
    paras = algo_paras[algo]
    for para in paras:
        res = simulate_one_bidding_strategy_with_parameter(cases, tcost, proportion, algo, para)
        # print res
        writer.write(res + '\n')

'''
if len(sys.argv) == 6:
    print 'Usage: python rtb_opt.py train.(win).yzx.txt test.yzx.txt rtb.result.txt'
    exit(-1)
'''

yzps_train = []          # clk and price and pctr for train
yzps_test = []           # clk and price and pctr for test
total_cost_train = 0     # total original cost during the train data
total_cost_test = 0      # total original cost during the test data
original_ecpc = 0.       # original eCPC from train data
original_ctr = 0.        # original ctr from train data

# read in train data for original_ecpc and original_ctr
fi = open(sys.argv[1], 'r') # train.yzx.txt
first = True
imp_num = 0
clk_num = 0
for line in fi:
    s = line.strip().split('\t')
    y = int(s[0])
    z = int(s[1])
    p = float(s[2])
    imp_num += 1
    clk_num += y
    #original_ctr += y
    total_cost_train += z
    yzps_train.append((y, z, p))
fi.close()

original_ecpc = total_cost_train * 1.0 / clk_num
original_ctr = clk_num * 1.0 / imp_num

# read in test data
fi = open(sys.argv[2], 'r') # test.yzp.txt
for line in fi:
    s = line.strip().split('\t')
    y = int(s[0])
    z = int(s[1])
    p = float(s[2])
    yzps_test.append((y, z, p))
    total_cost_test += z
fi.close()

# parameters setting for each bidding strategy
budget_proportions = [16, 8, 4, 2] # , 32, 8]
const_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 301, 10)
rand_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 501, 10)
mcpc_paras = [1]
lin_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 400, 10) + range(400, 800, 50)

#algo_paras = {"const":const_paras, "rand":rand_paras, "mcpc":mcpc_paras, "lin":lin_paras}
algo_paras = {"lin":lin_paras}
#algo_paras = sys.argv[5]
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
        simulate_one_bidding_strategy(yzps_train, total_cost_train, proportion, algo, fo)
fo.close()


# test
#print '\ntest\n'
fo = open(sys.argv[4], 'w')  # rtb.test.results.txt
header = "prop\tclks\tbids\timps\twinr\tbudget\tspend\tratio\talgo\tpara"
fo.write(header + "\n")
print header
for proportion in budget_proportions:
    for algo in prop_algo_optimal_para[proportion]:
        res = simulate_one_bidding_strategy_with_parameter(yzps_test, total_cost_test, proportion,
                                                           algo, prop_algo_optimal_para[proportion][algo])
        fo.write(res + '\n')
        print res
fo.close()
