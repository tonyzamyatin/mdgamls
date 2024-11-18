import argparse
import json
import os

import numpy as np
import pyvista as pv
from IPython.core.display import Markdown
from IPython.core.display_functions import display

volume_data = pv.read("shoulder.vti")

# Directory to save images
output_dir = "rendered_images"
os.makedirs(output_dir, exist_ok=True)

# Configurations for experimentation
configurations = [
    {"cmap": "viridis", "opacity": "linear", "shade": True, "blending": "composite", "name": "Config 1"},
    {"cmap": "plasma", "opacity": "sigmoid", "shade": False, "blending": "maximum", "name": "Config 2"},
    {"cmap": "gray", "opacity": "linear_r", "shade": True, "blending": "average", "name": "Config 3"},
    {"cmap": "coolwarm", "opacity": "geom", "shade": False, "blending": "composite", "name": "Config 4"},
    {"cmap": "bone", "opacity": "geom", "shade": True, "blending": "composite", "name": "Config 5"},
]


# Helper functions
def save_description(config_name, description):
    """Save the description to a text file."""
    desc_path = os.path.join(output_dir, f"{config_name.replace(' ', '_')}.txt")
    with open(desc_path, "w") as f:
        f.write(description)


def load_description(config_name):
    """Load a description from a text file if it exists."""
    desc_path = os.path.join(output_dir, f"{config_name.replace(' ', '_')}.txt")
    if os.path.exists(desc_path):
        with open(desc_path, "r") as f:
            return f.read().strip()
    return ""


def save_configuration(config_name, config):
    """Save the configuration details to a JSON file."""
    config_path = os.path.join(output_dir, f"{config_name.replace(' ', '_')}_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def load_configuration(config_name):
    """Load configuration details from a JSON file."""
    config_path = os.path.join(output_dir, f"{config_name.replace(' ', '_')}_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


def render_configuration(config, screenshot=False):
    """Render a specific configuration interactively."""
    config_name = config["name"]
    cmap = config["cmap"]
    opacity = config["opacity"]
    shade = config["shade"]
    blending = config["blending"]
    img_path = os.path.join(output_dir, f"{config_name.replace(' ', '_')}.png")

    pl = pv.Plotter(title=f"{config_name} - cmap: {cmap}, opacity: {opacity}, shade: {shade}, blending: {blending}")
    pl.add_volume(
        volume_data,
        cmap=cmap,  # Colormap used for volume rendering (e.g., 'gray', 'viridis', 'plasma')
        opacity=opacity,  # Opacity function to control transparency (e.g., 'linear', 'sigmoid')
        shade=shade,  # Boolean to toggle shading (True adds light/shadow effects for depth)
        blending=blending,  # Blending mode for volume rendering ('composite', 'maximum', 'average')
        opacity_unit_distance=20,  # Controls transparency scaling
        mapper='smart'
    )

    # Add a screenshot button (press 's' to save)
    def save_screenshot():
        pl.screenshot(img_path)
        print(f"Screenshot saved for {config_name} at {img_path}")

    pl.add_key_event("s", save_screenshot)  # Press 's' to save a screenshot during interaction

    # Display the interactive plot
    pl.show()
    pl.close()

    # Save the configuration and description
    save_configuration(config_name, config)
    # Handle description
    current_desc = load_description(config_name)
    print(f"Current description for {config_name}:")
    print(current_desc if current_desc else "[No description yet]")
    new_desc = input(f"Enter description for {config_name} (leave blank to keep current): ")
    if new_desc:
        save_description(config_name, new_desc)


# Selective rendering
def interactive_rendering(config_indices=None):
    """
    Render selected configurations interactively.

    Parameters:
    - config_indices: List of indices to render. None means render all.
    """
    indices = config_indices if config_indices else range(len(configurations))
    for idx in indices:
        render_configuration(configurations[idx])


# Generate Markdown Report
def generate_markdown():
    """Generate a markdown file using stored screenshots, descriptions, and configurations."""
    markdown_file = "volume_task2_report.md"
    with open(markdown_file, "w") as f:
        f.write("# Volume Rendering Report\n\n")
        for config in configurations:
            config_name = config["name"]
            img_path = os.path.join(output_dir, f"{config_name.replace(' ', '_')}.png")
            description = load_description(config_name)
            config_details = load_configuration(config_name)
            if os.path.exists(img_path):
                f.write(f"## {config_name}\n\n")
                if config_details:
                    f.write("**Configuration Used:**\n")
                    f.write(f"```json\n{json.dumps(config_details, indent=4)}\n```\n\n")
                f.write(f"![{config_name}]({img_path})\n\n")
                f.write(f"**Description**: {description}\n\n")
            else:
                print(f"Warning: No screenshot found for {config_name}")
    print(f"Markdown report saved as {markdown_file}")


# CLI Integration
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Volume Rendering CLI")
    parser.add_argument(
        "--render",
        nargs="*",
        type=int,
        help="Render specific configurations by index (1-based). If empty, renders all.",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Generate the markdown report.",
    )
    args = parser.parse_args()

    if args.render is not None:
        indices = [(idx - 1) for idx in args.render] if args.render else None
        interactive_rendering(config_indices=indices)
    elif args.markdown:
        generate_markdown()
    else:
        parser.print_help()

# Example usage:
# Render configurations 1 and 3 interactively:
# python script.py --render 1 3
# Note: During interaction, press 's' to save the screenshot before closing the window.
#
# Generate a markdown report from existing screenshots and descriptions:
# python script.py --markdownn
