import pandas
from scipy.cluster.vq import kmeans, whiten
from numpy import zeros
from matplotlib import pyplot as plt

consolidated_data = pandas.read_csv("../new_consolidated_data.csv", delimiter=',')

latest_data = consolidated_data[consolidated_data["Year"] == max(consolidated_data["Year"])]

features = latest_data.iloc[:,2:-13]

whitened = whiten(features)

k_distortion = zeros(50)

for k in range(1,51):
    centroids, distortion = kmeans(whitened, k)
    k_distortion[k-1] = distortion

fig, ax = plt.subplots()
plt.plot(range(1,51), k_distortion)
plt.xlabel("Number of clusters")
plt.ylabel("Distortion")
plt.savefig("output/states_latest_year_elbow.svg")
plt.show()
