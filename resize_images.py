import os
from PIL import Image

def resize_images(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            img_path = os.path.join(source_dir, filename)
            try:
                img = Image.open(img_path)
                img_resized = img.resize((224, 224))
                dest_path = os.path.join(dest_dir, filename)
                img_resized.save(dest_path)
                print(f"Resized and saved: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")