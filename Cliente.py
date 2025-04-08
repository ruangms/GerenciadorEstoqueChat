# cliente.py
import socket
import threading

def receber(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"[SERVIDOR] {msg}")
        except:
            break

def iniciar_cliente(host='localhost', porta=5555):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, porta))

    threading.Thread(target=receber, args=(cliente,), daemon=True).start()

    print("Digite mensagens ou comandos. Ex: /estoque add Alimentos Arroz 10")
    while True:
        msg = input("> ")
        if msg.lower() == "/sair":
            break
        cliente.send(msg.encode())

if __name__ == "__main__":
    iniciar_cliente()
