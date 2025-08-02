# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 12:57:01 2025

@author: bowto
"""



class BinaryTree:
    def __init__(self, compare=(lambda x, y: hash(x) < hash(y)), equiv=None):
        self.left = None
        self.right = None
        self.value = None
        self.compare = compare
        if(equiv == None):
            self.equiv = lambda x, y: not compare(x, y) and not compare(y, x)
        else:
            self.equiv = equiv
        
    def append(self, val, autobalance=True):
        if(self.value == None):
            self.value = val
        elif(self.equiv(val, self.value)):
            l = 0
            r = 0
            if(self.left != None):
                l = len(self.left)
            if(self.right != None):
                r = len(self.right)
            if(l < r):
                if(self.left == None):
                    self.left = BinaryTree(compare=self.compare)
                self.left.append(val)
            else:
                if(self.right == None):
                    self.right = BinaryTree(compare=self.compare)
                self.right.append(val)
        elif(self.compare(val, self.value)):
            if(self.left == None):
                self.left = BinaryTree(compare=self.compare)
            self.left.append(val)
        else:
            if(self.right == None):
                self.right = BinaryTree(compare=self.compare)
            self.right.append(val)
        if(autobalance):
            self.balance()
    
    def __len__(self):
        l = 0
        if(self.value != None):
            l += 1
        if(self.left != None):
            l += len(self.left)
        if(self.right != None):
            l += len(self.right)
        return l
    
    def __list__(self):
        l = []
        r = []
        if(self.left != None):
            l = list(self.left)
        if(self.right != None):
            r = list(self.right)
        if(self.value == None):
            return l + r
        else:
            return l + [self.value] + r
        
    def __iter__(self):
        for item in self.__list__():
            yield item
            
    def __str__(self):
        return f"<{self.left}-{self.value}-{self.right}>"

    def isBalanced(self):
        l = 0
        r = 0
        if(self.left != None):
            l = len(self.left)
        if(self.right != None):
            r = len(self.right)
        
        if (abs(l - r) > 1):
            return False
        elif(self.left != None and self.right != None):
                return (self.left.isBalanced() and self.right.isBalanced())
        else:
            return True
        
    def popLeftmost(self):
        if(self.left == None):
            v = self.value
            if(self.right == None):
                self.value = None
            else:
                r = self.right 
                self.value = r.value
                self.left = r.left
                self.right = r.right
            return v
        else:
            return self.left.popLeftmost()
    
    def popRightmost(self):
        if(self.right == None):
            v = self.value
            if(self.left == None):
                self.value = None
            else:
                l = self.left 
                self.value = l.value
                self.left = l.left
                self.right = l.right
            return v
        else:
            return self.right.popRightmost()
     
    def push(self, T):
        if(T == None or T.value == None):
            return
        elif(self.equiv(T.value, self.value)):
            l = 0
            r = 0
            if(self.left != None):
                l = len(self.left)
            if(self.right != None):
                r = len(self.right)
            if(l < r):
                if(self.left == None):
                    self.left = T
                    return
                else:
                    return self.left.push(T)
            else:
                if(self.right == None):
                    self.right = T
                    return
                else:
                    return self.right.push(T)
        elif(self.compare(T.value, self.value)):
            if(self.left == None):
                self.left = T
                return
            else:
                return self.left.push(T)
        else:
            if(self.right == None):
                self.right = T
                return
            else:
                return self.right.push(T)

    def remove(self, value):
        if(self.value == None):
            return None
        if(self.equiv(value, self.value)):
            v = self.value
            l = self.left
            r = self.right
            if(l == None):
                if(r == None):
                    self.value = None
                else:
                    self.value = r.value
                    self.left = r.left
                    self.right = r.right
            elif(r == None):
                self.value = l.value
                self.left = l.left
                self.right = l.right
            else:
                r.push(l)
                self.value = r.value
                self.left = r.left
                self.right = r.right
            self.balance()
            return v
        elif(self.compare(value, self.value)):
            if(self.left == None):
                return None
            else:
                return self.left.remove(value)
        else:
            if(self.right == None):
                return None
            else:
                return self.right.remove(value)
        
    def __getitem__(self, value):
        if(self.value == None):
            return None
        if(self.equiv(value, self.value)):
            return self.value
        elif(self.compare(value, self.value)):
            if(self.left == None):
                return None
            else:
                return self.left.__getitem__(value)
        else:
            if(self.right == None):
                return None
            else:
                return self.right.__getitem__(value)
            
    def __in__(self, value):
        return value == self.__getitem__(value)
    
    def balance(self):
        l = 0
        r = 0
        if(self.left != None):
            l = len(self.left)
        if(self.right != None):
            r = len(self.right)
        
        while((abs(l - r) > 1)):
            if r > l:
                val = self.value
                right = self.right
                left = self.left
                
                right.append(val, autobalance=False)
                right.push(left)
                
                self.value = right.value
                self.right = right.right
                self.left = right.left
                
            else:
                val = self.value
                right = self.right
                left = self.left
                
                left.append(val, autobalance=False)
                left.push(right)
                
                self.value = left.value
                self.right = left.right
                self.left = left.left
            
            if(self.left != None):
                l = len(self.left)
            else:
                l = 0
            if(self.right != None):
                r = len(self.right)
            else:
                r = 0
                
        if(self.left != None):
            self.left.balance()
        if(self.right != None):
            self.right.balance()
            
class dictionary():
    def __init__(self):
        self.data = BinaryTree(compare=lambda x,y:x[0] < y[0])
    
    def __setitem__(self, key, value):
        g = self.data.__getitem__([hash(key), [key, value]])
        if(g == None):
            self.data.append([hash(key), [key, value]])
        else:
            found = False
            for x in g[1:]:
                if x[0] == key:
                    found = True
                    x.remove(x[1])
                    x.append(value)
            if not found:
                g.append([key, value])
    
    def __getitem__(self, key):
        g = self.data.__getitem__([hash(key), [key, None]])
        if(g == None):
            raise KeyError(key)
        else:
            found = False
            for x in g[1:]:
                if x[0] == key:
                    found = True
                    return x[1]
            if not found:
                raise KeyError(key)
                
    def __str__(self):
        items = [x[1:] for x in list(self.data)]
        items = sum(items, [])
        items = [f"{x[0]}: {x[1]}" for x in items]
        items = "{" + ', '.join(items) + "}"
        return items

d = dictionary()

d[15] = 2
d[-2] = 30
d[-1] = 99
d[15] = 5

print(d)
print(d[-2])
print(d[-1])

d = dict()

d[15] = 2
d[-1] = 99
d[-2] = 30
d[15] = 5

print(d)
print(d[-2])
print(d[-1])
