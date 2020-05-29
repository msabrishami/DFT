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
            x = torch.cat((h, feature), dim=1)

            return self.linear(x)


class GCNLSTMLayer(nn.Module):
    def __init__(self, in_feats, out_feats, num_layers=3):
        super(GCNLSTMLayer, self).__init__()
        self.out_feats = out_feats
        self.num_layers = num_layers

        self.lstm = nn.LSTM(in_feats, out_feats, num_layers=self.num_layers) #2*out_feats as to separate node and neibours features

    def forward(self, g, feature, state):
        # Creating a local scope so that all the stored ndata and edata
        # (such as the `'h'` ndata below) are automatically popped out
        # when the scope exits.
        with g.local_scope():
            g.ndata['h'] = feature.view(-1,self.out_feats)
            g.update_all(gcn_msg, gcn_reduce)
            h = g.ndata['h']
            return self.lstm(torch.cat((h.view(1,-1,self.out_feats), feature.view(1,-1,self.out_feats)), 2), state)

    def init_hidden(self, batch_size):
        return (Variable(torch.zeros(self.num_layers, batch_size, self.out_feats)),
                Variable(torch.zeros(self.num_layers, batch_size, self.out_feats)))

class LSTMGCN(nn.Module):
    def __init__(self, feature_dim=6, output_dim=1, weight_dim=512, depth=10):
        super(LSTMGCN, self).__init__()
        self.input_layer = GCNLayer(2*feature_dim, weight_dim)
        self.lstm_layer = GCNLSTMLayer(2*weight_dim, weight_dim) #as we concat node feature and its neighbours features
        self.output_layer = nn.Linear(weight_dim, output_dim)
        self.weight_dim = weight_dim
        self.feature_dim = feature_dim
        self.depth = depth

    def forward(self, g, features):
        batch_size = features.size(0)
        x = F.relu(self.input_layer(g, features))

        h_t, c_t = self.lstm_layer.init_hidden(batch_size)
        h_t, c_t = h_t.cuda(), c_t.cuda()

        output, state = self.lstm_layer(g, x.view(-1,batch_size,self.weight_dim),(h_t,c_t))
        for i in range(self.depth):
            _, state = self.lstm_layer(g, state[0][0], state)

        x = self.output_layer(state[0][0])
        return x

