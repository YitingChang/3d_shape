import numpy as np
import os
import open3d as o3d

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

# Get the input mesh (stl) folder
input_folder_dir = os.path.join(main_dir, 'stl_no_base')
# Get the category folders
category_folders = os.listdir(input_folder_dir)
# Create an output point cloud (ply) folder
output_folder_dir = os.path.join(main_dir, f"ply_{num_points}_no_base")
os.makedirs(output_folder_dir, exist_ok = True)

for cat in category_folders:
    # input
    input_category_dir = os.path.join(input_folder_dir, cat)
    # output
    output_category_dir = os.path.join(output_folder_dir,cat)
    os.makedirs(output_category_dir, exist_ok = True)
    input_files = os.listdir(input_category_dir)
    for input in input_files:
        mesh = o3d.io.read_triangle_mesh(os.path.join(input_category_dir, input))
        # Function to uniformly sample points from the mesh.
        pcd = mesh.sample_points_uniformly(number_of_points=num_points)
        # Get file name
        root, ext = os.path.splitext(input)
        # Save the point cloud in PLY format
        o3d.io.write_point_cloud(os.path.join(output_category_dir, f"{root}.ply"), pcd)




