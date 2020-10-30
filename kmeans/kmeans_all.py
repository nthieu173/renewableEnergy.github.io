from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter
from graphviz import Graph
from matplotlib import colors
import pandas
import numpy as np

def clustering(data_file):
    consolidated_data = pandas.read_csv(data_file, delimiter=',')

    states = consolidated_data.iloc[:,0]
    features = consolidated_data.iloc[:,2:-13]
    renew_percent = consolidated_data.iloc[:,-1] / 100

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=15, n_init=2000)
    labels = kmeans.fit_predict(scaled)

    label_dict = dict([(k,Counter()) for k in range(0,15)])

    label_renewable = dict([(k,[]) for k in range(0,15)])

    for (i, label) in enumerate(labels):
        state = states.iloc[i]
        label_dict[label][state] += 1
        label_renewable[label] += [renew_percent.iloc[i]]
    
    for l in label_renewable:
        label_renewable[l] = np.mean(label_renewable[l])

    return label_dict, label_renewable

def graph_label(data, renewable):
    num_all_rows_of_state = 19

    g = Graph("all_years_clustering", engine="fdp",
        format="svg", edge_attr={"penwidth":"4"}, node_attr={"style":"filled"})

    for lab in data:
        if len(data[lab]) == 1:
            g.node(next(iter(data[lab])))
            continue
        complete_node = []
        incomplete_node = []
        for state in data[lab]:
            dist = data[lab][state]
            if dist == num_all_rows_of_state:
                complete_node += [state]
            else:
                incomplete_node += [(state, dist)]
        node_color = colors.to_hex([0,1,0, renewable[lab]], keep_alpha=True)
        if len(complete_node) > 0:
            g.node(str(lab), label=",".join(complete_node), fillcolor=node_color)
        else:
            g.node(str(lab), label="", width=str(0.2), height=str(0.2), fillcolor=node_color)
        for state, dist in incomplete_node:
            edge_color = [0,0,0,dist/num_all_rows_of_state]
            g.edge(str(lab), state, weight=str(dist),
                color=colors.to_hex(edge_color, keep_alpha=True))
    g.render("output/all_years_clustering", view=True, cleanup=True)

def main():
    label_state, label_renewable = clustering("../new_consolidated_data.csv")
    graph_label(label_state, label_renewable)

if __name__ == "__main__":
    main()