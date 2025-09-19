import sys

# Se comprueba si se ha pasado más de un argumento
# (el primero es siempre el nombre del script).
if len(sys.argv) > 1:
    # Si hay un argumento, se usa como nombre de archivo.
    nombre_archivo = sys.argv[1]
    with open(nombre_archivo, "w") as archivo_salida:
        for line in sys.stdin:
            archivo_salida.write(line)
else:
    # Si no hay argumentos, se escribe en la salida estándar (terminal).
    for line in sys.stdin:
        sys.stdout.write(line)
