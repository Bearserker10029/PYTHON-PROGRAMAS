import asyncio
import os
import aiohttp
import aiofiles
from PIL import Image, ImageFilter
import io

def read_image_urls(file_path):
    with open(file_path, 'r') as f:
        image_urls = [line.strip() for line in f if line.strip()]

    image_urls = image_urls * 1
    return image_urls

async def download_image(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        content = await response.read()
        return content  # Devuelve los datos de la imagen en bytes

def process_image(image_data):
    # Convert bytes data to PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Apply a computationally intensive sharpening filter
    for _ in range(10):
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Save processed image to bytes
    output = io.BytesIO()
    image.save(output, format='JPEG')
    return output.getvalue()  # Return processed image data as bytes

async def save_image(image_data, filename):
    async with aiofiles.open(filename, 'wb') as f:
        await f.write(image_data)

async def process_single_image(idx, url, session):
    print(f"Processing image {idx}")
    try:
        # I/O-bound operation: Download the image asynchronously
        image_data = await download_image(session, url)

        # CPU-bound operation: Process the image (this will block the event loop)
        processed_image_data = process_image(image_data)

        # I/O-bound operation: Save the processed image asynchronously
        await save_image(processed_image_data, f"./processed_images_async/processed_image_{idx}.jpg")

    except Exception as e:
        print(f"Failed to process {url}: {e}")

async def main():
    if not os.path.exists('processed_images_async'):
        os.mkdir('processed_images_async')
    # Read image URLs from the text file
    image_urls = read_image_urls('url_imagenes.txt')

    # Create an aiohttp session for making HTTP requests
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks for asyncio.gather
        tasks = [
            process_single_image(idx, url, session)
            for idx, url in enumerate(image_urls,start=1)
        ]

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
