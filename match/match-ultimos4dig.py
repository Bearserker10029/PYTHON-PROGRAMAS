import os
import time

def buscar_codigo(codigo: str):
    inicio_total = time.perf_counter()
    
    # Procesar archivos del 1 al 50
    for i in range(1, 51):
        nombre_archivo = f"archivo{i}.csv"
        
        if not os.path.exists(nombre_archivo):
            print(f"Archivo {nombre_archivo} no encontrado")
            continue

        inicio_archivo = time.perf_counter()
        contador = 0
        
        with open(nombre_archivo, "r") as f:
            for linea in f:
                cadena = ""

                for caracter in linea:
                    if '0' <= caracter <= '9':
                        cadena += caracter
                # Buscar coincidencia
                if codigo in cadena:
                    contador += 1
        
        tiempo_archivo = time.perf_counter() - inicio_archivo
        print(f"Archivo: {nombre_archivo}, Coincidencias: {contador}, Tiempo: {tiempo_archivo:.2f}s")
    
    tiempo_total = time.perf_counter() - inicio_total
    print(f"\nTiempo total de ejecución: {tiempo_total:.2f}s")

if __name__ == "__main__":
    codigo_completo = ""
    while True:
        codigo_completo = input("Ingrese su código de 8 dígitos: ")
        es_valido = len(codigo_completo) == 8
        
        if es_valido:
            for c in codigo_completo:
                if not ('0' <= c <= '9'):
                    es_valido = False
                    break
        
        if es_valido:
            break
        print("Error: Debe ser un código de 8 dígitos numéricos.")
    
    # Extraer últimos 4 dígitos
    codigo_busqueda = codigo_completo[-4:]
    buscar_codigo(codigo_busqueda)