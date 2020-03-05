import numpy as np
import random


def create_sample(dimensions,value_range):
    parent = np.random.randint(value_range, size=(1,dimensions)).astype('float_').flatten()-(value_range/2)
    return parent


def create_new_sample(parents,dimensions,sample_rate,value_range):
    for i in range(2,len(parents)):
        if sample_rate >= random.uniform(0, 1):
            idx = np.random.randint(0,len(parents))
            parents[idx] = create_sample(dimensions,value_range)
    return parents