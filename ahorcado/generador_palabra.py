import requests
import random
import sys
from concurrent.futures import ProcessPoolExecutor

def procesar_linea(linea):
    palabra = linea.split('/')[0].strip().lower()
    if len(palabra) >= 3 and palabra.isalpha():
        return palabra
    return None

def generar_palabras():
    url = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Spanish.dic"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        lineas = response.text.splitlines()
        
        # Procesamiento paralelo
        with ProcessPoolExecutor() as executor:
            resultados = list(executor.map(procesar_linea, lineas))
        
        # Filtrar y eliminar duplicados
        palabras = list(set([p for p in resultados if p is not None]))
        
        if len(palabras) < 1000:
            print(f"Error: Solo hay {len(palabras)} palabras válidas.", file=sys.stderr)
            return False
        
        # Selección aleatoria y escritura
        with open("palabras.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(random.sample(palabras, 1000)))
            
        return True

    except Exception as e:
        print(f"Error crítico: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if generar_palabras():
        print("¡Archivo generado correctamente!")
    else:
        print("Error al generar el archivo.", file=sys.stderr)