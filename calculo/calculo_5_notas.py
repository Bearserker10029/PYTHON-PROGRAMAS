import sys

numero1= int(sys.argv[1])
numero2= int(sys.argv[2])
numero3= int(sys.argv[3])
numero4= int(sys.argv[4])
numero5= int(sys.argv[5])

#ponerlos en un rango
numeros=[numero1,numero2,numero3,numero4,numero5]

#ordenar numeros
for i in range (4):
    for j in range (4-i):
        if numeros[j]>numeros[j+1]:
            numero_copia=numeros[j]
            numeros[j]=numeros[j+1]
            numeros[j+1]=numero_copia
print(numeros)

#promedio
sumadenumeros=sum(numeros)
promedio=(sumadenumeros-numeros[0])/4
print(f"El promedio es: {promedio}\n")
print(f"La mediana es: {numeros[2]}\n")