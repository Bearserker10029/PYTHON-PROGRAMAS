#Operaciones con matrices

########################
#Traspone una matriz Mt
def trasponer(M):
    R=[]
    for j in range (len(M[0])):
        R.append([])
        for i in range (len(M)):
            R[j].append(M[i][j])
    return(R)

#Complejo conjugado de una matriz M*
def conjugar(M):
    R=[]
    for i in range (len(M)):
        R.append([])
        for j in range (len(M[0])):
            R[i].append((M[i][j]).conjugate())
    return(R)

#Menor i,j de la matriz M
def menor(M,i,j):
    R=[]
    if (len(M)) > 1:
        fila = -1
        for k in range (len(M)):
            if k != i:
                fila += 1
                R.append([])
                for l in range (len(M[0])):
                    if l != j:
                        R[fila].append(M[k][l])
        return(R)
    else:
        return(1) # si tiene una sola fila retorna 1 (sirve para determinante)

#Determinante de una matriz M                             
def determinante(M):
    if len(M)==len(M[0]): #Deben ser de igual cant filas y col
        d = M[0][0]
        if (len(M[0])) > 1:
            d = 0
            for j in range (len(M[0])):
                signo=(-1)**(j)
                d += M[0][j]*signo * determinante(menor(M,0,j))
        return(d)
    else:
        return(0)

#Inversa de una matriz M
# calcula M^-1 = (1/determinante(M))*((M adjunta)traspuesta)
def inversa(M):
    d = determinante(M)
    if d != 0:
        R=[]
        for i in range (len(M)):
            R.append([])
            for j in range (len(M[0])):
                signo=(-1)**(i+j)
                R[i].append(signo * determinante(menor(M,i,j)) / d)
        R = trasponer(R)        
        return(R)
    else:
        return(0)

#Multiplica una matriz por un escalar M*a
def escalar(M, a):
    R=[]
    for i in range (len(M)):
        R.append([])
        for j in range (len(M[0])):
            R[i].append(M[i][j]*a)
    return(R)

#Suma 2 matrices M+N
def sumar(M, N):
    if len(M)==len(N) and len(M[0])==len(N[0]): #Deben ser de igual cant filas y col
        R=[]
        for i in range (len(M)):
            R.append([])
            for j in range (len(M[0])):
                R[i].append(M[i][j]+N[i][j])
        return(R)
    else:
        return(0)

#Multiplica 2 matrices M*N
def multiplicar(M, N):
    if len(M[0])==len(N): #Debe ser cantidad de col de M = cant filas de N
        R=[]
        for i in range (len(M)):
            R.append([])
            for j in range (len(N[0])):
                p=0
                for k in range (len(M[0])):
                    p += M[i][k]*N[k][j]
                R[i].append(p)
        return(R)
    else:
        return(0)

#Producto tensorial de 2 matrices MxN
def tensorial(M, N):
    filM = len(M)
    colM = len(M[0])
    filN = len(N)
    colN = len(N[0])
    R=[]

    for i in range (filM):
        for k in range (filN):
            R.append([])
            for j in range (colM):
                for l in range (colN):
                    R[filN*i+k].append(M[i][j]*N[k][l])
    return(R)

#Muestra una matriz M con nombre (opcional)
def vermatriz(M, nombre=""):
    if len(nombre)>0:
        print(nombre, "=")
    print("[")
    for i in range (len(M)):
        print(" ",M[i])
    print("]")
    return

#Muestra una matriz M con formato según Complejo, Real o Entero
#con hasta 3 dec, justificada a izq 15 espacios y nombre (opcional)
def vermatrizf(M, nombre=""):
    ancho = 15                  #matriz con Complejos
    Ms = str(M)
    if "j" not in Ms:           #matriz con Reales
        ancho = 8
        if "." not in Ms:
            ancho = 4           #matriz con Enteros
        
    if len(nombre)>0:
        print(nombre, "=")
    print("[")
    for i in range (len(M)):
        print(" [", end="")
        for j in range (len(M[0])):
            if ancho == 4:
                print ("{0:4d}".format(M[i][j]), end="")
            else:    
                print(str(" {0:.3f}".format(M[i][j])).ljust(ancho), end="")
        print(" ]")
    print("]")
    return

#Ingresa una matriz de filas x columnas
# permite complejos, ingresarlos como: RE+IMj
def ingresar(filas, columnas):
    R=[]
    for f in range (filas):
        R.append([])
        for c in range (columnas):
            p = complex(input(" "+str(f)+" "+str(c)+"= "))
            R[f].append(p)
    vermatriz(R)
    return(R)

#Guarda una matriz en un archivo en disco
def guardar(matriz, archivo):
    with open(archivo, 'w') as f:
        matriz_txt = str(matriz)
        f.write(matriz_txt)
    return

#Lee una matriz de un archivo en disco
def leer(archivo):
    with open(archivo, 'r') as f:
        matriz_txt=f.read()
        matriz = eval(matriz_txt)
    return(matriz)   


########################
        
#A=[[1,2],[3,4]]
#B=[[1.1,2.2],[30,40]]
#C=[[3j, -4j], [5, 6+2.2j]]
#D=[[1+3j, 2], [3, 4+2.2j]]
#n=2

#S=sumar(A,B)
#print ("Suma de ", A, " + ", B, " = ", S)

#E=escalar(A,n)
#print ("Producto de ", A, " x ", n, " = ", E)

#P=multiplicar(A,B)
#print ("Producto de ", A, " * ", B, " = ", P)

#T=tensorial(A,B)
#print ("Producto tensorial de ", A, " x ", B, " = ")
#print (T)

#Escribe archivo
#A="[[(1.5+0j), (2+2j)], [(1+0j), (3.1+0.2j)]]"
#guardar(A, 'pruebaGuardar')

#Lee desde archivo
#print(leer('pruebaGuardar'))



