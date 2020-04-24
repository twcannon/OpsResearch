#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from statsmodels.discrete.discrete_model import Poisson
model =Poisson(endog=doi.Infections.astype(float), exog=add_constant(doi.CYPOPDENS.astype(float))) #Endog is the dependent variable here
results = model.fit()
print(results.summary())  


# In[ ]:


DENSCOEF = 1 - np.exp(.0007)    #.0007 is the coefficient of our endogenous variable of interest
print('CYPOPDENS coefficent exponetiated: {} '.format(np.exp(DENSCOEF)))  #outputs workable percentage

