import mate_mutate
import numpy as np
import sys
# # Ax=b

# parent_matrix = np.array([
#     [1.0,2.0,3.5,4.0,6.6],
#     [1.0,2.0,3.5,4.0,6.6],
#     [7.2,2.3,7.0,3.0,8.0],
#     [7.2,2.3,7.0,3.0,8.0],
#     [7.2,2.3,7.0,3.0,8.0],
#     [7.2,2.3,7.0,3.0,8.0],
#     [1.2,3.0,0.6,5.0,0.1]
#     ])


# # print(mate_mutate.mate_swap(parent_matrix))
# print(mate_mutate.mate_crossover(parent_matrix,20))

# sys.exit()

# # print('\nmating functions:')
# # print('original matrix:\n', parent_matrix)
# # print('mean',mate_mutate.mate_mean(parent_matrix))
# # print('median',mate_mutate.mate_median(parent_matrix))
# # print('swap',mate_mutate.mate_swap(parent_matrix))

# # print('\nmutating functions:')
# # print('original vector:\n', parent_matrix[0])
# # print('flip',mate_mutate.mutate_flip(parent_matrix[0]))
# # print('insert',mate_mutate.mutate_insert(parent_matrix[0]))
# # print('reverse',mate_mutate.mutate_reverse(parent_matrix[0]))

# s = 20
# n = 4
# A = np.random.randint(21, size=(n,n)).astype('float_')
# p = []
# p_T = []
# b = np.random.randint(21, size=(n,1)).astype('float_')
# percent = 0.25

# #create initial population
# print(b)
# print(A)

# for i in range(s):
# 	parent = np.random.randint(21, size=(n,1)).astype('float_')
# 	p.append(parent)
# 	p_T.append(parent.T)

# p = np.array(p)
# p_T = np.array(p_T)
 	
#  #evaluate fitness of initial population
# norm = []
# for i in range(s):
# 	A_p  = np.matmul(A,p[i])
# 	diff = abs(b-A_p)
# 	norm.append(np.linalg.norm(diff))
# print(norm)

# norm = np.array(norm)

# #find top percent of initial pop 
# k = int(s*percent)
# idx = np.argpartition(norm, k)
# print(norm[idx[:k]])
# print(p[idx[:k]])

# #new parents
# p = p[idx[:k]]
# p_T = p_T[idx[:k]]
# print(p)
# print(p_T)

 	

# # to mate / mutate

# mate_mutate.mate_swap(p_T)



import mate_mutate
import numpy as np


s = 40
n = 5
A = np.random.randint(21, size=(n,n)).astype('float_')
p = []
b = np.random.randint(21, size=(n,1)).astype('float_')
percent = 0.25

#create initial population
# print(b)
# print(A)

# p = np.empty((s, n))

for i in range(s):
	parent = np.random.randint(21, size=(1,n)).astype('float_').flatten()
	p.append(parent)

p = np.array(p)
# print(p)
# print('-------------------')
 #evaluate fitness of initial population
norm = []
for i in range(s):
	A_p  = np.matmul(A,p[i].T)
	diff = abs(b-A_p)
	norm.append(np.linalg.norm(diff))
# print(norm)

norm = np.array(norm)

#find top percent of initial pop 
k = int(s*percent)
idx = np.argpartition(norm, k)
# print(norm[idx[:k]])
# print(p[idx[:k]])

#new parents
p = p[idx[:k]]
# print(p)


 	

# to mate / mutate

p = mate_mutate.mate(p,s,.333,.333,.333)
print(p)

p = mate_mutate.mutate(p,0.85,.333,.333,.333)
print(p)



