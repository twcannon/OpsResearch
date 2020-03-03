import numpy as np
import random


def mate_mean(parent_matrix):
    return np.mean(parent_matrix, axis=0)


def mate_median(parent_matrix):
    return np.median(parent_matrix, axis=0)


def mate_swap(parent_matrix):
    p_shape = parent_matrix.shape
    parent_slices = np.sort(np.asarray(random.sample(range(p_shape[1]), p_shape[0])))
    child_vector = []
    for index in range(p_shape[0]):
        parent_vector = parent_matrix[index].tolist()
        if index == 0:
            if parent_slices[index] == 0:
                child_vector = child_vector + [parent_vector[0]]
            else:
                child_vector = child_vector + parent_vector[0:parent_slices[index]+1]
        elif index == p_shape[0]-1:
            child_vector = child_vector + parent_vector[(parent_slices[index-1]+1):p_shape[1]]
        else:
            if (parent_slices[index-1]+1) == parent_slices[index]:
                child_vector = child_vector + [parent_vector[parent_slices[index]]]
            else:
                child_vector = child_vector + parent_vector[(parent_slices[index-1]+1):parent_slices[index]+1]
    return child_vector


def mutate_flip(parent_vector):
    i1, i2 = random.sample(range(len(parent_vector)), 2)
    parent_vector[i1], parent_vector[i2] = parent_vector[i2], parent_vector[i1]
    return parent_vector


def mutate_insert(parent_vector):
    parent_vector = list(parent_vector)
    index_list    = range(len(parent_vector))
    element       = parent_vector.pop(random.sample(index_list, 1)[0])
    parent_vector.insert(random.sample(index_list, 1)[0], element)
    return np.asarray(parent_vector)


def mutate_reverse(parent_vector):
    parent_slices = np.sort(np.asarray(random.sample(range(len(parent_vector)), 2)))
    p_v_list = parent_vector.tolist()
    reversed_p_v_list = parent_vector.tolist()[parent_slices[0]:parent_slices[1]+1]
    reversed_p_v_list.reverse()
    child_vector = parent_vector.tolist()[0:parent_slices[0]]+\
        reversed_p_v_list+\
        (parent_vector.tolist()[parent_slices[1]+1:] if (parent_slices[1] < len(parent_vector)-1) else [])
    return child_vector