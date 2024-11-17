import numpy as np
import pyvista as pv

pl = pv.Plotter()

volume_data = pv.read(None)
volume_data_min = min(volume_data.active_scalars)
volume_data_max = max(volume_data.active_scalars)

class MarchingCubesMesh():
    def __init__(self):
        self.mesh = None

        # Task: change the isovalue variable to extract the isosurface that corresponds to the bones
        self.isovalue = None

        self.mesh = pl.add_mesh(volume_data.contour([self.isovalue], method='marching_cubes'), color='gray')

vis = MarchingCubesMesh()

pl.show()