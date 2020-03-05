import numpy as np
import random


def create_sample(dimensions,value_range):
    parent = np.random.randint(value_range, size=(1,dimensions)).astype('float_').flatten()-(value_range/2)
    return parent


def create_new_sample(parents,dimensions,sample_rate,value_range,min_p_norms):
    hold_out_num = int(len(parents)*.1)
    idxs = np.argpartition(min_p_norms, hold_out_num if hold_out_num > 0 else 1)
    for i in range(len(parents)):
        if i in idxs:
            next
        else:
            if sample_rate >= random.uniform(0, 1):
                # idx = np.random.randint(0,len(parents))
                parents[i] = create_sample(dimensions,value_range)
    return parents