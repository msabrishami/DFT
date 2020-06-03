import sys
sys.path.insert(1, '../circuit/')

import dgl
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch import Sequential
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

# Constant values
EPS = 1e-6

torch.manual_seed(0)
np.random.seed(0)

parser = OptionParser()
parser.add_option('-w', '--weight-dim', dest='weight_dim', default=512, type='int',
                  help='weight dimension (default: 512)')
parser.add_option('-d', '--depth', dest='depth', default=20, type='int',
                  help='number of hops explored in the graph (default: 20)')
parser.add_option('-o', '--objective', dest='objective', default="lev", type='str',
                  help='learning objective (default: level)')
parser.add_option('-m', '--model', dest='model', default="LSTMGCN", type='str',
                  help='model architecture (default: LSTMGCN)')
parser.add_option('--train-circuit', dest='circuit_train', default="c1355", type='str',
                  help='circuit name (default: c1355)')
parser.add_option('--test-circuit', dest='circuit_test', default="c432", type='str',
                  help='circuit name (default: c432)')
parser.add_option('-p', '--problem', dest='problem', default="classification", type='str',
                  help='classification or regression? (default: classification)')
parser.add_option('-l', '--loss', dest='loss', default="CE", type='str',
                  help='loss function (default: cross entropy)')
parser.add_option('-b', '--bidirectional', dest='bidirectional', action="store_true",
                  help='make the graph uni-directional or bi-directional')
parser.add_option('-s', '--sigmoid', dest='sigmoid', action="store_true",
                  help='Sigmoid function applied to the logits')
parser.add_option('-f','--features',  dest='features', type='str', help='What features are given to the nodes', default=None)
(options, args) = parser.parse_args()

