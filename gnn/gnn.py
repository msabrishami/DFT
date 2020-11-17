
import sys
import os
import time
import numpy as np
import copy
import pdb

import dgl
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from dgl import DGLGraph
from dgl.nn.pytorch.utils import Sequential
import networkx as nx

import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

from models.vanilla_gcn import VanillaGCN, FakeGCN
from models.lstm_gcn import LSTMGCN
import config
from utils import get_options

sys.path.insert(1, "../circuit/")

torch.manual_seed(0)
np.random.seed(0)

def load_data(options, path, feat_list=None):
    """
    loads the circuit graph in nx format, converts it to DGLGraph
    returns: graph, graph-reversed, features, labels
    """

    print("Loading graph from {}".format(path))
    graph_nx = nx.read_graphml(path)

    if options.bidirectional:
        raise NameError("Bidirectional graph not supported")
        edges = copy.deepcopy(graph_nx.edges())
        graph_nx_rev = copy.deepcopy(graph_nx)
        for edge in edges:
            graph_nx_rev.add_edge(edge[1],edge[0])
        graph_nx_rev.remove_edges_from(list(edges))

    graph = DGLGraph(graph_nx)
    graph_rev = DGLGraph(graph_nx_rev) if options.bidirectional else None

    all_ids = list(graph_nx.nodes.keys())
    
    # Suggestion, if complicated, read from config file
    if feat_list == None:
        feat_list = [x.strip() for x in options.features.split(",")] if options.features else []
        
        gate_list = None
        if "gtype" in feat_list:
            if options.const_gtype:
                gtypes = config.GTYPES
            else:
                gtypes = set()
                for node_id in graph_nx.nodes:
                    gtypes.add(graph_nx.nodes[node_idx]["gtype"])
            feat_list.remove("type")
            feat_list.extend(["gtype-" + x for x in gtypes])

    data = np.zeros((len(graph_nx.nodes), len(feat_list)), dtype=np.float32)
    label = np.zeros(len(graph_nx.nodes), dtype=np.float32)
    
    
    for node_id in graph_nx.nodes:
        node_idx = all_ids.index(node_id)
        for feat_idx, feat_name in enumerate(feat_list):
            if "gtype-" in feat_name:
                gtype = graph_nx.nodes[node_id]['gtype']
                data[node_idx, feat_idx] = 1.0
            else:
                data[node_idx, feat_idx] = graph_nx.nodes[node_id][feat_name]

        label[node_idx] = graph_nx.nodes[node_id][options.objective]
    
    data = torch.FloatTensor(data).cuda()
    label = torch.FloatTensor(label).cuda()

    print("Graph, data, and label are loaded")
    return graph, graph_rev, data, label, feat_list, graph_nx.nodes


def load_loss(options):
    # Loss function
    if options.loss == "L1":
        loss = torch.nn.L1Loss()
    elif options.loss == "L2":
        loss = torch.nn.MSELoss()
    elif options.loss == "CE":
        # loss = torch.nn.CrossEntropyLoss()
        loss = torch.nn.BCEWithLogitsLoss()
    else:
        raise ValueError('The loss ' + options.loss + ' is not valid.')

    return loss

def load_model(options, feat_dim, output_dim):
    g_train_rev = None
    
    if options.model == "FakeGCN":
        net = FakeGCN(feature_dim=feat_dim, output_dim=output_dim, 
                weight_dim=options.weight_dim, depth=options.depth, 
                rev=True if g_train_rev else False, dropout=0.4).cuda()

    elif options.model == "VanillaGCN":
        net = VanillaGCN(feature_dim=feat_dim, output_dim=output_dim, 
                weight_dim=options.weight_dim, depth=options.depth, 
                rev=True if g_train_rev else False, dropout=0.25).cuda()

    elif options.model == "LSTMGCN":
        net = LSTMGCN(feature_dim=feat_dim, output_dim=output_dim, 
                weight_dim=options.weight_dim, depth=options.depth, 
                rev=True if g_train_rev else False).cuda()
    else:
        raise ValueError('The model ' + options.model + ' is not valid.')

    return net



def evaluate(net, options, g, data, labels, mask, loss_function, g_rev=None, debug=False):
    net.eval()
    with torch.no_grad():
        logits = net(g, data, g_rev=g_rev)
        logits = logits.squeeze()
        if options.sigmoid:
            logits = torch.sigmoid(logits)
        logits = logits[mask]
        labels = labels[mask]

        if options.problem == "regression":
            n_digits = 1
            loss = loss_function(logits.squeeze(), labels)
            labels = labels.cpu().numpy()
            logits = logits.squeeze().cpu().numpy()
            # grid_size = 20
            # grid_count = np.zeros((grid_size, grid_size), dtype=np.float32)
            # labels_max = np.max(labels)
            # labels_min = np.min(labels)
            # labels_buckets = np.linspace(labels_min-config.EPS, labels_max, num=grid_size)
            preds = logits

            # TODO: this is temp
            accuracy = None 

        if options.problem == "classification":
            assert labels.ndim == 1 and labels.size() == logits.size()
            preds = torch.sigmoid(logits)
            preds = preds > config.BC_TH
            # if num-classes > 1:
            # _, indices = torch.max(logits, dim=1)
            # correct = torch.sum(indices == labels)
            # accuracy = correct.item() * 1.0 / len(labels)

            correct = (preds == labels).sum().item()
            accuracy = correct / labels.shape[0]
            loss = loss_function(logits, labels).item()
            
            # labels = labels.cpu().numpy()
            # indices = indices.cpu().numpy()
            # grid_size = 20
            # grid_count = np.zeros((grid_size, grid_size), dtype=np.float32)
            # labels_max = np.max(labels)
            # labels_min = np.min(labels)
            # labels_buckets = np.linspace(labels_min-config.EPS, labels_max, num=grid_size)

        if debug:
            print("Samples: {}".format(len(labels)))
            outfile = open("report-temp.log", "w")
            outfile.write("Labels,")
            outfile.write(",".join([str(x) for x in labels.tolist()] ))
            outfile.write("\nLogits,")
            outfile.write(",".join([str(x) for x in logits.tolist()] ))
            outfile.write("\n")
            print("Saved! Press C to continue")
            outfile.close()
            pdb.set_trace()
        
        """
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
        """
        return accuracy, loss

