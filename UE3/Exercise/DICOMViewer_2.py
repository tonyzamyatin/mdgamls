import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pydicom
import os

import scipy.ndimage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.ndimage import zoom

ct_data = None
filtered_data = None
interpolation_method = "bicubic"


# Function that displays the DICOM images
def display_dicom_image():
    directory = filedialog.askdirectory()
    if directory:
        dicom_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.lower().endswith('.dcm')]
        if dicom_files:
            dicom_files.sort()
            global ct_data, filtered_data
            ct_data = load_ct_volume(dicom_files)
            refresh_images()
            slice_slider.config(to=len(ct_data) - 1)
            slice_label.config(text="")
        else:
            slice_label.config(text="No DICOM files found in the selected directory")


# Function that loads the CT volume (in the form of an entire folder)
def load_ct_volume(dicom_files):
    ct_slices = [pydicom.dcmread(file_path).pixel_array for file_path in dicom_files]
    return ct_slices


# Function to update interpolation method
def update_interpolation_method(new_method):
    global interpolation_method
    interpolation_method = new_method
    refresh_images()


# Function to resample a single image slice
def resample_image(slice, zoom_factor, method):
    order = {"nearest": 0, "bilinear": 1, "bicubic": 3}.get(method, 3)  # Default to bicubic
    return zoom(zoom(slice, 1 / zoom_factor, order=order), zoom_factor, order=order)


# Update refresh_images to include resampling
def refresh_images():
    """Reapply the filter to the images and refresh the display."""
    global filtered_data
    if 'ct_data' in globals() and ct_data is not None:
        zoom_factor = 4
        filtered_data = [resample_image(slice, zoom_factor, interpolation_method) for slice in ct_data]
        display_slice(slice_slider.get())


# Function that displays a single slice at a time
def display_slice(slice_number):
    ax.clear()
    slice = filtered_data[slice_number]
    ax.imshow(slice, cmap='gray')
    canvas.draw()
    slice_label.config(text=f"Slice {slice_number}/{len(filtered_data) - 1}")


# UI --- no need to touch this part (unless you want to make UI changes)
app = tk.Tk()
app.title("DICOM Viewer (resampling)")

frame = ttk.Frame(app)
frame.pack(expand=True, fill='both')
display_button = ttk.Button(frame, text="Load DICOM", command=display_dicom_image)
display_button.grid(row=0, column=0)

# Dropdown for selecting interpolation method
interpolation_dropdown = ttk.Combobox(frame, values=["nearest", "bilinear", "bicubic"])
interpolation_dropdown.current(2)  # Default to "bicubic"
interpolation_dropdown.bind("<<ComboboxSelected>>", lambda e: update_interpolation_method(interpolation_dropdown.get()))
interpolation_dropdown.grid(row=1, column=0, sticky="ew")

fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=2, column=0)

app.update()
slice_slider = tk.Scale(frame, from_=0, to=0, orient="horizontal", length=app.winfo_width() - 2 * 20,
                        command=lambda x: display_slice(slice_slider.get()))
slice_slider.grid(row=3, column=0)
slice_label = ttk.Label(frame, text="", foreground="black")
slice_label.grid(row=5, column=0)

app.mainloop()
