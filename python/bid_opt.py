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

def bidding_ortb(pctr, base_ctr, para):
    return int(math.sqrt(pctr * para[0] * para[1] / base_ctr + para[0] * para[0]) - para[0])

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
        elif algo == "ortb":
            bid = bidding_ortb(pctr, original_ctr, para)
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
    wr = imps * 1.0 / bids
    sr = max (0.001, cost * 1.0 / budget)
    wr_sr = wr / sr

    if proportion not in prop_algo_optimal_perf:
        prop_algo_optimal_perf[proportion] = {}
        prop_algo_optimal_para[proportion] = {}
        prop_algo_optimal_wr_sr[proportion] = {}
    if algo not in prop_algo_optimal_perf[proportion]:
        prop_algo_optimal_perf[proportion][algo] = -1
        prop_algo_optimal_wr_sr[proportion][algo] = -1
    if clks > prop_algo_optimal_perf[proportion][algo]:
        prop_algo_optimal_perf[proportion][algo] = clks
        prop_algo_optimal_para[proportion][algo] = para
        prop_algo_optimal_wr_sr[proportion][algo] = wr_sr
    elif clks == prop_algo_optimal_perf[proportion][algo]:
        if wr_sr > prop_algo_optimal_wr_sr[proportion][algo]:
            prop_algo_optimal_perf[proportion][algo] = clks
            prop_algo_optimal_para[proportion][algo] = para
            prop_algo_optimal_wr_sr[proportion][algo] = wr_sr

    #return '%d\t%d\t%d\t%d\t%.3f\t%d\t%d\t%.3f\t%s\t%d' \
    #       % (proportion, clks, bids, imps, imps * 1.0 / bids, budget, cost, cost * 1.0 / budget, algo, para)

    return '{campaign:>4}\t{setting:>4}\t{proportion:>4}\t{clicks:>5}\t{bids:>8}\t{impressions:>8}\t' \
           '{winrate:>6}\t{budget:>8}\t{spend:>8}\t' \
           '{ratio:>6}\t{algorithm:>6}\t{parameter:>8}'.format(
            campaign = campaign,
            setting = unbias_setting,
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
        writer.write(res.replace(' ', '') + '\n')

'''
if len(sys.argv) == 6:
    print 'Usage: python ../python/rtb_opt.py $folder/$campaign/train.wyzp.imp.txt
    $folder/$campaign/test.wyzp.txt
    $resultsfolder/bid.opt.results.imp.$campaign.train.txt
    $resultsfolder/bid.opt.results.imp.$campaign.test.txt'
    exit(-1)
'''

data_folder = '../../make-ipinyou-data/'
result_folder = '../results/bid-opt/'
campaign = sys.argv[1]
unbias_setting = sys.argv[2]
train_file = data_folder + campaign + '/train.wyzp.{}.txt'.format(unbias_setting)
test_file = data_folder + campaign + '/test.wyzp.txt'
train_result_file = result_folder + 'bid.opt.results.{}.{}.train.txt'.format(unbias_setting, campaign)
test_result_file = result_folder + 'bid.opt.results.{}.{}.test.txt'.format(unbias_setting, campaign)

wyzps_train = []          # winrate, clk and price and pctr for train
wyzps_test = []           # winrate, clk and price and pctr for test
total_cost_train = 0     # total original cost during the train data
total_cost_test = 0      # total original cost during the test data
original_ecpc = 0.       # original eCPC from train data
original_ctr = 0.        # original ctr from train data

# read in train data for original_ecpc and original_ctr
# fi = open(train_file, 'r') # train.wyzp.xxxx.txt
# ws = 0
# num = 0
# for line in fi:
#     s = line.strip().split('\t')
#     ws += 1. / float(s[0])
#     num += 1
# fi.close()
# rate = num / ws

imp_num_train = 0
clk_num_train = 0
fi = open(train_file, 'r')
for line in fi:
    s = line.strip().split('\t')
    w = 1. / float(s[0]) # * rate
    y = int(s[1])
    z = int(s[2])
    p = float(s[3])
    imp_num_train += 1 * w
    clk_num_train += y * w
    total_cost_train += z * w
    wyzps_train.append((w, y, z, p))
fi.close()
wyzps_train.reverse()

original_ecpc = total_cost_train * 1. / clk_num_train
original_ctr = clk_num_train * 1. / imp_num_train
rate_train = total_cost_train * 1. / imp_num_train
#print 'Train B/N:', rate_train
print 'Base ctr:', original_ctr
# read in test data
imp_num_test = 0
fi = open(test_file, 'r') # test.wyzp.txt
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
#print 'bp:', b_p

budget_proportions = [64, 32, 16, 8, 4] # , 1, 0.5, 0.25] # , 32, 8]
const_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 301, 10)
rand_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 501, 10)
mcpc_paras = [1]
#lin_paras = range(2, 20, 2) + range(20, 100, 5) + range(100, 400, 10) + range(400, 800, 50)
lin_paras = [t * 0.025 for t in (range(1, 400, 1) + range(400, 1000, 5) + range(1000, 2000, 20))]
#algo_paras = {"const":const_paras, "rand":rand_paras, "mcpc":mcpc_paras, "lin":lin_paras}
algo_paras = {"lin":lin_paras}
prop_algo_optimal_para = {}
prop_algo_optimal_perf = {}
prop_algo_optimal_wr_sr = {}

# initalisation finished
# rock!

# train
#print '\ntrain\n'
fo = open(train_result_file, 'w')  # rtb.train.results.txt
#header = "proportion\tclicks\tbids\timpressions\tbudget\tspend\tstrategy\tparameter"
#header = "prop\tclks\tbids\timps\tbudget\tspend\talgo\tpara"
header = '{campaign:>4}\t{setting:>4}\t{proportion:>4}\t{clicks:>5}\t{bids:>8}\t{impressions:>8}\t{winrate:>6}\t{budget:>8}\t{spend:>8}\t' \
           '{ratio:>6}\t{algorithm:>6}\t{parameter:>8}'.format(
            campaign = 'camp',
            setting = 'set',
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
fo.write(header.replace(' ', '') + "\n")
#print header
for proportion in budget_proportions:
    for algo in algo_paras:
        simulate_one_bidding_strategy(wyzps_train, total_cost_train, proportion, algo, fo)
fo.close()


# test
#print '\ntest\n'
b_p = 1
fo = open(test_result_file, 'w')  # rtb.test.results.txt
#header = "prop\tclks\tbids\timps\twinr\tbudget\tspend\tratio\talgo\tpara"

fo.write(header.replace(' ', '') + "\n")
print header
for proportion in budget_proportions:
    for algo in prop_algo_optimal_para[proportion]:
        res = simulate_one_bidding_strategy_with_parameter(wyzps_test, total_cost_test, proportion,
                                                           algo, prop_algo_optimal_para[proportion][algo])
        fo.write(res.replace(' ', '') + '\n')
        print res
fo.close()

#print prop_algo_optimal_para
#print prop_algo_optimal_perf