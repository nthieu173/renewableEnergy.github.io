import numpy as np
import sklearn
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors

# Uncomment following lines to print dataframe without truncation
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

#class Unsupervised_Learning():
#    def __init__(self, data_file='new_consolidated_data.csv', PCA_ncomp=0, kMeans_ncluster=):
#        self.df = pd.read_csv('new_consolidated_data.csv', sep=',', header=0)
#        del self.df['State']
#        del self.df['Year']
#        self.features = df.iloc[:,2:-13]
#        self.renew_percent = df.iloc[:,-1] / 100

df = pd.read_csv('../new_consolidated_data.csv', sep=',', header=0)
del df['State']
del df['Year']

features = df.iloc[:,2:-13]
renew_percent = df.iloc[:,-1] / 100

scaler = StandardScaler()
features = scaler.fit_transform(features)
# Center and scale features
scaled_features = sklearn.preprocessing.scale(features)

# Perform PCA on scaled features
pca = PCA(n_components='mle', svd_solver='full')
pca.fit(scaled_features)

rd_features = pca.transform(scaled_features)

# Plot variance recovered
n_components = len(pca.components_)
idx_comp = range(1, n_components+1)
rec_var = np.cumsum(pca.explained_variance_ratio_)
fig1 = plt.figure()
plt.title(f'PCA Results - {n_components} components (MLE)')
plt.xlabel('PC')
plt.xticks(idx_comp)
plt.ylabel('Variance')
plt.bar(idx_comp, pca.explained_variance_ratio_, label='variance of PC')
#plt.step(idx_comp, rec_var, where='mid', label='cumulative recovered variance')
plt.plot(idx_comp, rec_var, label='cumulative recovered variance') # I think this looks better
plt.legend(loc='best')
plt.savefig("output/recovered_variance.svg")

#fig2 = plt.figure()
#plt.title('hi')


plt.show()
