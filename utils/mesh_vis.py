import open3d as o3d

# input_file = r'/home/yiting/Documents/Data/Shapes/stl_no_base/axial_component/axial_component_120.stl'
# input_file = r'/home/yiting/Documents/Data/Shapes/stl_no_base/sheet/sheet_030.stl'
input_file = r'/home/yiting/Documents/Data/Shapes/stl_no_base/torso/torso_085.stl'
mesh = o3d.io.read_triangle_mesh(input_file) 
o3d.visualization.draw_geometries([mesh])