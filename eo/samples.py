import numpy as np
import random


def create_sample(dimensions):
    print(np.random.randint(dimensions, size=(1,dimensions)).astype('float_').flatten())
    sys.exit()
    parent = np.random.randint(dimensions, size=(1,dimensions)).astype('float_').flatten()-(dimensions/2)
    print(parent)
    return parent


def create_new_sample(parents,dimensions,sample_rate):
    for i in range(len(parents)):
        if sample_rate >= random.uniform(0, 1):
            idx = np.random.randint(0,len(parents))
            parents[idx] = create_sample(dimensions)
    return parents