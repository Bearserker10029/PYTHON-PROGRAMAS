import sys

# 1. Verificar que el número de argumentos sea 3 (script + entrada + salida)
if len(sys.argv) != 3:
    # Imprimir un mensaje de error claro si no es correcto
    print("Error: Se requieren exactamente dos argumentos.", file=sys.stderr)
    print("Uso: python pregunta2d.py <archivo_de_entrada> <archivo_de_salida>", file=sys.stderr)
    sys.exit(1) # Terminar el programa con un código de error

# 2. Asignar los nombres de archivo a variables
archivo_entrada = sys.argv[1]
archivo_salida = sys.argv[2]

try:
    # 3. Abrir, leer y cerrar de forma segura el archivo de entrada
    with open(archivo_entrada, "r") as infile:
        contenido = infile.read()
    
    # 4. Abrir, escribir y cerrar de forma segura el archivo de salida
    with open(archivo_salida, "w") as outfile:
        outfile.write(contenido)

except FileNotFoundError:
    # 5. Capturar el error si el archivo de entrada no existe
    print(f"Error: El archivo de entrada '{archivo_entrada}' no se encontró.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    # Capturar cualquier otro error que pueda ocurrir
    print(f"Ocurrió un error: {e}", file=sys.stderr)
    sys.exit(1)
