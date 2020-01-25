import numpy as np 
import matplotlib.pyplot as plt
import random
import statistics 
from collections import Counter


frame_size = 10
frame = np.zeros((frame_size,frame_size))


start = (2,2)
end = (8,8)
step_limit = 1000

num_ants = 5000
decay_rate = 0.90
term_node_rate = 0.65

iterations = 1

term_node_aot = []


kernel_array = []
exclude = [0,frame_size]
for i in range(0,frame_size):
    row_array = []
    for j in range(0,frame_size):
        term_kernel = np.random.randint(100, size=(3, 3))/100
        kernel = np.full((3, 3),(1.0/8))
        kernel[1][1] = 0
        if i == 0:
            kernel[0][0] = 0
            kernel[0][1] = 0
            kernel[0][2] = 0
        if i == frame_size-1:
            kernel[2][0] = 0
            kernel[2][1] = 0
            kernel[2][2] = 0
        if j == 0:
            kernel[0][0] = 0
            kernel[1][0] = 0
            kernel[2][0] = 0
        if j == frame_size-1:
            kernel[0][2] = 0
            kernel[1][2] = 0
            kernel[2][2] = 0
        kernel[term_kernel < term_node_rate] = 0
        row_array.append(kernel)
    kernel_array.append(row_array)




class Ant:

    def __init__(self, x, y, end, kernel_array,step_limit,term_node_aot):
        self.x = x
        self.y = y
        self.end = end
        self.kernel_array = kernel_array
        self.goal = False
        self.term = False
        self.limit = False
        self.x_path = [x]
        self.y_path = [y]
        self.step_limit = step_limit
        self.step_num = 0
        self.backprop = []
        self.term_node_aot = term_node_aot

    def step(self):
        kernel = self.kernel_array[self.x][self.y]
        # if np.array_equal(kernel, np.zeros((3, 3), float)):
        #     self.term = True
        #     print('ant found termination node at step number: '+str(self.step_num))
        #     return 'term'
        if self.step_num == self.step_limit:
            self.limit = True
            # print('ant reached the step_limit of: '+str(self.step_limit))
            return 'limit'
        elif (self.x,self.y) == end:
            self.goal = True
            print('ant found the food at step number: '+str(self.step_num)+'!!!!')
            return 'goal'
        else:
            probs = np.random.randint(100, size=(3, 3))/100
            calc = np.multiply(kernel,probs)
            direction = np.unravel_index(np.argmax(calc, axis=None), calc.shape)
            self.backprop.append([self.x,self.y,direction[0],direction[1]])
            self.term_node_entry = (self.x,self.y)
            new_x = self.x + (direction[0]-1)
            new_y = self.y + (direction[1]-1)
            if (new_x < 0 or new_x > frame_size-1) or (new_y < 0 or new_y > frame_size-1):
                # self.term_node_aot.append((new_x,new_y))
                self.kernel_array[self.x][self.y][direction[0]][direction[1]] = 0
                self.term = True
                print('ant found termination node at step number: '+str(self.step_num))
                return 'term'
            # print('---------')
            # print(direction[0],direction[1])
            # print(new_x,new_y)
            if (new_x,new_y) in term_node_aot:
                self.kernel_array[self.x][self.y][direction[0]][direction[1]] = 0
            else:
                new_kern = self.kernel_array[new_x][new_y]
                if np.array_equal(new_kern, np.zeros((3, 3), float)):
                    self.term_node_aot.append((new_x,new_y))
                    self.kernel_array[self.x][self.y][direction[0]][direction[1]] = 0
                    self.term = True
                    print('ant found termination node at step number: '+str(self.step_num))
                    return 'term'
                else:
                    self.x = self.x + (direction[0]-1)
                    self.y = self.y + (direction[1]-1)
                    self.x_path.append(self.x)
                    self.y_path.append(self.y)
                    self.step_num += 1


total_average_steps = [] 
hist_array = []
for iteration in range(iterations): 
    transient_nodes = []
    print('======================================')
    print('iteration number: ' + str(iteration))
    backprop_array = []
    tuple_zips = []
    for ant in range(num_ants):
        ant = Ant(start[0],start[1],end,kernel_array,step_limit,term_node_aot)
        while ant.goal is False and ant.term is False and ant.limit is False:
            result = ant.step()
        term_node_aot = ant.term_node_aot
        plt.plot(ant.x_path,ant.y_path)
        tuple_zips.extend(list(zip(ant.x_path,ant.y_path)))
        backprop_array.append([ant.backprop,result])

    term_node_unique = list(set(term_node_aot))
    for term_node in term_node_unique:
        plt.plot(term_node[0],term_node[1],'*k')

    values, counts = np.unique(tuple_zips, return_counts=True)
    if min(counts) == 1:
        index_arr = np.where(counts == np.amin(counts))
        for index in index_arr[0]:
            transient_nodes.append(tuple_zips[index])

    for trans_node in transient_nodes:
        plt.plot(trans_node[0],trans_node[1],'*b')
    plt.plot(start[0],start[1],'og')
    plt.plot(end[0],end[1],'or')
    plt.xlim((-1, frame_size))
    plt.ylim((-1, frame_size))
    # plt.show()
    plt.savefig(str(iteration)+'.png')
    plt.close()

    print('-------------------')
    print('back propogation:')
    back_step_array = []
    for back_data in backprop_array:
        back_step_num = len(back_data[0])
        if back_step_num != step_limit:
            back_step_array.append(back_step_num)

    hist_array.append(back_step_array)
    bins = np.arange(0, step_limit, 10)
    print(sum(1 for i in back_step_array if i <=100)/num_ants)
    print(sum(1 for i in back_step_array if i <=200)/num_ants)
plt.hist(hist_array,bins=bins,histtype='step',density=True)
plt.savefig('histogram.png')