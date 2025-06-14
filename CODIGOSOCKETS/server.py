#!/usr/bin/env python3
import socket
import threading
import sys
from typing import Tuple, List

# Lista global que mantiene las conexiones activas de los clientes
connections: List[socket.socket] = []


def handle_user_connection(conn: socket.socket, address: Tuple[str, int]) -> None:
    """
    Atiende a un cliente: recibe sus mensajes y los reenvía (broadcast) al resto.
    """
    while True:
        try:
            data = conn.recv(1024)
        except ConnectionResetError:
            # El cliente cerró abruptamente la conexión
            remove_connection(conn)
            break
        except Exception as e:
            print(f"Error al recibir datos de {address}: {e}")
            remove_connection(conn)
            break

        if not data:
            # Si recv devuelve b'', el cliente cerró la conexión limpiamente
            print(f"Cliente {address[0]}:{address[1]} se ha desconectado.")
            remove_connection(conn)
            break

        # Decodificar el mensaje entrante
        try:
            message = data.decode("utf-8", errors="replace")
        except Exception:
            message = "<mensaje no decodificable>"

        # Registrar en consola
        print(f"{address[0]}:{address[1]} -> {message}")

        # Construir el mensaje a reenviar y
        # hacer broadcast al resto de conexiones
        msg_to_send = f"From {address[0]}:{address[1]} - {message}"
        broadcast(msg_to_send, conn)


def broadcast(message: str, sender_conn: socket.socket) -> None:
    """
    Reenvía el mensaje a todos los clientes conectados,
    excepto al que lo envió.
    """
    for client_conn in list(connections):
        if client_conn is sender_conn:
            continue
        try:
            client_conn.sendall(message.encode("utf-8"))
        except Exception as e:
            print(f"Error enviando broadcast a {client_conn.getpeername()}: {e}")
            remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    """
    Cierra el socket y lo elimina de la lista de conexiones activas.
    """
    if conn in connections:
        try:
            conn.close()
        except Exception:
            pass
        connections.remove(conn)


def server(port: int) -> None:
    """
    Inicia el servidor: acepta conexiones de clientes y
    crea un hilo para atenderlos.
    """
    LISTENING_PORT = port

    # Crear socket TCP/IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permitir reutilizar la dirección si se reinicia rápido
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(("", LISTENING_PORT))
        server_socket.listen(4)
        print(f"Servidor ejecutándose en el puerto {LISTENING_PORT}. Esperando conexiones...")

        while True:
            try:
                conn, addr = server_socket.accept()
            except KeyboardInterrupt:
                print("\nDeteniendo servidor por solicitud del usuario.")
                break
            except Exception as e:
                print(f"Error al aceptar conexión: {e}")
                continue

            # Agregar conexión a la lista global
            connections.append(conn)
            print(f"Cliente conectado: {addr[0]}:{addr[1]} (conexiones activas: {len(connections)})")

            # Crear y arrancar hilo daemon para manejar al cliente
            client_thread = threading.Thread(
                target=handle_user_connection,
                args=(conn, addr),
                daemon=True
            )
            client_thread.start()

    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

    finally:
        # Cerrar todas las conexiones pendientes
        for conn in connections:
            try:
                conn.close()
            except Exception:
                pass
        connections.clear()

        try:
            server_socket.close()
        except Exception:
            pass

        print("Servidor cerrado.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 server.py <puerto>")
        sys.exit(1)

    try:
        port_number = int(sys.argv[1])
    except ValueError:
        print("El puerto debe ser un número entero.")
        sys.exit(1)

    server(port_number)
