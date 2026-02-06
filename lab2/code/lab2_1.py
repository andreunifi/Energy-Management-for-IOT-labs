import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

from skimage import exposure, color
from skimage.color import hsv2rgb, rgb2hsv, rgb2lab, lab2rgb 
    # Edge-aware mask
from skimage import filters
#Constants:
# OLED power model coefficients 
W0 = 0.7755
WR = 1.48169521e-6
WG = 1.77746705e-7
WB = 2.14348309e-7
Y = 0.7755

max_dist = 4

# Directory containing the .tiff images
image_dir = "../misc"


def load_images():
    # Iterate through all .tiff files in the directory
    images = []
    for file_name in os.listdir(image_dir):
        if file_name.endswith(".tiff"):
                file_path = os.path.join(image_dir, file_name)
                with Image.open(file_path) as image:
                    image.show();
                    image_array = np.array(image)
                    images.append(image_array)
    return images

def load_images_verbose():
    # Iterate through all .tiff files in the directory
    images = []
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
                    images.append(image_array)
    return images



def compute_power(image_array):
    #Estimate OLED power consumption of an RGB image.
    #image_rgb: numpy array (H, W, 3), uint8 [0–255]
    #Returns total power (W)
    
    R = image_array[:, :, 0]
    G = image_array[:, :, 1]
    B = image_array[:, :, 2]

    pixel_power = WR * (R**Y) + WG * (G**Y) + WB * (B**Y)
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


def chroma_reduction(image_rgb, chroma_scale=0.4, edge_strength=1.5, blue_scale = 0.5, green_scale = 0.5):
    #
    #Reduce chroma (a/b in Lab) while preserving edges.
    #   - chroma_scale: fraction of chroma to keep
    #   - edge_strength: higher = more protection near edges
    #
    lab = color.rgb2lab(image_rgb/255)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]


    edges = filters.sobel(L)
    edges = (edges - edges.min()) / (edges.max() - edges.min() + 1e-8)
    edge_mask = np.clip(edges / edge_strength, 0, 1)

    factor = chroma_scale + (1 - chroma_scale) * edge_mask
    a *= factor
    b *= factor


    a = np.where(a<0, a*green_scale, a)
    b = np.where(b<0, b*blue_scale, b)

    lab[..., 1] = a
    lab[..., 2] = b
    return (lab2rgb(lab) * 255).astype(np.uint8)

def luminance_reduction(img, factor=0.8):
    lab = rgb2lab(img/255)
    L = lab[..., 0]
    L *= 0.8
    lab[..., 0] = L
    return(lab2rgb(lab)*255).astype(np.uint8)

def manipulate_image(image_array):
    # Manipulation example: make the image darker
    image_array_v1 = (image_array * 0.8).astype(np.uint8)
    image_v1 = Image.fromarray(image_array_v1)
    image_v1.show()
    return image_array_v1

def manipualate_red(image_array):
    # Manipulation example: manipulate the red channel
    image_array_v2 = image_array[:, :, 0]
    image_v2 = Image.fromarray(image_array_v2)
    image_v2.show()

def manipulate_hsv_V(image_array, delta=0.2):
    # Convert 
    hsv = rgb2hsv(image_array/255)
    hsv[:, :, 2] = hsv[:, :, 2] * (1 - delta)
    return (hsv2rgb(hsv)*255).astype(np.uint8)

def manipulate_hsv_equalization(image_array):
    hsv = rgb2hsv(image_array/255)
    
    hsv[:, :, 2] = exposure.equalize_hist(hsv[:, :, 2])
    
    return (hsv2rgb(hsv)*255).astype(np.uint8)


def manipulate_hsv_equalization_adapt(image_array):
    hsv = rgb2hsv(image_array/255)
    
    hsv[:, :, 2] = exposure.equalize_adapthist(hsv[:, :, 2], clip_limit=0.03)
    
    return (hsv2rgb(hsv)*255).astype(np.uint8)

def convert_to_lab():
    # Convert RGB to Lab color space
    image_array_lab = rgb2lab(image_array)
    return image_array_lab



def analyze(image_orig, image_mod):
    power_orig = compute_power(image_orig)
    power_mod  = compute_power(image_mod)
    distortion = compute_distortion(image_orig, image_mod)

    power_saved_pct = ((power_orig - power_mod) / power_orig) * 100

    print("-" * 65)
    print(f"{'Metric':<20}{'Original':>15}{'Modified':>15}")
    print("-" * 65)
    print(f"{'Power (W)':<20}{power_orig:>15.4f}{power_mod:>15.4f}")
    print(f"{'Distortion (%)':<20}{distortion:>30.2f}")
    print("-" * 65)

    if power_saved_pct >= 0:
        print(f"Power saved: {power_saved_pct:6.2f} %")
        if distortion >= max_dist:
            print(f"⚠️  Maximum distortion reached")
    else:
        print(f"⚠️  Power increase: {abs(power_saved_pct):6.2f} %")

    print("-" * 65)

def main():
    images = load_images()
    image_to_show = 2
    print(f"Loaded: {len(images)} image")

    for i in range(len(images)):
        original = images[i];
        modified = original
       
        modified = luminance_reduction(modified)
        #modified = manipulate_hsv_V(modified)
        modified = reduce_blue(modified)

        analyze(original, modified)
        if i == image_to_show:
            # Create side-by-side plot
            plt.figure(figsize=(10, 5))

            # Original
            plt.subplot(1, 2, 1)  # 1 row, 2 columns, first subplot
            plt.imshow(original)
            plt.title("Original")
            plt.axis('off')

            # Modified
            plt.subplot(1, 2, 2)  # 1 row, 2 columns, second subplot
            plt.imshow(modified)
            plt.title("Modified")
            plt.axis('off')

            plt.show()

if __name__ == "__main__":
    main()




# DONE:
#  - hsv: equalization (not good)
#  - hsv: luminance reduction
#  - rgb: blue reduction
#  - custom: dithering and lossless chroma

