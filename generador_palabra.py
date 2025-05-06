import requests
import random

# Descargar lista oficial de palabras en español (fuente confiable)
url = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Spanish.dic"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    # Procesar palabras (eliminar flags y formato .dic)
    palabras = [linea.split('/')[0].strip() for linea in response.text.splitlines() if len(linea.split('/')[0].strip()) >= 3]
    palabras = list(set(palabras))  # Eliminar duplicados
    
    if len(palabras) < 1000:
        print(f"Error: Solo hay {len(palabras)} palabras disponibles")
    else:
        seleccion = random.sample(palabras, 1000)
        with open("palabras.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(seleccion))
        print("¡Archivo generado con 1000 palabras REALES del español!")

except requests.exceptions.RequestException as e:
    print("Error al descargar el diccionario:", e)