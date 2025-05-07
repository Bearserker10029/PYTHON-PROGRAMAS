import asyncio
import random

PRECIO_MINIMO = 20000   #El precio base al que se inicia la subasta

async def ofertar(participante):
    while True:
        await asyncio.sleep(random.randint(0,11))
        valorSubastaActual=max(listaMontos)
        if (listaMontos[int(ord(participante))-97]<valorSubastaActual or listaMontos[int(ord(participante))-97]==(PRECIO_MINIMO)) and random.randint(0,1):
            listaMontos[int(ord(participante))-97]=random.randint(valorSubastaActual+500,int((valorSubastaActual+500)*1.2)+1)
            print(f"Participante {participante} hizo reoferta de {listaMontos[int(ord(participante))-97]}")
	
async def main():
	await asyncio.wait_for(asyncio.gather(ofertar('a'),ofertar('b'),ofertar('c'),ofertar('d'),ofertar('e')),timeout=60)
	    	
def posicionGanador(listaMontos):
	mayor=0
	for i in range(len(listaMontos)):
		if listaMontos[i]>=mayor:
			mayor=listaMontos[i]
			posicionMayor=i
	return posicionMayor

if __name__ == "__main__":
    listaMontos=[PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO]
    try:
        asyncio.run(main())
    except asyncio.exceptions.TimeoutError:
        print("Se cumplió el tiempo de 60 segundos.\nOfertas finales: {'a':",listaMontos[0],",'b':",listaMontos[1],",'c':",listaMontos[2],",'d':",listaMontos[3],",'e':",listaMontos[4],"}\nEl ganador es: ",chr(posicionGanador(listaMontos)+97))