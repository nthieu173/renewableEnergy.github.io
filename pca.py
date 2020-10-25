import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('new_consolidated_data.csv', sep=',',header=0)

features = df.iloc[:,2:-13]

pca = PCA(n_components=3, svd_solver='full')# In[25]:

pca.fit(features)

reduced = pca.transform(features)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(reduced[:,0],reduced[:,1],reduced[:,2])
plt.show()