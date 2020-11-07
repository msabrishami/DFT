#!/bin/bash
# Classification task on level
# python gnn.py --weight-dim=32 --depth=10 --objective=lev --model=VanillaGCN --train-circuit=c3540 --test-circuit=c432 --problem=classification --loss=CE --bidirectional

# Regression task on D_p
# python gnn.py --weight-dim=128 --depth=3 --objective=CC1 --features=C0,C1,CO,CC0,CC1,gtype --model=VanillaGCN --train-circuit=c7552 --test-circuit=c7552 --problem=regression --loss=L2 --sigmoid
python gnn.py --weight-dim=64 --depth=2 --objective=CC1 --features=C0,C1,CO,CC0,CC1 --model=FakeGCN --train-circuit=c432 --test-circuit=c432 --problem=regression --loss=L2 --sigmoid
