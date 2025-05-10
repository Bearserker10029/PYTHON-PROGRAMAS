import csv
import re
from time import time
from urllib.request import urlopen, Request
import statistics
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

def fetch_url(url: str):
    """
    Fetches the URL synchronously, records elapsed time, and returns stats.
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as resp:
        html_bytes = resp.read()
    html = html_bytes.decode('utf-8', errors='replace')
    return analyze_html(html)

def load_csv(file_path: str):
    """
    Loads a single-column CSV (with header) of URLs.
    """
    urls = []
    with open("links.csv", "r") as f:
    #Completar función
        contenido=csv.reader(f)
        next(contenido)
        for dato in contenido:
            urls.append(dato[0])
    return urls

def main():
    urls = load_csv('links.csv')
    results = []
    N=[50,100,250,500]
    for url in urls:
        try:
            inicio=time()
            stats = fetch_url(url)
            results.append(time()-inicio)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            stats = None
    data=[]
    for i in N:
        elementos_50=results[:i]
        media_50 = statistics.mean(elementos_50)
        mediana_50 = statistics.median(elementos_50)
        desviacion_estandar_50 = statistics.stdev(elementos_50) if len(elementos_50) > 1 else 0
        data.append((media_50, mediana_50, desviacion_estandar_50))

    return data,results,N,tiempo

if __name__ == '__main__':
    inicio=time()
    data,result,N=main()
    print(f"Tiempo total: {time() - inicio}")

    for idx, (media, mediana, desviacion) in enumerate(data):
        print(f"\nN = {N[idx]}:")
        print(f"Media: {media:.4f}s | Mediana: {mediana:.4f}s | Desviación: {desviacion:.4f}s")

    plt.hist(result)
    plt.show()