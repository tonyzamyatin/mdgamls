import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import numpy as np
import pydicom
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.ndimage import gaussian_filter, median_filter, uniform_filter

# Global variables
ct_data = None
filtered_data = None
filter_type = "original"
filter_params = {"gaussian_radius": 3, "gaussian_std": 1, "kernel_size": 3}


# Function that displays the DICOM images
def display_dicom_image():
    directory = filedialog.askdirectory()
    if directory:
        dicom_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.lower().endswith('.dcm')]
        if dicom_files:
            dicom_files.sort()
            global ct_data, filtered_data
            ct_data = load_ct_volume(dicom_files)
            filtered_data = filter_ct_slices(ct_data, filter_type)
            display_slice(0, filtered_data)
            slice_slider.config(to=len(filtered_data) - 1)
            slice_label.config(text="")
        else:
            slice_label.config(text="No DICOM files found in the selected directory")


# Function that loads the CT volume (in the form of an entire folder)
def load_ct_volume(dicom_files):
    """Returns the DICOM images as a list of np.ndarrays"""
    ct_slices = [pydicom.dcmread(file_path).pixel_array for file_path in dicom_files]
    return ct_slices


def filter_ct_slices(ct_slices, filter_type):
    """
    Applies the specified filter to each slice in a CT volume.

    Parameters:
        ct_slices (list or np.ndarray): The input CT slices as a list or array of 2D arrays (grayscale images).
        filter_type (str): The type of filter to apply. Options include:
            - "gaussian": Applies a Gaussian filter for smoothing the image.
            - "median": Applies a median filter for reducing noise while preserving edges.
            - "average": Applies an average (uniform) filter for smoothing the image by averaging the pixel values in a local neighborhood.

    Returns:
        np.ndarray: A NumPy array of filtered CT slices.

    Filter Descriptions and Parameters:
    -----------------------------------
    1. **Gaussian Filter**:
        - Smooths the image by applying a Gaussian kernel, which reduces noise and detail.
        - Parameters:
            - `sigma` (filter_params["gaussian_std"]): The standard deviation of the Gaussian kernel. Controls the degree of smoothing. Larger values result in more smoothing.
            - `radius` (filter_params["gaussian_radius"]): Defines the extent of the kernel's area of influence. Affects how far the smoothing effect reaches.

    2. **Median Filter**:
        - Reduces noise in the image by replacing each pixel's value with the median of its neighbors. Useful for removing salt-and-pepper noise while preserving edges.
        - Parameter:
            - `size` (filter_params["kernel_size"]): The size of the neighborhood (kernel) used to calculate the median. Larger sizes lead to stronger noise reduction but may reduce image detail.

    3. **Average (Uniform) Filter**:
        - Applies a uniform filter where each pixel is replaced by the average of its neighbors. This smooths the image by averaging out local pixel values.
        - Parameter:
            - `size` (filter_params["kernel_size"]): The size of the neighborhood (kernel) over which the averaging is done. Larger sizes result in more extensive smoothing.

    Note:
        If `filter_type` is not recognized, the original `ct_slices` are returned without modification.
    """
    if filter_type == "gaussian":
        return np.array([gaussian_filter(slice, sigma=filter_params["gaussian_std"], radius=filter_params["gaussian_radius"]) for slice in ct_slices])
    elif filter_type == "median":
        return np.array([median_filter(slice, size=filter_params["kernel_size"]) for slice in ct_slices])
    elif filter_type == "average":
        return np.array([uniform_filter(slice, size=filter_params["kernel_size"]) for slice in ct_slices])
    return ct_slices  # Return unmodified if no filter is selected


# Function that displays a single slice at a time
def display_slice(slice_number, data):
    ax.clear()
    slice = data[slice_number]  # np.ndarray
    ax.imshow(slice, cmap='gray')
    canvas.draw()
    slice_label.config(text=f"Slice {slice_number}/{len(data) - 1}")


# Function to update the filter type and parameters
def update_filter_type(new_filter):
    global filter_type
    filter_type = new_filter
    update_filter_inputs()
    refresh_images()


def update_filter_inputs():
    # Show or hide input fields based on the filter type
    if filter_type == "gaussian":
        gaussian_frame.grid(row=4, column=0, sticky="ew")
        kernel_frame.grid_remove()
    elif filter_type in ["median", "average"]:
        gaussian_frame.grid_remove()
        kernel_frame.grid(row=4, column=0, sticky="ew")
    else:
        gaussian_frame.grid_remove()
        kernel_frame.grid_remove()


# Function to update parameter values
def update_param(param, value):
    # If the entry is empty, set a default value to avoid ValueError
    if value == "":
        return
    filter_params[param] = int(value)
    refresh_images()  # Reload and display images with updated parameters


def refresh_images():
    """Reapply the filter to the images and refresh the display."""
    global filtered_data
    if 'ct_data' in globals():
        filtered_data = filter_ct_slices(ct_data, filter_type)
        display_slice(slice_slider.get(), filtered_data)


# UI --- no need to touch this part (unless you want to make UI changes)
app = tk.Tk()
app.title("DICOM Viewer")

frame = ttk.Frame(app)
frame.pack(expand=True, fill='both')
display_button = ttk.Button(frame, text="Load DICOM", command=display_dicom_image)
display_button.grid(row=0, column=0)

# Dropdown menu for selecting the filter type
filter_dropdown = ttk.Combobox(frame, values=["original", "gaussian", "median", "average"])
filter_dropdown.current(0)
filter_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filter_type(filter_dropdown.get()))
filter_dropdown.grid(row=1, column=0, sticky="ew")

# Input fields for Gaussian parameters
gaussian_frame = ttk.Frame(frame)
ttk.Label(gaussian_frame, text="Gaussian Radius:").grid(row=0, column=0)
gaussian_radius_entry = ttk.Entry(gaussian_frame)
gaussian_radius_entry.insert(0, "3")
gaussian_radius_entry.grid(row=0, column=1)
gaussian_radius_entry.bind("<KeyRelease>", lambda e: update_param("gaussian_radius", gaussian_radius_entry.get()))

ttk.Label(gaussian_frame, text="Gaussian Std:").grid(row=1, column=0)
gaussian_std_entry = ttk.Entry(gaussian_frame)
gaussian_std_entry.insert(0, "1")
gaussian_std_entry.grid(row=1, column=1)
gaussian_std_entry.bind("<KeyRelease>", lambda e: update_param("gaussian_std", gaussian_std_entry.get()))

# Input fields for median and average kernel size
kernel_frame = ttk.Frame(frame)
ttk.Label(kernel_frame, text="Kernel Size:").grid(row=0, column=0)
kernel_size_entry = ttk.Entry(kernel_frame)
kernel_size_entry.insert(0, "3")
kernel_size_entry.grid(row=0, column=1)
kernel_size_entry.bind("<KeyRelease>", lambda e: update_param("kernel_size", kernel_size_entry.get()))

# Hide input frames by default
update_filter_inputs()

fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=2, column=0)

app.update()
slice_slider = tk.Scale(frame, from_=0, to=0, orient="horizontal", length=app.winfo_width() - 2 * 20,
                        command=lambda x: display_slice(slice_slider.get(), filtered_data))
slice_slider.grid(row=3, column=0)
slice_label = ttk.Label(frame, text="", foreground="black")
slice_label.grid(row=5, column=0)

app.mainloop()
