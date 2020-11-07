

import sys
import os
sys.path.insert(1, '../circuit/')

import dgl
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch.utils import Sequential
import numpy as np
import time
import copy
import networkx as nx

import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from optparse import OptionParser
from models.vanilla_gcn import VanillaGCN
from models.lstm_gcn import LSTMGCN
import seaborn as sns; sns.set()
import pdb


import config

path = os.path.join(config.GRAPH_DIR,  "c17_10e4.graphml")
print("Loading train graph from {}".format(path))
graph_train = nx.read_graphml(path)
g_train = DGLGraph(graph_train)
all_types = []
all_ids_train = list(graph_train.nodes.keys())

for node_id in graph_train.nodes:
    if graph_train.nodes[node_id]['gtype'] not in all_types:
        all_types.append(graph_train.nodes[node_id]['gtype'])

print(all_types)
features_list = [x.strip() for x in options.features.split(",")] if options.features else []
feature_dim = 1 #1 is the default feature_dim when no features are provided
for feature_name in features_list:
    if feature_name == "gtype":
        feature_dim += len(all_types)
    else:
        feature_dim += 1

