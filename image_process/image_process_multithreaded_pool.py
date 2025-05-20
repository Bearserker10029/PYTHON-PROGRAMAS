import os
import requests
from PIL import Image, ImageFilter
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        save_image(processed_image_data, f"./processed_images_multithread_pool/processed_image_{idx}.jpg")
    except Exception as e:
        print(f"Error al procesar {url}: {e}")

def main():
    if not os.path.exists('processed_images_multithread_pool'):
        os.mkdir('processed_images_multithread_pool')
    image_urls = read_image_urls('url_imagenes.txt')
    max_workers = 10  # Ajustar según las capacidades del sistema

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_image, idx, url): idx
            for idx, url in enumerate(image_urls,start=1)
        }

        for future in as_completed(futures):
            idx = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Imagen {idx + 1} generó una excepción: {e}")

if __name__ == "__main__":
    main()
