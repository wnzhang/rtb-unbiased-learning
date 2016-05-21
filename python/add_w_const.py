import sys

print 'Begin to add w=1 to', ((sys.argv[1]).split('/'))[-1]
fi = open(sys.argv[1], 'r') # yzx
fo = open(sys.argv[2], 'w') # wyzx where w = 1
for line in fi:
    if line.strip():
        s = line.strip().split()
        nl = '\t'.join( ['1'] + s)
        fo.write(nl + '\n')
fi.close()
fo.close()
print 'Finished creating file:', ((sys.argv[2]).split('/'))[-1]
print '-------------------'