
# coding: utf-8

# In[13]:


import numpy as np
from sklearn.decomposition import PCA
import pandas as pd


# In[18]:


df = pd.read_csv('new_consolidated_data.csv', sep=',',header=0)
del df['State']
del df['Year']
np_array = df.values


# In[24]:


pca = PCA(n_components='mle', svd_solver='full')


# In[25]:


pca.fit(np_array)

