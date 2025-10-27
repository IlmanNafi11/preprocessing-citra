from resize_images import resize_images

def main():
    # Resize images from sakit to sakit-resize
    resize_images('sakit', 'sakit-resize')

    # Resize images from sehat to sehat-resize
    resize_images('sehat', 'sehat-resize')

    print("All images have been resized.")

if __name__ == "__main__":
    main()