import numpy as np
import pyvista as pv

pl = pv.Plotter()

volume_data = pv.read(None)
volume_data_min = min(volume_data.active_scalars)
volume_data_max = max(volume_data.active_scalars)

class VolumeCustomTF():
    def __init__(self):
        self.volume = None

        self.slider_center_value = 1900
        self.slider_spread_value = 360

        self.slider_center = pl.add_slider_widget(
            self.slider_center_callback,
            [volume_data_min, volume_data_max],
            value=self.slider_center_value,
            title='Center',
            pointa=(0.1, 0.9),
            pointb=(0.4, 0.9)
        )
        self.slider_spread = pl.add_slider_widget(
            self.slider_spread_callback,
            [1, 500],
            value=self.slider_spread_value,
            title='Spread',
            pointa=(0.5, 0.9),
            pointb=(0.8, 0.9)
        )

        self.recreate_volume()

    # Task: modify this transfer function, so the densities around the center density are more opaque
    # The spread parameter determines how big is the neighborhood of opaque densities around the center density
    # Returns: between 255 (opaque) and 0 (transparent)
    def transfer_function(self, density, center, spread):
        return 255
    
    def recreate_volume(self):
        if self.volume is not None:
            pl.remove_actor(self.volume)

        self.volume = pl.add_volume(
            volume_data,
            opacity=[
                self.transfer_function(
                    volume_data_max * (i / 255) + volume_data_min,
                    self.slider_center_value,
                    self.slider_spread_value
                )
                for i in range(256)
            ],
            mapper='smart',
            shade=True)

    def slider_center_callback(self, value):
        self.slider_center_value = value
        self.recreate_volume()
        
    def slider_spread_callback(self, value):
        self.slider_spread_value = value
        self.recreate_volume()

vis = VolumeCustomTF()

pl.show()