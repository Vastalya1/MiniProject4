import cv2
import os

def process_images(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    tile_size = 128  # Size of each tile
    final_size = 1024  # Resize image to this size before tiling

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Read image
        image = cv2.imread(input_path)
        if image is None:
            print(f"Skipping {filename}: Not a valid image file")
            continue

        # Get original dimensions
        height, width = image.shape[:2]

        # Ensure the image is 1920x1080 before processing
        if width == 1920 and height == 1080:
            # Step 1: Center crop to 1080x1080
            x_start = (width - height) // 2  # Crop width equally from both sides
            cropped_image = image[:, x_start:x_start + height]

            # Step 2: Resize to 1024x1024
            resized_image = cv2.resize(cropped_image, (final_size, final_size))

            # Step 3: Split into 128x128 tiles (64 tiles in total)
            for row in range(8):  # 1024 / 128 = 8 rows
                for col in range(8):  # 1024 / 128 = 8 columns
                    x = col * tile_size
                    y = row * tile_size
                    tile = resized_image[y:y+tile_size, x:x+tile_size]

                    # Step 4: Save each tile with modified name
                    tile_filename = f"{os.path.splitext(filename)[0]}_tile_{row}{col}.jpg"
                    tile_output_path = os.path.join(output_folder, tile_filename)
                    cv2.imwrite(tile_output_path, tile)
                    print(f"Saved: {tile_filename} -> {tile_output_path}")
        else:
            print(f"Skipping {filename}: Not 1920x1080")

# Example usage
input_folder = "D:\\_official_\\_MIT ADT_\\_SEMESTER 6_\\MP4\\dataset\\newTrain"   # Replace with actual folder path
output_folder = "D:\\_official_\\_MIT ADT_\\_SEMESTER 6_\\MP4\\dataset\\modifyTest\\masks" # Replace with actual folder path
process_images(input_folder, output_folder)
