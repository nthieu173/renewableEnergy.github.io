from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from collections import Counter
import pandas
import os

print(os.getcwd())

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

reversed_counter_label = []

for counter in ordered_label:
    reversed_counter = dict([(count, []) for count in counter.values()])
    for state, count in counter.items():
        reversed_counter[count] += [state]
    reversed_counter_label += [reversed_counter]

for (k,counter) in enumerate(reversed_counter_label):
    print("Cluster {}: ".format(k+1), end="")
    sorted_list = [(count, counter[count]) for count in counter]
    sorted_list.sort(key=lambda t: t[0],reverse=True)
    for count, states in sorted_list:
        print("{}: {}, ".format(count, states),end="")
    print("")