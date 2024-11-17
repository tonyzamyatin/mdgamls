import numpy as np
import pyvista as pv

volume_data = pv.read("shoulder.vti")

# Extract the range of scalar values in the dataset for setting isovalue)
volume_data_min = volume_data.active_scalars.min()
volume_data_max = volume_data.active_scalars.max()
print(f"Scalar range: {volume_data_min} to {volume_data_max}")


class MarchingCubesMesh():
    def __init__(self, isovalue, color='gray', opacity=1.0, ambient=0., diffuse=1., specular=0.):
        self.mesh = None

        # Task: change the isovalue variable to extract the isosurface that corresponds to the bones
        self.isovalue = isovalue

        # Generate the isosurface using the marching cubes algorithm
        self.mesh = volume_data.contour([self.isovalue], method='marching_cubes')

        # Add the mesh to the plotter with visualization parameters
        pl.add_mesh(self.mesh, color=color, opacity=opacity, ambient=ambient, diffuse=diffuse, specular=specular)
        print(f"Marching cubes mesh created with isovalue: {self.isovalue}")


# Experimentally determined isovalue to extract the bone structure
isovalue = 1200

color = 'salmon'    # Color of the isosurface
opacity = 0.5       # Transparency of the isosurface


def plot_configurations():
    configurations = [
        {"ambient": 1.0, "diffuse": 0.0, "specular": 0.0, "description": "Ambient 1, Diffuse 0, Specular 0"},
        {"ambient": 0.0, "diffuse": 1.0, "specular": 0.0, "description": "Ambient 0, Diffuse 1, Specular 0"},
        {"ambient": 0.0, "diffuse": 0.0, "specular": 1.0, "description": "Ambient 0, Diffuse 0, Specular 1"},
        {"ambient": 1.0, "diffuse": 1.0, "specular": 0.0, "description": "Ambient 1, Diffuse 1, Specular 0"},
    ]

    for config in configurations:
        pl = pv.Plotter(title=config["description"])  # Create a new plotter for each configuration
        vis = MarchingCubesMesh(isovalue, color=color,
                    ambient=config["ambient"],
                    diffuse=config["diffuse"],
                    specular=config["specular"])
        pl.show()


# plot_configurations()     # Uncomment to plot the different configurations for ambient, diffuse, specular

# Comment on configuration
# (Ambient 1, Diffuse 0, Specular 0): The object appears uniformly illuminated without any shadows or highlights.
# This is because ambient lighting provides a uniform light intensity independent of the surface orientation.
# As a result, the 3D structure is hard to discern, and the rendering lacks depth or detail.

# (Ambient 0, Diffuse 1, Specular 0): The object is illuminated primarily through diffuse reflection,
# which simulates light scattering evenly across a surface. This highlights the overall shape and contours of the object,
# making the 3D structure recognizable. However, the object appears relatively dark because there is no ambient lighting.

# (Ambient 0, Diffuse 0, Specular 1): The object is rendered with specular reflection, emphasizing shiny highlights.
# Specular lighting simulates light bouncing directly off smooth surfaces, creating reflective spots.
# Without ambient or diffuse lighting, the rest of the object remains unlit, resulting in a dark appearance
# with small, bright reflective points.

# (Ambient 1, Diffuse 1, Specular 0): The combination of ambient and diffuse lighting makes the object uniformly bright,
# while shadows and shading from diffuse reflection enhance the visibility of the 3D structure. However,
# excessive ambient lighting reduces the contrast, causing finer details to appear washed out.

# Experimental Configuration (Ambient 0.5, Diffuse 0.8, Specular 0.2): This balanced configuration uses moderate ambient
# lighting to maintain overall visibility, diffuse lighting to highlight contours and 3D structure, and a touch of
# specular lighting to add subtle reflective highlights. The result is a detailed and visually appealing representation
# of the bone with good depth and contrast.


# Experimental configuration

ambient = 0.5    # Ambient lighting (higher values increase brightness without directional lighting)
diffuse = 0.8    # Diffuse reflection (spread-out light reflection)
specular = 0.2   # Specular reflection (shiny highlights)

pl = pv.Plotter(title="Experimental configuration")  # Create a new plotter for each configuration
vis = MarchingCubesMesh(isovalue, color=color,
            ambient=ambient,
            diffuse=diffuse,
            specular=specular)
pl.show()

# Note: I am no medial expert, but to me, it looks like the bone is fractured.
