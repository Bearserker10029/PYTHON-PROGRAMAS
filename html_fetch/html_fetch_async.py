#!/usr/bin/env python3
import asyncio
import time
import re
import json
import aiohttp
from bs4 import BeautifulSoup
from collections import Counter

# ——— Configuración ———
URLS_FILE    = 'urls_html.txt'
OUTPUT_FILE  = 'html_results_async.json'
TOP_WORDS    = 10      # cuántas palabras mostrar por página
GLOBAL_TOP   = 50      # cuántas palabras guardar globalmente
CONCURRENCY  = 10      # número máximo de descargas concurrentes

async def fetch_html(session: aiohttp.ClientSession, url: str) -> str:
    """Descarga el HTML de la URL de forma asíncrona."""
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()

def analyze_html(html: str) -> (int, Counter):
    """Parses HTML, cuenta enlaces y palabras."""
    soup = BeautifulSoup(html, 'html.parser')

    # 1) contar enlaces <a href="...">
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    n_links = len(links)

    # 2) extraer texto y tokenizar
    text = soup.get_text()
    words = re.findall(r'\w+', text.lower())
    cnt = Counter(words)

    return n_links, cnt

async def process_url(sem: asyncio.Semaphore,
                      session: aiohttp.ClientSession,
                      url: str,
                      global_counter: Counter):
    """Descarga y analiza una sola URL, controlando concurrencia."""
    async with sem:
        html = await fetch_html(session, url)
    n_links, counter = analyze_html(html)
    global_counter.update(counter)
    topk = counter.most_common(TOP_WORDS)
    print(f"[ASYNC] {url} → enlaces={n_links}, top-{TOP_WORDS} palabras={topk}")

async def main():
    # Leer lista de URLs
    with open(URLS_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    global_counter = Counter()
    sem = asyncio.Semaphore(CONCURRENCY)
    start = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [
            process_url(sem, session, url, global_counter)
            for url in urls
        ]
        await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"\n[ASYNC] Tiempo total: {elapsed:.2f} s")

    # Guardar top GLOBAL_TOP palabras
    top_global = global_counter.most_common(GLOBAL_TOP)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        json.dump(top_global, out, ensure_ascii=False, indent=2)
    print(f"[ASYNC] Top {GLOBAL_TOP} palabras globales escritas en {OUTPUT_FILE}")

if __name__ == '__main__':
    asyncio.run(main())
