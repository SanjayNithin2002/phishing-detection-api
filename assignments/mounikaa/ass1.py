#!/usr/bin/env python
# coding: utf-8

# # ADS ASSIGNMENT 03
# ## NAME: MOUNIKAA V
# ## REG NO:20BIT0050

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# importing necessary libraries


# ## 2) Load the dataset

# In[2]:


data=pd.read_csv('Housing.csv')


# In[3]:


data


# In[4]:


data.head()


# In[5]:


data.shape


# ## 3. Perform Below Visualizations.
# ###  Univariate Analysis
# ###  Bi-Variate Analysis
# ###  Multi-Variate Analysis

# ### 1)Univariate analysis

# In[6]:


#piechart-I’m performing analysis of the variable 'furnishingstatus' and displaying it in the form of piechart 
abc=data['furnishingstatus'].value_counts()
abc


# In[7]:


list = data['furnishingstatus'].unique()
plt.pie(abc, autopct='% 2f',labels=list)
plt.legend()


# ### 2)Bivariate analysis

# Bivariate analysis-I’m using the variables 'price' and 'mainroad' to plot a bar graph.

# In[8]:


plt.bar(data['mainroad'],data['price'])


# ### 3)Multivariate analysis

# In[9]:


plt.figure(figsize=(8,6))
sns.scatterplot(data=data,x="stories",y="area",hue="furnishingstatus")
plt.show()


# ### 4. Perform descriptive statistics on the dataset.

# In[10]:


data.describe()


# In[11]:


data.mean()


# In[12]:


data.median()


# In[13]:


data.mode()


# In[14]:


data.std()


# In[15]:


data.var()


# In[16]:


data.kurt()


# In[17]:


data.skew()


# ### 5. Check for Missing values and deal with them.

# In[18]:


#checking for null values


# In[19]:


data.isnull().sum()


# no null(missing) values in the given dataset

# ### 6. Find the outliers and replace them outliers

# In[20]:


plt.boxplot(data.price)


# In[77]:


quantile=data['price'].quantile(q=[0.75,0.25,0.50])
quantile


# In[78]:


columns=['price','area','bedrooms','bathrooms','stories','mainroad','guestroom','basement','hotwaterheating','airconditioning','parking','furnishingstatus']
for column in columns:
  q1=data[column].quantile(0.25)
  q3=data[column].quantile(0.75)
  IQR=q3-q1
  lowerbound=q1-(1.5*IQR)
  upperbound=q3+(1.5*IQR)
  # print(column,q1,q3,IQR,lowerbound,upperbound)

  #outliers
  outliers = data[(data[column] < lowerbound) | (data[column] > upperbound)]
  print(column,outliers)
  #replacing with median
  data.loc[(data[column] < lowerbound) | (data[column] > upperbound), column] = data[column].median()


# In[79]:


plt.boxplot(data['price'])


# ### 7. Check for Categorical columns and perform encoding.

# The categorical columns here are :'mainroad','guestroom','basement','hotwaterheating','airconditioning','furnishingstatus'

# In[23]:


from sklearn.preprocessing import LabelEncoder


# In[24]:


le=LabelEncoder()


# In[25]:


data['mainroad']=le.fit_transform(data['mainroad'])
data['guestroom']=le.fit_transform(data['guestroom'])
data['basement']=le.fit_transform(data['basement'])
data['hotwaterheating']=le.fit_transform(data['hotwaterheating'])
data['airconditioning']=le.fit_transform(data['airconditioning'])
data['furnishingstatus']=le.fit_transform(data['furnishingstatus'])


# In[26]:


data.head()


# all categorical columns are now converted to numerical columns

# ### 8. Split the data into dependent and independent variables.

# In[80]:


x=data.drop(columns='price')
x
#independent variable


# In[81]:


y=data['price']
y #dependent variable


# ### 9. Scale the independent variables

# In[82]:


from sklearn.preprocessing import StandardScaler


# In[83]:


names=x.columns
names


# In[84]:


sc=StandardScaler()


# In[85]:


x=sc.fit_transform(x)
x


# In[86]:


x=pd.DataFrame(x,columns=names)
x


# scaling is done

# ### 10. Split the data into training and testing

# In[66]:


from sklearn.model_selection import train_test_split


# In[67]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)


# In[68]:


x_train.shape


# In[69]:


x_test.shape


# ### 11.Model Building

# In[87]:


#Logistic Regression and Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression


# ### 12.Train the model ,13. Test the model,14.Evaluation metrics

# In[89]:


#1)linear Regression
lr=LinearRegression()


# In[90]:


lr.fit(x_train,y_train)


# In[91]:


pred=lr.predict(x_test)
pred


# In[92]:


y_test


# In[93]:


from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error


# In[94]:


error=y_test-pred
error


# In[95]:


se=error*error
se


# In[96]:


mse=np.mean(se)
mse


# In[98]:


mse1=mean_squared_error(y_test,pred)
mse1
#mean squared error


# In[99]:


rmse=np.sqrt(mse1)
rmse
#root mean squared error


# In[100]:


r2_score(y_test,pred)
# accuracy


# In[101]:


mae=mean_absolute_error(y_test,pred)
mae
#mean absolute error


# accuracy of linear regression is nearly 56 %.

# In[ ]:


# 2)LogisticRegression


# In[102]:


log_reg=LogisticRegression()


# In[103]:


log_reg.fit(x_train,y_train)


# In[142]:


pred1=log_reg.predict(x_test)


# In[143]:


pred1


# In[144]:


pred2=log_reg.predict(x_train)
pred2


# In[145]:


from sklearn.metrics import accuracy_score,confusion_matrix,classification_report


# In[146]:


accuracy_score(y_test,pred1)#for testing with test data


# In[147]:


print(confusion_matrix(y_test,pred1))


# In[149]:


print(classification_report(y_test,pred1))


# In[150]:


# FOR TESTING WITH TRAINING DATA 
accuracy_score(y_train,pred2)


# In[151]:


confusion_matrix(y_train,pred2)


# In[ ]:





# In[111]:


#KNN
from sklearn.neighbors import KNeighborsClassifier


# In[112]:


knn=KNeighborsClassifier()


# In[113]:


knn.fit(x_train,y_train)


# In[152]:


pred3=knn.predict(x_test)


# In[153]:


pred3


# In[157]:


pred4=knn.predict(x_train)
pred4


# In[ ]:


#for test dataset


# In[155]:


accuracy_score(y_test,pred3)


# In[158]:


#for train dataset
accuracy_score(y_train,pred4)


# In[117]:


#DecisionTree
from sklearn.tree import DecisionTreeClassifier


# In[118]:


dt=DecisionTreeClassifier()


# In[119]:


dt.fit(x_train,y_train)


# In[120]:


pred2=dt.predict(x_test)
pred2


# In[121]:


accuracy_score(y_test,pred2)


# In[122]:


#RandomForest
from sklearn.ensemble import RandomForestClassifier


# In[123]:


rf=RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)


# In[124]:


rf.fit(x_train,y_train)


# In[129]:


pred3=rf.predict(x_train)


# In[130]:


pred3


# In[133]:


confusion_matrix(y_train,pred3)


# In[134]:


accuracy_score(y_train,pred3)


# for test dataset
# 

# In[160]:


pred5=rf.predict(x_test)
pred5


# In[161]:


accuracy_score(y_test,pred5)


# In[ ]:


# for random forest algorithm while testing the model with training data we get high accuracy of 96%.

