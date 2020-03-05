import numpy as np


def find_norm(A,b,p,s):
    norm = []
    for i in range(s):
        A_p  = np.matmul(A,p[i].T)
        diff = abs(b-A_p)
        norm.append(np.linalg.norm(diff))
    return np.array(norm)



def find_fittest(A,b,p,s,percent):
    norm = find_norm(A,b,p,s)
    
    k = int(s*percent)
    idx = np.argpartition(norm, k)
    return p[idx[:k]]