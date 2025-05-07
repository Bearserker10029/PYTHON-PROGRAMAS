import asyncio
import time

N=200_000

async def calc_potencia(n:int ,ident: int):
    p=1
    cont=n

    while cont>0:
        p*=n
        cont -=1

    return p


async def main(num:int):
    await asyncio.gather(*(calc_potencia(N//num,idx) for idx in range(num)))


if __name__ == '__main__':
    num=64
    inicio = time.perf_counter()
    asyncio.run(main(num))
    fin = time.perf_counter()

    t_ejecucion = fin - inicio

    print(f"Tiempo total de ejecucion asincrono {num} corrutinas: {t_ejecucion:.6f} segundos")