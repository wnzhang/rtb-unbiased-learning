import math
import numpy as np

def get_relative_information_gain(y, yp):
    # cross entropy = avg( y[i] log yp[i] + (1 - y[i]) log(1 - yp[i]) )
    # entropy = - (avg(y) log avg(y) + (1 - avg(y)) log(1 - avg(y)))
    # rig = entropy + cross_entropy

    for i in range(len(yp)):
        if yp[i] < 1E-8:
            yp[i] = 1E-8
        elif yp[i] > 1 - 1E-8:
            yp[i] = 1 - 1E-8

    y = np.array(y)
    yp = np.array(yp)

    '''
    p = np.average(yp)
    h = - (p * np.log(p) + (1 - p) * np.log(1 - p))
    ce = np.average(y * np.log2(yp) + (1 - y) * np.log2(1 - yp))
    rig = (ce + h) / h
    '''

    ce = 0.
    for i in range(len(yp)):
        ce += y[i] * np.log2(yp[i]) + (1- y[i]) * np.log2(1 - yp[i])
    ce = ce / len(yp)
    p_avg = np.average(y)
    h = - (p_avg * np.log2(p_avg) + (1 - p_avg) * np.log2(1 - p_avg))
    ig = ce + h
    rig = ig / h
    return rig


def get_cross_entropy(y, yp):
    # cross entropy = avg( y[i] log yp[i] + (1 - y[i]) log(1 - yp[i]) )
    # entropy = - (avg(y) log avg(y) + (1 - avg(y)) log(1 - avg(y)))
    # rig = entropy + cross_entropy

    for i in range(len(yp)):
        '''
        if yp[i] < 1E-8:
            yp[i] = 1E-8
        elif yp[i] > 1 - 1E-8:
            yp[i] = 1 - 1E-8
        '''

    y = np.array(y)
    yp = np.array(yp)

    '''
    p = np.average(yp)
    h = - (p * np.log(p) + (1 - p) * np.log(1 - p))
    ce = np.average(y * np.log2(yp) + (1 - y) * np.log2(1 - yp))
    rig = (ce + h) / h
    '''

    ce = 0.
    for i in range(len(yp)):
        ce += - y[i] * np.log2(yp[i]) - (1- y[i]) * np.log2(1 - yp[i])
    ce = ce / len(yp)
    return ce