from multiprocessing import Pool
import time
import matplotlib.pyplot as plt


def sumatoria(args)->int:
    f,n = args
    sumatoria=0

    while n>f:
        sumatoria+=2*n
        n-=1

    return sumatoria

def paralelizar(n:int):
    proc_num=[4,8,16]
    suma_paralela=[]
    tiempo_paralelo=[]
    
    for num in proc_num:        
        inicio_paralelo=time.perf_counter()
        division=n//num
        rangos=[]

        for i in range(num):
            inicio = i * division
            fin = (i + 1) * division
            rangos.append((inicio, fin))

        with Pool(processes=num) as p:
            resultados = p.map(sumatoria, rangos)

        suma_total = sum(resultados)
        suma_paralela.append(suma_total)
        fin_paralelo = time.perf_counter()
        tiempo_paralelo.append(fin_paralelo - inicio_paralelo)

    return suma_paralela, tiempo_paralelo, proc_num

if __name__ == '__main__':
    N=[pow(10,5),pow(10,6),5*pow(10,6),pow(10,7),5*pow(10,7),pow(10,8),pow(10,9)]
    for n in N:
        inicio_serial=time.perf_counter()
        suma_serial=sumatoria((0,n))
        fin_serial=time.perf_counter()
        tiempo_serial=fin_serial-inicio_serial


        suma_paralela, tiempo_paralelo, proc_num=paralelizar(n)
        
        #print (suma_paralela)
        #print (suma_serial)

        for i in range(len(suma_paralela)):
            assert suma_paralela[i] == suma_serial == n*(n+1), "suma incorrecta"

        print(f"numero {n}")
        print(f"Tiempo de ejecución serial: {tiempo_serial}")

        #print(suma_paralela)
        for i in range(len(proc_num)):

            print(f"p = {proc_num[i]}, Tiempo de ejecución paralelo: {tiempo_paralelo[i]}")

        speedup=[]
        for i in range(len(proc_num)):
            resultado=tiempo_serial/tiempo_paralelo[i]
            speedup.append(resultado)
        plt.plot(proc_num,speedup)
        plt.show()