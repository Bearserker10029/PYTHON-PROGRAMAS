import asyncio
import time
from random import randint


SOCK_BUFFER = 1024

async def is_prime(x: int) -> bool:
    if x < 2: return False
    if x % 2 == 0: return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True

async def nth_prime(n: int) -> int:
    count, candidate = 0, 1
    while count < n:
        candidate += 1
        if await is_prime(candidate):
            count += 1
    return candidate

async def fact(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

async def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("Cliente conectado")

    try:
        while True:
            data = await reader.read(SOCK_BUFFER)
            await asyncio.sleep(randint(3, 7))
            if data:
                codigo = int(data.decode())
                loop = asyncio.get_event_loop()
                Fib = await loop.run_in_executor(None, nth_prime, codigo)
                Fact = await loop.run_in_executor(None, fact, codigo)
                Prime = await loop.run_in_executor(None, fib, codigo)
                writer.write(f"Fib: {Fib}, Fact: {Fact}, Prime: {Prime}".encode())
                await writer.drain()
            else:
                print("No hay mas datos")
                break
    except IndexError:
        print("No hay notas para este alumno")
    except ConnectionResetError:
        print("El usuario cerró la conexión abruptamente")
    finally:
        writer.close()
        await writer.wait_closed()

    print("conexion cerrada")

async def main():
    server_address = ("0.0.0.0", 5000)

    server = await asyncio.start_server(handle_client, server_address[0], server_address[1])

    async with server:
        print(f"Iniciando el servidor en {server_address[0]}:{server_address[1]}")
        await server.serve_forever()


if __name__ == '__main__':
    inicio = time.perf_counter()
    asyncio.run(main())
    fin = time.perf_counter()

    print(f"Tiempo total de ejecucion: {(fin - inicio):.6f} segundos")
