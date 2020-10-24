from scipy.cluster.vq import kmeans, whiten
from numpy import genfromtxt, zeros
from matplotlib import pyplot as plt

consolidated_data = genfromtxt('new_consolidated_data.csv', delimiter=',',skip_header=1)

features = consolidated_data[:,2:-13]

whitened = whiten(features)

k_distortion = zeros(50)

for k in range(1,51):
    centroids, distortion = kmeans(whitened, k)
    k_distortion[k-1] = distortion

fig, ax = plt.subplots()
plt.plot(range(1,51), k_distortion)
plt.xlabel("Number of clusters")
plt.ylabel("Distortion")
plt.show()
