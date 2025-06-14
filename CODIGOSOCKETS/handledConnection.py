#!/usr/bin/env python3
import socket
import threading

print_lock = threading.Lock()

def threaded(client_socket: socket.socket) -> None:
    """
    Función que maneja la comunicación con un cliente:
    recibe datos, los invierte y los envía de vuelta.
    """
    while True:
        try:
            data = client_socket.recv(1024)
        except ConnectionResetError:
            # El cliente cerró abruptamente la conexión
            break

        if not data:
            print("Bye")
            # Liberar el candado antes de terminar el hilo
            print_lock.release()
            break

        # Invertir el contenido de bytes
        reversed_data = data[::-1]

        try:
            client_socket.sendall(reversed_data)
        except BrokenPipeError:
            # El cliente cerró la conexión antes de que se pudiera enviar
            break

    client_socket.close()


def Main() -> None:
    host = "0.0.0.0"
    port = 8888

    # Crear socket TCP/IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    print(f"Socket enlazado al puerto {port}")

    # Poner el socket en modo escucha
    server_socket.listen(5)
    print("Socket en modo escucha…")

    try:
        while True:
            # Esperar y aceptar una conexión entrante
            client_socket, addr = server_socket.accept()

            # Adquirir el candado antes de crear el hilo
            print_lock.acquire()
            print(f"Conectado a: {addr[0]}:{addr[1]}")

            # Iniciar un hilo para atender al cliente
            client_thread = threading.Thread(
                target=threaded,
                args=(client_socket,),
                daemon=True
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    Main()
