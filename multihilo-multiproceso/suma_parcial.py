from multiprocessing import Process, Array


def suma_parcial(arr, inicio, fin, idx)->int:

    ### Completar: Implementar la suma parcial
    # CODIGO
    ###

    #Inicio la suma parcial en 0

    suma_part=0
    #Hallo suma de cuadrados  en un rango
    while fin>inicio:
        suma_part+=fin**2
        fin-=1
        
    #Guardo el resultado en un array
    arr[idx]=suma_part


if __name__ == "__main__":
    compartido = Array('i', 8)  # 8 espacios para 8 resultados parciales
    
    #Creo una lista de la cantidad de procesos

    procesos = list(range(8))
    #print(procesos)
    N = 1000
    bloque = N // 8  # = 25
    ### Completar: Implementar la suma de los 8 procesos
    # CODIGO
    ###
    suma=list()

    # Creo los procesos y los rangos que se requieran


    for p in procesos:
        inicio=bloque*p
        fin=bloque*(p+1)
        p=Process(target=suma_parcial,args=(compartido,inicio,fin,p))
        p.start()
        p.join()
        #print(compartido[:])

    #Imprimo los arrays
    suma=compartido[:]

    ### Completar: Implementar la suma total
    suma_total = sum(suma)
    ###
    
    print(f"Suma total de cuadrados del 1 al 1000: {suma_total}")