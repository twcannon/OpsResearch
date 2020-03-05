import mate_mutate
import evaluate_pop
import samples
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

mpl.rcParams['figure.max_open_warning'] = 0


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


sample_size = 100
dimensions = 3
value_range = 20
A = np.random.randint(value_range, size=(dimensions,dimensions)).astype('float_')
p = []
b = np.random.randint(value_range, size=(dimensions,1)).astype('float_')
surviving_percent = 0.2
new_sample_rate = .5
count_criteria = 25


min_norm = 99999999999

for i in range(sample_size):
    parent = samples.create_sample(dimensions,value_range)
    p.append(parent)
p = np.array(p)

count=0
old_norm=0
min_norm_list = []
iteration = 0
while count <= count_criteria: 
    iteration+=1
    p,min_p_norms = evaluate_pop.find_fittest(A,b,p,sample_size,surviving_percent)
    
    p = samples.create_new_sample(p,dimensions,new_sample_rate,value_range,min_p_norms)
    # mate(parents,desired_pop,swap_pct,mean_pct,median_pct)
    parents,children = mate_mutate.mate(p,sample_size,(1./3.),(1./3.),(1./3.))

    # mutate(parents,mutate_prob,flip_pct,insert_pct,reverse_pct,scale_pct)
    parents = mate_mutate.mutate(parents,0.85,(1./4.),(1./4.),(1./4.),(1./4.))

    p = np.concatenate((children,parents),axis=0)
    

    norms = evaluate_pop.find_norms(A,b,p,sample_size)
    min_norm = np.min(norms)

    if min_norm == old_norm:
        count+=1
    else:
        count=0

    old_norm = min_norm
    min_norm_list.append(min_norm)

    cur_best_soln = np.matmul(A,np.transpose([p[np.argmin(norms)]]))
    all_cur_solns = np.matmul(A,p.T)
    # print('cur_best_soln',cur_best_soln)
    # print('all_cur_solns',all_cur_solns.T)

    print('min norm',min_norm)
    # print('min vector',p[np.argmin(norms)].T)

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(p)):
        cur_A_p = np.matmul(A,np.transpose([p[i]]))
        ax.plot(cur_A_p[0], cur_A_p[1], cur_A_p[2], 'o', markersize=10, color='g', alpha=0.2)
    a = Arrow3D([0, b[0][0]], 
                [0, b[1][0]], 
                [0, b[2][0]], mutation_scale=20, 
                lw=3, arrowstyle="-|>", color="r")
    a_min = Arrow3D([0, cur_best_soln[0][0]], 
                    [0, cur_best_soln[1][0]], 
                    [0, cur_best_soln[2][0]], mutation_scale=20, 
                    lw=3, arrowstyle="-|>", color="b")
    ax.add_artist(a)
    ax.add_artist(a_min)
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_zlim(-25, 25)
    plt.draw()
    # plt.show()
    plt.savefig(str(iteration)+'_vectors.png')
    # sys.exit()


print('number of iterations', iteration)

solution = p[np.argmin(norms)]
print('solution vector',solution)

print('Ax',np.matmul(A,np.transpose([solution])))
print('b',b)

fig = plt.figure()
ax = fig.add_subplot(111)
print(min_norm_list)
ax.plot(min_norm_list)
# plt.show()
plt.savefig('convergence.png')