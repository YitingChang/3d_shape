# Concatenate ply data for each vh_object and create a label
# Category labels: axial components = 1, torso = 2, sheet = 3.

import os
from plyfile import PlyData
import h5py
import numpy as np


def mesh_preprocess(input_file_path):
    # Load PLY file
    ply_data = PlyData.read(input_file_path)

    # Extract vertex data (assuming the PLY file has 'x', 'y', 'z' coordinates)
    vertex_data = ply_data['vertex'].data

    # Convert vertex coordinates to a NumPy array
    vertices = np.vstack([vertex_data['x'], vertex_data['y'], vertex_data['z']]).T

    # Check if the PLY file contains normal vectors ('nx', 'ny', 'nz')
    if 'nx' in vertex_data.dtype.names and 'ny' in vertex_data.dtype.names and 'nz' in vertex_data.dtype.names:
        normals = np.vstack([vertex_data['nx'], vertex_data['ny'], vertex_data['nz']]).T
    else:
        normals = None
        print("The PLY file does not contain normal vectors.")

    # Get label (axial_component = 1, torso = 2, sheet = 3)
    category = input.split('_')[0]
    if category == 'axial':
        label = 1
    elif category == 'torso':
        label = 2
    elif category == 'sheet':
        label = 3
    else:
        print('Not in any category')
    return vertices, label, normals

# Write numpy array data and label to h5_filename
def save_h5(h5_filename, data, label, normal, name, data_dtype='uint8', label_dtype='uint8', normal_dtype='uint8', name_dtype='S25'):
    h5_fout = h5py.File(h5_filename, "w")
    h5_fout.create_dataset(
            'data', data=data,
            compression='gzip', compression_opts=4,
            dtype=data_dtype)
    h5_fout.create_dataset(
            'label', data=label,
            compression='gzip', compression_opts=1,
            dtype=label_dtype)
    h5_fout.create_dataset(
            'normal', data=normal,
            compression='gzip', compression_opts=4,
            dtype=normal_dtype)
    
    # Convert Unicode strings to byte strings before saving
    name_bytes = np.array([n.encode('utf-8') for n in name], dtype=name_dtype)

    h5_fout.create_dataset(
            'name', data=name_bytes,
            compression='gzip', compression_opts=4,
            dtype=name_dtype)
    h5_fout.close()


if __name__ == "__main__":

    ### Setting ###
    # Get input mesh (stl) folder path
    input_folder_dir = r'/home/yiting/Documents/Data/Shapes/ply_1024_no_base'
    # Get the category folders
    category_folders = os.listdir(input_folder_dir)
    # Get the output dir
    output_dir = r'/home/yiting/Documents/GitHub/dgcnn.pytorch/data/vhObject_ply_hdf5_1024'

    for cat in category_folders:
        # input path
        input_category_dir = os.path.join(input_folder_dir, cat)
        input_files = os.listdir(input_category_dir)
        # output
        data_all = []
        label_all = []
        normal_all = []
        name_all = []
        file_name = f"ply_data_{cat}.h5"

        for input in input_files:
            input_file_path = os.path.join(input_category_dir, input)
            vertices, label, normals = mesh_preprocess(input_file_path)
            name, ext = os.path.splitext(input)

            # Append the data to lists
            data_all.append(vertices)
            label_all.append(label)
            normal_all.append(normals)
            name_all.append(name)

        # Convert lists to NumPy arrays
        data_all = np.array(data_all)  # Shape: (X, N, 3) where X is the number of ply objects and N is the number of vertices in each PLY
        label_all = np.array(label_all) 
        name_all = np.array(name_all)

        # If normal_all is not empty, concatenate into a NumPy array
        normal_all = np.array(normal_all) if normal_all else None  # Shape: (X, N, 3) if normals are present

        h5_file_path = os.path.join(output_dir, file_name)
        save_h5(h5_file_path, data_all, label_all, normal_all, name_all)
        print(f"Saved: {h5_file_path}")

