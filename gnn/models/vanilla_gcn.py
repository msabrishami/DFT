import dgl
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch import Sequential
import numpy as np

gcn_msg = fn.copy_src(src='h', out='m')
gcn_reduce = fn.mean(msg='m', out='h')

class GCNLayer(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(GCNLayer, self).__init__()
        self.linear = nn.Linear(in_feats, out_feats)

    def forward(self, g, feature, g_rev=None):
        with g.local_scope():
            g.ndata['h'] = feature
            g.update_all(gcn_msg, gcn_reduce)
            h_in = g.ndata['h']
        if g_rev:
            with g_rev.local_scope():
                g_rev.ndata['h'] = feature
                g_rev.update_all(gcn_msg, gcn_reduce)
                h_out = g_rev.ndata['h']
            x = torch.cat((h_in, h_out, feature), dim=1)
        else:
            x = torch.cat((h_in, feature), dim=1)
        # added g_rev in the output because dgl.Sequentional doesn't provide g_rev for the next layer
        return F.relu(self.linear(x)), g_rev

class VanillaGCN(nn.Module):
    def __init__(self, feature_dim=6, output_dim=1, weight_dim=512, depth=10, rev=False):
        super(VanillaGCN, self).__init__()
        self.input_layer = nn.Linear(feature_dim, weight_dim)
        self.hidden_layers = Sequential(*[GCNLayer(3*weight_dim if rev else 2*weight_dim, weight_dim) for i in range(depth)])
        self.output_layer = nn.Linear(weight_dim, output_dim)

    def forward(self, g, features, g_rev=None):
        x = F.relu(self.input_layer(features))
        x, _ = self.hidden_layers(g, x, g_rev)
        x = self.output_layer(x)
        return x

