import os
import threading
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
    response.raise_for_status()
    return response.content  # Devuelve los datos de la imagen en bytes

def process_image(image_data):
    # Convertir bytes a objeto PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Aplicar un filtro de nitidez intensivo en CPU
    for _ in range(10):
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Guardar la imagen procesada en bytes
    output = io.BytesIO()
    image.save(output, format='JPEG')
    return output.getvalue()  # Devuelve los datos de la imagen procesada en bytes

def save_image(image_data, filename):
    with open(filename, 'wb') as f:
        f.write(image_data)

def process_single_image(idx, url):
    print(f"Procesando imagen {idx}")
    try:
        image_data = download_image(url)
        processed_image_data = process_image(image_data)
        save_image(processed_image_data, f"./processed_images_multithread/processed_image_{idx}.jpg")
    except Exception as e:
        print(f"Error al procesar {url}: {e}")

def main():
    if not os.path.exists('processed_images_multithread'):
        os.mkdir('processed_images_multithread')
    image_urls = read_image_urls('url_imagenes.txt')
    threads = []

    for idx, url in enumerate(image_urls, start=1):
        thread = threading.Thread(target=process_single_image, args=(idx, url))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
