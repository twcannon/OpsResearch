import mate_mutate
import evaluate_pop
import samples
import numpy as np
import sys


sample_size = 100
dimensions = 3
value_range = 20
A = np.random.randint(value_range, size=(dimensions,dimensions)).astype('float_')
p = []
b = np.random.randint(value_range, size=(dimensions,1)).astype('float_')
surviving_percent = 0.25
new_sample_rate = .35
count_criteria = 50


min_norm = 99999999999

for i in range(sample_size):
    parent = samples.create_sample(dimensions,value_range)
    p.append(parent)
p = np.array(p)

count=0
old_norm=0
while count <= count_criteria: 
    p = evaluate_pop.find_fittest(A,b,p,sample_size,surviving_percent)
    
    p = samples.create_new_sample(p,dimensions,new_sample_rate,value_range)
    # mate(parents,desired_pop,swap_pct,mean_pct,median_pct)
    parents,children = mate_mutate.mate(p,sample_size,(1./3.),(1./3.),(1./3.))

    p = np.concatenate((children,parents),axis=0)
    
    # mutate(parents,mutate_prob,flip_pct,insert_pct,reverse_pct,scale_pct)
    p = mate_mutate.mutate(p,0.85,(1./4.),(1./4.),(1./4.),(1./4.))

    norms = evaluate_pop.find_norms(A,b,p,sample_size)
    min_norm = np.min(norms)

    if min_norm == old_norm:
        count+=1
    else:
        count=0

    old_norm = min_norm

    print('min norm',np.min(norms))
    # print('min vector',p[np.argmin(norms)].T)

solution = p[np.argmin(norms)]
print('solution vector',solution)

print('Ax',np.matmul(A,np.transpose([solution])))
print('b',b)