import asyncio
import random

PRECIO_MINIMO = 20000   #El precio base al que se inicia la subasta
PRECIO_MAXIMO = 100000  #El precio maximo que cualquiera de los participantes está dispuesto a pagar(úselo como tope en random.randint()

async def ofertar(participante):
	await asyncio.sleep(random.randint(0,10))
	listaMontos[int(ord(participante))-97]=random.randint(PRECIO_MINIMO,PRECIO_MAXIMO)
	
async def main():
	await asyncio.gather(ofertar('a'),ofertar('b'),ofertar('c'),ofertar('d'),ofertar('e'))
	print("Ofertas finales: {'a':",listaMontos[0],",'b':",listaMontos[1],",'c':",listaMontos[2],",'d':",listaMontos[3],",'e':",listaMontos[4],"}\nEl ganador es: ",chr(posicionGanador(listaMontos)+97))
	
def posicionGanador(listaMontos):
	mayor=0
	for i in range(len(listaMontos)):
		if listaMontos[i]>=mayor:
			mayor=listaMontos[i]
			posicionMayor=i
	return posicionMayor

if __name__ == "__main__":
	listaMontos=[0,0,0,0,0]
	asyncio.run(main())