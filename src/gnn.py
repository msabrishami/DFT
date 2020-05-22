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

from models.vanilla_gcn import VanillaGCN
from models.lstm_gcn import LSTMGCN
net = VanillaGCN().cuda()
print(net)


def load_cora_data():
    circuit = Circuit('c1355')
    circuit.read_circuit()
    circuit.lev()
#    circuit.controllability()
#    circuit.observability()
    circuit.STAFAN(100, num_proc=8)
    circuit.co_ob_info()
    graph = circuit.gen_graph()
    g = DGLGraph(graph)

    all_types = []
    for n in circuit.nodes_lev:
        n_num_trans = circuit.node_ids.index(n.num)
        if n.gtype not in all_types:
            all_types.append(n.gtype)

    features = np.zeros((len(circuit.nodes_lev), len(all_types)))
    labels = np.zeros(len(circuit.nodes_lev), dtype=np.float32)
    for n in circuit.nodes_lev:
        n_num_trans = circuit.node_ids.index(n.num)
        features[n_num_trans, all_types.index(n.gtype)] = 1.0
        labels[n_num_trans] = circuit.nodes_lev[n_num_trans].C1 # TODO: for now, we are only taking C1 as the label. Need more explorations.

    np.random.seed(0)
    random_bools = np.random.choice(a=[False, True], size=(len(circuit.nodes_lev)), p=[0.2, 0.8])
    train_mask = th.BoolTensor(random_bools).cuda()
    test_mask = th.BoolTensor(np.invert(random_bools)).cuda()
    labels = th.FloatTensor(labels).cuda()
    features = th.FloatTensor(features).cuda()

    return g, features, labels, train_mask, test_mask


"""When a model is trained, we can use the following method to evaluate
the performance of the model on the test dataset:
"""

def evaluate(model, g, features, labels, mask):
    model.eval()
    with th.no_grad():
        logits = model(g, features)
        logits = logits[mask]
        labels = labels[mask]
        return F.l1_loss(logits, labels).item()


g, features, labels, train_mask, test_mask = load_cora_data()
optimizer = th.optim.Adam(net.parameters(), lr=1e-3)
dur = []
for epoch in range(5000):
    if epoch >=3:
        t0 = time.time()

    net.train()
    logits = net(g, features)

    loss = F.l1_loss(logits[train_mask].squeeze(), labels[train_mask])
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch >=3:
        dur.append(time.time() - t0)

    acc = evaluate(net, g, features, labels, test_mask)
    print("Epoch {:05d} | Loss {:.4f} | Test Loss {:.4f} | Time(s) {:.4f}".format(
            epoch, loss.item(), acc, np.mean(dur)))
