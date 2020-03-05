import numpy as np


def find_norms(A,b,p,s):
    norm = []
    for i in range(s):
        # p_t = np.transpose([p[i]])
        # print(p_t)
        # print(p[i])
        # print(type(p[i]))
        # sys.exit()
        # A_p  = np.matmul(A,p[i].T)
        A_p  = np.matmul(A,np.transpose([p[i]]))
        # print(A_p)
        # print(b)
        # print(b-A_p)
        diff = abs(b-A_p)
        norm.append(np.linalg.norm(diff))
        # print(norm)
        # sys.exit()
    return np.array(norm)



def find_fittest(A,b,p,s,percent):
    norm = find_norms(A,b,p,s)
    
    k = int(s*percent)
    idx = np.argpartition(norm, k)
    return p[idx[:k]]