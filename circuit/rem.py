
import random
bits = ["0","1","X"]

tp = [int(bits[random.randint(0,1)]) for _ in range(3)]
print(tp)
# tps = []
# for t in range(2**3):
#     tp = list(bin(t)[2:].zfill(2**3))
#     tps.append(tp)
# print(tps)