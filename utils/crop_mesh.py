import open3d as o3d
import numpy as np
import os

def crop_mesh(input_file, output_file):

    # Load the mesh
    mesh = o3d.io.read_triangle_mesh(input_file)  
    mesh.compute_vertex_normals()

    # Define a 3D bounding box for cropping
    bounding_box = o3d.geometry.AxisAlignedBoundingBox(min_bound=np.array([-20, -20, -2]),
                                                    max_bound=np.array([50, 50, 50]))

    # Crop the mesh using the bounding box
    cropped_mesh = mesh.crop(bounding_box)

    # # Visualize the cropped mesh (optional)
    # o3d.visualization.draw_geometries([cropped_mesh])

    # Save the cropped mesh
    o3d.io.write_triangle_mesh(output_file, cropped_mesh)

if __name__ == "__main__":

    ### Setting ###
    main_dir = r'/home/yiting/Documents/Data/Shapes'
    # Get the input mesh (stl) folder path
    input_folder_dir = os.path.join(main_dir, 'stl')
    # Get the category folders
    category_folders = os.listdir(input_folder_dir)
    # Get the output (png) folder path
    output_folder_dir = os.path.join(main_dir, 'stl_no_base')

    for cat in category_folders:
        # input path
        input_category_dir = os.path.join(input_folder_dir, cat)
        input_files = os.listdir(input_category_dir)
        # output path
        output_category_dir = os.path.join(output_folder_dir, cat)
        os.makedirs(output_category_dir, exist_ok = True)

        for input in input_files:
            input_file_path = os.path.join(input_category_dir, input)
            # Get file name
            root, ext = os.path.splitext(input)
            output_file_path = os.path.join(output_category_dir, f"{root}.stl")
            crop_mesh(input_file_path, output_file_path)
