import sys

# Verificar que se pasaron los argumentos correctos
print(sys.argv)
for i in sys.argv:
    print(i)
if len(sys.argv) != 3:
    print("Uso: python suma.py <numero1> <numero2>")
    sys.exit(1)

# Obtener los números de los argumentos
numero1 = int(sys.argv[1])
numero2 = int(sys.argv[2])

# Sumar los números
suma = numero1 + numero2

# Mostrar el resultado
print(f"La suma de {numero1} y {numero2} es: {suma}")