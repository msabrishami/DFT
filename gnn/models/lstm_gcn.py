import dgl
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch import Sequential
import numpy as np
from torch.autograd import Variable

gcn_msg = fn.copy_src(src='h', out='m')
gcn_reduce = fn.mean(msg='m', out='h')

def max_reduce(nodes):
    return {'h': torch.max(nodes.mailbox['m'], dim=1)[0]}

def max_norm_reduce(nodes):
    batch_size, incoming_count, weight_dim = nodes.mailbox['m'].shape
    norms = torch.norm(nodes.mailbox['m'], p=2, dim=2)
    ind_max = torch.max(norms, dim=1)[1] #.repeat(weight_dim).view(batch_size, weight_dim)
    reduced = nodes.mailbox['m'][range(batch_size), ind_max]
    return {'h': reduced}

class GCNLayer(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(GCNLayer, self).__init__()
        self.linear = nn.Linear(in_feats, out_feats)

    def forward(self, g, feature):
        with g.local_scope():
            g.ndata['h'] = feature
            g.update_all(gcn_msg, gcn_reduce)
            h = g.ndata['h']
            x = torch.cat((h, feature), dim=1)

            return self.linear(x)


class GCNLSTMLayer(nn.Module):
    def __init__(self, weight_dim, num_layers=3):
        super(GCNLSTMLayer, self).__init__()
        self.weight_dim = weight_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(2*weight_dim, weight_dim, num_layers=self.num_layers)

    def forward(self, g, feature, state):
        with g.local_scope():
            g.ndata['h'] = feature.view(-1,self.weight_dim)
            g.update_all(gcn_msg, max_norm_reduce)
            h = g.ndata['h']
            return self.lstm(torch.cat((h.view(1,-1,self.weight_dim), feature.view(1,-1,self.weight_dim)), 2), state)

    def init_hidden(self, batch_size):
        return (Variable(torch.zeros(self.num_layers, batch_size, self.weight_dim)),
                Variable(torch.zeros(self.num_layers, batch_size, self.weight_dim)))

class LSTMGCN(nn.Module):
    def __init__(self, feature_dim=6, output_dim=1, weight_dim=512, depth=10):
        super(LSTMGCN, self).__init__()
        self.input_layer = nn.Linear(feature_dim, weight_dim)
        self.lstm_layer = GCNLSTMLayer(weight_dim)
        self.output_layer = nn.Linear(weight_dim, output_dim)
        self.weight_dim = weight_dim
        self.feature_dim = feature_dim
        self.depth = depth

    def forward(self, g, features):
        batch_size = features.size(0)
        x = F.relu(self.input_layer(features))

        h_t, c_t = self.lstm_layer.init_hidden(batch_size)
        h_t, c_t = h_t.cuda(), c_t.cuda()

        output, state = self.lstm_layer(g, x.view(-1,batch_size,self.weight_dim),(h_t,c_t))
        for i in range(self.depth):
            _, state = self.lstm_layer(g, state[0][-1], state)

        x = self.output_layer(state[0][-1])
        return x

