import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import gamma
from scipy.special import erf
# import pandas as pd
# from scipy.optimize import fsolve
# from datetime import datetime,timedelta
# from scipy.special import gammainc#, gamma


url = 'https://usafactsstatic.blob.core.windows.net/public/2020/coronavirus-timeline/allData.json'
data = requests.get(url).json()


data_dict = {}

for entry in data:
	data_dict[entry['countyFIPS']] = {
	'name':entry['county'],
	'pop':entry['popul'],
	'state':entry['stateAbbr'],
	'deaths':np.array(entry['deaths']),
	'cases':np.array(entry['confirmed'])
	}


# county = '45019' ## CHS
county = '36061' ## NYC


# deaths = np.log(data_dict[county]['deaths'])
# cases = np.log(data_dict[county]['cases'])
deaths = data_dict[county]['deaths']
cases = data_dict[county]['cases']



def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))

def gamma_cdf_model(x,c,a,B):
    return c*gamma.cdf(x=time,a=a,scale=B)

def gauss_error_model(x,a,B,p):
	return p/2.*(1.+erf(a*x-a*B)) 


time = np.array([float(i) for i in list(range(1,len(data)+1))])
more_time = np.array([float(i) for i in list(range(1,(len(data)*2)+1))])

logistic_fit = curve_fit(logistic_model,time,data,p0=[2.,100.,20000.],maxfev=10000)
# gamma_cdf_fit = curve_fit(gamma_cdf_model,time,data,p0=[100.,60.,1.])
gauss_error_fit = curve_fit(gauss_error_model,time,data,p0=[0.,0.,0.],maxfev=10000)

# print('gamma:',gamma_cdf_fit[0])
# print('logistic',logistic_fit[0])
print('gauss error',gauss_error_fit[0])

plt.plot(time,data)
plt.plot(more_time,list(logistic_model(more_time,*logistic_fit[0])))
# plt.plot(more_time,gamma.cdf(more_time,*gamma_fit))
# plt.plot(time,gamma_cdf_model(time,*gamma_cdf_fit[0]))
plt.plot(more_time,gauss_error_model(more_time,*gauss_error_fit[0]))
plt.title('CHS County')
plt.show()


