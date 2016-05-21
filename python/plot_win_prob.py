import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt

data_folder = '../results/win-prob/'
output_correlation_file = data_folder + 'correlations.txt'
advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']

fo = open(output_correlation_file, 'w')
#fo.write('campaign\tuimp-pearson\tkimp-pearson\tuimp-cosine\tkimp-cosine\tuimp-kl\tkimp-kl\n')
fo.write('campaign\tuimp-pearson\tkimp-pearson\tfull-pearson\tuimp-kl\tkimp-kl\tfull-kl\n')

for adv in advs:
    print 'running ' + adv
    uimp_file = data_folder + adv + '.uimp.winprob.txt'
    kimp_file = data_folder + adv + '.kimp.winprob.txt'
    full_file = data_folder + adv + '.bid.winprob.txt'
    test_file = data_folder + adv + '.test.winprob.txt'

    uimp_data = pd.read_table(uimp_file, names=['bid', 'uimp'])
    kimp_data = pd.read_table(kimp_file, names=['bid', 'kimp'])
    full_data = pd.read_table(full_file, names=['bid', 'full'])
    test_data = pd.read_table(test_file, names=['bid', 'test'])

    data = uimp_data
    data['kimp'] = kimp_data['kimp']
    data['full'] = full_data['full']
    data['test'] = test_data['test']

    data['uimpd'] = data['uimp']
    data['kimpd'] = data['kimp']
    data['fulld'] = data['full']
    data['testd'] = data['test']

    data = data[data['bid'] <= 300]

    for i in range(0, len(data) - 1):
        data['uimpd'][len(data) - 1 - i] -= data['uimpd'][len(data) - 1 - i - 1]
        data['kimpd'][len(data) - 1 - i] -= data['kimpd'][len(data) - 1 - i - 1]
        data['fulld'][len(data) - 1 - i] -= data['fulld'][len(data) - 1 - i - 1]
        data['testd'][len(data) - 1 - i] -= data['testd'][len(data) - 1 - i - 1]

    corr_pearson = data.corr(method='pearson')
    uimp_pearson = corr_pearson['uimp']['test']
    kimp_pearson = corr_pearson['kimp']['test']
    full_pearson = corr_pearson['full']['test']

    uimp_cosine = 1 - cosine(data['uimp'], data['test'])
    kimp_cosine = 1 - cosine(data['kimp'], data['test'])
    full_cosine = 1 - cosine(data['full'], data['test'])

    uimp_kl_div = np.sum(data['testd'] * np.log10(data['testd'] / data['uimpd']), axis=0)
    kimp_kl_div = np.sum(data['testd'] * np.log10(data['testd'] / data['kimpd']), axis=0)
    full_kl_div = np.sum(data['testd'] * np.log10(data['testd'] / data['fulld']), axis=0)

    #fo.write('%s\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n' % (adv, uimp_pearson, kimp_pearson, uimp_cosine, kimp_cosine, uimp_kl_div, kimp_kl_div))
    fo.write('%s\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n' % (adv, uimp_pearson, kimp_pearson, full_pearson,
                                                           uimp_kl_div, kimp_kl_div, full_kl_div))

    plt.figure(figsize=(5,4))
    plt.plot(data['bid'], data['uimp'], 'b-.', label='UOMP')
    plt.plot(data['bid'], data['kimp'], 'r--', label='KMMP')
    plt.plot(data['bid'], data['full'], 'g:', label='FULL')
    plt.plot(data['bid'], data['test'], 'k-', label='Truth')
    plt.legend(loc='lower right')
    plt.xlabel('bid price')
    plt.xlim(0,300)
    plt.ylabel('Estimated win probability')
    plt.grid(True)
    plt.title('iPinYou campaign ' + adv)
    plt.tight_layout()
    plt.savefig(data_folder + adv + '-winprob.pdf', dpi=300)
    plt.close()

fo.close()