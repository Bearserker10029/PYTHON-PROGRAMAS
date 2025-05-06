from random import randint
import time
import os
from typing import Union



def carga_palabras(ruta: str = "palabras.txt", sep: str = "\n") -> list[str]:
    """
    Carga las palabras de la lista de palabras especificada en la ruta. Se puede incluir el separador que se debe utilizar.
    :param ruta: string que contiene la ruta del archivo que vamos a leer.
    :param sep: string que contiene el caracter separador para extraer las palabras.
    :returns: lista de strings que representa todas las palabras que el juego puede tener.
    """
    with open(ruta, "r") as f:
        contenido = f.read()
    lista = contenido.split(sep)
    return lista


def actualiza_puntaje(lp: list[str], fallos: int) -> None:
    """
    Imprime el puntaje actual en el terminal con la lista de letras actualizada y el puntaje (cantidad de fallos) actualizada.
    :param lp: Lista que representa las letras de la palabra, con las letras adivinadas siendo mostradas.
    :param fallos: Cantidad de fallos que todavia el usuario puede cometer.
    :returns: None
    """
    print(f"{' '.join(lp)} - Itentos: {fallos}")


def lee_letra() -> str:
    """
    Lee una letra por teclado, valida que el ingreso sea un unico caracter, si no es asi solicita se ingrese de nuevo hasta que la condicion se cumpla.
    :returns: String representando el caracter
    """

    while True:
        letra = input("Por favor ingrese una letra o palabra: ").lower()
        entrada_sin_espacios = ""
        for c in letra:
            if c != " ":
                entrada_sin_espacios += c
        if entrada_sin_espacios:
            return entrada_sin_espacios


def busca_letra(p: str, l: str, lp: list[str]) -> Union[list[str], bool]:
    """
    Busca la letra especificada dentro de la palabra para saber si se encuentra dentro de ella. Si se encuentra, 
    se reemplaza en la lista de strings el caracter '_' con la letra correspondiente, en la posicion correspondiente.
    :param p: string que representa a la palabra sobre la cual se hace la busqueda.
    :param l: string que representa a la letra que se va a buscar
    :param lp: lista de strings que representa a la palabra separada con cada caracter de esta siendo un elemento de la lista. Originalmente todos los caracteres estan escondidos ('_')
    :returns: lista de strings que representa a lista de la palabra actualizada y una bandera booleana indicando si la letra se encuentra en la palabra o no.
    """
    letra_encontrada = False

    for idx in range(len(p)):
        if l == p[idx]:
            lp[idx] = l
            letra_encontrada = True
    return lp, letra_encontrada


# palabras = ["arquitectura", "computadoras", "telecomunicaciones", "python", "ahorcado", "universidad", "alumnos", "perro", "proyector"]
if not os.path.exists("palabras.txt"):
    print("Error: palabras.txt no existe.")
    exit()
palabras = carga_palabras(ruta="palabras.txt", sep="\n")

cant_adiv=input("Cantidad de letras a adivinar:") 
palabras_filtradas=[]
for p in palabras:
    if cant_adiv == "" or len(p) == int(cant_adiv):
        palabras_filtradas.append(p)
if not palabras_filtradas:
    print("No hay palabras con esa longitud!")
    exit()

palabra=palabras_filtradas[randint(0, len(palabras_filtradas)-1)]
palabras.remove(palabra) 
with open("palabras.txt", "w") as f:
        f.write("\n".join(palabras))

lista_palabra = ["_"] * len(palabra)
intentos = 5
letras_adivinadas= []
letras_ingresadas = []


if __name__ == '__main__':
    status = ""
    inicio = time.perf_counter()
    intentos_adivinar=0

    while True:
        actualiza_puntaje(lista_palabra, intentos)
        entrada= lee_letra()
        
        if len(entrada) == len(palabra):
            if entrada == palabra:
                print("¡Ganaste! 🎉")
                status = "gano"
                lista_palabra = list(palabra)
            else:
                print("¡Perdiste! 😔")
                status = "perdio"
                intentos = 0
            break

        letra = entrada[0]
        if letra in letras_ingresadas:
            print("Letra ya ingresada!")
            continue
        letras_ingresadas.append(letra)
        
        lista_palabra, resultado= busca_letra(palabra, letra, lista_palabra)
        
        if resultado:
            letras_adivinadas.append(letra)
        
        if not resultado:
            print("La letra ingresada no se encuentra dentro de la palabra.")
            intentos -= 1

        if intentos == 0:
            print("Lo siento ha perdido el juego 😔")
            status = "perdio"
            break

        if "_" not in lista_palabra:
            print("Felicitaciones! Ha ganado el juego 🎉")
            status = "gano"
            break

        intentos_adivinar+=1
    fin = time.perf_counter()
    duracion = fin - inicio
    intentos_fallidos=intentos
    stat = f"{palabra},{status},{duracion},{intentos_adivinar+1},{intentos_fallidos+1},{''.join(letras_adivinadas)}\n"

    with open("stats.csv", "a") as f:
        f.write(stat)