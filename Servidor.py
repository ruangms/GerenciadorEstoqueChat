# servidor.py
import socket
import threading
from estoque import Estoque

estoque = Estoque()
clientes = []

def broadcast(mensagem, remetente):
    for cliente in clientes:
        if cliente != remetente:
            try:
                cliente.send(mensagem.encode())
            except:
                clientes.remove(cliente)

def lidar_com_cliente(cliente):
    while True:
        try:
            dados = cliente.recv(1024).decode()
            if not dados:
                break

            if dados.startswith("/estoque"):
                partes = dados.split()
                if len(partes) == 1:
                    resposta = estoque.listar()
                elif len(partes) >= 4:
                    operacao, cat, prod, qtd = partes[1], partes[2], partes[3], int(partes[4])
                    if operacao == "add":
                        estoque.adicionar(cat, prod, qtd)
                        resposta = f"Adicionado {qtd} {prod} em {cat}."
                    elif operacao == "rm":
                        sucesso = estoque.remover(cat, prod, qtd)
                        resposta = f"Removido {qtd} {prod} de {cat}." if sucesso else "Remoção inválida."
                    else:
                        resposta = "Operação desconhecida."
                    estoque._salvar()
                else:
                    resposta = "Uso: /estoque [add|rm] <categoria> <produto> <qtd>"
                cliente.send(resposta.encode())
            else:
                print(f"[MSG] {dados}")
                broadcast(dados, cliente)
        except Exception as e:
            print(f"[ERRO] {e}")
            clientes.remove(cliente)
            cliente.close()
            break

def iniciar_servidor(host='localhost', porta=5555):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen()
    print(f"Servidor escutando em {host}:{porta}")

    while True:
        cliente, _ = servidor.accept()
        clientes.append(cliente)
        print("Novo cliente conectado.")
        thread = threading.Thread(target=lidar_com_cliente, args=(cliente,))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
