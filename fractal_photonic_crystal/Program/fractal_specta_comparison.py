# -*- coding: cp1251 -*-
''''''
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

list_of_structures = ['PC2.csv',
                      'PC4.csv',
                      'PC6.csv',
                      'PC8.csv',
                      'PC10.csv',
                      'PC20.csv',
                      'PC100.csv']

legend_list = [r'$2$',
               r'$4$',
               r'$6$',
               r'$8$',
               r'$10$',
               r'$20$',
               r'$100$']

indices = {'air': '1+0.05792105/(238.0185-math.pow(x,-2))+0.00167917/(57.362-math.pow(x,-2))',
           'SiO2': 'math.sqrt(1+0.6961663/(1-math.pow(0.0684043/x, 2))+0.4079426/(1-math.pow(0.116241/x,2))+0.8974794/(1-math.pow(9.896161/x,2)))',
           'TiO2': 'math.sqrt(5.913+0.2441/(math.pow(x, 2)-0.0803))'}
materials = {'S':'SiO2', 'T':'TiO2'}

mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.unicode'] = True

AAA = 5
BBB = 1
label_position = 60
k_bottom = None

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

def structures_plot(list_of_structures):
    number_of_structures = len(list_of_structures)
    plt.rc('text', usetex=True)
    fig, axs = plt.subplots(number_of_structures, 1, sharex=True, sharey=True, figsize=(AAA, BBB*number_of_structures))
    fig.subplots_adjust(hspace=0.000, bottom=k_bottom)
    for i, structure_file in enumerate(list_of_structures):
        f = open(structure_file, 'rb')
        reader = csv.reader(f, delimiter=';', lineterminator='\n')
        structure_list = list(reader)
        structure = []
        structure.append('air')
        structure.append(1.0)
        while structure_list:
            structure.append(structure_list[0][0])
            structure.append(round(float(structure_list[0][1].replace(',', '.')), 3))
            structure_list = structure_list[1:]
        structure.append('air')
        structure.append(1.0)
        f.close()
        structure_name = structure_file[:-4]

        R_list = []
        for wl in wl_range:
            a = M(structure, wl)[0, 0]
            b = M(structure, wl)[0, 1]
            c = M(structure, wl)[1, 0]
            d = M(structure, wl)[1, 1]
            r = -c/d
            R = np.abs(r)**2
            R_list.append(100*R)

        k = 10000/wl_range
        axs[i].yaxis.set_ticks(np.arange(0, 99, 50))
        axs[i].set_ylabel(r'$R$, $\%$', fontsize=12)
        axs[i].plot(k, R_list, label=legend_list[i])
        axs[i].text(min(k), label_position, legend_list[i])
    plt.xlabel(r'$k$, $1/{cm}$', fontsize=12)
    plt.savefig('figure.pdf')
    plt.show()

wl_range = np.linspace(0.4, 1.5, num=1000)
structures_plot(list_of_structures)
