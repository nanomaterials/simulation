#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

material_flags = {'SiO2':0,
                   'TiO2':1}

list_of_files = ['TST0.csv',
                 'TST1.csv',
                 'TST2.csv',
                 'TST3.csv',
                 'TST4.csv',
                 'TST5.csv']

for file_name in list_of_files:
    f = open(file_name, 'rb')
    reader = csv.reader(f, delimiter=';', lineterminator='\n')
    structure_list = list(reader)
    structure = []
    while structure_list:
        structure.append(structure_list[0][0])
        structure.append(float(structure_list[0][1].replace(',', '.')))
        structure_list = structure_list[1:]
    f.close()

    y = []
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

    fig, ax = plt.subplots(figsize=(10, 0.5))
    ax.broken_barh(xarrays, (0, 1), facecolors='grey')
    ax.set_xlim(0, x_max)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    plt.savefig('structure' + file_name[:-4]+'.pdf')
#plt.show()


