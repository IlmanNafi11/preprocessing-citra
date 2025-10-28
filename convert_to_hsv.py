import os
import cv2

# Folder sumber → folder tujuan
PAIRS = [
    ("sakit-resize", "sakit-hsv"),
    ("sehat-resize", "sehat-hsv"),
]

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def is_image_file(fname: str) -> bool:
    return os.path.splitext(fname)[1].lower() in IMG_EXTS

def convert_one(in_path: str, out_path: str) -> bool:
    bgr = cv2.imread(in_path, cv2.IMREAD_COLOR)
    if bgr is None:
        print(f"[SKIP] Tidak bisa baca: {in_path}")
        return False
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    ok = cv2.imwrite(out_path, hsv)
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
            out_path = os.path.join(out_root, base + ".png")
            if convert_one(in_path, out_path):
                saved += 1

    print(f"Selesai: {src_dir} -> {dst_dir} | {saved}/{total} file tersimpan.")

def main():
    base_path = "/home/ilmannafi/Documents/project-pbl/resize-citra"
    for src, dst in PAIRS:
        src_full = os.path.join(base_path, src)
        dst_full = os.path.join(base_path, dst)
        if not os.path.isdir(src_full):
            print(f"[WARNING] Folder sumber tidak ditemukan: {src_full}")
            continue
        convert_dir(src_full, dst_full)

if __name__ == "__main__":
    main()