#!/usr/bin/python
import sys
from collections import defaultdict
from collections import OrderedDict

print 'Begin to combine files:', ((sys.argv[1]).split('/'))[-1], ((sys.argv[2]).split('/'))[-1]
bo_dict = defaultdict(list)

fi = open(sys.argv[1], 'r') #wyb.imp
for line in fi:
    s = line.strip().split()
    #s[0] = '1'
    o = "1"
    key = int(s[2])
    bo_dict[key].append(o)
fi.close()

fi = open(sys.argv[2], 'r') #wyb.lose
for line in fi:
    s = line.strip().split()
    #s[0] = '0'
    o = "0"
    key = int(s[2])
    bo_dict[key].append(o)
fi.close()

bo_dict_sort = OrderedDict(sorted(bo_dict.items()))

fo = open(sys.argv[3], 'w')
for key in bo_dict_sort:
    line = ' '.join([str(key)] + bo_dict_sort[key])
    fo.write(line + '\n')
fo.close()
print 'Finished creating file:', ((sys.argv[3]).split('/'))[-1]
print '-------------------'



