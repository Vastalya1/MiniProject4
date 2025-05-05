import os
import cv2
import numpy as np

# --- Settings ---
PATCH_SIZE = 128
MIN_PIXELS = 50        # Min pixels for a class to consider patch
MAX_OIL_PIXELS = 10    # Max oil pixels allowed in non-oil patches

# --- Color definitions (in BGR) ---
OIL_COLOR   = (124, 0, 255)     # RGB (255, 0, 124)
WATER_COLOR = (255, 221, 51)    # RGB (51, 221, 255)
OTHER_COLOR = (51, 204, 255)    # RGB (255, 204, 51)
BG_COLOR    = (0, 0, 0)         # RGB (0, 0, 0)

def create_class_mask(mask_img, target_color):
    """Create binary mask for a given color."""
    return cv2.inRange(mask_img, np.array(target_color), np.array(target_color))

def extract_patches(image, mask, class_color, label, min_pixels=MIN_PIXELS, max_oil_pixels=MAX_OIL_PIXELS):
    """Extract 128x128 patches containing a target class and minimal oil spill."""
    h, w = image.shape[:2]
    class_mask = create_class_mask(mask, class_color)
    oil_mask = create_class_mask(mask, OIL_COLOR)
    patches = []

    for y in range(0, h, PATCH_SIZE):
        for x in range(0, w, PATCH_SIZE):
            img_patch = image[y:y+PATCH_SIZE, x:x+PATCH_SIZE]
            mask_patch = mask[y:y+PATCH_SIZE, x:x+PATCH_SIZE]
            class_patch = class_mask[y:y+PATCH_SIZE, x:x+PATCH_SIZE]
            oil_patch = oil_mask[y:y+PATCH_SIZE, x:x+PATCH_SIZE]

            if img_patch.shape[:2] != (PATCH_SIZE, PATCH_SIZE):
                continue

            class_pixels = np.count_nonzero(class_patch)
            oil_pixels = np.count_nonzero(oil_patch)

            if class_pixels >= min_pixels and oil_pixels <= max_oil_pixels:
                patches.append((img_patch, mask_patch, x, y, label))

    return patches

def extract_oil_patches(image, mask, min_oil_pixels=MIN_PIXELS):
    """Extract 128x128 patches with oil present."""
    h, w = image.shape[:2]
    oil_mask = create_class_mask(mask, OIL_COLOR)
    patches = []

    for y in range(0, h, PATCH_SIZE):
        for x in range(0, w, PATCH_SIZE):
            img_patch = image[y:y+PATCH_SIZE, x:x+PATCH_SIZE]
            mask_patch = mask[y:y+PATCH_SIZE, x:x+PATCH_SIZE]
            oil_patch = oil_mask[y:y+PATCH_SIZE, x:x+PATCH_SIZE]

            if img_patch.shape[:2] != (PATCH_SIZE, PATCH_SIZE):
                continue

            if np.count_nonzero(oil_patch) >= min_oil_pixels:
                patches.append((img_patch, mask_patch, x, y, "oil"))

    return patches

def save_patches(patches, out_img_dir, out_mask_dir, prefix):
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_mask_dir, exist_ok=True)

    for (img_patch, mask_patch, x, y, label) in patches:
        base_name = f"{prefix}_{label}_{x}_{y}.png"
        cv2.imwrite(os.path.join(out_img_dir, base_name), img_patch)
        cv2.imwrite(os.path.join(out_mask_dir, base_name), mask_patch)

def process_dataset(images_dir, masks_dir, out_img_dir, out_mask_dir):
    files = sorted([f for f in os.listdir(images_dir) if f.endswith('.jpg')])

    for file in files:
        number = file[file.find('(')+1:file.find(')')]  # Extract number
        image_path = os.path.join(images_dir, file)
        mask_path = os.path.join(masks_dir, f"Oil ({number}).png")

        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path)

        if image is None or mask is None:
            print(f"Skipping {file}: Missing image or mask.")
            continue

        # Extract patches
        oil_patches   = extract_oil_patches(image, mask)
        water_patches = extract_patches(image, mask, WATER_COLOR, "water")
        other_patches = extract_patches(image, mask, OTHER_COLOR, "other")
        bg_patches    = extract_patches(image, mask, BG_COLOR, "background")

        all_patches = oil_patches + water_patches + other_patches + bg_patches

        # Save patches
        save_patches(all_patches, out_img_dir, out_mask_dir, f"Oil_{number}")

        print(f"Processed Oil ({number}): {len(all_patches)} patches")

# --- USAGE ---
images_path = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4/dataset/roiTest/images'
masks_path = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4/dataset/roiTest/masks'
output_images = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4/dataset/roiTest/patches/images'
output_masks = 'D:/_official_/_MIT ADT_/_SEMESTER 6_/MP4/dataset/roiTest/patches/masks'

process_dataset(images_path, masks_path, output_images, output_masks)
