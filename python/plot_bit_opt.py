#!/usr/bin/python
import sys
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter

result_folder = '../results/'
unbias_setting_ls = ["imp", "uimp", "kimp", "bid"]
campaigns = ["1458", "2259", "2261", "2821", "2997", "3358", "3386", "3427", "3476", "all"]

# click

result_file = result_folder + 'ortb.all.bid.opt.click.results.test.txt'

data = pd.read_table(result_file, header=0)
data['ki'] = (data['kimp'] - data['imp']) * 100.0 / data['imp']
data['ui'] = (data['uimp'] - data['imp']) * 100.0 / data['imp']
data['bi'] = (data['bid'] - data['imp']) * 100.0 / data['imp']

#data['ki'] = pd.Series(["{0:.2f}%".format(val * 100) for val in data['ki']], index = data.index)
#data['ui'] = pd.Series(["{0:.2f}%".format(val * 100) for val in data['ui']], index = data.index)
#data['bi'] = pd.Series(["{0:.2f}%".format(val * 100) for val in data['bi']], index = data.index)

data_all = data[data['camp']=='all']

plt.figure(figsize=(5,4))
plt.plot(data_all['prop'], data_all['ui'], 'b-.', label='UOMP')
plt.plot(data_all['prop'], data_all['ki'], 'r--', label='KMMP')
plt.plot(data_all['prop'], data_all['bi'], 'k-', label='FULL')
ax = plt.gca()

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)

plt.legend(loc='lower right')
plt.xlabel('Budget proportion')
plt.xlim(4,64)
plt.ylabel('Improvement over BIAS')
#plt.xscale('log')
#plt.grid(True)
plt.title('Click improvement over BIAS')
plt.tight_layout()
plt.savefig(result_folder + 'ortb-bid-opt-click-improvement.pdf', dpi=300)
plt.close()



# ecpc

result_file = result_folder + 'ortb.all.bid.opt.ecpc.results.test.txt'

data = pd.read_table(result_file, header=0)
data['ki'] = (data['kimp'] - data['imp']) * 100.0 / data['imp']
data['ui'] = (data['uimp'] - data['imp']) * 100.0 / data['imp']
data['bi'] = (data['bid'] - data['imp']) * 100.0 / data['imp']

data_all = data[data['camp']=='all']

plt.figure(figsize=(5,4))
plt.plot(data_all['prop'], data_all['ui'], 'b-.', label='UOMP')
plt.plot(data_all['prop'], data_all['ki'], 'r--', label='KMMP')
plt.plot(data_all['prop'], data_all['bi'], 'k-', label='FULL')
ax = plt.gca()

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)

plt.legend(loc='upper left')
plt.xlabel('Budget proportion')
plt.xlim(4,64)
plt.ylabel('Improvement over BIAS')
#plt.xscale('log')
#plt.grid(True)
plt.title('eCPC improvement over BIAS')
plt.tight_layout()
plt.savefig(result_folder + 'ortb-bid-opt-ecpc-improvement.pdf', dpi=300)
plt.close()


# imps

result_file = result_folder + 'ortb.all.bid.opt.imps.results.test.txt'

data = pd.read_table(result_file, header=0)
data['ki'] = (data['kimp'] - data['imp']) * 100.0 / data['imp']
data['ui'] = (data['uimp'] - data['imp']) * 100.0 / data['imp']
data['bi'] = (data['bid'] - data['imp']) * 100.0 / data['imp']

data_all = data[data['camp']=='all']

plt.figure(figsize=(5,4))
plt.plot(data_all['prop'], data_all['ui'], 'b-.', label='UOMP')
plt.plot(data_all['prop'], data_all['ki'], 'r--', label='KMMP')
plt.plot(data_all['prop'], data_all['bi'], 'k-', label='FULL')
ax = plt.gca()

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(xticks)

plt.legend(loc='upper right')
plt.xlabel('Budget proportion')
plt.xlim(4,64)
plt.ylabel('Improvement over BIAS')
#plt.xscale('log')
#plt.grid(True)
plt.title('Imp. improvement over BIAS')
plt.tight_layout()
plt.savefig(result_folder + 'ortb-bid-opt-imps-improvement.pdf', dpi=300)
plt.close()