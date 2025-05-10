import random
from multiprocessing import Pool, cpu_count
import time
import matplotlib.pyplot as plt

def e_serial(arg):
    inicio, fin = arg
    n = fin - inicio
    suma_total=0
    for _ in range(n):
        suma=0 
        count=0
        while suma<=1:
            r=random.uniform(0,1)
            suma+=r
            count+=1
        suma_total+=count
    estimado=suma_total/n

    return estimado

def e_paralelo(n, num_cpu):
    rango=list(range(2,num_cpu+1))

    tiempo_paralelo=[]
   
    for cpu in rango:
        inicio_paralelo=time.perf_counter()
        rangos=[]
        division=n//cpu
        for i in range(cpu):
            inicio = i * division
            fin = (i + 1) * division if i < cpu - 1 else n
            rangos.append((inicio, fin))

        with Pool(processes=cpu) as p:
            resultado = p.map(e_serial, rangos)
            suma_paralela = sum(resultado)
        fin_paralelo=time.perf_counter()
        tiempo_paralelo.append(fin_paralelo-inicio_paralelo)
    return tiempo_paralelo, rango



if __name__ == '__main__':
    n=5*pow(10,7)
    num_cpu = cpu_count()
    inicio=time.perf_counter()
    estimado_serial=e_serial((0,n))
    fin=time.perf_counter()
    tiempo_serial=fin-inicio

    tiempo_paralelo, rango=e_paralelo(n,num_cpu)
    speedup=list()
    for i in range(len(tiempo_paralelo)):
        resultado=tiempo_serial/(tiempo_paralelo[i])
        speedup.append(resultado)
    plt.plot(rango,speedup)
    plt.show()
