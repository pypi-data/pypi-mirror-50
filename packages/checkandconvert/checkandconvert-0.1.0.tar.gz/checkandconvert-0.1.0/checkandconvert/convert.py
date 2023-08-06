#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

def convert_series_int(series):
    #a function to convert a series to an integer
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        #check that there are no strings in the series that cannot be converted
        all_strings = [s for s in series.values if type(s) is str]
        all_convertable = [x.isdigit() for x in all_strings]
        if False in all_convertable:
            raise TypeError("You have at least one str value in your Series not convertable to an int.")            
        else:
            values = series.values
            new_values = [int(x) for x in values]
            new_series = pd.Series(new_values, index = series.index)
            return new_series
                
                
def convert_series_float(series):
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        #check that there are no strings in the series that cannot be converted
        all_strings = [s for s in series.values if type(s) is str]
        all_convertable = [x.isdigit() for x in all_strings]
        if False in all_convertable:
            raise TypeError("You have at least one str value in your Series not convertable to a float.")            
        else:
            values = series.values
            new_values = [float(x) for x in values]
            new_series = pd.Series(new_values, index = series.index)
            return new_series
        
        
def convert_series_str(series):
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        values = series.values
        new_values = [str(x) for x in values]
        new_series = pd.Series(new_values, index = series.index)
        return new_series
    
    

def convert_series_bool(series):
    #any number or float not 0 will be converted to True
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        values = series.values
        new_values = [bool(x) for x in values]
        new_series = pd.Series(new_values, index = series.index)
        return new_series
    
    



# In[ ]:




