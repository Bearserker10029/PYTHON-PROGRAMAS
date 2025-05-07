import asyncio
import numpy as np

PRECIO_MINIMO = 20000   #El precio base al que se inicia la subasta

async def ofertar(participante):
    while True:
        await asyncio.sleep(np.random.randint(0,11))
        valorSubastaActual=max(listaMontos)
        if (listaMontos[int(ord(participante))-97]<valorSubastaActual or listaMontos[int(ord(participante))-97]==(PRECIO_MINIMO)) and np.random.randint(2):
            listaMontos[int(ord(participante))-97]=np.random.randint(valorSubastaActual+500,(valorSubastaActual+500)*1.2+1)
            print(f"Participante {participante} hizo reoferta de {listaMontos[int(ord(participante))-97]}")

async def sniper():
    await asyncio.sleep(57)
    listaMontos[5]=int(open('oferta_del_sniper.txt','r').read())
    print(f"Participante 'sniper' hizo reoferta de {listaMontos[5]}")


async def main():
	await asyncio.wait_for(asyncio.gather(ofertar('a'),ofertar('b'),ofertar('c'),ofertar('d'),ofertar('e'),sniper()),timeout=60)
	    	
def ganador(listaMontos):
        mayor=0
        for i in range(len(listaMontos)):
            if listaMontos[i]>=mayor:
                mayor=listaMontos[i]
                posicionMayor=i
        if posicionMayor!=5:
            return chr(posicionMayor(listaMontos)+97)
        else:
            return 'sniper'

if __name__ == "__main__":
    listaMontos=[PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,PRECIO_MINIMO,0]
    try:
        asyncio.run(main())
    except asyncio.exceptions.TimeoutError:
        print("Se cumplió el tiempo de 60 segundos.\nOfertas finales: {'a':",listaMontos[0],",'b':",listaMontos[1],",'c':",listaMontos[2],",'d':",listaMontos[3],",'e':",listaMontos[4],"'sniper':",listaMontos[5],"}\nEl ganador es: ",ganador(listaMontos))