#!/usr/bin/python
import sys
import os.path


result_folder = '../results/bid-opt/'
unbias_setting_ls = ["imp", "uimp", "kimp", "bid"]
campaigns = ["1458", "2259", "2261", "2821", "2997", "3358", "3386", "3427", "3476", "all"]

output_file = result_folder + '../all.bid.opt.results.test.txt'
output_file_2 = result_folder + '../all.bid.opt.click.results.test.txt'
output_file_3 = result_folder + '../all.bid.opt.ecpc.results.test.txt'
output_file_4 = result_folder + '../all.bid.opt.imps.results.test.txt'

header = '{campaign:>4}\t{setting:>4}\t{proportion:>4}\t{clicks:>5}\t{bids:>8}\t{impressions:>8}\t{winrate:>6}\t{budget:>8}\t{spend:>8}\t' \
           '{ratio:>6}\t{algorithm:>6}\t{parameter:>8}'.format(
            campaign = 'camp',
            setting = 'set',
            proportion = 'prop',
            clicks = 'clks',
            bids = 'bids',
            impressions = 'imps',
            winrate = 'winr',
            budget = 'budget',
            spend = 'spend',
            ratio = 'ratio',
            algorithm = 'algo',
            parameter = 'para'
        )

print header
fo = open(output_file, 'w')
fo.write(header.replace(' ', '') + "\n")
for campaign in campaigns:
    for unbias_setting in unbias_setting_ls:
        test_result_file = result_folder + 'bid.opt.results.{}.{}.test.txt'.format(unbias_setting, campaign)
        if os.path.isfile(test_result_file):
            fi = open(test_result_file, 'r')
            line_num = 0
            for line in fi:
                line_num += 1
                if line_num == 1:
                    continue
                fo.write(line)
                print line.strip()
fo.close()

import pandas as pd

fo = open(output_file_2, 'w')
fo.write('{}\t{}'.format('prop', 'camp'))
for setting in unbias_setting_ls:
    fo.write('\t{}'.format(setting))
fo.write('\n')

data = pd.read_table(output_file, header=0)
props = data['prop'].unique()
for prop in props:
    for campaign in campaigns:
        fo.write('{}\t{}'.format(prop, campaign))
        for setting in unbias_setting_ls:
            index = data[(data['set']==setting) & (data['prop']==prop) & (data['camp']==campaign)]['clks'].index[0]
            clks = data['clks'][index]
            fo.write('\t{}'.format(clks))
        fo.write('\n')
fo.close()


fo = open(output_file_3, 'w')
fo.write('{}\t{}'.format('prop', 'camp'))
for setting in unbias_setting_ls:
    fo.write('\t{}'.format(setting))
fo.write('\n')

data = pd.read_table(output_file, header=0)
data['ecpc'] = data['spend'] * 1.0 / data['clks']
props = data['prop'].unique()
for prop in props:
    for campaign in campaigns:
        fo.write('{}\t{}'.format(prop, campaign))
        for setting in unbias_setting_ls:
            index = data[(data['set']==setting) & (data['prop']==prop) & (data['camp']==campaign)]['ecpc'].index[0]
            ecpc = data['ecpc'][index]
            fo.write('\t{}'.format(ecpc))
        fo.write('\n')
fo.close()


fo = open(output_file_4, 'w')
fo.write('{}\t{}'.format('prop', 'camp'))
for setting in unbias_setting_ls:
    fo.write('\t{}'.format(setting))
fo.write('\n')

data = pd.read_table(output_file, header=0)
props = data['prop'].unique()
for prop in props:
    for campaign in campaigns:
        fo.write('{}\t{}'.format(prop, campaign))
        for setting in unbias_setting_ls:
            index = data[(data['set']==setting) & (data['prop']==prop) & (data['camp']==campaign)]['imps'].index[0]
            imps = data['imps'][index]
            fo.write('\t{}'.format(imps))
        fo.write('\n')
fo.close()