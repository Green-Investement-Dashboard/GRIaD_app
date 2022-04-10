#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:11:42 2021

@author: Clement
"""
import os 
import numpy

def list_dir_files (current):
        file_path = os.path.normcase(f'{current}')
        list_subdirr = []
        list_files = []
        for root, dirs, files in os.walk(file_path):
            list_subdirr.append(dirs)
            list_files.append(files)
            
        list_files = list(numpy.concatenate(list_files).flat)
        list_subdirr = list(numpy.concatenate(list_subdirr).flat)
        return list_subdirr, list_files
    
def id_shp (list_files):
    list_shp = []
    for files in list_files:
        split = files.split('.')
        if split [1] == 'shp':
            list_shp.append(files)
            
    return list_shp
            
def split_shp(list_shp, town, dpt):
    final_list = []
    for shp_file in list_shp:
        split1 = shp_file.split(town)
        split2 = split1[1].split(dpt)
        
        final_list.append([split1[0], split2[0], split2[1]])
    print(final_list)    
    return final_list
    

    
current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

dpt = str(34).zfill(3)
town = 'montpellier'

list_subdirr,list_files = list_dir_files (current)
list_shp  = id_shp (list_files)
final_list = split_shp(list_shp, town, dpt)