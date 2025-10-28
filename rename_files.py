import os

def rename_files(directory, prefix):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()
    for i, file in enumerate(files):
        name, ext = os.path.splitext(file)
        new_name = f"{prefix}_{i}{ext}"
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")

def main():
    base_path = "/home/ilmannafi/Documents/project-pbl/resize-citra"
    rename_files(os.path.join(base_path, "sakit"), "sakit")
    rename_files(os.path.join(base_path, "sehat"), "sehat")

if __name__ == "__main__":
    main()