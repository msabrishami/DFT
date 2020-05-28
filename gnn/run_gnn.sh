#!/bin/bash
python gnn.py --weight-dim=256 --depth=100 --objective=level --model=LSTMGCN --train-circuit=c3540 --test-circuit=c432 --problem=classification --loss=CE
