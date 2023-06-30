#!/usr/bin/env python
# coding: utf-8

# # SANJAYNITHIN 20BIT0150
# # ADS ASSIGNMENT 2

# In[2]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ## 2. Load the dataset.

# In[3]:


df=pd.read_csv('titanic.csv')


# In[4]:


df.head()


# In[5]:


df.shape


# In[6]:


df.columns


# ## 3. Perform Below Visualizations.
# ● Univariate Analysis
# ● Bi - Variate Analysis
# ● Multi - Variate Analysis

# In[7]:


# Univariate analysis

# Histogram

sns.histplot(df['alive'])



# In[35]:


import seaborn as sns 
sns.countplot(data=df,x='embarked')


# In[36]:


#piechart on gender 

df['sex'].value_counts().plot(kind="pie",autopct="%.2f")


# In[38]:


sns.boxplot(df['age'])


# In[39]:


# Bivariate analysis

# Scatter plot
sns.scatterplot(data=df,x="age",y="fare")


# In[9]:


# Multivariate Analysis

correlation_matrix = df[['age', 'sex', 'alive']].corr()

# Create a heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix Heatmap")
plt.show()


# ## 4. Perform descriptive statistics on the dataset.

# In[10]:


# Mean
df.mean()


# In[11]:


df.median()


# In[12]:


df.mode()


# In[13]:


df.max()


# In[14]:


df.min()


# In[15]:


# range

ran=df.max()-df.min()
ran


# In[ ]:


df.var()


# In[ ]:


df.std()


# In[ ]:


quantile=df['age'].quantile(q=[0.75,0.25,0.50])
quantile


# ## 5. Handle the Missing values.

# In[ ]:


df.isna()


# In[ ]:


df.isnull().any()


# In[ ]:


df.isnull().sum()


# In[16]:


df['age'].fillna(df['age'].mean(),inplace=True)


# In[17]:


df.isnull().sum()


# In[18]:


mode_category = df['deck'].mode().iloc[0]
df['deck'].fillna(mode_category, inplace=True)


# In[19]:


df.isnull().sum()


# In[20]:


df.dropna(axis=0, thresh=3, inplace=True)
df.dropna(subset=['embark_town', 'embarked'], inplace=True)


# In[21]:


df.isnull().sum()


# ## 6. Find the outliers and replace the outliers

# In[33]:


columns=['pclass','age','sibsp','parch','fare']
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

# In[27]:


df.info()


# In[28]:


from sklearn.preprocessing import LabelEncoder

le=LabelEncoder()

df.sex=le.fit_transform(df.sex)
df.alive=le.fit_transform(df.alive)
df.alone=le.fit_transform(df.alone)
df.who=le.fit_transform(df.who)
df.embarked=le.fit_transform(df.embarked)
df.adult_male=le.fit_transform(df.adult_male)
df['class']=le.fit_transform(df['class'])
df.deck=le.fit_transform(df.deck)
df.embark_town=le.fit_transform(df.embark_town)


# In[29]:


df.head()


# ## 8. Split the data into dependent and independent variables.

# ### y -> Dependent variable 
# ### x -> Independent variable

# In[36]:


y=df['survived']


# In[37]:


y.head()


# In[38]:


x=df.drop(columns=['survived'],axis=1)


# In[39]:


x.head()


# ## 9. Scale the independent variables

# In[109]:


name=x.columns
name


# In[89]:


from sklearn.preprocessing import MinMaxScaler

min_max=MinMaxScaler()


# In[90]:


X_scaled=min_max.fit_transform(x)


# In[91]:


X_scaled


# In[110]:


X=pd.DataFrame(X_scaled,columns=name)
X


# ## 10. Split the data into training and testing

# In[101]:


from sklearn.model_selection import train_test_split


# In[102]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)


# In[103]:


X_train.head()


# In[104]:


X_test.head()


# In[105]:


y_train


# In[106]:


y_test


# In[ ]:




