import sys

# Se abre el archivo en modo escritura ANTES de empezar a leer
with open("output_parte2b.txt", "w") as output_file:
    # Se itera por cada línea que entra por el teclado
    for line in sys.stdin:
        # Cada línea se escribe directamente en el archivo
        output_file.write(line)