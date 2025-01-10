"""
generate_surface_meshes.py

This script provides functions to load PCA components from an HDF5 file, sample new data points based on the PCA model,
and convert point clouds to surface meshes using VTK. The script is designed to facilitate the generation of synthetic surface
meshes from a biventricular statistical shape model.

Dependencies:
- numpy
- h5py
- os
- pathlib
- math
- vtk

Functions:
- load_h5py(input_path): Load PCA components, mean shape, explained variance from an HDF5 file.
- load_mean_vtk(input_path): Load mean shape in VTK format.
- sample(num_samples, num_components, explained_variance, boundary): Generate samples from a multivariate normal distribution
  based on the PCA model.
- pointcloud2surface(pointcloud, mesh): Create a surface mesh (VTK format) from a point cloud (numpy format), replicating the
  connectivity provided by an existing mesh.
- write_vtk_file(unstructured_grid, file_name): Write an unstructured grid to an ASCII VTK file.
- generate_synthetic_mesh(input_path, output_path, num_samples=1, num_components=94, boundary=-1): Load files, generate synthetic surface meshes and saves them to output directory in VTK format.

Usage:
1. Ensure that the required dependencies are installed.
2. Define the input and output paths, and possibly the number of samples to generate, the number of components to use, and the boundary for sampling.
3. Call the generate_synthetic_mesh function with the specified parameters.

"""


import numpy as np
import h5py
import os
from pathlib import Path
import math
import vtk

def load_h5py(input_path):
    """Load PCA components, mean shape, explained variance, and mean VTK data from an HDF5 file.
    Parameters:
    input_path (str): Path to the input folder.

    Returns:
    tuple: A tuple containing the following elements:
        - components (numpy.ndarray): PCA components.
        - mean (numpy.ndarray): Mean shape.
        - explained_variance (numpy.ndarray): Explained variance of each component.
        - mean_vtk (vtk.vtkUnstructuredGrid): Mean shape in VTK format.

    """
    with h5py.File(f"{input_path}/SSM.h5", "r") as f:
        components = f["components"][:]
        mean = f["mean"][:]
        explained_variance = f["explained_variance"][:]
    return components, mean, explained_variance

def load_mean_vtk(input_path):
    """Load the mean shape in VTK format from a file.
    Parameters:
    input_path (str): Path to the input folder.

    Returns:
    vtk.vtkUnstructuredGrid: Mean shape in VTK format.
    """
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(f"{input_path}/mean_shape.vtk")
    reader.Update()
    return reader.GetOutput()

def sample(num_samples, num_components, explained_variance, boundary):
    """Generate samples from a multivariate normal distribution based on the PCA model.
    Parameters:
    num_samples (int): Number of samples to generate.
    num_components (int): Number of PCA components to use. Should be less than 95 and larger than 0.
    explained_variance (numpy.ndarray): Explained variance of each component.
    boundary (float): Boundary value to clip the sampling at a fixed number of standard deviations from the mean. Use -1 for no clipping.

    Returns:
    samples (numpy.ndarray): Generated samples.
    """
    samples =  np.random.normal(0, 1, (num_samples, num_components))
    if boundary != -1:
        samples = np.clip(samples, -boundary, boundary)
    samples = samples * np.sqrt(explained_variance)
    return samples

def pointcloud2surface(pointcloud, mesh):
    """Create a surface mesh (VTK format) from a point cloud (numpy format), replicating the connectivity provided by 'mesh'.
    Parameters:
    pointcloud (numpy.ndarray): Point cloud data.
    mesh (vtk.vtkUnstructuredGrid): Existing VTK mesh to replicate connectivity.

    Returns:
    mesh (vtk.vtkUnstructuredGrid): Generated surface mesh.
    """
    if len(pointcloud.shape) != 2:
        pointcloud = np.reshape(pointcloud, (-1, 3))
    points = mesh.GetPoints()

    for pt_idx in range(points.GetNumberOfPoints()):
        pt = pointcloud[pt_idx]
        points.SetPoint(pt_idx, pt[0], pt[1], pt[2])

    return mesh

def write_vtk_file(unstructured_grid, file_name):
    """Write an unstructured grid to an ASCII VTK file.
    Parameters:
    unstructured_grid (vtk.vtkUnstructuredGrid): Unstructured grid data.
    file_name (str): Name of the output file.
    
    Returns:
    None
    """
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(file_name)
    writer.SetInputData(unstructured_grid)
    writer.SetFileTypeToASCII()
    writer.Write()

def generate_synthetic_mesh(input_path, output_path, num_samples=1, num_components=94, boundary=-1):
    """
    Generate and store synthetic surface meshes using PCA parameters stored in an HDF5 file.
    Parameters:
    input_path (str): Path to folder containing the input data (SSM.h5 and mean_shape.vtk).
    output_path (str): Path to the directory where the synthetic surface meshes will be saved.
    num_samples (int): Number of synthetic samples to generate. Should be larger than 0.
    num_components (int): Number of PCA components to use. Should be less than 95 and larger than 0.
    boundary (float): Boundary value to clip the sampling at a fixed number of standard deviations from the mean. Use -1 for no clipping.

    Returns:
    None
    """

    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist.")
        return False
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        
    if num_samples <= 0:
        print(f"Error: The number of samples to generate '{num_samples}' must be larger than 0.")
        return False
    
    if num_components >= 95 or num_components <= 0:
        print(f"Error: The number of components '{num_components}' must be smaller than 95 and larger than 0.")
        return False
    
    if not (-1 == boundary or (0 < boundary <= 5)):
        print(f"Error: The sampling boundary '{boundary}' must be -1 (no explicit boundary) or in the range ]0, 5].")
        return False

    # Load PCA parameters from HDF5
    components, mean, explained_variance = load_h5py(input_path)
    mean_vtk = load_mean_vtk(input_path)

    # reduce number of components to the specified number
    components, explained_variance = components[:num_components], explained_variance[:num_components]

    # Sample synthetic points in PCA space
    samples = sample(num_samples, num_components, explained_variance, boundary)

    # Transform to original space
    synthetic_pointclouds = samples @ components + mean

    for i in range(num_samples):
        order = math.floor(math.log(num_samples, 10)) + 1
        synthetic_surface = pointcloud2surface(synthetic_pointclouds[i], mean_vtk)
        write_vtk_file(synthetic_surface, str(Path(output_path) / f"synthetic{str(i).zfill(order)}.vtk"))