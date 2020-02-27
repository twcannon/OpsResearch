import numpy as np
import math
import matplotlib.pyplot as plt

b_a_data = np.genfromtxt('before_after.csv',delimiter=",",skip_header=1,dtype='|U50')
b_a_data_summed = np.genfromtxt('before_after_summed.csv',delimiter=",",skip_header=1,dtype='|U50')

# print(b_a_data)
print(b_a_data_summed)




# col_rows, col_cols = np.where(b_a_data == 'Colorado')
# colorado_data = b_a_data[col_rows]
# print(colorado_data)
# colorado_counts = [int(row[2]) for row in colorado_data]
# print(colorado_counts)
# plt.hist(colorado_counts, bins='auto',density = True)
# plt.title("Histogram of Colorado Highway Accidents (Poisson Process)")
# plt.show()



# data_array = []
# labels = ['Alaska','California','Colorado','District of Columbia','Massachusetts','Nevada','Oregon','Vermont','Washington']
# for label in labels:
# 	rows, cols = np.where(b_a_data == label)
# 	state_data = b_a_data[rows]
# 	state_counts = [int(row[2]) for row in state_data]
# 	data_array.append(state_counts)
# # plt.hist(data_array, bins='auto', density=True, label=labels)
# plt.hist([int(row[2]) for row in b_a_data], bins='auto', density=True, label=labels)
# plt.title("Histogram of Highway Accidents (Poisson Process)")
# plt.show()



# State,After,Before
 # ['California','3259','3569'],

sum_data = [['AK','65','63'],
 ['CO','452','432'],
 ['DC','23','19'],
 ['MA','335','348'],
 ['NV','290','313'],
 ['OR','419','386'],
 ['VT','59','61'],
 ['WA','406','403']]

fig, ax = plt.subplots()

i=1
ticks=[]
for row in sum_data:
	ticks.append(int((i*10)+5))
	ax.broken_barh([(int(row[1])-math.sqrt(int(row[1])), (2*math.sqrt(int(row[1])))), (int(row[2])-math.sqrt(int(row[2])), (2*math.sqrt(int(row[2]))))], ((i*10), 9), facecolors=('tab:blue','tab:red'),alpha=0.5)
	i+=1

# ax.set_ylim(5, 35)
# ax.set_xlim(0, 200)
ax.set_title('Overlapped Poisson Noise of Highway Accidents')
ax.set_xlabel('Count of Highway Accidents')
ax.set_yticks(ticks)
ax.set_yticklabels([row[0] for row in sum_data])
ax.grid(True)


plt.show()