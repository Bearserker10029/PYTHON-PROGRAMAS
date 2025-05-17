from threading import Thread
import time
from random import randint


saldo = 10000

def retirar(cantidad):
    global saldo
    ### Completar: Verificar si hay saldo suficiente, restar el monto y simular tiempo de espera
    # CODIGO
    ###
    # Comparar si hay saldo para retirar
    if saldo>=cantidad:
        time.sleep(randint(0,1))
        saldo-=cantidad
        
    

if __name__ == '__main__':
    '''Creo los hilos'''
    hilos = f"{','.join([f'hilo {idx + 1}' for idx in range(15)])}".split(",")

    #print(hilos)
    ### Completar: Simular 15 retiros utilizando hilos. Considerar retiros de 100 soles por cada hilo
    # CODIGO
    cantidad=100
    ###
    threads=list()
    #Crear los hilos
    for hilo in hilos:

        hilo=Thread(target=retirar, args=(cantidad,))
        hilo.start()
        threads.append(hilo)

    for t in threads:
        hilo.join()

    print(f"Saldo final: {saldo}")