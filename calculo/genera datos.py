import random
N=500

def generadatos():
    with open("datos.csv","w+") as f:
        lista=[str(random.randint(0,50)) for _ in range(N)]
        # print(lista)
        f.write(",".join(lista))

if __name__=="__main__":
    generadatos()
    """     with open("datos.csv","r") as f:
            contenido=f.read()
        numeros = [int(valor) for valor in contenido.split(",")]
        promedio=sum(numeros)/len(numeros)
        print(promedio) """