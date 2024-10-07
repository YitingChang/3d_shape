
"""

The backbone of this script was from dgcnn.pytorch. 
Here, it wasmodified to load vh_Object data and create a DataLoader class.

"""

import os
import sys
import glob
import h5py
import numpy as np
import torch
import json
import cv2
import pickle
from torch.utils.data import Dataset


def load_data_cls(partition):
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # DATA_DIR = os.path.join(BASE_DIR, 'data')
    DATA_DIR = r'/home/yiting/Documents/Shape_analysis/dgcnn_vh/data'
    all_data = []
    all_label = []
    for h5_name in glob.glob(os.path.join(DATA_DIR, 'modelnet40_ply_hdf5_2048', '*%s*.h5'%partition)):
        f = h5py.File(h5_name, 'r+')
        data = f['data'][:].astype('float32')
        label = f['label'][:].astype('int64')
        f.close()
        all_data.append(data)
        all_label.append(label)
    all_data = np.concatenate(all_data, axis=0)
    all_label = np.concatenate(all_label, axis=0)
    return all_data, all_label

def load_data_vh(vh_cat):
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # DATA_DIR = os.path.join(BASE_DIR, 'data')
    DATA_DIR = r'/home/yiting/Documents/Shape_analysis/dgcnn_vh/data'
    h5_name = os.path.join(DATA_DIR, 'vhObject_ply_hdf5_1024', f"ply_data_{vh_cat}.h5")
    f = h5py.File(h5_name, 'r+')
    data_all = f['data'][:].astype('float32')
    label_all = f['label'][:].astype('int64')
    name_all = f['name'][:].astype('str')

    return data_all, label_all, name_all 

def translate_pointcloud(pointcloud):
    xyz1 = np.random.uniform(low=2./3., high=3./2., size=[3])
    xyz2 = np.random.uniform(low=-0.2, high=0.2, size=[3])
       
    translated_pointcloud = np.add(np.multiply(pointcloud, xyz1), xyz2).astype('float32')
    return translated_pointcloud


def jitter_pointcloud(pointcloud, sigma=0.01, clip=0.02):
    N, C = pointcloud.shape
    pointcloud += np.clip(sigma * np.random.randn(N, C), -1*clip, clip)
    return pointcloud


def rotate_pointcloud(pointcloud):
    theta = np.pi*2 * np.random.uniform()
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    pointcloud[:,[0,2]] = pointcloud[:,[0,2]].dot(rotation_matrix) # random rotation (x,z)
    return pointcloud


class ModelNet40(Dataset):
    def __init__(self, num_points, partition='train'):
        self.data, self.label = load_data_cls(partition)
        self.num_points = num_points
        self.partition = partition        

    def __getitem__(self, item):
        pointcloud = self.data[item][:self.num_points]
        label = self.label[item]
        if self.partition == 'train':
            pointcloud = translate_pointcloud(pointcloud)
            np.random.shuffle(pointcloud)
        return pointcloud, label

    def __len__(self):
        return self.data.shape[0]
    

class vhObject(Dataset):
    def __init__(self, vh_cat, num_points):
        self.data, self.label, self.name = load_data_vh(vh_cat)
        self.num_points = num_points

    def __getitem__(self, item):
        pointcloud = self.data[item][:self.num_points]
        label = self.label[item]
        name = self.name[item]
        return pointcloud, label, name

    def __len__(self):
        return self.data.shape[0]
    
