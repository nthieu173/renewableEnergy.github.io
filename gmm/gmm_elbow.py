from sklearn import mixture
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas
import matplotlib.pyplot as plt

consolidated_data = pandas.read_csv('../new_consolidated_data.csv', delimiter=',')

states = consolidated_data.iloc[:, 0]
features = consolidated_data.iloc[:, 2:-13]
renew_percent = consolidated_data.iloc[:, -1] / 100

scaler = StandardScaler()
scaled = scaler.fit_transform(features)

n_components = np.arange(1, 50)

clfs = [mixture.GaussianMixture(n).fit(scaled) for n in n_components]
bics = [clf.bic(scaled) for clf in clfs]
aics = [clf.aic(scaled) for clf in clfs]

plt.plot(n_components, bics, label = 'BIC')
plt.plot(n_components, aics, label = 'AIC')
plt.xlabel('n_components')
plt.legend()
plt.show()
