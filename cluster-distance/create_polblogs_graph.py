import networkx as nx
import numpy as np 
import pickle

dataFile = "datasets/polblogs/polblogs.gml"

G = nx.read_gml(dataFile , label='id')

links = np.zeros((1490,1490))
attributes = np.empty(1490)

for node_id in G.node:
    attributes[node_id-1] = G.node[node_id]['value']
    for neighbor_id in G.neighbors(node_id):
        links[node_id-1][neighbor_id-1] = 1

print np.sum(links)

attributes_links = {"attributes":attributes , "links":links}
pickle.dump(attributes_links , open("pol_data.p" , "wb"))

