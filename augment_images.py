import os
import cv2
import numpy as np
import albumentations as A

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def is_image_file(fname: str) -> bool:
    return os.path.splitext(fname)[1].lower() in IMG_EXTS

def augment_one(in_path: str, out_dir: str, filename: str) -> int:
    img = cv2.imread(in_path)
    if img is None:
        print(f"[SKIP] Tidak bisa baca: {in_path}")
        return 0
    
    base, ext = os.path.splitext(filename)
    saved_count = 0
    
    augmentations = {
        "rot90": A.Rotate(limit=(90, 90), p=1.0),
        "rot180": A.Rotate(limit=(180, 180), p=1.0),
        "rot270": A.Rotate(limit=(270, 270), p=1.0),
        "hflip": A.HorizontalFlip(p=1.0),
        "bright": A.RandomBrightnessContrast(brightness_limit=(0.2, 0.5), contrast_limit=(0, 0), p=1.0),
        "contrast": A.RandomBrightnessContrast(brightness_limit=(0, 0), contrast_limit=(-0.2, 0.2), p=1.0),
        "noise": A.GaussNoise(var_limit=(0.01*255, 0.01*255), p=1.0)
    }
    
    for aug_name, augmenter in augmentations.items():
        try:
            img_aug = augmenter(image=img)['image']
            out_filename = f"{base}_{aug_name}{ext}"
            out_path = os.path.join(out_dir, out_filename)
            cv2.imwrite(out_path, img_aug)
            saved_count += 1
        except Exception as e:
            print(f"[ERROR] Gagal augmentasi {aug_name} pada {filename}: {e}")
    
    return saved_count

def augment_dir(src_dir: str, dst_dir: str):
    ensure_dir(dst_dir)
    total, saved = 0, 0
    
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        out_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        ensure_dir(out_root)
        
        for fname in sorted(files):
            if not is_image_file(fname):
                continue
            total += 1
            in_path = os.path.join(root, fname)
            saved += augment_one(in_path, out_root, fname)
    
    print(f"Selesai: {src_dir} -> {dst_dir} | {saved} file augmentasi tersimpan dari {total} file original.")

def main():
    base_path = "/home/ilmannafi/Documents/project-pbl/resize-citra"
    pairs = [
        ("sakit-resize", "sakit-augmentation"),
        ("sehat-resize", "sehat-augmentation"),
    ]
    
    for src, dst in pairs:
        src_full = os.path.join(base_path, src)
        dst_full = os.path.join(base_path, dst)
        if not os.path.isdir(src_full):
            print(f"[WARNING] Folder sumber tidak ditemukan: {src_full}")
            continue
        augment_dir(src_full, dst_full)

if __name__ == "__main__":
    main()
