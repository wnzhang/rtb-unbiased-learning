#!/usr/bin/python
import os
import  sys

results = []
path = sys.argv[1]
for file in os.listdir(path):
    if not file.endswith('~') and 'test.aucRmse.' in file:
        s = file.strip().split('.')
        algo = s[2]
        cam = s[3]
        s[3] = algo
        s[2] = cam
        del s[4]

        ss = []

        fi = open(path + '/'+file, 'r')
        for line in fi:
            ss = line.strip().split()
        s = s + ss
        results.append(s)
fo = open(sys.argv[2], 'w')
fo.write('campaign\t' + 'algo\t' + 'auc\t' + 'rmse\n')
for i in sorted(results):
    s = '\t'.join(i[2:])
    fo.write(s + '\n')
fo.close()
