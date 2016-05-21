#!/usr/bin/python
import sys
import math


def bidding_mcpc(ecpc, pctr):
    return int(ecpc * pctr)

def win_auction(case, bid):
    return bid > case[1]  # bid > winning price

# budgetProportion clk cnv bid imp budget spend para
def simulate_one_bidding_strategy_with_parameter(cases, ctrs, tcost, proportion, writer_win, writer_lose):
    budget = int(tcost / proportion) # intialise the budget
    wins = []
    cost = 0
    clks = 0
    bids = 0
    imps = 0
    for idx in range(0, len(cases)):
        pctr = ctrs[idx]
        bid = bidding_mcpc(original_ecpc, pctr)
        bids += 1
        case = cases[idx]
        if win_auction(case, bid):
            imps += 1
            clks += case[0]
            cost += case[1]
            writer_win.write(str(case[0]) + '\t' + str(case[1]) + '\t' + str(case[2])+'\n')
        else:
            writer_lose.write(str(bid)+'\n')

        if cost > budget:
            break
    #return str(proportion) + '\t' + str(clks) + '\t' + str(bids) + '\t' + \
        #str(imps) + '\t' + str(budget) + '\t' + str(cost) + '\t' + str(para)
    return "finished"

'''
def simulate_one_bidding_strategy(cases, ctrs, tcost, proportion, writer_win, writer_lose):
    para = 1
    res = simulate_one_bidding_strategy_with_parameter(cases, ctrs, tcost, proportion,para)
    #print res
    for win_bid in res:
        writer.write(win_bid + '\n')
'''
'''
if len(sys.argv) < 3:
    print 'Usage: python mcpc-bid.py train.yzp.txt train.win.yzp.txt'
    exit(-1)
'''

clicks_prices = []  # clk and price
y_z_x = []          # y z and x
pctrs = []          # pCTR from logistic regression prediciton
total_cost_train = 0
total_cost = 0      # total original cost during the test data
original_ecpc = 0.  # original eCPC from train data
original_ctr = 0.   # original ctr from train data

# read in train.yzp.base for original_ecpc and original_ctr and orginal pctr
fi = open(sys.argv[1], 'r') # train.yzp.base.txt
first = True
imp_num = 0
clk_num = 0
for line in fi:
    s = line.strip().split()
    click = int(s[0])  # y
    cost = int(s[1])  # z
    pctrs.append(float(s[2])) #p
    imp_num += 1
    clk_num += click
    #original_ctr += click
    #original_ecpc += cost
    total_cost_train += cost
fi.close()
original_ecpc = total_cost_train * 1.0 / clk_num

# read in train.yzx.bid for bid information
fi = open(sys.argv[2], 'r') # train.yzp.txt
for line in fi:
    s = line.strip().split()
    click = int(s[0])
    #pctrs.append(float(s[2]))
    winning_price = int(s[1])
    x = ' '.join(s[2:])
    y_z_x.append((click, winning_price, x))
    clicks_prices.append((click, winning_price))
    total_cost += winning_price
fi.close()

# parameters setting for each bidding strategy
budget_proportions = [1] #64, 16] # , 32, 8]
mcpc_paras = [1]


# initalisation finished
# rock!

fo = open(sys.argv[3], 'w')  # train.yzx.imp.txt
fp = open(sys.argv[4], 'w')  # train.yzx.lose.txt
#header = "proportion\tclicks\tbids\timpressions\tbudget\tspend\tparameter"
#header = "prop\tclks\tbids\timps\tbudget\tspend\tpara"
#fo.write(header + "\n")
#print header
for proportion in budget_proportions:

    #simulate_one_bidding_strategy(clicks_prices, pctrs, total_cost, proportion, fo, fp)
    simulate_one_bidding_strategy_with_parameter(y_z_x, pctrs, total_cost, proportion, fo, fp)
fo.close()
fp.close()
print 'finished'
