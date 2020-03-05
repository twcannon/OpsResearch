import numpy as np
import random



def weighted_random_by_dct(dct):
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'



def mate(parents,desired_pop,swap_pct,mean_pct,median_pct):

    def mate_swap(parent1,parent2):
        crossover_point = np.uint8(np.random.randint(1,(len(parents[0])-1)))
        parent1_idx = i%parents.shape[0]
        parent2_idx = (i+1)%parents.shape[0]
        child = np.empty(len(parents[0]))
        child[0:crossover_point] = parent1[0:crossover_point]
        child[crossover_point:] = parent2[crossover_point:]
        return child

    def mate_mean(parent1,parent2):
        parent_matrix = np.stack((parent1,parent2),axis=0)
        return np.mean(parent_matrix, axis=0)

    def mate_median(parent1,parent2):
        parent_matrix = np.stack((parent1,parent2),axis=0)
        return np.median(parent_matrix, axis=0)


    children = np.empty((desired_pop-len(parents),len(parents[0])))
    num_children = desired_pop-len(parents)
    for i in range(num_children):
        np.random.shuffle(parents)
        parent1 = parents[0]
        parent2 = parents[1]
        
        weight_dict = {
          "swap_pct": swap_pct,
          "mean_pct": mean_pct,
          "median_pct": median_pct
        }

        mate_function_dict = {
            'swap_pct':mate_swap,
            'mean_pct':mate_mean,
            'median_pct':mate_median
        }

        key = weighted_random_by_dct(weight_dict)
        child = mate_function_dict.get(key, lambda: 'Invalid')(parent1,parent2)

        children[i] = child

    return np.concatenate((children,parents),axis=0)

# def mate_swap(parent_matrix):
#     p_shape = parent_matrix.shape
#     parent_slices = np.sort(np.asarray(random.sample(range(p_shape[1]), p_shape[0])))
#     child_vector = []
#     for index in range(p_shape[0]):
#         parent_vector = parent_matrix[index].tolist()
#         if index == 0:
#             if parent_slices[index] == 0:
#                 child_vector = child_vector + [parent_vector[0]]
#             else:
#                 child_vector = child_vector + parent_vector[0:parent_slices[index]+1]
#         elif index == p_shape[0]-1:
#             child_vector = child_vector + parent_vector[(parent_slices[index-1]+1):p_shape[1]]
#         else:
#             if (parent_slices[index-1]+1) == parent_slices[index]:
#                 child_vector = child_vector + [parent_vector[parent_slices[index]]]
#             else:
#                 child_vector = child_vector + parent_vector[(parent_slices[index-1]+1):parent_slices[index]+1]
#     return child_vector


def mutate(parents,mutate_prob,flip_pct,insert_pct,reverse_pct):


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


    for i in range(len(parents)):
        if mutate_prob > random.uniform(0, 1):

            weight_dict = {
              "flip_pct": flip_pct,
              "insert_pct": insert_pct,
              "reverse_pct": reverse_pct
            }

            mutate_function_dict = {
                'flip_pct':mutate_flip,
                'insert_pct':mutate_insert,
                'reverse_pct':mutate_reverse
            }

            key = weighted_random_by_dct(weight_dict)
            parents[i] = mutate_function_dict.get(key, lambda: 'Invalid')(parents[i])

        else:
            next
    return parents