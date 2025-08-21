import string
import random
import csv
import os

def generar_contrasena(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    
    if longitud > 4:
        mayuscula = random.choice(string.ascii_uppercase)
        minuscula = random.choice(string.ascii_lowercase)
        numero = random.choice(string.digits)
        simbolo = random.choice(string.punctuation)
        
        resto = [random.choice(caracteres) for _ in range(longitud - 4)]
        
        contrasena = list(mayuscula + minuscula + numero + simbolo + "".join(resto))
        random.shuffle(contrasena)
        return "".join(contrasena)
    else:
        return "".join(random.choice(caracteres) for _ in range(longitud))


def guardar_en_csv(plataforma, usuario, contrasena, archivo="contraseñas.csv"):
    datos = []
    encontrado = False

    # Si el archivo existe, lo leemos
    if os.path.isfile(archivo):
        with open(archivo, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            datos = list(reader)

        # Buscar encabezado
        if datos and datos[0] == ["Plataforma", "Usuario", "Contraseña"]:
            start_idx = 1
        else:
            # Si no hay encabezado, lo agregamos luego
            datos.insert(0, ["Plataforma", "Usuario", "Contraseña"])
            start_idx = 1

        # Buscar si ya existe la plataforma y usuario
        for row in datos[start_idx:]:
            if row[0] == plataforma and row[1] == usuario:
                row[2] = contrasena  # Modificar contraseña
                encontrado = True
                break

    # Si no existe, lo añadimos
    if not encontrado:
        datos.append([plataforma, usuario, contrasena])

    # Reescribir el archivo
    with open(archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(datos)


# --- Programa principal ---
longitud = int(input("Ingrese el tamaño de la contraseña: "))
plataforma = input("Ingrese la plataforma: ")
usuario = input("Ingrese el usuario: ")

contrasena = generar_contrasena(longitud)
print("\nLa contraseña generada es:", contrasena)

opcion = input("¿Quieres cambiar la contraseña? (s/n): ").lower()
if opcion == "s":
    contrasena = input("Ingrese su nueva contraseña: ")

guardar_en_csv(plataforma, usuario, contrasena)
print("\n✅ Datos guardados/modificados en 'contraseñas.csv'")
