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
    return winfun

def win_prob(bid):
    if bid in winfun:
        return winfun[bid]
    for key in sorted(winfun):
        if bid <= key:
            return winfun[key]
    return 1.

def work(input_file, output_file, idx):
    global winfun
    fi = open(input_file, 'r')
    mps = []
    for line in fi:
        mp = int(line.strip().split()[idx])
        mps.append(mp)
    winfun = get_bid_landscape(mps)

    print 'output win prob to ' + output_file
    fof = open(output_file, 'w')
    for bid in range(302):
        fof.write('%d\t%.8f\n' % (bid, win_prob(bid)))
    fof.close()

winfun = {}
advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
for adv in advs:
    print adv

    input_test_file = '../../make-ipinyou-data/{}/test.yzx.txt'.format(adv)
    win_prob_file = '../results/win-prob/{}.test.winprob.txt'.format(adv)

    work(input_test_file, win_prob_file, 1)

    input_full_file = '../../make-ipinyou-data/{}/train.wyzx.bid.txt'.format(adv)
    win_prob_file = '../results/win-prob/{}.bid.winprob.txt'.format(adv)

    work(input_full_file, win_prob_file, 2)
