from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from collections import Counter
import pandas

consolidated_data = pandas.read_csv('new_consolidated_data.csv', delimiter=',')

states_years = consolidated_data.iloc[:,0:1]

features = consolidated_data.iloc[:,2:-13]

scaler = StandardScaler()

scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=15, n_init=50)
labels = kmeans.fit_predict(scaled)

label_dict = dict([(k,[]) for k in range(0,15)])

for (i, label) in enumerate(labels):
    label_dict[label] += [states_years.iloc[i]["State"]]

ordered_label = []
for label in label_dict:
    ordered_label += [Counter(label_dict[label])]

ordered_label.sort(key=lambda c: len(c))

for (k,counter) in enumerate(ordered_label):
    print("Cluster {}: ".format(k+1), end="")
    for state in counter:
        print("{}: {}, ".format(state, counter[state]),end="")
    print("")