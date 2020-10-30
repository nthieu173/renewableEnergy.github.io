import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px

import matplotlib.pyplot as plt
from matplotlib import colors

df = pd.read_csv('new_consolidated_data.csv', sep=',',header=0)

features = df.iloc[:,2:-13]

renew_percent = df.iloc[:,-1] / 100

scaler = StandardScaler()
scaled = scaler.fit_transform(features)
pca = PCA(n_components=3, svd_solver='full')

pca.fit(scaled)

reduced = pca.transform(scaled)

n = len(renew_percent)
color_percent = np.vstack((np.zeros(n),renew_percent.to_numpy(),np.zeros(n))).T #Darker less renewable
#color_percent = np.vstack((1 - renew_percent.to_numpy(),np.ones(n),1 - renew_percent.to_numpy())).T #Lighter less renewable


row_color = np.apply_along_axis(colors.to_hex, 1, color_percent)

fig =px.scatter_3d(df, x=reduced[:,0], y=reduced[:,1], z=reduced[:,2],
    color="renewable_energy_percentage", hover_data=["State","Year","renewable_energy_percentage"])

fig.show()
fig.write_html("output/pca.html")
