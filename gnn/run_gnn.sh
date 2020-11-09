#!/bin/bash
# Classification task on level
# python gnn.py --weight-dim=32 --depth=10 --objective=lev --model=VanillaGCN --train-circuit=c3540 --test-circuit=c432 --problem=classification --loss=CE --bidirectional


# Regression, gtype given 
# python gnn.py --weight-dim=256 --depth=3 --objective=B0 --features=C0,C1,CO,CC0,CC1,gtype --model=VanillaGCN --train-circuit=c7552 --test-circuit=c7552 --problem=regression --loss=L2 --sigmoid


# Regression problem with limited features, output is input
# THIS WORKED -- DON't CHANGE SETUP
# python gnn.py --weight-dim=32 --depth=1 --objective=B0 --features=C0,C1,B0,B1 --model=FakeGCN --train-circuit=c432 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid

# THIS WORKED -- DON't CHANGE SETUP
# python gnn.py --weight-dim=32 --depth=1 --objective=B0 --features=C0,C1,B0,B1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid

# THIS DOES NOT WORK, SCOAP is not scaled!  
# python gnn.py --weight-dim=32 --depth=1 --objective=B0 --features=C0,C1,B0,B1,CO,CC0,CC1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid

# WORKED!  
# python gnn.py --weight-dim=32 --depth=1 --objective=B0 --features=C0,C1,B0,B1,CB0,CB1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid

# Worked! Run it again with better otimizer, but loss is around 0.002 with ADAM10e-2
# python gnn.py --weight-dim=32 --depth=1 --objective=B --features=C0,C1,B0,B1,CB0,CB1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid


 python gnn.py --weight-dim=32 --depth=1 --objective=B --features=C0,C1,B0,B1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid



# Regression problem with limited features, output not input
# python gnn.py --weight-dim=64 --depth=3 --objective=B --features=C0,C1,B0,B1,CO,CC0,CC1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid


# Regression problem with more features
# python gnn.py --weight-dim=64 --depth=3 --objective=B --features=C0,C1,B0,B1,CO,CC0,CC1,CB0,CB1 --model=FakeGCN --train-circuit=c6288 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid


# python gnn.py --weight-dim=64 --depth=3 --objective=HTO --features=C0,C1,B0,B1,CO,CC0,CC1,CB0,CB1,B   --model=FakeGCN --train-circuit=c432 --test-circuit=c432 --problem=classification --loss=CE
