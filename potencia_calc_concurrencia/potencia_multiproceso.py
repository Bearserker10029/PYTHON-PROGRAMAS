from multiprocessing import Process
import time

N = 200_000

def calc_potencia(n: int) -> int:

    p=1
    cont=n

    while cont>0:
        p*=n
        cont -=1
    return p


if __name__ == '__main__':
    inicio = time.perf_counter()
    proc_num=64
    procesos=[]
    for _ in range(proc_num):
        proceso = Process(target=calc_potencia, args=(N // proc_num, ))
        proceso.start()
        procesos.append(proceso)

    for proceso in procesos:
        proceso.join()

    fin = time.perf_counter()

    t_ejecucion = fin - inicio
    print(f"Tiempo total de ejecucion de {proc_num} procesos: {t_ejecucion:.6f} segundos")