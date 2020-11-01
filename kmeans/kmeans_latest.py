import pandas
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from collections import Counter
from matplotlib import colors
from matplotlib import pyplot as plt

num_all_rows_of_state = 19

def clustering(data_file):
    consolidated_data = pandas.read_csv(data_file, delimiter=',')
    latest_data = consolidated_data[consolidated_data["Year"] == max(consolidated_data["Year"])]

    features = latest_data.iloc[:,2:-13]

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=15, n_init=2000)
    labels = kmeans.fit_predict(scaled)

    label_states = [[] for i in range(15)]

    for (i, label) in enumerate(labels):
        label_states[label] += [i]
    label_states.sort(key=lambda s: len(s), reverse=True)
    for (i, states) in enumerate(label_states):
        label_states[i] = sorted(list(states), key=lambda s: latest_data["renewable_energy_percentage"].iloc[s])
    listed_states = [item for l in label_states for item in l]

    label_color = []
    distinct_colors = ["#2f4f4f", "#00fa9a", "#a0522d", "#FFDF00","#006400", "#ff69b4", "#4b0082",
        "#ff0000", "#00ced1", "#ffa500", "#00ff00", "#0000ff", "#ff00ff", "#1e90ff", "#D2691E"]
    for (i,states) in enumerate(label_states):
        for s in states:
            label_color += [distinct_colors[i]]

    f = plt.figure(figsize=(16,8))
    plt.bar(range(50), latest_data["renewable_energy_percentage"].iloc[listed_states],
        tick_label=latest_data["State"].iloc[listed_states], color=label_color)

    plt.savefig("output/latest_year_clustering.svg")
    plt.show()

def main():
    clustering("../new_consolidated_data.csv")

if __name__ == "__main__":
    main()