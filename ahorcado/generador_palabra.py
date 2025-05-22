import requests
import random
import sys

def generar_palabras():
    url = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Spanish.dic"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        palabras = [linea.split('/')[0].strip() for linea in response.text.splitlines() if len(linea.split('/')[0].strip()) >= 3]
        palabras = list(set(palabras))  # Eliminar duplicados
        
        if len(palabras) < 1000:
            print(f"Error: Insuficientes palabras ({len(palabras)})", file=sys.stderr)
            return False
        
        seleccion = random.sample(palabras, 1000)
        with open("palabras.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(seleccion))
        return True  # Éxito

    except Exception as e:
        print(f"Error crítico: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if generar_palabras():
        print("¡Archivo generado correctamente!")
    else:
        print("Error al generar el archivo.", file=sys.stderr)