import time

def obtener_memoria():
    with open("/proc/meminfo", "r") as f:
        meminfo = f.readlines()

    mem_total = 0
    mem_available = 0

    for linea in meminfo:
        if "MemTotal" in linea:
            mem_total = int(linea.split()[1])  # En KB
        if "MemAvailable" in linea:
            mem_available = int(linea.split()[1])  # En KB

    porcentaje = (mem_available / mem_total) * 100
    return porcentaje

while True:
    porcentaje = obtener_memoria()
    print(f"Memoria disponible: {porcentaje:.2f}%")

    time.sleep(2)
