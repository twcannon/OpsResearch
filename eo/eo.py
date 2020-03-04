import mate_mutate
import numpy as np

# Ax=b

# parent_matrix = np.array([
#     [1.0,2.0,3.5,4.0,6.6],
#     [7.2,2.3,7.0,3.0,8.0],
#     [1.2,3.0,0.6,5.0,0.1]
#     ])


# print('\nmating functions:')
# print('original matrix:\n', parent_matrix)
# print('mean',mate_mutate.mate_mean(parent_matrix))
# print('median',mate_mutate.mate_median(parent_matrix))
# print('swap',mate_mutate.mate_swap(parent_matrix))

# print('\nmutating functions:')
# print('original vector:\n', parent_matrix[0])
# print('flip',mate_mutate.mutate_flip(parent_matrix[0]))
# print('insert',mate_mutate.mutate_insert(parent_matrix[0]))
# print('reverse',mate_mutate.mutate_reverse(parent_matrix[0]))

s = 10
n = 4
A = np.random.randint(21, size=(n,n)).astype('float_')
p = []
b = np.random.randint(21, size=(n,1)).astype('float_')
percent = 0.25

#create initial population
print(b)
print(A)

for i in range(s):
	p.append(np.random.randint(21, size=(n,1)).astype('float_'))
 	
 #evaluate fitness of initial population
norm = []
for i in range(s):
	A_p  = np.matmul(A,p[i])
	diff = abs(b-A_p)
	norm.append(np.linalg.norm(diff))
print(norm)

norm = np.array(norm)
p = np.array(p)

#find top percent of initial pop 
k = int(s*percent)
idx = np.argpartition(norm, k)
print(norm[idx[:k]])
print(p[idx[:k]])

#new parents
p = p[idx[:k]]
print(p)

 	

# to mate / mutate

# mate_mutate.mutate_flip(p[i])