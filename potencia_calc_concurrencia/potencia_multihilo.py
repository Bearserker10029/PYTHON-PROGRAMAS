from threading import Thread
import time


N = 200_000



def calc_potencia(n: int):

    p=1
    cont=n
    while cont>0:
        p*=n
        cont -=1
    return p



if __name__ == '__main__':
    inicio = time.perf_counter()
    hilo_num=64
    hilos=[]
    for _ in range(hilo_num):
        hilo = Thread(target=calc_potencia, args=(N // hilo_num, ))
        hilo.start()
        hilos.append(hilo)

    for _ in hilos:
        hilo.join()
    fin = time.perf_counter()

    t_ejecucion = fin - inicio
    print(f"Tiempo total de ejecucio multihilo de {hilo_num} hilos: {t_ejecucion:.6f} segundos")