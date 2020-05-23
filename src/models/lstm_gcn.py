import dgl
import dgl.function as fn
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from dgl import DGLGraph
from dgl.nn.pytorch import Sequential
import numpy as np

from torch.autograd import Variable

gcn_msg = fn.copy_src(src='h', out='m')
gcn_reduce = fn.sum(msg='m', out='h')

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


class GCNLSTMLayer(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(GCNLSTMLayer, self).__init__()
        self.out_feats = out_feats
        self.lstm = nn.LSTM(in_feats, out_feats)

    def forward(self, g, feature, state):
        # Creating a local scope so that all the stored ndata and edata
        # (such as the `'h'` ndata below) are automatically popped out
        # when the scope exits.
        with g.local_scope():
            g.ndata['h'] = feature.view(-1,self.out_feats)
            g.update_all(gcn_msg, gcn_reduce)
            h = g.ndata['h']
            return self.lstm(h.view(1,-1,self.out_feats), state)

    def init_hidden(self, batch_size):
        return (Variable(th.zeros(1, batch_size, self.out_feats)),
                Variable(th.zeros(1, batch_size, self.out_feats)))
        hidden = Variable(next(self.lstm.parameters()).data.new(batch_size, 1, self.out_feats), requires_grad=False)
        cell = Variable(next(self.lstm.parameters()).data.new(batch_size, 1, self.out_feats), requires_grad=False)
        return hidden.zero_(), cell.zero_()

class LSTMGCN(nn.Module):
    def __init__(self, feature_dim=6, output_dim=1, weight_dim=512, depth=10):
        super(LSTMGCN, self).__init__()
        self.input_layer = GCNLayer(feature_dim, weight_dim)
        self.lstm_layer = GCNLSTMLayer(weight_dim, weight_dim)
        self.output_layer = self.output_layer = nn.Linear(weight_dim, output_dim)
        self.weight_dim = weight_dim
        self.feature_dim = feature_dim
        self.depth = depth

    def forward(self, g, features):
        batch_size = features.size(0)
        x = F.relu(self.input_layer(g, features))

        h_t, c_t = self.lstm_layer.init_hidden(batch_size)
        h_t, c_t = h_t.cuda(), c_t.cuda()

        _, state = self.lstm_layer(g, x.view(-1,batch_size,self.weight_dim),(h_t,c_t))

        for i in range(self.depth):
            _, state = self.lstm_layer(g, state[0], state)
        h_t = state[0]
        c_t = state[1]
        x = self.output_layer(h_t.view(-1, self.weight_dim))
        return x

