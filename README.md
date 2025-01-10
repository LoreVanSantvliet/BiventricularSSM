# Biventricular statistical shape model

This repository is associated with the paper "**Integrating anatomy and electrophysiology in the healthy human heart: Insights from biventricular statistical shape analysis using universal coordinates**". It contains code to generate synthetic biventricular surface meshes with anatomical tags (LV endo, LV epi, RV endo, RV epi) from a statistical shape model (SSM).

This repository is accompanied by the following [Zenodo repository](https://doi.org/doi:10.5281/zenodo.14261122), containing the biventricular SSM itself, and a synthetic cohort of 100 biventricular, volumetric meshes, including fiber orientation and anatomical tags for LV and RV endo- and epicardium, and LV septum.

## Quickstart

**For inferring new, synthetic surface meshes of biventricular anatomy**
1. Download the SSM file (file name "SSM.h5") and mean shape file (file name "mean_shape.vtk") from [Zenodo](https://doi.org/doi:10.5281/zenodo.14261122), and save it at a location of choice, for example `/Users/ABC/Documents/BivMeshes/`.
2. Clone this repository or download the generate_surface_meshes.py file.
3. Generate new synthetic surface meshes by sampling from the SSM, by calling the function generate_surface_mesh, and supplying as arguments the SSM file path, the path to the output folder, and the number of meshes to be created. Optionally, you can modify the number of principal components used, and the sampling boundary.

   A minimal example to generate 10 synthetic surface meshes is provided below. The code should be located in the same folder as the generate_surface_meshes.py file.

   ```
   import generate_surface_meshes as gsm

   input_path = "/Users/ABC/Documents/BivMeshes/" # change to input folder (containing SSM.h5 and mean_shape.vtk)
   output_path = "/Users/ABC/Documents/BivMeshes/" # change to output path of choice
   num_samples = 10 # change to the amount of meshes you want to create

   gsm.generate_surface_mesh(input_path=input_path, output_path=output_path, num_samples=num_samples)
   ```
   After running the code, the provided output folder will contain the generated synthetic surface meshes in [vtk format](https://docs.vtk.org/en/latest/design_documents/VTKFileFormats.html).

**For using the pre-made synthetic cohort of biventricular, volumetric meshes**
1. Download the synthetic cohort from [Zenodo](https://doi.org/doi:10.5281/zenodo.14261122), consisting of files synthetic_vol_000to009.zip, synthetic_vol_010to019.zip, synthetic_vol_020to029.zip, synthetic_vol_030to039.zip, synthetic_vol040to049.zip, synthetic_vol_050to059.zip, synthetic_vol060to069.zip, synthetic_vol_070to079.zip, synthetic_vol_080to089.zip and synthetic_vol_090to099.zip.
2. Unzip these 10 files.
The resulting folders contain 100 synthetic volumetric meshes in [vtk format](https://docs.vtk.org/en/latest/design_documents/VTKFileFormats.html), compatible with most cardiac simulation software, including fibers and anatomical tags.

## Contact
Additional inquiries about data and code availability, questions, suggestions and feedback can be directed to Lore Van Santvliet (lore.vansantvliet@kuleuven.be), or by filing an [issue](https://github.com/LoreVanSantvliet/BiventricularSSM/issues).

## Citation
When using this work, please cite the paper "Integrating anatomy and electrophysiology in the healthy human heart: Insights from biventricular statistical shape analysis using universal coordinates".

