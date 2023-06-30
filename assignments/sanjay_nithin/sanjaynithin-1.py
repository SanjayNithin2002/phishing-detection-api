#!/usr/bin/env python
# coding: utf-8

# ## SANJAY NITHIN 20BIT0150

# ## ASSIGNMENT 1 19/05/2023

# #### 1. Assign your Name to variable name and Age to variable age. Make a Python program that prints your name and age.
# 

# In[2]:


name='SANJAYNITHIN'
age=19
print('The Name is',name,'and my age is',age)


# #### 2. X="Datascience is used to extract meaningful insights."
# Split the string

# In[7]:


X="Datascience is used to extract meaningful insights."
spl=X.split()
print(spl)


# #### 3. Make a function that gives multiplication of two numbers

# In[8]:


def mul(a,b):
    c=a*b
    return c

mul(5,2)


# #### 4. Create a Dictionary of 5 States with their capitals. also print the keys and values.

# In[10]:


cap={'Tamilnadu':'Chennai','Karnataka':'Banglore','Bihar':'Patna','Assam':'Dispur','Arunachal Pradesh':'Itanagar'}

print(cap)

print(cap.keys())
print(cap.values())


# #### 5. Create a list of 1000 numbers using range function.

# In[11]:


num = list(range(1000))
print(num)


# #### 6. Create an identity matrix of dimension 4 by 4

# In[12]:


import numpy as np

identity = np.eye(4)
print(identity)


# #### 7. Create a 3x3 matrix with values ranging from 1 to 9

# In[13]:


import numpy as np

mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(mat)


# #### 8. Create 2 similar dimensional array and perform sum on them.

# In[15]:


import numpy as np

mat1=np.array([[1,2],[3,4]])
mat2=np.array([[1,2],[3,4]])

print(mat1+mat2)


# #### 9. Generate the series of dates from 1st Feb, 2023 to 1st March, 2023 (both inclusive)

# In[1]:


import pandas as pd 
startdate=pd.to_datetime('2023-02-01')
enddate=pd.to_datetime('2023-03-01')
dates=pd.date_range(startdate,enddate)
dates


# #### 10. Given a dictionary, convert it into corresponding dataframe and display it
# dictionary = {'Brand': ['Maruti', 'Renault', 'Hyndai'], 'Sales' : [250, 200, 240]}

# In[16]:


import pandas as pd

dictionary = {'Brand': ['Maruti', 'Renault', 'Hyundai'], 'Sales': [250, 200, 240]}

df = pd.DataFrame(dictionary)
print(df)

