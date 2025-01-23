import socket
import threading

# Configurações do cliente
SERVER_HOST = '26.207.181.224'  # Endereço IP do servidor
SERVER_PORT = 5555  # Porta do servidor

def receber_mensagens(usuario_socket):
    """
    Escuta e exibe mensagens enviadas pelo servidor.

    Args:
        usuario_socket (socket.socket): Socket conectado ao servidor.
    """
    while True:
        try:
            mensagem = usuario_socket.recv(1024).decode('utf-8')
            if mensagem:
                print(mensagem)
        except:
            print("[ERRO] Conexão com o servidor perdida.")
            usuario_socket.close()
            break


def inicia_usuario():
    """
    Inicia o cliente, conectando-se ao servidor e gerenciando a comunicação.
    Permite o envio de mensagens e exibe mensagens recebidas.
    """
    try:
        usuario_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        usuario_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[CONECTADO] Conexão estabelecida com {SERVER_HOST}:{SERVER_PORT}")

        # Thread para receber mensagens do servidor
        thread_recebida = threading.Thread(target=receber_mensagens, args=(usuario_socket,))
        thread_recebida.start()

        while True:
            mensagem = input("Digite sua mensagem ou '@nome_usuario Mensagem' para mensagem privada: ")
            if mensagem.lower() == 'sair':
                print("[DESCONECTANDO] Encerrando a conexão.")
                usuario_socket.close()
                break
            usuario_socket.send(mensagem.encode('utf-8'))
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Verifique se ele está em execução.")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    inicia_usuario()
