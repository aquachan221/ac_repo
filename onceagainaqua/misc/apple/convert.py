import os
from PIL import Image
from pillow_heif import register_heif_opener

# Activate HEIC support for Pillow
register_heif_opener()

# 🔧 Folder containing HEIC images
source_folder = 'C:\\ac_repo\\onceagainaqua\\web\\static\\images'  # ← Replace this

# Loop through all files
for filename in os.listdir(source_folder):
    if filename.lower().endswith('.heic'):
        heic_path = os.path.join(source_folder, filename)
        
        # Create output filename
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        jpg_path = os.path.join(source_folder, jpg_filename)

        # Convert and save as JPEG
        image = Image.open(heic_path)
        image.save(jpg_path, format='JPEG')

        # Delete original HEIC file
        os.remove(heic_path)

        print(f"✅ Converted {filename} → {jpg_filename} and deleted the original.")