def load_data_with_model():
    """
    This function loads the circuit graph, then returns the features, labels, model, split train/test sets
    """
    # Read the train circuit
    graph_train = nx.readwrite.graphml.read_graphml('../data/graph/'+options.circuit_train+'_10e4.graphml')
    # Read the test circuit
    graph_test = nx.readwrite.graphml.read_graphml('../data/graph/'+options.circuit_test+'_10e4.graphml')

    # Create a reverse graph in which the direction of the edges are reversed
    g_train_rev = None
    g_test_rev = None
    if options.bidirectional:
        edges = copy.deepcopy(graph_train.edges())
        graph_train_rev = copy.deepcopy(graph_train)
        for edge in edges:
            graph_train_rev.add_edge(edge[1],edge[0])
        graph_train_rev.remove_edges_from(list(edges))

        edges = copy.deepcopy(graph_test.edges())
        graph_test_rev = copy.deepcopy(graph_test)
        for edge in edges:
            graph_test_rev.add_edge(edge[1],edge[0])
        graph_test_rev.remove_edges_from(list(edges))

        g_train_rev = DGLGraph(graph_train_rev)
        g_test_rev = DGLGraph(graph_test_rev)

    g_train = DGLGraph(graph_train)
    g_test = DGLGraph(graph_test)

    # Extract the unique gate types present in the train adn test circuits for creating the labels
    all_types = []
    all_ids_train = list(graph_train.nodes.keys())
    all_ids_test = list(graph_test.nodes.keys())

    for node_id in graph_train.nodes:
        if graph_train.nodes[node_id]['gtype'] not in all_types:
            all_types.append(graph_train.nodes[node_id]['gtype'])
    for node_id in graph_test.nodes:
        if graph_test.nodes[node_id]['gtype'] not in all_types:
            all_types.append(graph_test.nodes[node_id]['gtype'])

    # Compute the feature dimension based on the requested features
    features_list = [x.strip() for x in options.features.split(",")] if options.features else []
    feature_dim = 1 #1 is the default feature_dim when no features are provided
    for feature_name in features_list:
        if feature_name == "gtype":
            feature_dim += len(all_types)
        else:
            feature_dim += 1

    features_train = np.zeros((len(graph_train.nodes), feature_dim), dtype=np.float32)
    features_test = np.zeros((len(graph_test.nodes), feature_dim), dtype=np.float32)
    labels_train = np.zeros(len(graph_train.nodes), dtype=np.float32)
    labels_test = np.zeros(len(graph_test.nodes), dtype=np.float32)

    # Create the features and labels for train circuit
    for node_id in graph_train.nodes:
        node_index = all_ids_train.index(node_id)
        feature_ind_counter = 0
        for feature_name in features_list:
            if feature_name == "gtype":
                features_train[node_index, feature_ind_counter + all_types.index(graph_train.nodes[node_id]['gtype'])] = 1.0
                feature_ind_counter += len(all_types)
            else:
                features_train[node_index, feature_ind_counter] = graph_train.nodes[node_id][feature_name]
                feature_ind_counter += 1
        if options.objective == "D_p":
            labels_train[node_index] = graph_train.nodes[node_id]['D0_p'] + graph_train.nodes[node_id]['D1_p']
        else:
            labels_train[node_index] = graph_train.nodes[node_id][options.objective]

    # Create the features and labels for test circuit
    for node_id in graph_test.nodes:
        node_index = all_ids_test.index(node_id)
        feature_ind_counter = 0
        for feature_name in features_list:
            if feature_name == "gtype":
                features_test[node_index, feature_ind_counter + all_types.index(graph_test.nodes[node_id]['gtype'])] = 1.0
                feature_ind_counter += len(all_types)
            else:
                features_test[node_index, feature_ind_counter] = graph_test.nodes[node_id][feature_name]
                feature_ind_counter += 1
        if options.objective == "D_p":
            labels_test[node_index] = graph_test.nodes[node_id]['D0_p'] + graph_test.nodes[node_id]['D1_p']
        else:
            labels_test[node_index] = graph_test.nodes[node_id][options.objective]

    print ("All labels: ")
    print (np.sort(labels_train))

    random_bools = np.random.choice(a=[False, True], size=(len(graph_train.nodes)), p=[0.05, 0.95])
    train_mask = torch.BoolTensor(random_bools).cuda()
    test_mask = torch.BoolTensor(np.invert(random_bools)).cuda()
    features_train = torch.FloatTensor(features_train).cuda()
    features_test = torch.FloatTensor(features_test).cuda()

    # Instantiating the appropriate model
    if options.problem == "regression":
        output_dim = 1
        labels_train = torch.FloatTensor(labels_train).cuda()
        labels_test = torch.FloatTensor(labels_test).cuda()
    elif options.problem == "classification":
        output_dim = int(max(np.concatenate((labels_train, labels_test)))+1)
        labels_train = torch.LongTensor(labels_train).cuda()
        labels_test = torch.LongTensor(labels_test).cuda()
    else:
        raise ValueError('The problem ' + options.problem + ' is not valid.')

    if options.model == "VanillaGCN":
        net = VanillaGCN(feature_dim=features_train.shape[1], output_dim=output_dim, weight_dim=options.weight_dim, depth=options.depth, rev=True if g_train_rev else False).cuda()
    elif options.model == "LSTMGCN":
        net = LSTMGCN(feature_dim=features_train.shape[1], output_dim=output_dim, weight_dim=options.weight_dim, depth=options.depth, rev=True if g_train_rev else False).cuda()
    else:
        raise ValueError('The model ' + options.model + ' is not valid.')

    # Loss function
    if options.loss == "L1":
        loss = torch.nn.L1Loss()
    elif options.loss == "L2":
        loss = torch.nn.MSELoss()
    elif options.loss == "CE":
        loss = torch.nn.CrossEntropyLoss()
    else:
        raise ValueError('The loss ' + options.loss + ' is not valid.')

    return g_train, g_test, g_train_rev, g_test_rev, features_train, labels_train, train_mask, test_mask, features_test, labels_test, net, loss


def evaluate(net, g, features, labels, mask, loss_function, g_rev=None):
    net.eval()
    with torch.no_grad():
        logits = net(g, features, g_rev=g_rev)
        logits = logits.squeeze()
        if options.sigmoid:
            logits = torch.sigmoid(logits)
        logits = logits[mask]
        labels = labels[mask]

        if options.problem == "regression":
