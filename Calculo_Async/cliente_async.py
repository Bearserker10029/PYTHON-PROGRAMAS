import asyncio
import time
from random import randint
import statistics

SOCK_BUFFER = 1024


async def nota_client(sem):
    inicio = time.perf_counter()

    async with sem:

        reader, writer = await asyncio.open_connection('localhost', 5000)

        codigo=str(randint(0,100))

        #print(f'Send: {codigo!r}')
        writer.write(codigo.encode("utf-8"))
        await writer.drain()

        data = await reader.read(SOCK_BUFFER)
        #print(f'Received: {data.decode("utf-8")!r}')

        #print('Close the connection')
    writer.close()
    await writer.wait_closed()
    fin = time.perf_counter()
    t_ejecucion=fin-inicio
    return t_ejecucion


async def main():
    N_values = [200, 500, 800, 1200]
    results = {}
    for K in N_values:
        sem = asyncio.Semaphore(K)
        tiempos = await asyncio.gather(*[nota_client(sem) for _ in range(K)])
        resultados = {
            "media": statistics.mean(tiempos),
            "desviacion": statistics.stdev(tiempos),
            "p90": sorted(tiempos)[int(0.9 * K)],
            "p99": sorted(tiempos)[int(0.99 * K)]
        }
        results[K] = resultados
    return results


if __name__ == '__main__':
    N=[200,500,800,1200]
    notas=asyncio.run(main())
    for i in N:
        elementos_50=notas[:i]
        media=sum(elementos_50)//len(elementos_50)
        desviacion_estandar_50 = statistics.stdev(elementos_50)
        elementos_50.sort
        p90=elementos_50[90*len(elementos_50)//100]
        p99=elementos_50[99*len(elementos_50)//100]

        print(f"Media {media}, Desviacion estandar {desviacion_estandar_50}, P90 {p90}, P99 {p99}")

