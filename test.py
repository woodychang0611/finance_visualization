import numpy as np
import math
def random_weight(len):
    def F():    
        rand = np.random.random(len)
        rand = np.exp(rand*30)
        n=0
        threshold = np.sort(rand)[-n]
        func =lambda s:s if (s>=threshold) else 0
        rand = np.array(list(func(i) for i in rand))
        a = rand / rand.sum()
        return a
    return F

f = random_weight(100)
for i in range(100):
    a = f()
    a = a[a != 0]
    a = np.sort(a)
    print(a[-10])
    print(a[-1]/a[0])
