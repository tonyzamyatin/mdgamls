# Volume Rendering Report

## Config 1

**Configuration Used:**
```json
{
    "cmap": "viridis",
    "opacity": "linear",
    "shade": true,
    "blending": "composite",
    "name": "Config 1"
}
```

![Config 1](rendered_images\Config_1.png)

**Description**: The **viridis** colormap, which is perceptually linear, provides good visual contrast, with bluish tones representing low-density tissue and greenish-yellow tones highlighting high-density tissue. However, the **linear** opacity transfer function, combined with the **composite** blending function, does not sufficiently emphasize the high-density bone structures. This is because the **linear** opacity function assigns opacity values proportionally to the scalar density values. Consequently, soft tissues are assigned relatively high opacity values, which dominate the visualization and reduce the clarity of high-density structures. The **composite** blending function further averages these contributions, producing a somewhat "mushy" appearance. Switching to a blending function like **maximum** would better highlight the high-density bone structures by prioritizing their contributions over those of the surrounding tissue.

## Config 2

**Configuration Used:**
```json
{
    "cmap": "plasma",
    "opacity": "sigmoid",
    "shade": false,
    "blending": "maximum",
    "name": "Config 2"
}
```

![Config 2](rendered_images\Config_2.png)

**Description**: The **plasma** colormap, which is perceptually linear, transitions smoothly from light pink for low-density tissues to yellow for high-density regions
. While perceptually uniform, the color scheme is not ideal for visualizing bone structures, as it does not provide an intuitive distinction between
high-density and medium-density tissues. The absence of **shading** further reduces the perception of the 3D structure, making it challenging to discern depth and spatial relationships. However, adding shading might not complement the colormap effectively due to its reliance on color rather than light and shadow contrast. The **sigmoid** opacity function performs better than the linear one for this use case. Opacity increases exponentially in the lower half of the scalar range and logarithmically in the upper half (following a sigmoid curve). While this improvement makes the bones more visible, the opacity of medium-density tissues, such as cartilage, remains too high. This results in "pinkish mushy blobs" that obscure the finer details of the bone structure. Using the **maximum** blending function effectively accentuates the bones by prioritizing their higher scalar values over those of surrounding tissues, making the bones more distinct and prominent in the visualization.

## Config 3

**Configuration Used:**
```json
{
    "cmap": "gray",
    "opacity": "linear_r",
    "shade": true,
    "blending": "average",
    "name": "Config 3"
}
```

![Config 3](rendered_images\Config_3.png)

**Description**: The **gray** colormap is neutral and does not emphasize scalar variations through color, making it entirely dependent on the opacity function and blending mode to reveal internal structures. Using **reverse linear opacity** assigns higher opacity to lower scalar values and lower opacity to higher scalar values, which is the opposite of what is typically needed for visualizing dense structures like bones. As a result, the low-density regions (e.g., air or soft tissue) are completely opaque, obscuring the high-density regions entirely. This produces a solid gray cube with no transparency or visible internal structures, as the high-opacity low-density regions dominate the visualization.

## Config 4

**Configuration Used:**
```json
{
    "cmap": "coolwarm",
    "opacity": "geom",
    "shade": false,
    "blending": "composite",
    "name": "Config 4"
}
```

![Config 4](rendered_images\Config_4.png)

**Description**: The **coolwarm** colormap is unsuitable for this use case as it assigns red only to the very highest scalar density values, while the majority of the range is mapped to white. This results in a visualization where most structures appear washed out, with minimal color variation to differentiate between density ranges. Furthermore, the **geom** opacity function exacerbates the issue by assigning opacity only to the very highest density values, leaving most of the volume, including the bones (which are not as dense as the highest regions), nearly completely transparent. Consequently, the combination of the colormap and opacity function results in a visualization where almost nothing is rendered, making it ineffective for highlighting bone structures.

## Config 5

**Configuration Used:**
```json
{
    "cmap": "bone",
    "opacity": "geom",
    "shade": true,
    "blending": "composite",
    "name": "Config 5"
}
```

![Config 5](rendered_images\Config_5.png)

**Description**: The **bone** colormap is the ideal choice for this task as it is specifically tailored for medical imaging, offering smooth transitions from black to white that are well-suited for highlighting dense structures like bones. The **sigmoid_20** opacity function is also optimal, as it assigns linear opacity values to scalar densities within the range of -20 to 20. This ensures that medium-density tissues are appropriately transparent, while high-density structures like bones remain prominently visible. Adding **shading** further enhances the 3D perception of the structures, making it easier to understand spatial relationships within the volume. Finally, the **maximum** blending function is perfect for accentuating high-density bone tissue by prioritizing their contribution over surrounding low-density regions. Based on experimentation, this configuration delivers the clearest and most detailed visualization for this dataset, effectively highlighting the bones.

