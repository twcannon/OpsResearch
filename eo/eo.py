import mate_mutate
import numpy as np

# Ax=b

parent_matrix = np.array([
    [1.0,2.0,3.5,4.0,6.6],
    [7.2,2.3,7.0,3.0,8.0],
    [1.2,3.0,0.6,5.0,0.1]
    ])


print('\nmating functions:')
print('original matrix:\n', parent_matrix)
print('mean',mate_mutate.mate_mean(parent_matrix))
print('median',mate_mutate.mate_median(parent_matrix))
print('swap',mate_mutate.mate_swap(parent_matrix))

print('\nmutating functions:')
print('original vector:\n', parent_matrix[0])
print('flip',mate_mutate.mutate_flip(parent_matrix[0]))
print('insert',mate_mutate.mutate_insert(parent_matrix[0]))
print('reverse',mate_mutate.mutate_reverse(parent_matrix[0]))