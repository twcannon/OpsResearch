from intersection import intersection
import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import fsolve

def f(x):
    return ((-1.0/3)*(x**3))+((1.75)*(x**2))

def f_prime(x):
    return (-(x-3.5)*x)

def slope(y_1,x_1,x_2):
    return (y_1-f(x_2))/(x_1-x_2)

statue = [7.5,4]


print('\nat time 3:')
print('slope = '+str(round(slope(statue[0],statue[1],3),2)))
print('f\' = '+str(round(f_prime(3),2)))


print('\nat time 3.3:')
print('slope = '+str(round(slope(statue[0],statue[1],3.3),2)))
print('f\' = '+str(round(f_prime(3.3),2)))

print('\nat time 3.4:')
print('slope = '+str(round(slope(statue[0],statue[1],3.4),2)))
print('f\' = '+str(round(f_prime(3.4),2)))


print('\n')



x = np.linspace(-0.5, 5)
print(x)



# x,y=intersection(x1,y1,x2,y2)
a,b=intersection(x,slope(statue[0],statue[1],x),x,f_prime(x))
a = np.delete(a,2)
b = np.delete(b,2)

plt.plot(x,f(x), label = 'f(x)')
plt.plot(x,f_prime(x), label = 'f\'(x)')
plt.plot(x,slope(7.5,4,x), label = 'slope between f(x) and statue')
plt.plot(a,b,"*k")
plt.plot(statue[1],statue[0],"or")
plt.plot(a,f(a),".k")
for i in range(len(a)):
    plt.text(a[i],f(a[i]),'('+str(round(a[i],1))+','+str(round(f(a[i]),1))+')',verticalalignment='bottom')
plt.ylim(top=20)
plt.legend()
plt.savefig("graph.png")

print(a)
print(b)