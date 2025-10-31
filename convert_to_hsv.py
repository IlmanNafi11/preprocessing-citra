import os
import cv2
import numpy as np

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def is_image_file(fname: str) -> bool:
    return os.path.splitext(fname)[1].lower() in IMG_EXTS

def convert_one(in_path: str, out_path: str) -> bool:
    img_bgr = cv2.imread(in_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        print(f"[SKIP] Tidak bisa baca: {in_path}")
        return False
    
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    v_channel = img_hsv[:,:,2]
    v_enhanced = clahe.apply(v_channel)
    img_hsv[:,:,2] = v_enhanced
    
    ok = cv2.imwrite(out_path, img_hsv)
    if not ok:
        print(f"[FAIL] Gagal simpan: {out_path}")
    return ok

def convert_dir(src_dir: str, dst_dir: str):
    ensure_dir(dst_dir)
    total, saved = 0, 0

    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        out_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        ensure_dir(out_root)

        for fname in files:
            if not is_image_file(fname):
                continue
            total += 1
            in_path = os.path.join(root, fname)
            base, _ = os.path.splitext(fname)
            out_path = os.path.join(out_root, base + ".jpg")
            if convert_one(in_path, out_path):
                saved += 1

    print(f"Selesai: {src_dir} -> {dst_dir} | {saved}/{total} file tersimpan.")

def main():
    base_path = "/home/ilmannafi/Documents/project-pbl/resize-citra"
    pairs = [
        ("sakit-augmentation", "sakit-hsv"),
        ("sehat-augmentation", "sehat-hsv"),
    ]
    
    for src, dst in pairs:
        src_full = os.path.join(base_path, src)
        dst_full = os.path.join(base_path, dst)
        if not os.path.isdir(src_full):
            print(f"[WARNING] Folder sumber tidak ditemukan: {src_full}")
            continue
        convert_dir(src_full, dst_full)

if __name__ == "__main__":
    main()