#!/usr/bin/python
import os
import  sys
import os.path

results = []
data_folder = '../results/auc-rmse-ce-subtest/'
advs = ['1458', '2259', '2261', '2821', '2997', '3358', '3386', '3427', '3476', 'all']
algos = ['imp', 'uimp', 'kimp', 'bid']
cam_algo_perf = {}
for adv in advs:
    for algo in algos:
        ss = []
        file = data_folder + 'test.ar.rounds.' + algo + '.' + adv + '.txt'
        if os.path.isfile(file):
            fi = open(file, 'r')
            for line in fi:
                ss = line.strip().split()
                #break  # only one line
            # perfs = ('%.4f' % float(ss[0]), '%.4f' % float(ss[1]), '%.4f' % float(ss[2]))
                perf = (float(ss[1]), float(ss[2]), float(ss[3]))
                if adv not in cam_algo_perf:
                    cam_algo_perf[adv] = {}
                if algo not in cam_algo_perf[adv]:
                    cam_algo_perf[adv][algo] = perf
                elif perf[2] < cam_algo_perf[adv][algo][2]:
                    cam_algo_perf[adv][algo] = perf


fo = open(data_folder + 'cam-algo-auc-rmse-ce.txt', 'w')
fo.write('auc\n')
fo.write('cam\t' + '\t'.join(algos) + '\n')
for adv in advs:
    fo.write(adv)
    for algo in algos:
        fo.write('\t' + '%.4f' % cam_algo_perf[adv][algo][0])
    fo.write('\n')

fo.write('\nrmse\n')
fo.write('cam\t' + '\t'.join(algos) + '\n')
for adv in advs:
    fo.write(adv)
    for algo in algos:
        fo.write('\t' + '%.4f' % cam_algo_perf[adv][algo][1])
    fo.write('\n')

fo.write('\nce\n')
fo.write('cam\t' + '\t'.join(algos) + '\n')
for adv in advs:
    fo.write(adv)
    for algo in algos:
        fo.write('\t' + '%.6f' % cam_algo_perf[adv][algo][2])
    fo.write('\n')
fo.close()
