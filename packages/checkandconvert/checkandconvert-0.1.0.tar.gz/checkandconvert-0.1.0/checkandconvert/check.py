#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd   
  
def is_type_string(series, all=True):
    #function that checks whether all values in a series are of type str
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        if all is not True and all is not False:
            raise ValueError("all needs to be set to True or False.")
        else:
            if all is True:
            #only return True if ALL values are of type String
                bad_list = ['bad' for value in series.values if isinstance(value, str) is not True]
                #see if the list is empty
                if bad_list:
                    return False
                else:
                    return True
            else:
                #will return True if at least one value in the Series is a string
                bad_list = ['bad' for value in series.values if isinstance(value, str) is not True]
                #aren't any at all - length of the list will be the same as the length of the series
                if len(bad_list) == len(series):
                    return False
                else:
                    #there is at least one string value in the series
                    return True
                
                
def is_type_float(series):
    #function that checks whether all values in a series are of type float
    #when passing a series of numeric values, they are either all floats or not
    # therefore don't include all=True 
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        #return True if ALL values are of type float
        bad_list = ['bad' for value in series.values if isinstance(value, float) is not True]
        #see if the list is empty
        if bad_list:
            return False
        else:
            return True
        

def is_type_int(series):
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        #return True if all values are of type int
        bad_list = ['bad' for value in series.values.tolist() if isinstance(value, int) is not True]
        if bad_list:
            return False
        else:
            return True
        

        

def is_type_bool(series, all=True):
    if isinstance(series, pd.Series) is False:
        raise TypeError("Your data needs to be a Series.")
    else:
        if all is not True and all is not False:
            raise ValueError("all needs to be set to True or False.")
        else:
            if all is True:
                bad_list = ['bad' for value in series.values.tolist() if isinstance(value, bool) is not True]
                if bad_list:
                    return False
                else:
                    return True
            else:
                bad_list = ['bad' for value in series.values.tolist() if isinstance(value, bool) is not True]
                if len(bad_list) == len(series):
                    return False
                else:
                    return True
                
                


# In[ ]:




