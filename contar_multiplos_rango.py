import sys

numero= int(sys.argv[1])
lim_inf= int(sys.argv[2])
lim_sup= int(sys.argv[3])

if lim_inf > lim_sup:
    print("Error: El límite inferior no puede ser mayor al superior.")
    exit()

contador = 0
for n in range(lim_inf, lim_sup + 1):
    if n % numero == 0:
        contador += 1

print(f"Hay {contador} múltiplos de {numero} en este rango")
