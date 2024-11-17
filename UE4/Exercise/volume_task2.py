import numpy as np
import pyvista as pv

pl = pv.Plotter()

volume_data = pv.read(None)

class VolumeDefaultTF():
    def __init__(self):

        self.volume = pl.add_volume(volume_data,
            cmap='gray', # 'viridis', 'plasma', etc. https://matplotlib.org/stable/users/explain/colors/colormaps.html
            opacity='sigmoid', # 'linear', 'linear_r', 'geom', 'geom_r', 'sigmoid'
            mapper='smart',
            shade=True,
            blending= 'composite', # 'maximum', 'composite', 'average'
            opacity_unit_distance=20 # no need to touch this, unless you know what you are doing :)
        )

vis = VolumeDefaultTF()

pl.show()