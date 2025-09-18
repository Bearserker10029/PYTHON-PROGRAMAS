# ADVERTENCIA: Este script está diseñado para funcionar únicamente en sistemas Linux.

try:
    # Se abre el archivo especial del sistema de procfs.
    with open("/proc/cpuinfo", "r") as f:
        # Se inicializa el contador en 0.
        procesadores = 0
        # Se lee cada línea del archivo.
        for line in f:
            # Si la línea, sin espacios, comienza con la palabra "processor",
            # se incrementa el contador.
            if line.strip().startswith("processor"):
                procesadores += 1
    
    print(f"Cantidad de procesadores: {procesadores}")

except FileNotFoundError:
    print("Error: Este script solo es compatible con sistemas Linux,")
    print("ya que el archivo /proc/cpuinfo no fue encontrado.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
