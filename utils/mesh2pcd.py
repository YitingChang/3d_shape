import numpy as np
import os

# Data structure
# Shapes/stl/axial_component/axia_component_000.stl
#                           /axia_component_001.stl
# Shapes/stl/sheet/sheet_000.stl
#                 /sheet_001.stl  
# Shapes/stl/torso/torso_000.stl
#                 /torso_001.stl  

### Setting ###
main_dir = r'/home/yiting/Documents/Data/Shapes'
num_points = 1024

# Get the mesh (stl) folder
mesh_file_path = os.path.join(main_dir, 'stl')
# Get the category folders
category_folders = os.listdir(mesh_file_path)
# Create a point cloud (ply) folder
os.makedirs(os.path.join(main_dir, 'ply'), exist_ok = True)

for cat in category_folders:
    # input
    stl_category_path = os.path.join(main_dir, 'stl',cat)
    # output
    ply_category_path = os.path.join(main_dir, 'ply',cat)
    os.makedirs(ply_category_path,exist_ok = True)
    mesh_files = os.listdir(stl_category_path)
    for me in mesh_files:
        mesh = o3d.io.read_triangle_mesh(os.path.join(stl_category_path,me))
        # Function to uniformly sample points from the mesh.
        pcd = mesh.sample_points_uniformly(number_of_points=num_points)
        # Get file name
        root, ext = os.path.splitext(me)
        # Save the point cloud in PLY format
        o3d.io.write_point_cloud(os.path.join(ply_category_path, root + '.ply'), pcd)




