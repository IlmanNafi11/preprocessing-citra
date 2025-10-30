import subprocess
import sys
import os

def main():
    venv_python = os.path.join(os.getcwd(), 'venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        print("Virtual environment tidak ditemukan. Membuat venv...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        subprocess.run([os.path.join('venv', 'bin', 'pip'), 'install', '-r', 'requirements.txt'])
        venv_python = os.path.join(os.getcwd(), 'venv', 'bin', 'python')

    print("Menjalankan rename_files.py...")
    subprocess.run([venv_python, 'rename_files.py'])

    print("Menjalankan resize_images.py...")
    subprocess.run([venv_python, 'resize_images.py'])

    print("Menjalankan convert_to_hsv.py...")
    subprocess.run([venv_python, 'convert_to_hsv.py'])

    print("Menjalankan remove_background.py...")
    subprocess.run([venv_python, 'remove_background.py'])

    print("Semua proses selesai.")

if __name__ == "__main__":
    main()