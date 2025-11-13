import random

pobl=[]
for pajaro in range(99):
    w=[]
    for peso in range(4):
        w.append(round(random.uniform(-1, 1), 2))
    pobl.append(w)
print(w)
print(pobl)


class pajaro:
    def __init__(self, w, vy):
        self.w0= w[0]
        self.w1= w[1]
        self.w2= w[2]
        self.w3= w[3]
        self.w4= w[4]
        self.w5= w[5]
        self.vy= vy

    

