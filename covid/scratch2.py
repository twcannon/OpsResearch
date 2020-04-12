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

# python scratch.py Deaths Country USA
# python scratch.py Deaths state NY
# python scratch.py Deaths county 45019
# python scratch.py Cases county 36061

### args
d_c = sys.argv[1]
geo = sys.argv[2]
val = sys.argv[3]

### get data
csv_counties_data = np.genfromtxt('covid-19-data/us-counties.csv', delimiter=',', names=True, skip_header=0, dtype=None)
csv_states_data = np.genfromtxt('covid-19-data/us-states.csv', delimiter=',', names=True, skip_header=0, dtype=None)

nyt_data_dict = {}
print(np.unique(csv_counties_data['fips']))
print(np.unique(csv_counties_data['date']))

for i in range(len(csv_counties_data)):
    fips_code = str(csv_counties_data[i][3])
    if (fips_code) in nyt_data_dict:
        nyt_data_dict[(fips_code)]['date'].append(csv_counties_data[i][0])
        nyt_data_dict[(fips_code)]['cases'].append(csv_counties_data[i][4])
        nyt_data_dict[(fips_code)]['deaths'].append(csv_counties_data[i][5])
    else:
        nyt_data_dict[(fips_code)] = {}
        nyt_data_dict[(fips_code)]['date'] = []
        nyt_data_dict[(fips_code)]['cases'] = []
        nyt_data_dict[(fips_code)]['deaths'] = []
        nyt_data_dict[(fips_code)]['county'] = csv_counties_data[i][1]
        nyt_data_dict[(fips_code)]['state'] = csv_counties_data[i][2]

print(nyt_data_dict['6075'])
sys.exit()


json_url = 'https://usafactsstatic.blob.core.windows.net/public/2020/coronavirus-timeline/allData.json'
data = requests.get(json_url).json()
print(data)

def safeget(dct,*keys):
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError,TypeError):
            return None
    return dct


data_dict = {}
last_name = ''
for entry in data:
    if geo == 'state':
        if last_name != entry['stateAbbr']:
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
        last_name = entry['stateAbbr']
    elif geo == 'county':
        data_dict[entry['countyFIPS']] = {
            'name':entry['county'],
            'pop':entry['popul'],
            'state':entry['stateAbbr'],
            'deaths':np.array(entry['deaths']),
            'cases':np.array(entry['confirmed'])
        }
    elif geo == 'country':
        if last_name != 'USA':
            data_dict['USA'] = {
                'name':'USA',
                'pop':entry['popul'],
                'deaths':np.array(entry['deaths']),
                'cases':np.array(entry['confirmed'])
            }
        else:
            data_dict['USA'] = {
                'name':'USA',
                'pop':data_dict['USA']['pop']+entry['popul'],
                'deaths':data_dict['USA']['deaths']+np.array(entry['deaths']),
                'cases':data_dict['USA']['cases']+np.array(entry['confirmed'])
            }
        last_name = 'USA'


def clean_data(data):
    tot = len(data)
    new_data = []
    init = True
    for i in (range(tot)):
        if i == tot:
            new_data.append(data[i])
        else:
            if init is True:
                new_data.append(data[i])
                init = False
            else:
                if data[i] < new_data[-1]:
                    new_data.append(new_data[-1])
                else:
                    new_data.append(data[i])
    return np.array(new_data)


rate_tol = 1e-15

pop = float(data_dict[val]['pop'])

# deaths = np.log(data_dict[val]['deaths'])
# cases = np.log(data_dict[val]['cases'])
# print(data_dict[val]['deaths'])
deaths = clean_data(data_dict[val]['deaths'])
cases  = clean_data(data_dict[val]['cases'])
# print(deaths)


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
case_gauss_error_fit = curve_fit(gauss_error_model,case_time,case_data,p0=[0.,0.,0.],maxfev=10000)

# print('gamma:',gamma_cdf_fit[0])
# print('death logistic',death_logistic_fit[0])
# print('death gauss error',death_gauss_error_fit[0])

print('\n')

if d_c.lower() == 'deaths':
    total_deaths = death_gauss_error_fit[0][2]
    death_error = np.sqrt(np.diag(death_gauss_error_fit[1]))
    print('\ndeaths so far:',death_data[-1])
    print('estimated total deaths:',int(total_deaths),'with 1 stdev of',death_error[2])
    print('death/pop ratio',total_deaths/pop)
    print('\n')

    death_model = gauss_error_model(more_time,*death_gauss_error_fit[0])
    death_upper = gauss_error_model(more_time,
        death_gauss_error_fit[0][0]+death_error[0],
        death_gauss_error_fit[0][1]+death_error[1],
        death_gauss_error_fit[0][2]+death_error[2])
    death_lower = gauss_error_model(more_time,
        death_gauss_error_fit[0][0]-death_error[0],
        death_gauss_error_fit[0][1]-death_error[1],
        death_gauss_error_fit[0][2]-death_error[2])

    plt.plot(death_plot_time,death_plot_data, '.k',label = 'data')
    plt.plot(more_time+time_diff,gauss_error_model(more_time,*death_gauss_error_fit[0]),label = 'model')
    plt.fill_between(more_time+time_diff, death_lower, death_upper, alpha=0.2)

elif d_c.lower() == 'cases':
    total_cases = case_gauss_error_fit[0][2]
    case_error = np.sqrt(np.diag(case_gauss_error_fit[1]))
    print('\ncases so far:',case_data[-1])
    print('estimated total cases:',total_cases,'with 1 stdev of',case_error[2])
    print('case/pop ratio',total_cases/pop)
    print('\n')

    case_model = gauss_error_model(more_time,*case_gauss_error_fit[0])
    case_upper = gauss_error_model(more_time,
        case_gauss_error_fit[0][0]+case_error[0],
        case_gauss_error_fit[0][1]+case_error[1],
        case_gauss_error_fit[0][2]+case_error[2])
    case_lower = gauss_error_model(more_time,
        case_gauss_error_fit[0][0]-case_error[0],
        case_gauss_error_fit[0][1]-case_error[1],
        case_gauss_error_fit[0][2]-case_error[2])

    plt.plot(case_time,case_data, '.k',label = 'data')
    plt.plot(more_time,gauss_error_model(more_time,*case_gauss_error_fit[0]),label = 'model')
    plt.fill_between(more_time, case_lower, case_upper, alpha=0.2)
# plt.plot(case_time,case_data)
# plt.plot(death_time+time_diff,logistic_model(death_time,*death_logistic_fit[0]))
# plt.plot(more_time,gamma.cdf(more_time,*gamma_fit))
# plt.plot(time,gamma_cdf_model(time,*gamma_cdf_fit[0]))
plt.title(d_c+' '+data_dict[val]['name'])
plt.legend()
plt.show()


