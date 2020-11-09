
 
from optparse import OptionParser

def get_options():    
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
    parser.add_option('-f','--features',  dest='features', type='str', 
            help='What features are given to the nodes', default=None)
    (options, args) = parser.parse_args()

    return options, args