#            if torch.max(labels) <= 1: #The range will be 0-1
            n_digits = 1
            logits_rounded = torch.round(logits.squeeze() * 10**n_digits) / (10**n_digits)
            labels_rounded = torch.round(labels * 10**n_digits) / (10**n_digits)
            correct = torch.sum(logits_rounded == labels_rounded)
#            else:
#                correct = torch.sum(torch.round(logits.squeeze()) == labels)

            accuracy = correct.item() * 1.0 / len(labels)
            loss = loss_function(logits.squeeze(), labels)
            labels = labels.cpu().numpy()
            logits = logits.squeeze().cpu().numpy()
            grid_size = 20
            grid_count = np.zeros((grid_size, grid_size), dtype=np.float32)
            labels_max = np.max(labels)
            labels_min = np.min(labels)
            labels_buckets = np.linspace(labels_min-EPS, labels_max, num=grid_size)
            preds = logits

        if options.problem == "classification":
            _, indices = torch.max(logits, dim=1)
            correct = torch.sum(indices == labels)
            accuracy = correct.item() * 1.0 / len(labels)
            loss = loss_function(logits, labels).item()

            grid_size = 20
            grid_count = np.zeros((grid_size, grid_size), dtype=np.float32)
            labels = labels.cpu().numpy()
            indices = indices.cpu().numpy()
            labels_max = np.max(labels)
            labels_min = np.min(labels)
            labels_buckets = np.linspace(labels_min-EPS, labels_max, num=grid_size)
            preds = indices

        for i in range(len(labels_buckets)-1):
            for j in range(len(labels_buckets)-1):
                 count = (np.logical_and(np.logical_and(labels > labels_buckets[i], labels <= labels_buckets[i+1]), \
                          np.logical_and(preds > labels_buckets[j], preds <= labels_buckets[j+1]))).sum()
                 grid_count[len(labels_buckets)-1-j, i] = count

        plt.figure()
        ax = sns.heatmap(grid_count)
        fig = ax.get_figure()
        axis_labels = [] #[round(x,2) for x in labels_buckets]
        fig.savefig(options.problem + ".png", annot=True)
        plt.close()
        return accuracy, loss

g_train, g_test, g_train_rev, g_test_rev, features_train, labels_train, train_mask, test_mask, features_test, labels_test, net, loss_function = load_data_with_model()

#g, features, labels, train_mask, test_mask, net, loss_function = load_data_with_model()
optimizer = torch.optim.Adam(net.parameters(), lr=1e-2)
dur = []

# Gradient clipping for avoiding gradient explosion
#for p in net.parameters():
#    p.register_hook(lambda grad: torch.clamp(grad, -0.1, 0.1))

for epoch in range(50000):
    random_bools = np.random.choice(a=[False, True], size=(len(g_train.nodes())), p=[0.2, 0.8])
    train_mask = torch.BoolTensor(random_bools).cuda()
    test_mask = torch.BoolTensor(np.invert(random_bools)).cuda()

    t0 = time.time()
    net.train()
    logits = net(g_train, features_train, g_train_rev)
    logits = logits.squeeze()
    if options.sigmoid:
        logits = torch.sigmoid(logits)
    loss = loss_function(logits[train_mask], labels_train[train_mask])

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    dur.append(time.time() - t0)

    test_accuracy_ctr, test_loss_ctr = evaluate(net, g_train, features_train, labels_train, test_mask, loss_function, g_rev=g_train_rev)
    test_accuracy_cte, test_loss_cte = evaluate(net, g_test, features_test, labels_test, [True]*len(labels_test), loss_function, g_rev=g_test_rev)

    print("Epoch {:05d} | Train Loss {:.4f} | Source Circuit's Test Loss {:.4f} | Source Circuit's Test Acc {:.4f} | Target Circuit's Test Loss {:.4f} | Target Circuit's Test Acc {:.4f} | Time(s) {:.4f}".format(
            epoch, loss.item(), test_loss_ctr, test_accuracy_ctr, test_loss_cte, test_accuracy_cte, np.mean(dur)))
