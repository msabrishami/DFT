#!/bin/bash
python gnn.py --weight-dim=1024 --depth=30 --objective=level --model=LSTMGCN --train-circuit=c499 --test-circuit=c432 --problem=classification --loss=CE
