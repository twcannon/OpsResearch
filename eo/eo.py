import mate_mutate
import evaluate_pop
import numpy as np
import sys


sample_size = 40
dimensions = 5
A = np.random.randint(21, size=(dimensions,dimensions)).astype('float_')
p = []
b = np.random.randint(21, size=(dimensions,1)).astype('float_')
percent = 0.25

for i in range(sample_size):
	parent = np.random.randint(21, size=(1,dimensions)).astype('float_').flatten()
	p.append(parent)
p = np.array(p)
 
p = evaluate_pop.find_fittest(A,b,p,sample_size,percent)

p = mate_mutate.mate(p,sample_size,.333,.333,.333)

p = mate_mutate.mutate(p,0.85,.333,.333,.333)
