import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORTA = 5555  # Porta de escuta do servidor
MAXUSUARIOS = 3  # Número máximo de usuários permitidos

# Estruturas de controle
usuarios = {}  # Dicionário que mapeia sockets para nomes de usuários
usuario_threads = []  # Lista para armazenar threads de usuários
servidor = None  # Socket do servidor
rodando = False  # Flag para indicar se o servidor está em execução

def atualiza_lista_usuarios() -> None:
    """
    Summary:
        Atualiza a lista de usuários online para todos os usuários conectados.
        
    Args:
        None
        
    Returns:
        None
    """
    user_list = "Usuários online: " + ", ".join(usuarios.values())
    usuarios_desconectados = []

    for usuario in usuarios:
        try:
            usuario.send(user_list.encode('utf-8'))
        except OSError:
            usuarios_desconectados.append(usuario)

    for usuario in usuarios_desconectados:
        del usuarios[usuario]

def manter_usuario(usuario_socket, endereco_usuario) -> None:
    """
    Summary:
        Gerencia a interação com um usuário conectado.
        Solicita um nome de usuário, processa mensagens privadas e gerencia desconexões.

    Args:
        usuario_socket (socket.socket): Socket do cliente.
        endereco_usuario (tuple): Endereço IP e porta do cliente.
        
    Returns:
        None
        
    Raises:
        OSError: Erro ao enviar ou receber dados do usuário.
    """
    usuario_socket.send("Escolha um nome de usuário: ".encode('utf-8'))
    usuario_name = usuario_socket.recv(1024).decode('utf-8')
    usuarios[usuario_socket] = usuario_name
    print(f"[CONEXÃO] {usuario_name} conectado com o endereço {endereco_usuario}")

    atualiza_lista_usuarios()

    while True:
        try:
            message = usuario_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.startswith("@"):
                nome_destino, privada = message[1:].split(" ", 1)
                mensagem_privada(usuario_socket, nome_destino, privada)
            else:
                usuario_socket.send(
                    "Para enviar uma mensagem privada, use o formato '@nome_usuario Mensagem'.".encode('utf-8')
                )
        except:
            break

    print(f"[DESCONECTADO] {usuario_name} desconectado.")
    
    if usuario_socket in usuarios:
        del usuarios[usuario_socket]
    
    usuario_socket.close()
    atualiza_lista_usuarios()

def mensagem_privada(transmissor, nome_destino, message) -> None:
    """
    Summary:
        Envia uma mensagem privada para o destinatário especificado.

    Args:
        transmissor (socket.socket): Socket do cliente que enviou a mensagem.
        nome_destino (str): Nome do usuário destinatário.
        message (str): Conteúdo da mensagem.
        
    Returns:
        None
    """
    nome_transmissor = usuarios[transmissor]
    for usuario_socket, usuario_name in usuarios.items():
        if usuario_name == nome_destino:
            usuario_socket.send(f"@{nome_transmissor}: {message}".encode('utf-8'))
            return
    transmissor.send(f"Usuário '{nome_destino}' não encontrado.".encode('utf-8'))

def iniciar_servidor() -> None:
    """
    Summary:
        Inicia o servidor, escutando por novas conexões e gerenciando os usuários conectados.
        
    Args:
        None
        
    Returns:
        None
        
    Raises:
        OSError: Erro ao aceitar novas conexões.
    """
    global servidor, rodando
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen(MAXUSUARIOS)
    rodando = True
    print(f"\n[INICIADO] Servidor escutando em {HOST}:{PORTA}")

    while rodando:
        try:
            usuario_socket, endereco_usuario = servidor.accept()
            
            if len(usuarios) >= MAXUSUARIOS:
                print(f"[CHEIO] Conexão recusada para {endereco_usuario}. Limite de usuários atingido.")
                usuario_socket.close()
                continue

            usuario_thread = threading.Thread(target=manter_usuario, args=(usuario_socket, endereco_usuario))
            usuario_threads.append(usuario_thread)
            usuario_thread.start()
        except:
            break

def stop_servidor() -> None:
    """
    Summary:
        Encerra o servidor, desconectando todos os usuários e limpando os recursos.
        
    Args:
        None
        
    Returns:
        None
    """
    global rodando
    rodando = False
    for usuario_socket in list(usuarios.keys()):
        usuario_socket.close()
    for thread in usuario_threads:
        thread.join()
    usuarios.clear()
    usuario_threads.clear()
    if servidor:
        servidor.close()
    print("[ENCERRADO] Servidor foi encerrado.")

def main_menu() -> None:
    """
    Summary:
        Exibe o menu principal para controle do servidor. Permite iniciar, encerrar o servidor ou sair do programa.
        
    Args:
        None
        
    Returns:
        None
    """
    while True:
        print("\nMenu:")
        print("1. Iniciar servidor")
        print("2. Encerrar servidor")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            if not rodando:
                threading.Thread(target=iniciar_servidor).start()
            else:
                print("[AVISO] O servidor já está em execução.")
        elif choice == "2":
            if rodando:
                stop_servidor()
            else:
                print("[AVISO] O servidor já está encerrado.")
        elif choice == "3":
            if rodando:
                stop_servidor()
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Inicializa o programa
if __name__ == "__main__":
    main_menu()