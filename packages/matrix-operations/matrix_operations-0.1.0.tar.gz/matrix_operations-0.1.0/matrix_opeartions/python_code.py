import math
import numpy as np

class MatrixOperations:
    def __init__(self):
        pass
    
    def zeros(self, m=0, n=0):
        matrix=[]
        for i in range(m):
            ele=[]
            for j in range(n):
                ele.append(0)
            matrix.append(ele)
        return matrix
    
    def add(self, a, b):
        a=np.array(a)
        b=np.array(b)
        z=self.zeros(a.shape[0], b.shape[1])
        k=a.shape[0]
        for i in range(k):
            for j in range(k):
                z[i][j] = a[i][j] + b[i][j]
        return z
    
    def sub(self, a, b):
        a=np.array(a)
        b=np.array(b)
        z=self.zeros(a.shape[0], b.shape[1])
        k=a.shape[0]
        for i in range(k):
            for j in range(k):
                z[i][j] = a[i][j] - b[i][j]
        return z
    
    def mul(self, a, b):
        a=np.array(a)
        b=np.array(b)
        z=self.zeros(a.shape[0], b.shape[1])
        k=a.shape[0]
        for i in range(k):
            for j in range(k):
                z[i][j] = a[i][j] * b[i][j]
        return z
    
    def div(self, a, b):
        a=np.array(a)
        b=np.array(b)
        z=self.zeros(a.shape[0], b.shape[1])
        k=a.shape[0]
        for i in range(k):
            for j in range(k):
                z[i][j] = a[i][j] / b[i][j]
        return z
    
    def dot(self, a, b):
        return np.dot(a,b)
    
    def identity(self, m=0, n=0):
        matrix=[]
        for i in range(m):
            ele=[]
            for j in range(n):
                if i==j:
                    ele.append(1)
                else:
                    ele.append(0)
            matrix.append(ele)    
        return matrix           
    
    def fill_matrix(self, m, n, num=0):
        matrix=[]
        for i in range(m):
            ele=[]
            for j in range(n):
                ele.append(num)
            matrix.append(ele)
        return matrix
    