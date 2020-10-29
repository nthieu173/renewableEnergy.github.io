import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors

df = pd.read_csv('new_consolidated_data.csv', sep=',',header=0)

features = df.iloc[:,2:-13]

renew_percent = df.iloc[:,-1] / 100

pca = PCA(n_components=3, svd_solver='full')# In[25]:

pca.fit(features)

reduced = pca.transform(features)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = len(renew_percent)
color_percent = np.vstack((np.zeros(n),renew_percent.to_numpy(),np.zeros(n))).T
row_color = np.apply_along_axis(colors.to_hex, 1, color_percent)

ax.scatter(reduced[:,0],reduced[:,1],reduced[:,2],c=row_color)
plt.show()