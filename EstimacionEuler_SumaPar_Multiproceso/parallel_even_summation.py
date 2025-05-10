from multiprocessing import Pool
import time
import matplotlib.pyplot as plt

def sumatoria(n: int)->int:
    n_par=0
    sumatoria=0

    while n>0:
        n_par=2*n
        sumatoria+=n_par
        n-=1

    return sumatoria

def doble(i: int) -> int:
    return 2 * i

def paralelizar(n:int):
    proc_num=[4,8,16]
    suma_paralela=[]
    tiempo_paralelo=[]
    
    for num in proc_num:        
        inicio_paralelo=time.perf_counter()
        with Pool(processes=num) as p:
            resultado = p.map(doble,range(1,n+1))
            suma=sum(resultado)
        fin_paralelo=time.perf_counter()

        suma_paralela.append(suma)
        tiempo_paralelo.append(fin_paralelo-inicio_paralelo)
    return suma_paralela, tiempo_paralelo, proc_num

if __name__ == '__main__':
    N=[pow(10,5),pow(10,6),5*pow(10,6),pow(10,7),5*pow(10,7),pow(10,8),pow(10,9)]
    for n in N:
        inicio_serial=time.perf_counter()
        suma_serial=sumatoria(n)
        fin_serial=time.perf_counter()
        tiempo_serial=fin_serial-inicio_serial


        suma_paralela, tiempo_paralelo, proc_num=paralelizar(n)
        
        print(suma_paralela)
        print (suma_serial)


        assert all(s == suma_serial for s in suma_paralela) and suma_serial == n*(n+1), "suma incorrecta"

        print(f"numero {n}")
        print(f"Tiempo de ejecución serial: {tiempo_serial}")

        print(suma_paralela)
        for i in range(len(proc_num)):

            print(f"p = {proc_num[i]}, Tiempo de ejecución paralelo: {tiempo_paralelo[i]}")

        speedup=[]
        for i in range(len(proc_num)):
            resultado=tiempo_serial/tiempo_paralelo[i]
            speedup.append(resultado)
        plt.plot(proc_num,speedup)
        plt.show()