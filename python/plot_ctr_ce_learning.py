import pandas as pd
import matplotlib.pyplot as plt

data_folder = '../results/auc-rmse-ce-subtest/'
input_file = data_folder + 'all-ce-rounds.txt'
output_file = data_folder + 'all-ce-perf-narrow.pdf'

all_data = pd.read_table(input_file, header=0)

plt.figure(figsize=(5,4))
plt.plot(all_data['round'], all_data['imp'], '.g-', label='BIAS')
plt.plot(all_data['round'], all_data['uimp'], '+r-', label='UOMP')
plt.plot(all_data['round'], all_data['kimp'], 'sb-', label='KMMP')
plt.plot(all_data['round'], all_data['bid'], 'dk-', label='FULL')
plt.legend(loc='upper right') # , bbox_to_anchor=(1.5, 0)
plt.xlabel('Training Round')
plt.xlim(1,20)
plt.ylabel('Cross entropy')
plt.grid(True)
#plt.title('iPinYou campaign all cross-entropy performance')
plt.tight_layout()
plt.savefig(output_file, dpi=300)
plt.close()