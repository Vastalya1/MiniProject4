import os
import time
import exiftool

# Set directory and new date
directory = r"D:\Random_coding\images"  # Change this to your directory path
new_date = "2004:08:09 12:00:00"  # Format: YYYY:MM:DD HH:MM:SS
new_timestamp = int(time.mktime(time.strptime(new_date, "%Y:%m:%d %H:%M:%S")))  # Convert to UNIX timestamp

# Define supported formats
image_extensions = (".jpg", ".jpeg", ".png", ".tiff", ".tif", ".heic")
video_extensions = (".mp4", ".mov", ".avi", ".mkv", ".hevc")

# Get list of image and video files
media_files = [os.path.join(directory, f) for f in os.listdir(directory)
               if f.lower().endswith(image_extensions + video_extensions)]

# Modify metadata and file timestamps
with exiftool.ExifTool() as et:
    for media in media_files:
        if media.lower().endswith(image_extensions):
            # Update EXIF metadata
            et.execute(
                b"-AllDates=" + new_date.encode(),
                b"-DateTimeOriginal=" + new_date.encode(),
                b"-CreateDate=" + new_date.encode(),
                b"-ModifyDate=" + new_date.encode(),
                media.encode()
            )
        
        elif media.lower().endswith(video_extensions):
            # Update EXIF metadata for videos
            et.execute(
                b"-CreateDate=" + new_date.encode(),
                b"-ModifyDate=" + new_date.encode(),
                b"-TrackCreateDate=" + new_date.encode(),
                b"-TrackModifyDate=" + new_date.encode(),
                media.encode()
            )

        # ✅ **Update file system timestamps (Date Created & Date Modified)**
        os.utime(media, (new_timestamp, new_timestamp))  # (access_time, modified_time)
        print(f"✅ Updated: {media}")

print("\n🎉 Metadata and file timestamps updated successfully!")
