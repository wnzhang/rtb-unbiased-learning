bid_upper = 301

def estimate_c(bw):
    # model win = b / (b + l)
    ls = range(1, bid_upper)
    min_loss = 9E50
    optimal_c = -1
    for l in ls:
        loss = 0
        for (bid, win) in bw:
            y = win
            yp = bid * 1.0 / (bid + l)
            loss += (y - yp) * (y - yp)
        if loss < min_loss:
            min_loss = loss
            optimal_c = l
    return optimal_c

data_folder = '../results/win-prob/'
output_file = data_folder + 'camp-set-c.txt'
advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
sets = ['imp', 'uimp', 'kimp', 'bid']

fo = open(output_file, 'w')
for adv in advs:
    print adv
    for set in sets:
        fi = open(data_folder + '{}.{}.winprob.txt'.format(adv, set), 'r')
        bw = []
        for line in fi:
            s = line.strip().split()
            bw.append((int(s[0]), float(s[1])))
        fi.close()
        optimal_c = estimate_c(bw)
        fo.write('{}\t{}\t{}\n'.format(adv, set, optimal_c))
fo.close()
