#!/usr/bin/env python3
import socket
import sys

def main():
    HOST = '0.0.0.0'  # Escuchar en todas las interfaces
    PORT = 5000       # Puerto arbitrario no privilegiado

    # Crear socket TCP/IPv4
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Permitir reutilizar la dirección en caso de reinicio rápido
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind((HOST, PORT))
        except socket.error as e:
            print(f"Bind fallido. Código de error: {e}")
            sys.exit(1)

        print("Socket ligado correctamente al puerto", PORT)

        server_socket.listen(10)
        print("Socket en modo escucha...")

        # Bucle principal: aceptar conexiones entrantes
        while True:
            try:
                conn, addr = server_socket.accept()
            except KeyboardInterrupt:
                print("\nServidor detenido por el usuario.")
                break
            except Exception as e:
                print(f"Error al aceptar conexión: {e}")
                continue

            with conn:
                print(f"Conectado con {addr[0]}:{addr[1]}")

                try:
                    data = conn.recv(1024)
                except ConnectionResetError:
                    print("La conexión fue restablecida por el cliente.")
                    continue
                except Exception as e:
                    print(f"Error recibiendo datos: {e}")
                    continue

                if not data:
                    # Si recv devuelve b'', el cliente cerró la conexión
                    print("No se recibió ningún dato. Cerrando conexión.")
                    continue

                # Decodificar datos recibidos y preparar la respuesta
                texto_recibido = data.decode("utf-8", errors="replace")
                reply = f"OK...{texto_recibido}"

                try:
                    conn.sendall(reply.encode("utf-8"))
                except BrokenPipeError:
                    print("No se pudo enviar la respuesta: tubería rota.")
                except Exception as e:
                    print(f"Error enviando datos: {e}")

        print("Cerrando socket del servidor.")

if __name__ == "__main__":
    main()
