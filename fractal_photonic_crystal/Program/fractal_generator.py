#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Изменение параметров - по 3-5 картинок - программно, изображение структуры - мелкая врезка
- STS -> STTS -> STTTS и т.д.
- Обратная вставка SSTSS и т.д. - остается малая прослойка по Т
- STS/TST - попеременная замена
- разный размер структуры
- STSTSTST - это частный случай фрактальной замены, где T не масштабируется в размерах
- сравнить с фотонным кристаллом с таким же количеством слоев и наименьшим размером от фрактального кристалла либо промежуточный вариант относительно разбиения
- идея для практики - применение в лазерах с несколькими гармониками - частоты идут друг за другом, подобрать случай
- форма кривых - чему соответствует?
- случай, когда структуры следуют друг за другом
-!!! Половина структуры - разделить пополам фрактал
- Исходное слово отличается от замены
'''

materials = {'S':'SiO2', 'T':'TiO2'}

import pprint
import math
import numpy as np
import csv

wl_range = np.linspace(0.4, 2.0, num=2000)

import pprint
def paste_technique(phrase, letter1, letter2, thickness, number):
    '''1st letter for scale, 2nd - for fractal'''
    length = len(phrase)
    word = phrase
    for i in range(number):
        phrase = phrase.replace(letter1, letter1*length) # change letter without scaling
        phrase = phrase.replace(letter2, word)
    length = len(phrase)                                 # size of fractal word
    step = thickness/length                              # size of the smallest part
    parts = []
    thicknesses = []
    while True:
        position1 = phrase.find(letter1)
        position2 = phrase.find(letter2)
        position = max(position1, position2)
        if position == 0:
            segment = phrase[position]
            parts.append(segment)
            thicknesses.append(step*len(segment))
            break
        segment = phrase[:position]
        parts.append(segment)
        phrase = phrase[position:]
        thicknesses.append(step*len(segment))
    layers = []
    for part in parts:
        layers.append(materials[part[0]])
    structure = []
    for (layer, thickness) in zip(layers, thicknesses):
        structure.append(layer)
        structure.append(thickness)
    return structure

def paste_technique2(phrase, letter1, letter2, step, number):
    '''1st letter for scale, 2nd - for fractal'''
    length = len(phrase)
    word = phrase
    for i in range(number):
        phrase = phrase.replace(letter1, letter1*length) # change letter without scaling
        phrase = phrase.replace(letter2, word)
    print phrase
    parts = []
    thicknesses = []
    while True:
        position1 = phrase.find(letter1)
        position2 = phrase.find(letter2)
        position = max(position1, position2)
        if position == 0:
            segment = phrase[position]
            parts.append(segment)
            thicknesses.append(step*len(segment))
            break
        segment = phrase[:position]
        parts.append(segment)
        phrase = phrase[position:]
        thicknesses.append(step*len(segment))
    layers = []
    for part in parts:
        layers.append(materials[part[0]])
    structure = []
    for (layer, thickness) in zip(layers, thicknesses):
        structure.append(layer)
        structure.append(thickness)
    return structure

'''structure = paste_technique('TSST', 'T', 'S', 1.0, 4)
pprint.pprint(structure)'''

list_of_files = ['STS1.csv',
                 'STS2.csv',
                 'STS3.csv',
                 'STS4.csv',
                 'STS5.csv']

'''for (i, file_name) in enumerate(list_of_files):
    structure = paste_technique('STTS', 'T', 'S', 1.0, i)
    f = open(list_of_files[i], "w+")
    writer = csv.writer(f, delimiter=';', lineterminator='\n')
    structure_list = []
    while structure:
        structure_list.append([structure[:2][0], str(structure[:2][1]).replace('.', ',')])
        structure = structure[2:]
    writer.writerows(structure_list) 
    f.close()'''

for (i, file_name) in enumerate(list_of_files):
    structure = paste_technique2('STS', 'T', 'S', 0.2, i)
    f = open(list_of_files[i], "w+")
    writer = csv.writer(f, delimiter=';', lineterminator='\n')
    structure_list = []
    while structure:
        structure_list.append([structure[:2][0], str(structure[:2][1]).replace('.', ',')])
        structure = structure[2:]
    writer.writerows(structure_list) 
    f.close()
