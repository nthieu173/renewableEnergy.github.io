from sklearn import mixture
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas
import matplotlib.pyplot as plt
from collections import Counter

consolidated_data = pandas.read_csv('../new_consolidated_data.csv', delimiter=',')

states = consolidated_data.iloc[:, 0]
features = consolidated_data.iloc[:, 2:-13]
renew_percent = consolidated_data.iloc[:, -1] / 100

scaler = StandardScaler()
scaled = scaler.fit_transform(features)

gm_bic = []
gm_score = []
for i in range(2, 12):
    gm = mixture.GaussianMixture(n_components=15, n_init=2000).fit(scaled)
    print("BIC for number of cluster(s) {}: {}".format(i, gm.bic(scaled)))
    print("Log-likelihood score for number of cluster(s) {}: {}".format(i, gm.score(scaled)))
    print("-" * 100)
    gm_bic.append(-gm.bic(scaled))
    gm_score.append(gm.score(scaled))

plt.figure(figsize=(7, 4))
plt.title("The Gaussian Mixture model BIC \nfor determining number of clusters\n", fontsize=16)
plt.scatter(x=[i for i in range(2, 12)], y=np.log(gm_bic), s=150, edgecolor='k')
plt.grid(True)
plt.xlabel("Number of clusters", fontsize=14)
plt.ylabel("Log of Gaussian mixture BIC score", fontsize=15)
plt.xticks([i for i in range(2, 12)], fontsize=14)
plt.yticks(fontsize=15)
plt.show()
