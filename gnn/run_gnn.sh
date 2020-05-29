#!/bin/bash
python gnn.py --weight-dim=256 --depth=5 --objective=level --model=VanillaGCN --train-circuit=c3540 --test-circuit=c432 --problem=classification --loss=CE