def main():
        
    options, args = get_options()
    
    # path = os.path.join(config.GRAPH_DIR,  options.circuit_train + "_10e3.graphml")
    path = "./../data/graph/" + options.circuit_train  + "_10e3_HTC-0.05_HTO-0.02.graphml"
    g_train, g_train_rev, data_train, labels_train, feat_list, id_train = load_data(options, path)
    
    path = "./../data/graph/" + options.circuit_test  + "_10e3_HTC-0.05_HTO-0.02.graphml"
    g_test, g_test_rev, data_test, labels_test, _, id_test = load_data(options, path, feat_list)

    # random_bools = np.random.choice(a=[True, False], 
    #         size=(len(labels_train)), p=[config.TRAIN_RATIO, 1-config.TRAIN_RATIO])
    # train_mask = torch.BoolTensor(random_bools).cuda()
    # valid_mask = torch.BoolTensor(np.invert(random_bools)).cuda()
    print("data and model loaded")

    g_train = g_train.to(torch.device("cuda:0"))
    g_test = g_test.to(torch.device("cuda:0"))

    net = load_model(options, data_train.shape[1], 1)
    loss_function = load_loss(options)
    
    

    if config.OPT == "SGD":
        lr_milestone = [2000, 3000, 4000, 4500]
        optimizer = torch.optim.SGD(net.parameters(), lr=0.1, momentum=0.9)
        train_scheduler = optim.lr_scheduler.MultiStepLR(
                optimizer, milestones=lr_milestone, gamma=0.2) 
    elif config.OPT == "ADAM":
        optimizer = torch.optim.Adam(net.parameters(), lr=1e-2)
        train_scheduler = optim.lr_scheduler.MultiStepLR(
                optimizer, milestones=[1000000], gamma=0.2) 
    else:
        raise NameError("Optimizer was not found")
    dur = []

    
    # Gradient clipping for avoiding gradient explosion
    #for p in net.parameters():
    #    p.register_hook(lambda grad: torch.clamp(grad, -0.1, 0.1))

    
    for epoch in range(5000):
        # In each epoch we just pick a batch of samples to train (backprop)
        batch_mask = np.random.choice(a=[True, False], size=(len(g_train.nodes())), 
                p=[config.TRAIN_BATCH_RATIO, 1-config.TRAIN_BATCH_RATIO])
        train_mask = torch.BoolTensor(batch_mask).cuda()
        valid_mask = torch.BoolTensor(np.invert(batch_mask)).cuda()
    
        t0 = time.time()
        net.train()
        logits = net(g_train, data_train, g_train_rev)

        logits = logits.squeeze()
        if options.sigmoid:
            logits = torch.sigmoid(logits)
        loss = loss_function(logits[train_mask], labels_train[train_mask])
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_scheduler.step(epoch) 
    
        dur.append(time.time() - t0)

        debug = True if epoch in [3001] else False
    
        if epoch % 10 == 0:
            train_acc, _ = evaluate(net, options, g_train, data_train, labels_train, train_mask, loss_function, g_rev=g_train_rev, debug=debug)

            valid_acc, valid_loss = evaluate(net, options, g_train, data_train, labels_train, valid_mask, loss_function, g_rev=g_train_rev, debug=debug)

            test_acc, test_loss = evaluate(net, options, g_test, data_test, labels_test, [True]*len(labels_test), loss_function, g_rev=g_test_rev, debug=debug)
    
            if options.problem == "regression":
                print("Epoch {:05d} lr {:0.5f} | Train Loss {:.4f} | Valid Loss {:.4f} | Test Loss {:.4f} | Time(s) {:.4f}".format(epoch, optimizer.param_groups[0]['lr'], loss.item(), valid_loss, test_loss, np.mean(dur)))
            elif options.problem == "classification":
                print("Epoch {:05d} | Train> Loss {:.4f} Acc {:.4f} | \
                        Valid> Loss {:.4f} Acc {:.4f} | \
                         Test> Loss {:.4f} Acc{:.4f}".format(
                             epoch, loss.item(), train_acc, 
                             valid_loss, valid_acc, test_loss, test_acc))

        
    print("Training Done")
    train_acc, train_loss = evaluate(net, options, g_train, data_train, labels_train, 
            [True]*len(labels_train), loss_function, g_rev=g_train_rev, debug=True)
        
    test_acc, test_loss = evaluate(net, options, g_test, data_test, labels_test, 
            [True]*len(labels_test), loss_function, g_rev=g_test_rev, debug=True)
        
    print(train_loss.item(), "\t", test_loss.item())

if __name__ == "__main__":
    main()
