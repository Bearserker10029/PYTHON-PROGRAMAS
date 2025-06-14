#!/usr/bin/env python3
import socket
import threading
import sys

def handle_messages(conn: socket.socket) -> None:
    """
    Recibe mensajes enviados por el servidor y los muestra por consola.
    """
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                # Si recv devuelve b'', la conexión se ha cerrado
                print("La conexión con el servidor se ha cerrado.")
                break

            try:
                print(data.decode('utf-8'))
            except UnicodeDecodeError:
                print("<Mensaje recibido no pudo decodificarse como UTF-8>")

    except Exception as e:
        print(f"Error al manejar mensajes del servidor: {e}")

    finally:
        conn.close()


def client(host: str, port: int) -> None:
    """
    Inicia la conexión al servidor y gestiona el envío de mensajes desde el usuario.
    """
    try:
        # Crear socket TCP/IPv4 y conectarse al servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Crear un hilo para recibir mensajes del servidor
        receiver = threading.Thread(
            target=handle_messages,
            args=(sock,),
            daemon=True  # Marcamos el hilo como daemon para que no impida la salida
        )
        receiver.start()

        print("¡Conectado al chat!")
        print("Escribe un mensaje y presiona Enter. Para salir, escribe 'quit' y presiona Enter.\n")

        while True:
            try:
                msg = input()
            except EOFError:
                # Ctrl+D (EOF) finaliza cleanly
                break
            except KeyboardInterrupt:
                # Ctrl+C también finaliza cleanly
                break

            if msg.strip().lower() == 'quit':
                break

            # Enviar mensaje codificado en UTF-8
            try:
                sock.sendall(msg.encode('utf-8'))
            except BrokenPipeError:
                print("No se pudo enviar el mensaje: conexión cerrada por el servidor.")
                break

        # Cerrar conexión después de salir del bucle
        sock.close()
        print("Desconectado del servidor.")

    except ConnectionRefusedError:
        print(f"No se pudo conectar al servidor en {host}:{port}. ¿Está en ejecución?")
    except Exception as e:
        print(f"Error al conectarse o durante la comunicación: {e}")
        try:
            sock.close()
        except:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 client.py <host> <puerto>")
        sys.exit(1)

    server_host = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("El puerto debe ser un número entero.")
        sys.exit(1)

    client(server_host, server_port)
