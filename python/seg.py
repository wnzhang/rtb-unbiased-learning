#!/usr/bin/python
import sys

print 'Begin to segment', ((sys.argv[1]).split('/'))[-1]
line_num = 0
seg_point = 0
count = 0
#calculate line number
fi = open(sys.argv[1], 'r') #train.wyxz.txt
for line in fi.xreadlines():
    if line.strip():
        line_num += 1
fi.close()
#segment train.yxz.txt
fi = open(sys.argv[1], 'r') #train.wyxz.txt
fo = open(sys.argv[2], 'w') #train.wyzx.base.txt
fp = open(sys.argv[3], 'w') #train.wyzx.bid.txt
seg_point = line_num / 3
for line in fi:
    count += 1
    if count <= seg_point:
        fo.write(line)
    else:
        fp.write(line)
#print line_num, seg_point, count

fo.close()
fp.close()
fi.close()
print 'Finished creating files:', ((sys.argv[2]).split('/'))[-1], ((sys.argv[3]).split('/'))[-1]
print '-------------------'
