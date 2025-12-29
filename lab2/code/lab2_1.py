import numpy as np
from PIL import Image
import os

from skimage.color import rgb2lab, lab2rgb

#Constants:
# OLED power model coefficients 
W0 = 0.7755
WR = 1.48169521e-6
WG = 1.77746705e-7
WB = 2.14348309e-7

# Directory containing the .tiff images
image_dir = "lab2/misc"



# Iterate through all .tiff files in the directory
for file_name in os.listdir(image_dir):
    if file_name.endswith(".tiff"):
            file_path = os.path.join(image_dir, file_name)
            with Image.open(file_path) as image:
                print(f"Loaded image: {file_name}, size: {image.size}")
                image.show();
                image_array = np.array(image)
                print(f"Shape: {image_array.shape}")
                print(f"Red channel:\n{image_array[:, :, 0]}")
                print(f"Green channel:\n{image_array[:, :, 1]}")
                print(f"Blue channel:\n{image_array[:, :, 2]}")









def compute_oled_power(image_array):
    #Estimate OLED power consumption of an RGB image.
    #image_rgb: numpy array (H, W, 3), uint8 [0–255]
    #Returns total power (W)
    
    image_rgb = image_rgb.astype(np.float64)

    R = image_rgb[:, :, 0]
    G = image_rgb[:, :, 1]
    B = image_rgb[:, :, 2]

    pixel_power = WR * R + WG * G + WB * B
    total_power = W0 + np.sum(pixel_power)

    return total_power

def compute_distortion(image_orig, image_mod):
    """
    Computes LAB Euclidean distortion between two images.
    Returns normalized distortion (%)
    """
    lab_orig = rgb2lab(image_orig / 255.0)
    lab_mod  = rgb2lab(image_mod / 255.0)

    diff = lab_orig - lab_mod
    dist = np.sqrt(
        diff[:, :, 0]**2 +
        diff[:, :, 1]**2 +
        diff[:, :, 2]**2
    )

    # Average per pixel
    avg_dist = np.mean(dist)

    # Maximum LAB distance (given in slides)
    max_dist = np.sqrt(100**2 + 255**2 + 255**2)

    return (avg_dist / max_dist) * 100

def reduce_blue(image_rgb,delta=20):
    img = image_rgb.copy().astype(np.int16)
    img[:, :, 2] = np.clip(img[:, :, 2] - delta, 0, 255)
    return img.astype(np.uint8)



def manypulate_image(image_array):
    # Manipulation example: make the image darker
    image_array_v1 = (image_array * 0.6).astype(np.uint8)
    image_v1 = Image.fromarray(image_array_v1)
    image_v1.show()

def manypualate_red(image_array):
    # Manipulation example: manipulate the red channel
    image_array_v2 = image_array[:, :, 0]
    image_v2 = Image.fromarray(image_array_v2)
    image_v2.show()

def is_it_greyscale(image_array):
    image_array_v2 = image_array.copy()
    image_array_v2[:, :, 1] = 0  # Set green channel to 0
    image_array_v2[:, :, 2] = 0  # Set blue channel to 0
    image_v2 = Image.fromarray(image_array_v2)
    image_v2.show()


def convert_to_lab():
    # Convert RGB to Lab color space
    image_array_lab = rgb2lab(image_array)
    return image_array_lab

