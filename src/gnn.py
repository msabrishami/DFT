import dgl
import dgl.function as fn
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch import Sequential
import numpy as np
import time
import networkx as nx
from circuit import Circuit
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from optparse import OptionParser
from models.vanilla_gcn import VanillaGCN
from models.lstm_gcn import LSTMGCN

th.manual_seed(0)
np.random.seed(0)

parser = OptionParser()
parser.add_option('-w', '--weight-dim', dest='weight_dim', default=512, type='int',
                  help='weight dimension (default: 512)')
parser.add_option('-d', '--depth', dest='depth', default=20, type='int',
                  help='number of hops explored in the graph (default: 20)')
parser.add_option('-o', '--objective', dest='objective', default="level", type='str',
                  help='learning objective (default: level)')
parser.add_option('-m', '--model', dest='model', default="LSTMGCN", type='str',
                  help='model architecture (default: LSTMGCN)')
parser.add_option('-c', '--circuit', dest='circuit', default="c1355", type='str',
                  help='circuit name (default: c1355)')
parser.add_option('-p', '--problem', dest='problem', default="classification", type='str',
                  help='classification or regression? (default: classification)')

(options, args) = parser.parse_args()

def load_data_with_model():
    """
    This function loads the circuit graph, then returns the features, labels, model, split train/test sets
    """
    # Load the circuit
    circuit = Circuit(options.circuit)
    circuit.read_circuit()
    circuit.lev()
    circuit.STAFAN(10000, num_proc=8)
    circuit.co_ob_info()
    graph = circuit.gen_graph()
    g = DGLGraph(graph)

    # Extract the unique gate types present in the circuit for creating the labels
    if options.objective == "level":
        all_types = []
        for n in circuit.nodes_lev:
            n_num_trans = circuit.node_ids.index(n.num)
            if n.gtype not in all_types:
                all_types.append(n.gtype)
        features = np.zeros((len(circuit.nodes_lev), len(all_types)))
    else:
        raise ValueError('The objective ' + options.objective + ' is not available')

    labels = np.zeros(len(circuit.nodes_lev), dtype=np.float32)
    for n in circuit.nodes_lev:
        n_num_trans = circuit.node_ids.index(n.num)
        if options.objective == "level":
#            features[n_num_trans, all_types.index(n.gtype)] = 1.0
            labels[n_num_trans] = circuit.nodes_lev[n_num_trans].lev

        if options.objective == "C1":
            labels[n_num_trans] = circuit.nodes_lev[n_num_trans].C1

    random_bools = np.random.choice(a=[False, True], size=(len(circuit.nodes_lev)), p=[0.2, 0.8])
    train_mask = th.BoolTensor(random_bools).cuda()
    test_mask = th.BoolTensor(np.invert(random_bools)).cuda()
    features = th.FloatTensor(features).cuda()

    if options.problem == "regression":
        labels = th.FloatTensor(labels).cuda()
        if options.model == "VanillaGCN":
            net = VanillaGCN(feature_dim=features.shape[1], output_dim=1, weight_dim=options.weight_dim, depth=options.depth).cuda()
        if options.model == "LSTMGCN":
            net = LSTMGCN(feature_dim=features.shape[1], output_dim=1, weight_dim=options.weight_dim, depth=options.depth).cuda()

    if options.problem == "classification":
        labels = th.LongTensor(labels).cuda()
        if options.model == "VanillaGCN":
            net = VanillaGCN(feature_dim=features.shape[1], output_dim=len(np.unique(labels.cpu().numpy())), weight_dim=options.weight_dim, depth=options.depth).cuda()
        if options.model == "LSTMGCN":
            net = LSTMGCN(feature_dim=features.shape[1], output_dim=len(np.unique(labels.cpu().numpy())), weight_dim=options.weight_dim, depth=options.depth).cuda()
    print (np.unique(labels.cpu().numpy()))

    return g, features, labels, train_mask, test_mask, net


def evaluate(model, g, features, labels, mask):
    model.eval()
    with th.no_grad():
        logits = model(g, features)
        logits = logits[mask]
        labels = labels[mask]

        if options.problem == "regression":
            correct = th.sum(th.round(logits.squeeze()) == labels)
            accuracy = correct.item() * 1.0 / len(labels)
            loss = F.l1_loss(logits.squeeze(), labels)
            fig = plt.figure()
            matplotlib.pyplot.scatter(logits.squeeze().cpu().numpy(), labels.cpu().numpy())
            matplotlib.pyplot.xlabel("prediction")
            matplotlib.pyplot.ylabel("ground truth")
            fig.savefig(options.problem+'.png')

        if options.problem == "classification":
            _, indices = th.max(logits, dim=1)
            correct = th.sum(indices == labels)
            accuracy = correct.item() * 1.0 / len(labels)
            loss = F.nll_loss(F.log_softmax(logits), labels).item()
            fig = plt.figure()
            matplotlib.pyplot.scatter(indices.cpu().numpy(), labels.cpu().numpy())
            matplotlib.pyplot.xlabel("prediction")
            matplotlib.pyplot.ylabel("ground truth")
            fig.savefig(options.problem+'.png')
            matplotlib.pyplot.close()
        return accuracy, loss


g, features, labels, train_mask, test_mask, net = load_data_with_model()
optimizer = th.optim.Adam(net.parameters(), lr=1e-3)
dur = []

# Gradient clipping for avoiding gradient explosion
#for p in net.parameters():
#    p.register_hook(lambda grad: th.clamp(grad, -0.1, 0.1))

for epoch in range(5000):
    t0 = time.time()
    net.train()
    logits = net(g, features)

    if options.problem == "regression":
        loss = F.l1_loss(logits[train_mask].squeeze(), labels[train_mask])
    if options.problem == "classification":
        loss = F.nll_loss(F.log_softmax(logits[train_mask],1), labels[train_mask])

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    dur.append(time.time() - t0)

    test_accuracy, test_loss = evaluate(net, g, features, labels, test_mask)
    print("Epoch {:05d} | Train Loss {:.4f} | Test Loss {:.4f} | Test Acc {:.4f} | Time(s) {:.4f}".format(
            epoch, loss.item(), test_loss, test_accuracy, np.mean(dur)))
