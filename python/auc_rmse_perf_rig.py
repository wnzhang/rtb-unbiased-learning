#!/usr/bin/python
import os
import  sys

results = []
data_folder = '../results/auc-rmse-rig/'
advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
algos = ['imp', 'uimp', 'kimp', 'bid']
cam_algo_perf = {}
for adv in advs:
    for algo in algos:
        ss = []
        fi = open(data_folder + 'test.aucRmse.' + algo + '.' + adv + '.txt', 'r')
        for line in fi:
            ss = line.strip().split()
            break  # only one line

        if adv not in cam_algo_perf:
            cam_algo_perf[adv] = {}
        cam_algo_perf[adv][algo] = ('%.4f' % float(ss[0]), '%.4f' % float(ss[1]), '%.4f' % float(ss[2]))
fo = open(data_folder + 'cam-algo-auc-rmse-rig.txt', 'w')
fo.write('auc\n')
fo.write('cam\t' + '\t'.join(algos) + '\n')
for adv in advs:
    fo.write(adv)
    for algo in algos:
        fo.write('\t' + cam_algo_perf[adv][algo][0])
    fo.write('\n')

fo.write('\nrmse\n')
fo.write('cam\t' + '\t'.join(algos) + '\n')
for adv in advs:
    fo.write(adv)
    for algo in algos:
        fo.write('\t' + cam_algo_perf[adv][algo][1])
    fo.write('\n')

fo.write('\nrig\n')
fo.write('cam\t' + '\t'.join(algos) + '\n')
for adv in advs:
    fo.write(adv)
    for algo in algos:
        fo.write('\t' + cam_algo_perf[adv][algo][2])
    fo.write('\n')
fo.close()
