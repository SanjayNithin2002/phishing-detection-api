#!/usr/bin/env python
# coding: utf-8

# # SATHYANARAYANAN K
# # 20BIT0422
# # ADS ASSIGNMENT 3

# ## Importing libraries

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# ## 2. Load the dataset into the tool.

# In[2]:


df=pd.read_csv('Housing.csv')


# In[3]:


df.head()


# In[4]:


df.shape


# ## 3. Perform Below Visualizations.
# ● Univariate Analysis ● Bi - Variate Analysis ● Multi - Variate Analysis

# In[5]:


# Univariate analysis

# Histogram

sns.histplot(df['price'])


# In[6]:


import seaborn as sns 
sns.countplot(data=df,x='area')


# In[7]:


#piechart on gender 

df['furnishingstatus'].value_counts().plot(kind="pie",autopct="%.2f")


# In[8]:


sns.boxplot(df['price'])


# In[9]:


# Bivariate analysis

# Scatter plot
sns.scatterplot(data=df,x="price",y="furnishingstatus")


# In[61]:


# Multivariate Analysis

correlation_matrix = df[['price', 'furnishingstatus', 'area']].corr()

# Create a heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix Heatmap")
plt.show()


# ## 4. Perform descriptive statistics on the dataset.

# In[62]:


# Mean
df.mean()


# In[63]:


df.median()


# In[64]:


df.mode()


# In[65]:


df.max()


# In[66]:


df.min()


# In[67]:


# range

ran=df.max()-df.min()
ran


# In[68]:


df.var()


# In[69]:


df.std()


# In[70]:


quantile=df['price'].quantile(q=[0.75,0.25,0.50])
quantile


# ## 5. Check for Missing values and deal with them.

# In[22]:


df.isna().sum()


# ## 6. Find the outliers and replace them outliers

# In[71]:


columns=['price','area','bedrooms','bathrooms','stories','mainroad','guestroom','basement','hotwaterheating','airconditioning','parking','furnishingstatus']
for column in columns:
  q1=df[column].quantile(0.25)
  q3=df[column].quantile(0.75)
  IQR =q3-q1
  lowerbound=q1-(1.5*IQR)
  upperbound=q3+(1.5*IQR)
  # print(column,q1,q3,IQR,lowerbound,upperbound)


  #outliers
  outliers = df[(df[column] < lowerbound) | (df[column] > upperbound)]
  print(column,outliers)
  #replacing with median
  df.loc[(df[column] < lowerbound) | (df[column] > upperbound), column] = df[column].median()


# ## 7. Check for Categorical columns and perform encoding.

# In[24]:


df.info()


# In[25]:


from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()


# In[26]:


df.mainroad=le.fit_transform(df.mainroad)
df.guestroom=le.fit_transform(df.guestroom)
df.basement=le.fit_transform(df.basement)
df.hotwaterheating=le.fit_transform(df.hotwaterheating)
df.airconditioning=le.fit_transform(df.airconditioning)
df.furnishingstatus=le.fit_transform(df.furnishingstatus)


# In[27]:


df.head()


# ## 8. Split the data into dependent and independent variables.

# In[28]:


X = df.drop('price', axis=1)  
y = df['price'] 


# In[29]:


X


# In[30]:


y


# ## 9. Scale the independent variables
# 

# In[31]:


name=X.columns
name


# In[32]:


from sklearn.preprocessing import MinMaxScaler

min_max=MinMaxScaler()


# In[33]:


X_scaled=min_max.fit_transform(X)


# In[34]:


X_scaled


# In[35]:


x=pd.DataFrame(X_scaled,columns=name)
x


# ## 10. Split the data into training and testing

# In[36]:


from sklearn.model_selection import train_test_split


# In[37]:


X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)


# ## 11. Build the Model

# In[38]:


# Model Building
from sklearn.linear_model import LinearRegression
lr=LinearRegression()


# ## 12. Train the Model

# In[39]:


lr.fit(X_train,y_train)


# ## 13. Test the Model

# In[40]:


y_pred=lr.predict(X_test)


# In[41]:


y_pred


# In[42]:


y_test


# In[44]:


from sklearn.metrics import r2_score
acc=r2_score(y_pred,y_test)
acc


# ## 14. Measure the performance using Metrics.

# In[45]:


from sklearn.metrics import mean_squared_error,r2_score, mean_absolute_error


# In[46]:


# Error

E=y_test-y_pred
E


# In[47]:


# Squared Error

se=E*E
se


# In[48]:


# Mean squared error

mse=np.mean(se)
mse


# In[49]:


mse2=mean_squared_error(y_test,y_pred)
mse2


# In[50]:


# Mean Absolute Error
mae=mean_absolute_error(y_test,y_pred)
mae


# In[51]:


# Root Mean Square Error
rmse=np.sqrt(mse2)
rmse


# In[52]:


# R-Squared
r2=r2_score(y_test,y_pred)
r2


# ## Logistic Regression

# In[53]:


from sklearn.linear_model import LogisticRegression
Lr=LogisticRegression()


# In[55]:


Lr.fit(X_train,y_train)


# In[56]:


pred=lr.predict(X_test)


# In[57]:


pred1=lr.predict(X_train)


# In[72]:


from sklearn.metrics import r2_score
acc=r2_score(y_test,y_pred)
acc


# In[ ]:




