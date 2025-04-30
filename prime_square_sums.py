# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:41:56 2024

@author: bowto
"""
from functools import reduce

def triangular(n:int):
    return int(n * (n+1) / 2)

primes = [2]

def prime(n:int):
    x = len(primes)
    while len(primes) <= n:
        if x not in primes and x >= 2 and reduce((lambda a, b: a and b), map(lambda p: x % p > 0, primes)):
            primes.append(x)
        x += 1
    return primes[n]

def prime_factor(x:int):
    if(x == 0):
        return None
    elif(x < 0):
        result = prime_factor(-x)
        if(len(result.keys())>0):
            k = list(result.keys())[0]
            inc_dict(result, -k)
            inc_dict(result, k, count=-1)
        return result
    else:
        factors = dict()
        i = 0
        while x > 1:
            p = prime(i)
            if(x % p == 0):
                inc_dict(factors, p)
                x = x / p
            else:
                i += 1
        return factors

def isSquareSum(x:int):
    if(x == 0):
        return True
    elif(x < 0):
        return False
    else:
        factors = prime_factor(x)
        for p in factors:
            if(p % 4 == 3 and factors[p] % 2 != 0):
                return False
        return True

def unfactor(factors:dict):
    x = 1
    for p in factors:
        x *= pow(p, factors[p])
    return x

def inc_dict(d, key, count=1):
    if(key not in d):
        d[key] = 0
    d[key] += count
    if(d[key] == 0):
        del d[key]

def norm(x:complex):
    return int_pow(x.real, 2) + int_pow(x.imag, 2)

def gint(x:complex):
    return complex(int(round(x.real)), int(round(x.imag)))

def divides(p, x):
    q = x / p
    q = gint(q)
    return x == (p * q)

def gcd(a:complex, b:complex):
    if(norm(b) > norm(a)):
        return gcd(b, a)
    q = a / b
    q = gint(q)
    r = a - (q * b)
    if(r != 0):
        return gcd(b, r)
    else:
        return b
def int_pow(base:int, exp:int):
    if(isinstance(base, int) and isinstance(exp, int)):
        r = 1
        for i in range(exp):
            r *= base
        return r
    else:
        return int_pow(int(base), int(exp))

def gauss_factor(x:complex):
    d = gauss_factor_raw(x)
    n = dict()
    unit = 1
    for p in d:
        if(norm(p) == 1):
            unit *= pow(p, d[p])
        else:
            inc_dict(n, p, count=d[p])     
    if(len(n) > 0):
        k = list(n.keys())[0]
        inc_dict(n, gint(k * unit))
        inc_dict(n, k, count=-1)
    else:
        inc_dict(n, gint(unit))    
    return n

def gauss_factor_raw(x:complex):
    result = dict()
    if(not isinstance(x, complex)):
        return gauss_factor_raw(complex(x, 0))
    elif(x == complex(0,0)):
        return result
    elif(x.imag == 0):
        f = prime_factor(int(x.real))
        for p in f:
            if(p % 4 == 3):
                inc_dict(result, complex(p,0), count=f[p])
            elif(p == 2):
                inc_dict(result, complex(1,1), count=f[p])
                inc_dict(result, complex(1,-1), count=f[p])
            else:
                k = 0
                for n in range(2, p - 1):
                    if (int_pow(n, (p-1)/2) % p == (-1 % p)):
                        k = int_pow(n, (p-1)/4)
                        break
                q = gcd(complex(p,0), complex(k, 1))
                if(norm(q) == 1):
                   q = gcd(complex(p,0), complex(k, -1))
                inc_dict(result, q, count=f[p])
                inc_dict(result, gint(p/q), count=f[p])       
    elif(x.real == 0):
        result = gauss_factor_raw(complex(x.imag, 0))
        inc_dict(result, complex(0,1))
    else:
        g = gint(gcd(x.real, x.imag))
        if(norm(g) != 1):
            g_factors = gauss_factor_raw(g)
            p_factors = gauss_factor_raw(gint(x / g))
            for p in g_factors:
                inc_dict(result, p, count=g_factors[p])
            for p in p_factors:
                inc_dict(result, p, count=p_factors[p])
        else:
            f = gauss_factor_raw(int(norm(x)))
            val = complex(x.real, x.imag)
            for p in f:
                if(norm(p) != 1):
                    while divides(p, val):
                        inc_dict(result, p)
                        val = gint(val / p)
                        
            if(norm(val) != 1):
                inc_dict(result, val)
            elif(val != complex(1, 0)):
                if(len(result.keys())>0):
                    k = list(result.keys())[0]
                    inc_dict(result, gint(k * val))
                    inc_dict(result, k, count=-1)
                
    return result

#returns (sqrt(square part), square-free part)
def splitup(x:int):
    if(x == 0):
        return (0, 0)
    elif(x < 0):
        (y, z) = splitup(-x)
        return (y, -z)
    else:
        factors = prime_factor(x)
        f = dict()
        g = dict()
        for p in factors:
            if(factors[p] % 2 == 0):
                f[p] = int(factors[p] / 2)
            else:
                g[p] = 1
                ex = int((factors[p] - 1)/2)
                if(ex > 0):
                    f[p] = ex
        return(unfactor(f), unfactor(g))


def pretty_str(d:dict):
    r = ""
    for k in d:
        if(d[k] == 1):
            r += f"{k}, "
        else:
            r += f"{k}^{d[k]}, "
    return "[" + r[:-2] + "]"

print(gauss_factor(12181))

for i in range(1000):
    x = triangular(i)
    if(isSquareSum(x)):
        (y, z) = splitup(x)
        if(z == 0 or z == 1):
            print(f"{x} = {y}^2")
        else:
            print(f"{x} = {y}^2 * prod{pretty_str(gauss_factor(z))}")

