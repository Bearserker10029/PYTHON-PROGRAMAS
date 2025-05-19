import os
import requests
from PIL import Image, ImageFilter
import io

def read_image_urls(file_path):
    with open(file_path, 'r') as f:
        image_urls = [line.strip() for line in f if line.strip()]

    image_urls = image_urls * 1
    return image_urls

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return Image.open(io.BytesIO(response.content))

def process_image(image):
    # Apply a computationally intensive filter
    for _ in range(10):  # Increase the range for more CPU load
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    return image

def save_image(image, filename):
    image.save(filename)

def main():
    # I/O-bound operation: Read image URLs from a text file
    image_urls = read_image_urls('url_imagenes.txt')

    for idx, url in enumerate(image_urls):
        print(f"Processing image {idx+1}/{len(image_urls)}")

        try:
            # I/O-bound operation: Download the image
            image = download_image(url)

            # CPU-bound operation: Process the image
            processed_image = process_image(image)
            
            # check if the directory exists
            if not os.path.exists('processed_images_sync'):
                os.makedirs('processed_images_sync')
            
            # I/O-bound operation: Save the processed image
            save_image(processed_image, f"./processed_images_sync/processed_image_{idx+1}.jpg")

        except Exception as e:
            print(f"Failed to process {url}: {e}")

if __name__ == "__main__":
    main()
