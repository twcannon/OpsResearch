import numpy as np


def find_norms(A,b,p,s):
    norm = []
    for i in range(s):
        A_p  = np.matmul(A,np.transpose([p[i]]))
        diff = abs(b-A_p)
        norm.append(np.linalg.norm(diff))
    return np.array(norm)



def find_fittest(A,b,p,s,percent):
    norm = find_norms(A,b,p,s)
    
    k = int(s*percent)
    idx = np.argpartition(norm, k)
    return p[idx[:k]]