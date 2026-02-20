from PIL import Image
import numpy as np
import os

def analyze(path):
    img = Image.open(path)
    print(f"Path: {path}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    print(f"Format: {img.format}")
    img_array = np.array(img)
    unique_colors = np.unique(img_array.reshape(-1, img_array.shape[-1]), axis=0)
    print(f"Unique colors: {len(unique_colors)}")
    return img

def compare(path1, path2):
    img1 = Image.open(path1).convert('RGBA')
    img2 = Image.open(path2).convert('RGBA')
    if img1.size != img2.size:
        print(f"Sizes differ: {img1.size} vs {img2.size}")
        return False
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    diff = np.any(arr1 != arr2)
    if diff:
        print("Pixels differ!")
        return False
    else:
        print("Pixels are identical!")
        return True

try:
    img = analyze('download.png')
    
    # Try saving as WebP lossless
    img.save('my_lossless.webp', 'WEBP', lossless=True, quality=100)
    print(f"Saved my_lossless.webp: {os.path.getsize('my_lossless.webp')} bytes")
    
    print("\nVerifying my_lossless.webp...")
    compare('download.png', 'my_lossless.webp')
    
except Exception as e:
    print(f"Error: {e}")
