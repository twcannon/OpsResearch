import sys
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

# python scratch.py state NY
# python scratch.py county 45019
# python scratch.py county 36061

### args
d_c = sys.argv[1]
geo = sys.argv[2]
val = sys.argv[3]

### get data
url = 'https://usafactsstatic.blob.core.windows.net/public/2020/coronavirus-timeline/allData.json'
data = requests.get(url).json()

def safeget(dct,*keys):
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError,TypeError):
            return None
    return dct


data_dict = {}
last_state = ''
for entry in data:
    if geo == 'state':
        if last_state != entry['stateAbbr']:
            data_dict[entry['stateAbbr']] = {
                'name':entry['stateAbbr'],
                'pop':entry['popul'],
                'deaths':np.array(entry['deaths']),
                'cases':np.array(entry['confirmed'])
            }
        else:
            data_dict[entry['stateAbbr']] = {
                'name':entry['stateAbbr'],
                'pop':data_dict[entry['stateAbbr']]['pop']+entry['popul'],
                'deaths':data_dict[entry['stateAbbr']]['deaths']+np.array(entry['deaths']),
                'cases':data_dict[entry['stateAbbr']]['cases']+np.array(entry['confirmed'])
            }
        last_state = entry['stateAbbr']
    else:
        data_dict[entry['countyFIPS']] = {
            'name':entry['county'],
            'pop':entry['popul'],
            'state':entry['stateAbbr'],
            'deaths':np.array(entry['deaths']),
            'cases':np.array(entry['confirmed'])
        }

rate_tol = 1e-15



# county = '45019' ## CHS
county = '36061' ## NYC

pop = float(data_dict[val]['pop'])

# deaths = np.log(data_dict[county]['deaths'])
# cases = np.log(data_dict[county]['cases'])
deaths = data_dict[val]['deaths']
cases  = data_dict[val]['cases']

death_rate = deaths/pop
case_rate  = cases/pop

death_data = deaths[death_rate >= rate_tol]
death_plot_data = deaths[case_rate >= rate_tol]
case_data  = cases[case_rate   >= rate_tol]

case_time  = np.array([float(i) for i in list(range(1,len(case_data)+1))])
death_plot_time = case_time
death_time = np.array([float(i) for i in list(range(1,len(death_data)+1))])

time_diff = len(case_time)-len(death_time)

more_time = np.array([float(i) for i in list(range(1,(max([len(case_data)])*2)+1))])




def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))

def gamma_cdf_model(x,c,a,B):
    return c*gamma.cdf(x=time,a=a,scale=B)

def gauss_error_model(x,a,B,p):
	return p/2.*(1.+erf(a*x-a*B)) 


# death_logistic_fit = curve_fit(logistic_model,death_time,death_data,p0=[2.,100.,20000.],maxfev=10000)
# gamma_cdf_fit = curve_fit(gamma_cdf_model,time,data,p0=[100.,60.,1.])
death_gauss_error_fit = curve_fit(gauss_error_model,death_time,death_data,p0=[0.,0.,0.],maxfev=10000)

# print('gamma:',gamma_cdf_fit[0])
# print('death logistic',death_logistic_fit[0])
print('death gauss error',death_gauss_error_fit[0])

print('\n\ndeaths so far:',death_data[-1])
print('estimated total deaths:',death_gauss_error_fit[0][2])
print('\n')

plt.plot(death_plot_time,death_plot_data, 'o',label = 'data')
# plt.plot(case_time,case_data)
# plt.plot(death_time+time_diff,logistic_model(death_time,*death_logistic_fit[0]))
# plt.plot(more_time,gamma.cdf(more_time,*gamma_fit))
# plt.plot(time,gamma_cdf_model(time,*gamma_cdf_fit[0]))
plt.plot(more_time+time_diff,gauss_error_model(more_time,*death_gauss_error_fit[0]),label = 'model')
plt.title(d_c+' '+data_dict[val]['name'])
plt.legend()
plt.show()


