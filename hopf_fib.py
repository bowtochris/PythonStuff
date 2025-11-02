# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 16:25:28 2025

@author: bowto
"""

import scipy.spatial.transform
import math
import cmath
import matplotlib.pyplot as plt
import numpy as np
import random 
import colorsys 
from mpl_toolkits.mplot3d import axes3d
import imageio 
from pygifsicle import optimize

def dist(u, v):
    d = 0
    for i in range(3):
        d += (v[i] - u[i]) ** 2
    d = math.sqrt(d)
    return d  

def colorize(v, pov):
    d = dist(v, pov)
    d = d / (2 * math.sqrt(3))
    h = dist(v, [0, 0, 0]) / math.sqrt(3)
    c = colorsys.hsv_to_rgb(h, 1.0, 1 - d)
    c = [c[0], c[1], c[2], 0.5]
    c = [max(0, min(1, x)) for x in c]
    return c

def Hopf(x:complex, y:complex) -> tuple[complex, float]:
    z : complex = 2 * x * y.conjugate()
    w : float = (abs(x) ** 2) - (abs(y) ** 2)
    return (z, w)

def Hopf_points(a, b, c, d):
    x = complex(a, b)
    y = complex(c, d)
    z, w = Hopf(x, y)
    return (z.real, z.imag, w)

gif_path = "hopf.gif"
size = [200, 36, 100, 100]
c = [colorsys.hsv_to_rgb(k/360, 1.0, 0.5) for k in range(360)]
with imageio.get_writer(gif_path, mode='I', loop=0) as writer:
    for i in range(size[0]):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        ax.set_zlim(-2, 2)
        j = i * (size[1] / size[0])
        theta = np.linspace(0, 2*np.pi, size[2])
        phi = np.linspace(0, np.pi, size[3])
        
        psi = 2 * i * np.pi / size[0]
        eta = j * np.pi / size[1]
        
        theta, phi = np.meshgrid(theta, phi)
        
        x = np.cos(psi) * np.sin(phi)
        y = np.sin(psi)
        z = np.cos(theta) * np.sin(eta)
        w = np.sin(theta)
        
        a = x + 1j * y
        b = z + 1j * w
        
        Hz = 2 * a * np.conj(b)
        Hw = ((np.abs(a) ** 2) - (np.abs(b) ** 2)).real
        ax.plot_wireframe(Hz.real, Hz.imag, Hw, color=c)
        fpath = f"hopf/img_{i}.png"
        plt.savefig(fpath)
        writer.append_data(imageio.imread(fpath))
        plt.clf()
        plt.close()
        del ax
        del fig
        
optimize(gif_path)


    