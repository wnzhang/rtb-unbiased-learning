import math
import numpy as np

data_folder = '../../make-ipinyou-data/'
output_correlation_file = data_folder + 'correlations.txt'
advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']

for adv in advs:
    fi = open(data_folder + adv + '/test.yzx.txt')
    sum = 0.
    num = 0
    for line in fi:
        y = int(line.strip().split()[0])
        sum += y
        num += 1
    fi.close()
    p = sum / num
    h = p * np.log2(p) + (1 - p) * np.log2(1 - p)
    print '%s\t%.8f\t%.8f' % (adv, p, -h)