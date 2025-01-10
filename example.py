import generate_surface_meshes as gsm

input_path = "/Users/ABC/Documents/BivMeshes" # change to input folder (containing SSM.h5 and mean_shape.vtk)
output_path = "/Users/ABC/Documents/BivMeshes/" # change to output path of choice
num_samples = 10 # change to the amount of meshes you want to create

gsm.generate_surface_mesh(input_path=input_path, output_path=output_path, num_samples=num_samples)