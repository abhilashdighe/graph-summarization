import random
import sys
from networkx import *

numNodes = 10
numEdges = 20
numAttributes = 10
numValuesPerAttribute = 2
numClusters = 2


G = gnm_random_graph(numNodes,numEdges)

# some properties
print("node degree clustering")
for v in nodes(G):
    print('%s %d %f' % (v,degree(G,v),clustering(G,v)))

# print the adjacency list to terminal
try:
    write_adjlist(G,sys.stdout)
except TypeError: # Python 3.x
    write_adjlist(G,sys.stdout.buffer)
