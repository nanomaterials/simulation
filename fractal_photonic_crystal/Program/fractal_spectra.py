#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
#import sys

#reload(sys)  
#sys.setdefaultencoding('cp1251')    # Для правильной работы с сохранением папок в русскоязычном Windows
#from pylab import *
#rc('font',**{'family':'verdana'}) # Шрифт verdana содержит символы русского алфавита

indices = {'air': '1*x/x',
           'SiO2': 'math.sqrt(1+0.6961663/(1-math.pow(0.0684043/x, 2))+0.4079426/(1-math.pow(0.116241/x,2))+0.8974794/(1-math.pow(9.896161/x,2)))',
           'TiO2': 'math.sqrt(5.913+0.2441/(math.pow(x, 2)-0.0803))'}
materials = {'S':'SiO2', 'T':'TiO2'}

material_flags = {'SiO2':0, 'TiO2':1}

import math
import numpy as np
import matplotlib.pyplot as plt

f = open('Fibonacci.csv', 'rb')
reader = csv.reader(f, delimiter=';', lineterminator='\n')
structure_list = list(reader)
structure = []
while structure_list:
    structure.append(structure_list[0][0])
    structure.append(round(float(structure_list[0][1].replace(',', '.')), 3))
    structure_list = structure_list[1:]
f.close()

def n(material, x):
    nL = lambda x: eval(indices[material])
    return nL(x)

def splitting(structure):
    materials = structure[0::2]
    thicknesses = structure[1::2]
    return materials, thicknesses

def A(wl, material_1, material_2):
    n1 = n(material_1, wl)
    n2 = n(material_2, wl)
    matrix_A = np.matrix([[n2+n1, n2-n1], [n2-n1, n2+n1]])/(2*n2)
    return matrix_A

def B(wl, material, L):
    nm = n(material, wl)
    matrix_B = np.matrix([[np.exp(2*np.pi*1j*nm*L/wl), 0], [0, np.exp(-2*np.pi*1j*nm*L/wl)]])
    return matrix_B

def M(structure, wl):
    materials = splitting(structure)[0]
    thicknesses = splitting(structure)[1]
    matrix_M = A(wl, materials[0], materials[1])
    for i in range(len(materials)-2):
        matrix_B = B(wl, materials[i+1], thicknesses[i+1])
        matrix_M = np.dot(matrix_M, matrix_B)
        matrix_A = A(wl, materials[i+1], materials[i+2])
        matrix_M = np.dot(matrix_M, matrix_A)
    return matrix_M

def R(structure):
    R_list = []
    for wl in wl_range:
        a = M(structure, wl)[0, 0]
        b = M(structure, wl)[0, 1]
        c = M(structure, wl)[1, 0]
        d = M(structure, wl)[1, 1]
        r = -c/d
        t = a + b/r
        R = np.abs(r)**2
        R_list.append(100*R)
    wl_range2 = 1000/wl_range
    plt.figure(figsize=(8,5))
    plt.xlabel(r'k, 1/cm')
    plt.ylabel(r'R, %')
    plt.axis([np.amin(wl_range2), np.amax(wl_range2), 0, np.amax(R_list)])
    plt.plot(wl_range2, R_list)

    # Another part for inset structure
    '''y = []
    x_lengthes = []
    struct = structure
    while struct:
        y.append(material_flags[struct[0]])
        x_lengthes.append(struct[1])
        struct = struct[2:]
    x_minima = np.add.accumulate(x_lengthes)
    x_max = max(x_minima)
    x_minima = np.insert(x_minima[:-1], 0, 0.0)
    xarrays = []
    for (minimum, length, k) in zip (x_minima, x_lengthes, y):
        if k == 1:
            xarrays.append((minimum, length))
    inset= plt.axes([0.15, 0.8, 0.2, 0.05])
    plt.broken_barh(xarrays, (0, 1), facecolors='grey')
    plt.xticks([])
    plt.yticks([])'''
    plt.show()

wl_range = np.linspace(0.4, 1.5, num=2000)
R(structure)
