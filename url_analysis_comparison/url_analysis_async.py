import csv
import re
from time import time
import statistics
import asyncio
import aiohttp
import matplotlib.pyplot as plt



def analyze_html(html: str):
    """
    Return a dict of basic stats for a raw HTML string.
    """
    stats = {}
    stats['char_count'] = len(html)
    stats['byte_size']  = len(html.encode('utf-8'))
    stats['line_count'] = html.count('\n') + 1
    stats['word_count'] = len(html.split())
    stats['tag_count']  = html.count('<')
    stats['link_count'] = len(re.findall(r'<a\s', html, flags=re.IGNORECASE))
    stats['img_count']  = len(re.findall(r'<img\s', html, flags=re.IGNORECASE))
    stats['h1_count']   = len(re.findall(r'<h1\b', html, flags=re.IGNORECASE))
    stats['h2_count']   = len(re.findall(r'<h2\b', html, flags=re.IGNORECASE))
    stats['p_count']    = len(re.findall(r'<p\b', html, flags=re.IGNORECASE))
    return stats

async def fetch_url(session,url: str):
    """
    Fetches the URL synchronously, records elapsed time, and returns stats.
    """
    start = time()
    try:
        async with session.get(url) as resp:
            html=await resp.text()
            analyze_html(html)
            return time() - start
    except Exception as e:
        print(f"Error: {e}")
        return None

async def worker(session, queue, results):
    while not queue.empty():
        url = await queue.get()
        elapsed = await fetch_url(session, url)
        if elapsed:
            results.append(elapsed)
        queue.task_done()

def load_csv(file_path: str):
    """
    Loads a single-column CSV (with header) of URLs.
    """
    with open(file_path,"r")as f:
        reader = csv.reader(f)
        next(reader)
        return [row[0] for row in reader if row]


async def main():

    urls = load_csv('links.csv')
    queue = asyncio.Queue()
    results = []
    N = [50, 100, 250, 500]

    for url in urls:
        await queue.put(url)

    inicio = time()
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(worker(session, queue, results)) for _ in range(10)]
        await asyncio.gather(*tasks)
    tiempo_total = time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s")

    for idx,n in enumerate(N):
        subset = results[:n]
        media = statistics.mean(subset)
        mediana = statistics.median(subset)
        desviacion = statistics.stdev(subset)
        print(f"\nN = {n}:")
        print(f"Media: {media:.4f}s")
        print(f"Mediana: {mediana:.4f}s")
        print(f"Desviación estándar: {desviacion:.4f}s")
        plt.hist(subset)
        plt.show()
    return results,tiempo_total


if __name__ == '__main__':
    data,tiempo_total=asyncio.run(main())
    print(f"Tiempo total: {tiempo_total:.2f}s")

