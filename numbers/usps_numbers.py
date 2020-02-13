import h5py
import numpy as np
import matplotlib.pyplot as plt
with h5py.File('usps.h5', 'r') as hf:
    train = hf.get('train')
    train_data = train.get('data')[:]
    train_labels = train.get('target')[:]
    test = hf.get('test')
    test_data = test.get('data')[:]
    test_labels = test.get('target')[:]

sample = 2

matrix = np.array(train_data[sample]).reshape(16,16)
print(matrix)
print('sample label:',train_labels[sample])
plt.imshow(matrix, cmap='Blues')
plt.show()