import time


N = 200_000

def calc_potencia(n: int)->int:

    p=1
    cont=n
    while cont>0:
        p*=n
        cont -=1
    return p


if __name__ == '__main__':
    inicio = time.perf_counter()
    calc_potencia(N)
    fin = time.perf_counter()

    t_ejecucion = fin - inicio
    print(f"Tiempo total de ejecucion sincrono: {t_ejecucion:.6f} segundos")