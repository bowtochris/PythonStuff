# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 01:21:58 2025

@author: bowto
"""

import time
import math

class LFSRRand():
    inv_erf_coeff_dict = dict()
    
    def __init__(self, seed = 0):
        self.seed(seed)
        
    def seed(self, seed):
        if(seed == None or seed > 0):
            self.val = seed
        else:
            self.val = int(time.time_ns())
    
    def getState(self):
        return self.val
    
    def setState(self, state):
        self.val = state
    
    def nextByte(self):
        bit = self.val
        for i in [16,14,13,11]:
            bit = bit ^ (self.val >> i)
        bit = bit & 1
        self.val = (self.val >> 1) | (bit << 15)
        return self.val % 256
    
    def randbytes(self, n):
        barry = list()
        for i in range(n):
            barry.append(self.nextByte())
        return bytes(barry)
    
    def randrange(self, start, stop=None, step=None):
        if(step == None):
            step = 1
        
        if(stop == None):
            stop = start
            start = 0
        
        if(start > stop):
            temp = start
            start = stop
            stop = temp
        
        if(step < 0):
            step = - step
        
        diff = stop - start
        max_steps = math.ceil(diff/step)
        
        rval = self.getrandbits((int(max_steps / 256) * 2 + 2))
        rval %= max_steps
        
        return start + (rval * step)
    
    def randint(self, a, b):
        return self.randrange(a, stop = b+1, step = 1)
    
    def getrandbits(self, n):
        x = int.from_bytes(self.randbytes(math.ceil(n / 8)), byteorder='big', signed=False)
        x = x % (2 ** n)
        return x
    
    def random(self):
        size = 4
        bs = self.randbytes(size)
        x = int.from_bytes(bs, byteorder='big', signed=False) 
        x = x / (2 ** (8 * size))
        return x
    
    def choice(self, seq):
        if(not seq):
            raise IndexError("Cannot choose from an empty sequence")
        else:
            return seq[self.randint(0, len(seq) - 1)]
        
    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        if(k < 1):
            return None
        elif(k > 1):
            rval = []
            for i in range(k):
                rval += self.choices(population, weights, cum_weights=cum_weights)
            return rval
        else:
            if(not population):
                raise IndexError("Q")
                
            if(weights and cum_weights):
                raise TypeError("Q")
                
            if(not weights and not cum_weights):
                cum_weights = [i + 1 for i in range(len(population))]
                
            if(weights):
                cum_weights = [sum(weights[:i]) for i in range(len(weights))]
                
            if(cum_weights and not(all(cum_weights))):
                raise ValueError("Q")
                
            total = sum(cum_weights)
            rval = total * self.random()
            
            for i in range(len(population)):
                if(rval < cum_weights[i]):
                    return [population[i]]
                
            return [population[-1]]
        
    def shuffle(self, seq):
        indices = list(range(len(seq)))
        val = list()
        while(indices):
            i = self.choice(indices)
            indices.remove(i)
            val.append(seq[i])
            
        for i in range(len(seq)):
            seq[i] = val[i]
            
    def sample(self, population, k, *, counts=None):
        if(not(counts)):
            counts = [1 for _ in population]
        val = list()
        for i in range(len(population)):
            for _ in range(counts[i]):
                val.append(population[i])
        self.shuffle(val)
        return val[:k]
    
    def uniform(self, a, b):
        return a + (b-a) * self.random()

    def binomialvariate(self, n=1, p=0.5):
        return sum([self.random() < p for i in range(n)])
    
    def triangular(self, low=0, high=1, mode=None):
        if(mode == None):
            mode = (high - low)/2
        c = (mode - low) / (high - low)
        u = self.random()
        if(u < c):
            return low + math.sqrt(u * (high - low) * (mode - low))
        else:
            return high - math.sqrt((1 - u) * (high - low) * (high - mode))
        
    def gammavariate(self, alpha, theta):
        n = int(alpha)
        delta = alpha - n
        gn = - sum([math.log(self.random()) for _ in range(n)])
        gd = 0
        if(delta > 0):
            eta = math.inf
            while(eta > math.pow(gd, 1 - delta) * math.exp(- gd)):
                u = self.random()
                v = self.random()
                w = self.random()
                if(u <= math.e / (math.e + delta)):
                    gd = math.pow(v, 1/delta)
                    eta = w * math.pow(gd, 1 - delta)
                else:
                    gd = 1 - math.log(v)
                    eta = w * math.exp(- gd)
                
        return theta * (gn + gd)
        
    def betavariate(self, alpha, beta):
        x = self.gammavariate(alpha, 1)
        y = self.gammavariate(beta, 1)
        return x / (x + y)
    
    def inv_erf_coeff(k):
        if(k in LFSRRand.inv_erf_coeff_dict):
            return LFSRRand.inv_erf_coeff_dict[k]
        elif(k <= 1):
            LFSRRand.inv_erf_coeff_dict[k] = 1
            return 1
        else:
            y = 0
            for m in range(k):
                y += LFSRRand.inv_erf_coeff(m) * LFSRRand.inv_erf_coeff(k - 1 - m) / ((m + 1) * (2 * m + 1))
    
            LFSRRand.inv_erf_coeff_dict[k] = y
            return y
        
    def inv_erf(z):
        y = 0
        prec = 287
        sqrt_pi_two = math.sqrt(math.pi) / 2
        for k in range(prec):
            y += math.pow(z * sqrt_pi_two, 2 * k + 1) * LFSRRand.inv_erf_coeff(k) / (2 * k + 1)
        return y
    
    def normalvariate(self, mu=0.0, sigma=1.0):
        u = self.random()
        x = math.sqrt(2) * LFSRRand.inv_erf(2 * u - 1)
        return mu + sigma * x