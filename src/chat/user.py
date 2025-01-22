import socket
import threading

SERVER_HOST = '26.45.208.245'
SERVER_PORT = 5555

def receber_mensagens(usuario_socket):
    while True:
        try:
            messagem = usuario_socket.recv(1024).decode('utf-8')
            if messagem:
                print(messagem)
        except:
            print("[ERRO] Conexão com o servidor perdida.")
            usuario_socket.close()
            break

def inicia_usuario():
    usuario_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    usuario_socket.connect((SERVER_HOST, SERVER_PORT))

    thread_recebida = threading.Thread(target=receber_mensagens, args=(usuario_socket,))
    thread_recebida.start()

    while True:
        messagem = input("Digite sua mensagem ou '@nome_usuario Mensagem' para mensagem privada: ")
        if messagem.lower() == 'sair':
            print("[DESCONECTANDO] Encerrando a conexão.")
            usuario_socket.close()
            break
        usuario_socket.send(messagem.encode('utf-8'))

if __name__ == "__main__":
    inicia_usuario()