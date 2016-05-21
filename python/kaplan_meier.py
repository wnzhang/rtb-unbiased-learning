#!/usr/bin/python
import sys
from collections import defaultdict

print 'Begin to build Kaplan Meier estimator based on', ((sys.argv[1]).split('/'))[-1], 'and', ((sys.argv[3]).split('/'))[-1], 'for', ((sys.argv[2]).split('/'))[-1]
#build zb dictionary
bo_dict = defaultdict(list)
#add smooth data
upper = 301
for i in range(0, upper):
    bo_dict[i].append(1)

fi = open(sys.argv[1], 'r')
size = upper
for line in fi:
    s = line.strip().split()
    #b = int(s[0]) #boolean value
    b = int(s[0]) #bid price
    for i in range(1, len(s)):
        o = int(s[i])
        bo_dict[b].append(o)
        size += 1
fi.close()

size0 = size - 1

#build bdn list
bdns = []
wins = 0
for z in bo_dict:
    wins = sum(bo_dict[z])
    b = z
    d = wins
    n = size0
    bdn = [b, d, n]
    bdns.append(bdn)

    size0 -= len(bo_dict[z]) # len


#build new winning probability
zw_dict = {}
min_p_w = 0
bdns_length = len(bdns)
count = 0
p_l_tmp = (size - 1.0) / size
for bdn in bdns:
    count += 1
    b = float(bdn[0])
    d = float(bdn[1])
    n = float(bdn[2])
    p_l = p_l_tmp
    p_w = max(1.0 - p_l, min_p_w)
    zw_dict[int(b)] = p_w
    if count < bdns_length:
        p_l_tmp = (n - d) / n * p_l_tmp

def win_prob(bid):
    if bid in zw_dict:
        return zw_dict[bid]
    last_key = -1
    for key in zw_dict:
        if last_key == -1:
            last_key = key
        if bid <= key:
            return zw_dict[last_key]
        else:
            last_key = key
    return 1.

#read wyzx.imp to build wyzx.uimp.km
fi1 = open(sys.argv[2], 'r')
fi2 = open(sys.argv[3], 'r')
fo = open(sys.argv[4], 'w')
for line1 in fi1:
    line2 = fi2.readline()
    s1 = line1.strip().split()
    s2 = line2.strip().split()
    z = int(s2[2])
    s1[0] = str(win_prob(z))
    fo.write('\t'.join(s1) + '\n')
fi1.close()
fi2.close()
fo.close()
print 'Finished creating file:', ((sys.argv[4]).split('/'))[-1]
print '-------------------'

# output win prob
adv = 'null'
for a in ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']:
    if a in sys.argv[3]:
        adv = a
        break
win_prob_file = '../results/win-prob/{}.kimp.winprob.txt'.format(adv)
print 'output win prob to ' + win_prob_file
fof = open(win_prob_file, 'w')
for bid in range(302):
    fof.write('%d\t%.8f\n' % (bid, win_prob(bid)))
fof.close()

#print bdns
#print 'km win fun'
#print zw_dict
#print bo_dict[6]
'''
a = {}
for i in bo_dict:
    a[i] = sum(bo_dict[i])
print a
'''