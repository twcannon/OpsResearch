import sys
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf
import json
import csv


# Examples calls
# python gef_models.py deaths
# python gef_models.py cases

rate_tol = 1e-15

### args
d_c = sys.argv[1]

### get data
json_url = 'https://raw.githubusercontent.com/twcannon/OpsResearch/master/covid/county_data.json'
data_dict = requests.get(json_url).json()

fips_codes = data_dict.keys()


def gauss_error_model(x,a,B,p):
    return p/2.*(1.+erf(a*x-a*B)) 


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


with open('model_results_'+d_c+'.csv','w') as f1:
    writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
    writer.writerow(['County','Fips','start_date','a','B','p','a_e','B_e','p_e','model','upper','lower','counts'])


    for val in fips_codes:
        pop = float(data_dict[val]['pop'])

        dep = clean_data(np.array(data_dict[val][d_c.lower()]).astype(int))
        dep_rate = dep/pop
        dep_data = dep[dep_rate >= rate_tol]
        more_time = np.array([float(i) for i in list(range(1,(max([len(dep_data)])*2)+1))])
        # more_time = np.array([float(i) for i in list(range(1,(max([1])*365)+1))])
        if len(dep_data) <= 3:
            writer.writerow([data_dict[val]['name'],val,'','','','','','',''])
        else:
            dep_time = np.array([float(i) for i in list(range(1,len(dep_data)+1))])
            gauss_error_fit = curve_fit(gauss_error_model,dep_time,dep_data,p0=[0.,0.,0.],maxfev=50000)
            results = gauss_error_fit[0]
            results_error = np.sqrt(np.diag(gauss_error_fit[1]))

            case_model = gauss_error_model(more_time,*results)
            case_upper = gauss_error_model(more_time,
                results[0]+results_error[0],
                results[1]-results_error[1],
                results[2]+results_error[2])
            case_lower = gauss_error_model(more_time,
                results[0]-results_error[0],
                results[1]+results_error[1],
                results[2]-results_error[2])

            new_row = [data_dict[val]['name'],val,data_dict[val]['date'][0],results[0],results[1],results[2],results_error[0],results_error[1],results_error[2],str(case_model),str(case_upper),str(case_lower),dep]
            writer.writerow(new_row)

print('Done')