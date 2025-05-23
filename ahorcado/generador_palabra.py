import requests
import random
import sys
import time
import os
import shutil

def procesar_linea(linea):
    palabra = linea.split('/')[0].strip().lower()
    if len(palabra) >= 3 and palabra.isalpha():
        return palabra
    return None

def generar_palabras():
    url = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Spanish.dic"
    try:
        inicio = time.time()
        
        # Descargar el diccionario
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        lineas = response.text.splitlines()

        # Procesamiento secuencial
        resultados = [procesar_linea(linea) for linea in lineas]
        palabras = list(set(filter(None, resultados)))

        if len(palabras) < 1000:
            print(f"Error: Solo hay {len(palabras)} palabras válidas.", file=sys.stderr)
            return False

        # Guardar palabras aleatorias
        with open("palabras.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(random.sample(palabras, 1000)))
        
        fin = time.time()
        print(f"¡Archivo generado correctamente en {fin - inicio:.4f} segundos!")
        return True

    except Exception as e:
        print(f"Error crítico: {e}", file=sys.stderr)
        return False

def eliminar_pycache():
    pycache_path = "__pycache__"
    if os.path.exists(pycache_path) and os.path.isdir(pycache_path):
        try:
            shutil.rmtree(pycache_path)
            print("Carpeta '__pycache__' eliminada correctamente.")
        except Exception as e:
            print(f"No se pudo eliminar '__pycache__': {e}", file=sys.stderr)

if __name__ == "__main__":
    if generar_palabras():
        eliminar_pycache()
