import dgl
import dgl.function as fn
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch import Sequential
import numpy as np

gcn_msg = fn.copy_src(src='h', out='m')
gcn_reduce = fn.sum(msg='m', out='h')

"""We then proceed to define the GCNLayer module. A GCNLayer essentially performs
message passing on all the nodes then applies a fully-connected layer.
"""

class GCNLayer(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(GCNLayer, self).__init__()
        self.linear = nn.Linear(in_feats, out_feats)

    def forward(self, g, feature):
        # Creating a local scope so that all the stored ndata and edata
        # (such as the `'h'` ndata below) are automatically popped out
        # when the scope exits.
        with g.local_scope():
            g.ndata['h'] = feature
            g.update_all(gcn_msg, gcn_reduce)
            h = g.ndata['h']
            return self.linear(h)

"""The forward function is essentially the same as any other commonly seen NNs
model in PyTorch.  We can initialize GCN like any ``nn.Module``. For example,
let's define a simple neural network consisting of two GCN layers. Suppose we
are training the classifier for the cora dataset (the input feature size is
1433 and the number of classes is 7). The last GCN layer computes node embeddings,
so the last layer in general does not apply activation.
"""

class VanillaGCN(nn.Module):
    def __init__(self, weight_dim=512, depth=10):
        super(VanillaGCN, self).__init__()
        self.input_layer = GCNLayer(6, weight_dim)
        self.hidden_layers = Sequential(*[GCNLayer(weight_dim, weight_dim) for i in range(depth)])
        self.output_layer = GCNLayer(weight_dim, 1)

    def forward(self, g, features):
        x = F.relu(self.input_layer(g, features))
        x = self.hidden_layers(g, x)
        x = self.output_layer(g, x)
        return x

