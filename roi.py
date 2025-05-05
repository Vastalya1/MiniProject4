import os
import cv2
import numpy as np

# --- Settings ---
PATCH_SIZE = 128
MIN_OIL_PIXELS = 30  # Minimum oil pixels to consider it a valid ROI

# --- Color definitions ---
OIL_COLOR = (124, 0, 255)

def create_class_mask(mask_img, target_color):
    """Create binary mask for target color."""
    return cv2.inRange(mask_img, np.array(target_color), np.array(target_color))

def extract_oil_patches(image, mask, patch_size=PATCH_SIZE, min_pixels=MIN_OIL_PIXELS):
    """Extract patches where oil pixels are present."""
    h, w = image.shape[:2]
    oil_mask = create_class_mask(mask, OIL_COLOR)
    image_patches, mask_patches = [], []

    for y in range(0, h, patch_size):
        for x in range(0, w, patch_size):
            img_patch = image[y:y+patch_size, x:x+patch_size]
            mask_patch = mask[y:y+patch_size, x:x+patch_size]
            oil_patch = oil_mask[y:y+patch_size, x:x+patch_size]

            if img_patch.shape[:2] != (patch_size, patch_size):
                continue

            if np.count_nonzero(oil_patch) >= min_pixels:
                image_patches.append((img_patch, x, y))
                mask_patches.append((mask_patch, x, y))

    return image_patches, mask_patches

def save_patches(patches, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    for i, (patch, x, y) in enumerate(patches):
        filename = f"{prefix}_{x}_{y}.png"
        cv2.imwrite(os.path.join(output_dir, filename), patch)

def process_dataset(images_dir, masks_dir, out_img_dir, out_mask_dir):
    files = sorted([f for f in os.listdir(images_dir) if f.endswith('.jpg')])

    for file in files:
        # Extract number between parentheses
        number = file[file.find('(')+1:file.find(')')]  # Extracts 263 from Oil (263).jpg
        image_path = os.path.join(images_dir, file)
        mask_path = os.path.join(masks_dir, f"Oil ({number}).png")

        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path)

        if image is None or mask is None:
            print(f"Skipping {file}: Missing image or mask.")
            continue

        img_patches, mask_patches = extract_oil_patches(image, mask)
        save_patches(img_patches, out_img_dir, f"Oil_{number}")
        save_patches(mask_patches, out_mask_dir, f"Oil_{number}")

        print(f"Processed: Oil ({number})")


# --- USAGE ---
images_path = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4/dataset/roiTrain/images'
masks_path = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4/dataset/roiTrain/masks'
output_images = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4\dataset/roiTrain/oldPatches/images'
output_masks = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4\dataset/roiTrain/oldPatches/masks'

process_dataset(images_path, masks_path, output_images, output_masks)
