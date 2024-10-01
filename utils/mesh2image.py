import numpy as np
import trimesh
import pyrender
import matplotlib.pyplot as plt
import scipy
import cv2
import os

def render_mesh_to_image(stl_file_path, png_file_path):
    # Setting
    resolution=(1920, 1080)

    # Load the STL file
    mesh = trimesh.load(stl_file_path)

    # Create a Pyrender mesh
    pyrender_mesh = pyrender.Mesh.from_trimesh(mesh)

    # Create a Pyrender scene and add the mesh
    scene = pyrender.Scene()
    scene.add(pyrender_mesh)

    ### Set up the camera ###
    # Camera pose explained:
    # +X axis is towards the right of the screen
    # +Y axis is towards the top of the screen
    # -Z axis points into the screen (camera looks into the screen)
    yfov = np.pi / 4.0
    ywidth = 120  # mm
    camera_pose = np.eye(4)
    camera_pose[2, 3] = (
        ywidth / 2 / np.tan(yfov / 2)
    )  # Calculate correct distance for camera to have ywidth and yfov
    camera = pyrender.PerspectiveCamera(yfov=yfov)
    scene.add(camera, pose=camera_pose)

    ### Add a light source ###
    # Directional light
    light_euler = np.array([-np.pi / 4, 0, 0])
    R = scipy.spatial.transform.Rotation.from_euler("xyz", light_euler).as_matrix()
    light_pose = np.eye(4)
    light_pose[:3, :3] = R
    light = pyrender.DirectionalLight(color=[1, 1, 1], intensity=2.5e3)
    scene.add(light, pose=light_pose)

    # Create a renderer
    r = pyrender.OffscreenRenderer(resolution[0], resolution[1])
    color, _ = r.render(scene)

    cv2.imwrite(png_file_path, color)

if __name__ == "__main__":

    ### Setting ###
    main_dir = r'/home/yiting/Documents/Data/Shapes'
    # Get the mesh (stl) folder path
    mesh_file_path = os.path.join(main_dir, 'stl')
    # Get the category folders
    category_folders = os.listdir(mesh_file_path)
    # Get the output (png) folder path
    output_dir = r'/home/yiting/Documents/Shape_analysis/3d_to_2d'

    for cat in category_folders:
        # input path
        stl_category_path = os.path.join(main_dir, 'stl', cat)
        stl_files = os.listdir(stl_category_path)
        # output path
        png_category_path = os.path.join(output_dir, cat)
        os.makedirs(png_category_path, exist_ok = True)

        for stl in stl_files:
            stl_file_path = os.path.join(stl_category_path, stl)
            # Get file name
            root, ext = os.path.splitext(stl)
            png_file_path = os.path.join(png_category_path, f"{root}.png")
            render_mesh_to_image(stl_file_path, png_file_path)


