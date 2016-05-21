import pandas as pd
import matplotlib.pyplot as plt

data_folder = '../results/auc-rmse/'
advs = ['all'] # ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
algos = ['imp', 'uimp', 'kimp', 'bid']

for adv in advs:
    print 'running ' + adv

    first = True
    for algo in algos:
        file = data_folder + 'test.ar.rounds.' + algo + '.' + adv + '.txt'
        data = pd.read_table(file, names=['round', algo + '_auc', algo + '_rmse'])
        #print data
        #exit()

        if first:
            all_data = data.copy()
            first = False
        else:
            all_data[algo + '_auc'] = data[algo + '_auc']
            all_data[algo + '_rmse'] = data[algo + '_rmse']

    plt.figure(figsize=(5,4))
    plt.plot(all_data['round'], all_data['imp_auc'], '.g-', label='BIAS')
    plt.plot(all_data['round'], all_data['uimp_auc'], '+r-', label='UOMP')
    plt.plot(all_data['round'], all_data['kimp_auc'], 'sb-', label='KMMP')
    plt.plot(all_data['round'], all_data['bid_auc'], 'dk-', label='FULL')
    #plt.legend(loc='lower right') # , bbox_to_anchor=(1.5, 0)
    plt.xlabel('Training Round')
    plt.xlim(1,20)
    plt.ylabel('AUC')
    plt.grid(True)
    #plt.title('iPinYou campaign ' + adv + ' AUC performance')
    #plt.title('AUC performance')
    plt.tight_layout()
    plt.savefig(data_folder + adv + '-auc-perf-narrow.pdf', dpi=300)
    plt.close()