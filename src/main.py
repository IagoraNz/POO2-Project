import sys
import os
import socket
import threading
from PyQt5.QtWidgets import QScrollArea, QTableWidgetItem, QApplication, QAbstractItemView, QTableWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QStackedWidget, QTextEdit
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from backend.back import *
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSizePolicy, QSpacerItem
from POO2PROJECT.listar_clientes import ListarClientes

# Caminho para a fonte
font_path = os.path.abspath("./src/fonts/Montserrat-SemiBold.ttf")

button_style = """
    QPushButton {
        background-color: #f1f1f1;
        border: none;
        border-radius: 10px;
        font-size: 14px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #ffcccc;  /* Vermelho claro */
    }
    QPushButton:pressed {
        background-color: #cce7ff;  /* Azul claro */
    }
"""

background_style = """
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
"""

line_edit_style = """
    QLineEdit {
        border: 2px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
        background-color: #f9f9f9;
    }
    QLineEdit:focus {
        border: 2px solid #06417c;
        background-color: #fff;
    }
"""

class Tela(QWidget):
    def __init__(self, user=None, senha=None):
        super().__init__()
        self.setWindowTitle("DELTA")
        self.setFixedSize(1000, 500)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        self.setStyleSheet("background-color: white;")

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 0, 10, 175)  # Ajustado o margem superior para manter a imagem fixada
        self.layout.setSpacing(10)

        # Layout para a imagem da logomarca (sobreposta)
        self.image_layout = QHBoxLayout()
        self.image_layout.setContentsMargins(0, 35, 0, 0)  # Não aplicar margem
        self.image_layout.setSpacing(0)

        # Criar um QLabel para exibir a imagem superior (fixada sobreposta)
        self.label = QLabel(self)
        image_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(resized_pixmap)
        else:
            self.label.setText("Imagem não encontrada.")
        
        # Adicionar a imagem à layout
        self.image_layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addLayout(self.image_layout)

        # Criar um QLabel para exibir o texto de boas-vindas
        self.welcome_label = QLabel(self)
        self.welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 20px;")
        self.welcome_label.setFont(montserrat_bold)
        self.layout.addWidget(self.welcome_label)

        # Diminuir a distância entre os widgets
        self.layout.addSpacing(-25)

        # Botões
        bt_login = QPushButton("Login")
        bt_login.setFixedSize(200, 50)
        bt_login.setStyleSheet(button_style)
        bt_login.setFont(montserrat_bold)
        bt_login.clicked.connect(self.mostrar_formulario_login)
        self.layout.addWidget(bt_login, alignment=Qt.AlignHCenter)

        bt_cadastrar = QPushButton("Cadastro")
        bt_cadastrar.setFixedSize(200, 50)
        bt_cadastrar.setStyleSheet(button_style)
        bt_cadastrar.setFont(montserrat_bold)
        bt_cadastrar.clicked.connect(self.mostrar_formulario_cadastro)
        self.layout.addWidget(bt_cadastrar, alignment=Qt.AlignHCenter)

        # Criar um QLabel para sobrepor a imagem no canto inferior direito
        self.bottom_image_label = QLabel(self)
        bottom_image_path = os.path.abspath("./src/images/aviao.png")
        if os.path.exists(bottom_image_path):
            pixmap = QPixmap(bottom_image_path)
            resized_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ajuste para 300x300
            self.bottom_image_label.setPixmap(resized_pixmap)
        else:
            self.bottom_image_label.setText("Imagem não encontrada.")

        # Passar usuário e senha para a autenticação, caso existam
        self.auth = Autenticacao(user, senha)

        # Exibir a imagem no canto inferior direito
        self.bottom_image_label.setGeometry(
            self.width() - 300,  # X (direita)
            self.height() - 235,  # Y (baixo)
            300, 300 
        )

        # Configurar layout principal
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        # Manter a posição da imagem fixa no canto inferior direito
        self.bottom_image_label.setGeometry(
            self.width() - 300,  # X (direita)
            self.height() - 235,  # Y (baixo)
            300, 300 
        )
        super().resizeEvent(event)
    
    def mostrar_formulario_cadastro(self):
        # Limpar a tela de boas-vindas e botões
        self.welcome_label.setText("")
        self.layout.itemAt(3).widget().setVisible(False)
        self.layout.itemAt(4).widget().setVisible(False)

        # Criar os campos de cadastro (verifica se já foram criados antes)
        if not hasattr(self, 'usuario_input'):
            # Legenda abaixo da mensagem de boas-vindas
            tipo_funcionario_label = QLabel("Na última sessão digite 1 para Gerente ou 2 para Atendente.", self)
            tipo_funcionario_label.setAlignment(Qt.AlignHCenter)
            tipo_funcionario_label.setStyleSheet("color: darkgray;")
            self.layout.addWidget(tipo_funcionario_label, alignment=Qt.AlignHCenter)

            # Campo de entrada para o usuário
            self.usuario_input = QLineEdit(self)
            self.usuario_input.setPlaceholderText("Usuário")
            self.usuario_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.usuario_input, alignment=Qt.AlignHCenter)

            # Campo de entrada para a senha
            self.senha_input = QLineEdit(self)
            self.senha_input.setPlaceholderText("Senha")
            self.senha_input.setEchoMode(QLineEdit.Password)
            self.senha_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.senha_input, alignment=Qt.AlignHCenter)

            # Campo de entrada para o tipo de funcionário
            self.tipo_input = QLineEdit(self)
            self.tipo_input.setPlaceholderText("Tipo de Funcionário")
            self.tipo_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.tipo_input, alignment=Qt.AlignHCenter)

            # Botão para efetuar o cadastro
            bt_efetuar_cadastro = QPushButton("Efetuar Cadastro")
            bt_efetuar_cadastro.setFixedSize(200, 50)
            bt_efetuar_cadastro.setStyleSheet(button_style)
            bt_efetuar_cadastro.setFont(QFont("Montserrat", 10, QFont.Bold))
            bt_efetuar_cadastro.clicked.connect(self.efetuar_cadastro)
            self.layout.addWidget(bt_efetuar_cadastro, alignment=Qt.AlignHCenter)

        # Mostrar a tela de cadastro
        self.layout.itemAt(5).widget().setVisible(True)
        self.layout.itemAt(6).widget().setVisible(True)
        self.layout.itemAt(7).widget().setVisible(True)
        self.layout.itemAt(8).widget().setVisible(True)
        self.layout.itemAt(9).widget().setVisible(True)
        
    def efetuar_cadastro(self):
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()
        tipo = self.tipo_input.text()
        
        if not usuario or not senha or not tipo:
            print("Todos os campos devem ser preenchidos!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Todos os campos devem ser preenchidos!")
            msg.exec_()
            return
        
        if len(senha) < 8:
            print("A senha deve ter no mínimo 8 dígitos")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("A senha deve ter no mínimo 8 dígitos! Tente novamente...")
            msg.exec_()
            return

        if tipo not in ["1", "2"]:
            print("Tipo de usuário inválido! Deve ser 1 (Gerente) ou 2 (Atendente)")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Tipo de usuário inválido! Deve ser 1 (Gerente) ou 2 (Atendente)")
            msg.exec_()
            return

        if self.auth.cadastro(usuario, senha, tipo):
            print(f"Usuário {usuario} cadastrado com sucesso!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Usuário {usuario} cadastrado com sucesso!")
            msg.exec_()
            self.voltar_tela_inicial()
        else:
            print(f"Erro: Usuário {usuario} já existe.")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Erro")
            msg.setText(f"Erro: Usuário {usuario} já existe.")
            msg.exec_()

    def voltar_tela_inicial(self):
        # Limpar os campos de cadastro
        self.usuario_input.setText("")
        self.senha_input.setText("")
        self.tipo_input.setText("")

        # Remover os campos de cadastro
        self.layout.itemAt(5).widget().setVisible(False)
        self.layout.itemAt(6).widget().setVisible(False)
        self.layout.itemAt(7).widget().setVisible(False)
        self.layout.itemAt(8).widget().setVisible(False)

        # Recriar a tela inicial
        self.welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        self.layout.itemAt(3).widget().setVisible(True)
        self.layout.itemAt(4).widget().setVisible(True)
        
    def mostrar_formulario_login(self):
        # Limpar a tela de boas-vindas e botões
        self.welcome_label.setText("")
        self.layout.itemAt(3).widget().setVisible(False)
        self.layout.itemAt(4).widget().setVisible(False)

        # Criar os campos de login (verifica se já foram criados antes)
        if not hasattr(self, 'login_usuario_input'):
            self.login_usuario_input = QLineEdit(self)
            self.login_usuario_input.setPlaceholderText("Usuário")
            self.login_usuario_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.login_usuario_input, alignment=Qt.AlignHCenter)

            self.login_senha_input = QLineEdit(self)
            self.login_senha_input.setPlaceholderText("Senha")
            self.login_senha_input.setEchoMode(QLineEdit.Password)
            self.login_senha_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.login_senha_input, alignment=Qt.AlignHCenter)

            # Botão para efetuar o login
            bt_efetuar_login = QPushButton("Efetuar Login")
            bt_efetuar_login.setFixedSize(200, 50)
            bt_efetuar_login.setStyleSheet(button_style)
            bt_efetuar_login.setFont(QFont("Montserrat", 10, QFont.Bold))
            bt_efetuar_login.clicked.connect(self.efetuar_login)
            self.layout.addWidget(bt_efetuar_login, alignment=Qt.AlignHCenter)

        # Mostrar a tela de login
        self.layout.itemAt(5).widget().setVisible(True)
        self.layout.itemAt(6).widget().setVisible(True)
        self.layout.itemAt(7).widget().setVisible(True)

    def efetuar_login(self):
        usuario = self.login_usuario_input.text()
        senha = self.login_senha_input.text()

        if not usuario or not senha:
            print("Todos os campos devem ser preenchidos!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Todos os campos devem ser preenchidos!")
            msg.exec_()
            return

        tipo_usuario, mensagem = self.auth.login(usuario, senha)

        if tipo_usuario == 1:
            print(f"{mensagem}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"{mensagem}")
            msg.exec_()
            self.mostrar_tela_home()
        elif tipo_usuario == 2:
            print(f"{mensagem}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"{mensagem}")
            msg.exec_()
            self.mostrar_tela_home2()
        else:
            print("Usuário ou senha incorretos!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Usuário ou senha incorretos! Tente novamente...")
            msg.exec_()
            
    def mostrar_tela_home(self):
        self.tela_gerente = TelaGerente()
        self.tela_gerente.show()
        self.close()
    
    def mostrar_tela_home2(self):
        self.tela_atendente = TelaAtendente()
        self.tela_atendente.show()
        self.close()

class TelaGerente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Layout da esquerda (logo e botões)
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(0)

        # Logo
        self.logo_label = QLabel(self)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        # Adicionar logo ao layout
        self.left_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)

        # Widget para centralizar botões
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)

        # Botões
        self.bt_voos = QPushButton("Voos")
        self.bt_voos.setFixedSize(200, 50)
        self.bt_voos.setStyleSheet(button_style)
        self.bt_voos.setFont(montserrat_bold)
        self.bt_voos.clicked.connect(self.mostrar_tela_voos)

        self.bt_avioes = QPushButton("Aviões")
        self.bt_avioes.setFixedSize(200, 50)
        self.bt_avioes.setStyleSheet(button_style)
        self.bt_avioes.setFont(montserrat_bold)
        self.bt_avioes.clicked.connect(self.mostrar_tela_avioes)

        self.bt_chat = QPushButton("Chat")
        self.bt_chat.setFixedSize(200, 50)
        self.bt_chat.setStyleSheet(button_style)
        self.bt_chat.setFont(montserrat_bold)
        self.bt_chat.clicked.connect(self.mostrar_tela_chat_gerente)

        self.bt_sair = QPushButton("Sair")
        self.bt_sair.setFixedSize(200, 50)
        self.bt_sair.setStyleSheet(button_style)
        self.bt_sair.setFont(montserrat_bold)
        self.bt_sair.clicked.connect(self.mostrar_tela_inicial) 

        button_layout.addWidget(self.bt_voos)
        button_layout.addWidget(self.bt_avioes)
        button_layout.addWidget(self.bt_chat)
        button_layout.addWidget(self.bt_sair)

        # Espaçador abaixo dos botões
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addSpacerItem(spacer)

        # Adicionar widget ao layout esquerdo
        self.left_layout.addWidget(button_widget, alignment=Qt.AlignTop)
        self.layout.addLayout(self.left_layout)

        # StackedWidget para trocar entre telas
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Placeholder inicial
        self.placeholder_widget = QWidget()
        self.stacked_widget.addWidget(self.placeholder_widget)

    def mostrar_tela_voos(self):
        self.tela_voos = TelaVoos()
        self.tela_voos.show()
    
    def mostrar_tela_avioes(self):
        self.tela_avioes = TelaAvioes()
        self.tela_avioes.show()
    
    def mostrar_tela_inicial(self):
        self.tela_inicial = Tela()
        self.tela_inicial.show()
    
    def mostrar_tela_chat_gerente(self):
        self.tela_chat_gerente = TelaChat_Gerente()
        self.tela_chat_gerente.show()


SERVER_HOST = '26.7.161.228'
SERVER_PORT = 5555

class TelaChat_Gerente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = "path/to/your/font.ttf"  # Substitua pelo caminho correto da sua fonte
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        self.title_label = QLabel("Chat")
        self.title_label.setFont(montserrat_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Caixa de Mensagens
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(50, 20, 50, 0)
        self.messages_layout.setSpacing(10)

        # Caixa para as mensagens (usando QTextEdit)
        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.messages_box.setStyleSheet("background-color: #f5f5f5; padding: 15px; border-radius: 10px; border: 1px solid #ccc; height: 300px;")
        self.messages_layout.addWidget(self.messages_box)

        self.layout.addWidget(self.messages_widget)

        # Contêiner 3: Campo de mensagem e botão
        self.input_widget = QWidget()
        self.input_layout = QHBoxLayout(self.input_widget)
        self.input_layout.setContentsMargins(50, 20, 50, 0)
        self.input_layout.setSpacing(10)

        # Campo de entrada para a mensagem
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Digite sua mensagem...")
        self.message_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc;")
        self.input_layout.addWidget(self.message_input)

        # Botão de enviar
        self.bt_enviar = QPushButton("Enviar")
        self.bt_enviar.setFixedSize(100, 40)
        self.bt_enviar.setStyleSheet(button_style)
        self.bt_enviar.setFont(montserrat_bold)
        self.input_layout.addWidget(self.bt_enviar)

        self.layout.addWidget(self.input_widget)

        # Inicializar a conexão
        self.usuario_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usuario_socket.connect((SERVER_HOST, SERVER_PORT))

        # Criar e iniciar thread para receber mensagens
        self.thread_recebida = threading.Thread(target=self.receber_mensagens, args=(self.usuario_socket,))
        self.thread_recebida.start()

        # Conectar o botão de enviar
        self.bt_enviar.clicked.connect(self.enviar_mensagem)

    def receber_mensagens(self, usuario_socket):
        while True:
            try:
                mensagem = usuario_socket.recv(1024).decode("utf-8")
                if mensagem:
                    self.exibir_mensagem(mensagem, enviado=False)
            except:
                print("[ERRO] Conexão com o servidor perdida.")
                usuario_socket.close()
                break

    def exibir_mensagem(self, mensagem, enviado):
        """Exibir mensagens na caixa de mensagens."""
        cor = "blue" if enviado else "black"
        self.messages_box.append(f'<p style="color: {cor};">{mensagem}</p>')

    def enviar_mensagem(self):
        """Enviar mensagem digitada pelo usuário."""
        mensagem = self.message_input.text()
        if mensagem.lower() == "sair":
            print("[DESCONECTANDO] Encerrando a conexão.")
            self.usuario_socket.close()
            self.close()  # Fecha a janela
        elif mensagem:
            self.usuario_socket.send(mensagem.encode("utf-8"))
            self.exibir_mensagem(mensagem, enviado=True)
            self.message_input.clear()  # Limpa o campo de entrada

    
class TelaVoos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Voos - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Layout da esquerda
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(20)

        # Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.left_layout.addWidget(self.logo_widget)

        # Botões do lado esquerdo
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(15)
        self.button_layout.setAlignment(Qt.AlignTop)

        button_width = 200
        button_height = 50

        self.bt_cadastrar = QPushButton("Cadastrar")
        self.bt_cadastrar.setFixedSize(button_width, button_height)
        self.bt_cadastrar.setStyleSheet(button_style)
        self.bt_cadastrar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_cadastrar)
        self.bt_cadastrar.clicked.connect(self.mostrar_tela_cadastrar_voo)

        self.bt_alterar = QPushButton("Alterar")
        self.bt_alterar.setFixedSize(button_width, button_height)
        self.bt_alterar.setStyleSheet(button_style)
        self.bt_alterar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_alterar)
        self.bt_alterar.clicked.connect(self.mostrar_tela_alterar_voo)

        self.bt_remover = QPushButton("Remover")
        self.bt_remover.setFixedSize(button_width, button_height)
        self.bt_remover.setStyleSheet(button_style)
        self.bt_remover.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_remover)
        self.bt_remover.clicked.connect(self.mostrar_tela_remover_reserva_voo)

        self.bt_listar = QPushButton("Listar")
        self.bt_listar.setFixedSize(button_width, button_height)
        self.bt_listar.setStyleSheet(button_style)
        self.bt_listar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_listar)
        self.bt_listar.clicked.connect(self.mostrar_tela_listar_voo)


        self.bt_marcar_viagem = QPushButton("Marcar Voo")
        self.bt_marcar_viagem.setFixedSize(button_width, button_height)
        self.bt_marcar_viagem.setStyleSheet(button_style)
        self.bt_marcar_viagem.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_marcar_viagem)
        self.bt_marcar_viagem.clicked.connect(self.mostrar_tela_marcar_voo)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.button_layout.addWidget(self.bt_voltar)

        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button_layout.addSpacerItem(spacer)

        self.left_layout.addWidget(self.button_widget)
        self.layout.addLayout(self.left_layout)

        # Layout da direita com contêiner
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(20, 35, 20, 0)
        self.right_layout.setSpacing(20)

        self.label_container = QLabel("O que faremos com os voos?")
        self.label_container.setFont(montserrat_bold)
        self.label_container.setAlignment(Qt.AlignCenter)
        self.label_container.setStyleSheet("color: #333333;")
        self.right_layout.addWidget(self.label_container, alignment=Qt.AlignCenter)

        self.layout.addLayout(self.right_layout)
    
    def mostrar_tela_cadastrar_voo(self):
        # Certifique-se de ter uma instância de CadastroVoos disponível
        if not hasattr(self, 'cadastro_voos'):
            self.cadastro_voos = CadastroVoos()
        
        # Passe a instância de CadastroVoos para TelaVoos_Cadastrar
        self.tela_cadastrar_voo = TelaVoos_Cadastrar(self.cadastro_voos)
        self.tela_cadastrar_voo.show()

    def mostrar_tela_alterar_voo(self):
        self.tela_alterar_voo = TelaVoos_Alterar()
        self.tela_alterar_voo.show()
    
    def mostrar_tela_remover_reserva_voo(self):
        self.tela_remover_reserva_voo = TelaVoos_Remover()
        self.tela_remover_reserva_voo.show()
    
    def mostrar_tela_listar_voo(self):
        self.tela_listar_voo = TelaVoos_Listar()
        self.tela_listar_voo.show()
    
    def mostrar_tela_marcar_voo(self):
        self.tela_marcar_voo = TelaVoos_Marcar()
        self.tela_marcar_voo.show()


class TelaAvioes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Voos - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Layout da esquerda
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(20)  # Espaçamento entre logo e botões

        # Widget do logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.left_layout.addWidget(self.logo_widget)

        # Widget dos botões
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(15)
        self.button_layout.setAlignment(Qt.AlignTop)

        # Botões
        button_width = 200
        button_height = 50

        self.bt_cadastrar = QPushButton("Cadastrar")
        self.bt_cadastrar.setFixedSize(button_width, button_height)
        self.bt_cadastrar.setStyleSheet(button_style)
        self.bt_cadastrar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_cadastrar)
        self.bt_cadastrar.clicked.connect(self.mostrar_tela_cadastar_aviao)

        self.bt_alterar = QPushButton("Alterar")
        self.bt_alterar.setFixedSize(button_width, button_height)
        self.bt_alterar.setStyleSheet(button_style)
        self.bt_alterar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_alterar)
        self.bt_alterar.clicked.connect(self.mostrar_tela_alterar_aviao)

        self.bt_remover = QPushButton("Remover")
        self.bt_remover.setFixedSize(button_width, button_height)
        self.bt_remover.setStyleSheet(button_style)
        self.bt_remover.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_remover)
        self.bt_remover.clicked.connect(self.mostrar_tela_remover_aviao)

        self.bt_listar = QPushButton("Listar")
        self.bt_listar.setFixedSize(button_width, button_height)
        self.bt_listar.setStyleSheet(button_style)
        self.bt_listar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_listar)
        self.bt_listar.clicked.connect(self.mostrar_tela_listar_aviao)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.button_layout.addWidget(self.bt_voltar)

        # Espaçador abaixo dos botões
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button_layout.addSpacerItem(spacer)

        # Adicionar widget dos botões ao layout esquerdo
        self.left_layout.addWidget(self.button_widget)

        # Adicionar layout esquerdo ao layout principal
        self.layout.addLayout(self.left_layout)

        # Placeholder para conteúdos adicionais
        self.placeholder_widget = QWidget()
        self.layout.addWidget(self.placeholder_widget)

    def mostrar_tela_cadastar_aviao(self):
        self.tela_cadastrar_aviao = TelaAvioes_Cadastrar()
        self.tela_cadastrar_aviao.show()
    
    def mostrar_tela_alterar_aviao(self):
        self.tela_alterar_aviao = TelaAvioes_Alterar()
        self.tela_alterar_aviao.show()
    
    def mostrar_tela_remover_aviao(self):
        self.tela_remover_aviao = TelaAvioes_Remover()
        self.tela_remover_aviao.show()
    
    def mostrar_tela_listar_aviao(self):
        self.tela_listar_aviao = TelaAvioes_Listar()
        self.tela_listar_aviao.show()
    


class TelaVoos_Cadastrar(QMainWindow):
    def __init__(self, cadastro_voos):
        super().__init__()
        self.cadastro_voos = cadastro_voos  # Instância da classe CadastroVoos

        self.setWindowTitle("Cadastrar Voo - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Estilo dos campos e botões
        line_edit_style = """
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """
        button_style = """
            QPushButton {
                background-color: #f1f1f1;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffcccc;  /* Vermelho claro /
            }
            QPushButton:pressed {
                background-color: #cce7ff;  / Azul claro */
            }
        """

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo e título
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        self.title_label = QLabel("Cadastrar Voo")
        self.title_label.setFont(montserrat_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Campos de entrada
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        self.form_layout.setContentsMargins(50, 20, 50, 0)
        self.form_layout.setSpacing(20)

        self.sigla_input = QLineEdit(self)
        self.sigla_input.setPlaceholderText("Sigla")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.sigla_input)

        self.origem_input = QLineEdit(self)
        self.origem_input.setPlaceholderText("Origem")
        self.origem_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.origem_input)

        self.destino_input = QLineEdit(self)
        self.destino_input.setPlaceholderText("Destino")
        self.destino_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.destino_input)

        self.modelo_input = QLineEdit(self)
        self.modelo_input.setPlaceholderText("Modelo do Avião")
        self.modelo_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.modelo_input)

        self.assentos_input = QLineEdit(self)
        self.assentos_input.setPlaceholderText("Quantidade de Assentos")
        self.assentos_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.assentos_input)

        self.layout.addWidget(self.form_widget)

        # Contêiner 3: Botões
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 30, 0, 0)
        self.buttons_layout.setSpacing(20)

        button_width = 200
        button_height = 50

        self.bt_cadastrar = QPushButton("Cadastrar")
        self.bt_cadastrar.setFixedSize(button_width, button_height)
        self.bt_cadastrar.setStyleSheet(button_style)
        self.bt_cadastrar.setFont(montserrat_bold)
        self.bt_cadastrar.clicked.connect(self.cadastrar_voo)  # Conecta ao método de cadastro
        self.buttons_layout.addWidget(self.bt_cadastrar, alignment=Qt.AlignCenter)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)  # Fecha a janela
        self.buttons_layout.addWidget(self.bt_voltar, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.buttons_widget)

    def cadastrar_voo(self):
        sigla = self.sigla_input.text()
        origem = self.origem_input.text()
        destino = self.destino_input.text()
        modelo = self.modelo_input.text()
        assentos = self.assentos_input.text()  # Novo campo

        if not sigla or not origem or not destino or not modelo or not assentos:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        if not assentos.isdigit():
            QMessageBox.warning(self, "Erro", "Quantidade de assentos deve ser um número.")
            return

        sucesso, mensagem = self.cadastro_voos.cadastrar_voo(sigla, origem, destino, modelo, int(assentos))
        QMessageBox.information(self, "Resultado", mensagem)

class TelaAvioes_Cadastrar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastrar Avião - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Instância da classe MetodosGerente
        self.gerente = MetodosGerente()

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo e frase "Cadastrando Aviões"
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        self.title_label = QLabel("Cadastrar Avião")
        self.title_label.setFont(montserrat_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Campos de entrada
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        self.form_layout.setContentsMargins(50, 20, 50, 0)
        self.form_layout.setSpacing(20)

        self.sigla_input = QLineEdit(self)
        self.sigla_input.setPlaceholderText("Sigla")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.sigla_input)

        self.modelo_input = QLineEdit(self)
        self.modelo_input.setPlaceholderText("Modelo do Avião")
        self.modelo_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.modelo_input)

        self.assentos_input = QLineEdit(self)
        self.assentos_input.setPlaceholderText("Quantidade de Assentos")
        self.assentos_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.assentos_input)

        self.layout.addWidget(self.form_widget)

        # Contêiner 3: Botões
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 30, 0, 0)
        self.buttons_layout.setSpacing(20)

        button_width = 200
        button_height = 50

        self.bt_cadastrar = QPushButton("Cadastrar")
        self.bt_cadastrar.setFixedSize(button_width, button_height)
        self.bt_cadastrar.setStyleSheet(button_style)
        self.bt_cadastrar.setFont(montserrat_bold)
        self.bt_cadastrar.clicked.connect(self.cadastrar_aviao)
        self.buttons_layout.addWidget(self.bt_cadastrar, alignment=Qt.AlignCenter)

        # Botão "Voltar"
        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.bt_voltar, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.buttons_widget)

    def cadastrar_aviao(self):
        """Método para cadastrar um avião com os dados fornecidos nos campos de entrada."""
        sigla = self.sigla_input.text().strip()
        modelo = self.modelo_input.text().strip()
        assentos = self.assentos_input.text().strip()

        if not sigla or not modelo or not assentos.isdigit():
            print("Preencha todos os campos corretamente.")
            return

        # Chamando o método de cadastro da classe MetodosGerente
        sucesso = self.gerente.cadastrar_aviao(sigla, modelo, int(assentos))

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Avião cadastrado com sucesso!")
            print("Avião cadastrado com sucesso!")
            self.sigla_input.clear()
            self.modelo_input.clear()
            self.assentos_input.clear()
        else:
            print("Erro ao cadastrar o avião. Verifique os dados.")

class TelaVoos_Alterar(QMainWindow):
    def __init__(self, conn=None, parent=None):
        super().__init__(parent)
        self.conn = conn or psycopg2.connect(dbname='credenciais', user='poodois', password='1234', host='localhost', port=5432)
        self.setWindowTitle("Alterar Voo - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = "./src/fonts/Montserrat-Bold.ttf"
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Definindo o estilo dos botões
        button_width = 200
        button_height = 50
        button_style = """
            QPushButton {
                background-color: #f1f1f1;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffcccc;  /* Vermelho claro /
            }
            QPushButton:pressed {
                background-color: #cce7ff;  / Azul claro */
            }
        """
        # Contêiner de entrada para sigla
        self.sigla_container = QWidget()
        self.sigla_layout = QVBoxLayout(self.sigla_container)
        self.sigla_layout.setContentsMargins(100, 10, 100, 10)
        self.sigla_layout.setSpacing(15)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Digite a sigla do voo")
        self.sigla_input.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.sigla_layout.addWidget(self.sigla_input)

        self.buscar_button = QPushButton("Buscar Voo")
        self.buscar_button.setFixedSize(button_width, button_height)
        self.buscar_button.setFont(montserrat_bold)
        self.buscar_button.setStyleSheet(button_style)
        self.buscar_button.clicked.connect(self.buscar_voo_handler)
        self.sigla_layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.sigla_container)

        # Contêiner 2: Informações do voo
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.voo_info_label = QLabel("Informações do voo a serem exibidas aqui")
        self.voo_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.voo_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.voo_info_label)

        self.layout.addWidget(self.info_container)

        # Contêiner do título
        self.title_container = QLabel("Alterar Voo")
        self.title_container.setFont(montserrat_bold)
        self.title_container.setAlignment(Qt.AlignCenter)
        self.title_container.setStyleSheet("color: #333333; margin-top: 10px;")
        self.layout.addWidget(self.title_container)

        # Contêiner para os campos de edição
        self.edit_container = QWidget()
        self.edit_layout = QVBoxLayout(self.edit_container)
        self.edit_layout.setContentsMargins(100, 10, 100, 10)
        self.edit_layout.setSpacing(15)

        self.origem_input = QLineEdit()
        self.origem_input.setPlaceholderText("Digite a origem")
        self.origem_input.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.edit_layout.addWidget(self.origem_input)

        self.destino_input = QLineEdit()
        self.destino_input.setPlaceholderText("Digite o destino")
        self.destino_input.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.edit_layout.addWidget(self.destino_input)

        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Digite o modelo do avião")
        self.modelo_input.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.edit_layout.addWidget(self.modelo_input)

        self.layout.addWidget(self.edit_container)

        # Contêiner para os botões "Alterar Voo" e "Voltar"
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.buttons_layout.setSpacing(20)

        self.alterar_button = QPushButton("Alterar Voo")
        self.alterar_button.setFixedSize(button_width, button_height)
        self.alterar_button.setFont(montserrat_bold)
        self.alterar_button.setStyleSheet(button_style)
        self.alterar_button.clicked.connect(self.alterar_voo_handler)
        self.buttons_layout.addWidget(self.alterar_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(button_width, button_height)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.buttons_container)

    def buscar_voo_handler(self):
        # Método para buscar o voo e exibir as informações
        sigla = self.sigla_input.text().strip()
        if not sigla:
            self.voo_info_label.setText("Por favor, insira uma sigla.")
            self.voo_info_label.setStyleSheet("color: red;")
            return
        
        # Aqui você pode adicionar a lógica para buscar o voo no banco de dados
        # Suponha que o voo seja encontrado, atualize o info_label com informações do voo.
        self.voo_info_label.setText(f"Informações do voo {sigla} encontradas.")
        self.voo_info_label.setStyleSheet("color: green;")

    def alterar_voo_handler(self):
        sigla = self.sigla_input.text().strip()
        origem = self.origem_input.text().strip()
        destino = self.destino_input.text().strip()
        modelo_aviao = self.modelo_input.text().strip()

        if not sigla or not origem or not destino or not modelo_aviao:
            self.voo_info_label.setText("Todos os campos devem ser preenchidos.")
            self.voo_info_label.setStyleSheet("color: red;")
            return

        sucesso, mensagem = self.alterar_voo(sigla, origem, destino, modelo_aviao)
        self.voo_info_label.setText(mensagem)
        if sucesso:
            self.voo_info_label.setStyleSheet("color: green;")
        else:
            self.voo_info_label.setStyleSheet("color: red;")

    def alterar_voo(self, sigla: str, origem: str, destino: str, modelo_aviao: str) -> tuple:
        """Altera os dados de um voo existente pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    '''
                    UPDATE voos 
                    SET origem = %s, destino = %s, modelo_aviao = %s
                    WHERE sigla = %s;
                    ''',
                    (origem, destino, modelo_aviao, sigla)
                )
                self.conn.commit()

                if cur.rowcount > 0:
                    return True, "Dados do voo alterados com sucesso."
                else:
                    return False, "Voo não encontrado."
        except Exception as e:
            return False, f"Erro ao alterar voo: {str(e)}"

class TelaAvioes_Alterar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alterar Avião - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Contêiner de entrada para sigla
        self.sigla_container = QWidget()
        self.sigla_layout = QVBoxLayout(self.sigla_container)
        self.sigla_layout.setContentsMargins(100, 10, 100, 10)
        self.sigla_layout.setSpacing(15)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Digite a sigla do avião")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.sigla_layout.addWidget(self.sigla_input)

        self.buscar_button = QPushButton("Buscar Avião")
        self.buscar_button.setFixedSize(200, 50)
        self.buscar_button.setFont(montserrat_bold)
        self.buscar_button.setStyleSheet(button_style)
        self.buscar_button.clicked.connect(self.buscar_aviao)
        self.sigla_layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.sigla_container)

        # Contêiner 3: Informações do avião
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.aviao_info_label = QLabel("Informações do avião a serem exibidas aqui")
        self.aviao_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.aviao_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.aviao_info_label)

        self.layout.addWidget(self.info_container)

        # Contêiner de título
        self.title_container = QLabel("Alterar Avião")
        self.title_container.setFont(montserrat_bold)
        self.title_container.setAlignment(Qt.AlignCenter)
        self.title_container.setStyleSheet("color: #333333; margin-top: 10px;")
        self.layout.addWidget(self.title_container)

        # Contêiner para os campos de edição
        self.edit_container = QWidget()
        self.edit_layout = QVBoxLayout(self.edit_container)
        self.edit_layout.setContentsMargins(100, 10, 100, 10)
        self.edit_layout.setSpacing(15)

        # Campo de Modelo do Avião
        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Digite o modelo do avião")
        self.modelo_input.setStyleSheet(line_edit_style)
        self.edit_layout.addWidget(self.modelo_input)

        # Campo de Quantidade de Assentos
        self.assentos_input = QLineEdit()
        self.assentos_input.setPlaceholderText("Digite a quantidade de assentos")
        self.assentos_input.setStyleSheet(line_edit_style)
        self.edit_layout.addWidget(self.assentos_input)

        self.layout.addWidget(self.edit_container)

        # Contêiner para os botões "Alterar Avião" e "Voltar"
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.buttons_layout.setSpacing(20)

        self.alterar_button = QPushButton("Alterar Avião")
        self.alterar_button.setFixedSize(200, 50)
        self.alterar_button.setFont(montserrat_bold)
        self.alterar_button.setStyleSheet(button_style)
        self.alterar_button.clicked.connect(self.alterar_aviao)
        self.buttons_layout.addWidget(self.alterar_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.buttons_container)

    def buscar_aviao(self):
        sigla = self.sigla_input.text().strip()
        if not sigla:
            QMessageBox.warning(self, "Atenção", "Digite a sigla do avião.")
            return

        metodos_gerente = MetodosGerente()
        aviao = metodos_gerente.buscar_aviao_por_sigla(sigla)

        if aviao:
            self.modelo_input.setText(aviao[2])
            self.assentos_input.setText(str(aviao[3]))
            self.aviao_info_label.setText(f"Sigla: {aviao[1]}\nModelo: {aviao[2]}\nAssentos: {aviao[3]}")
        else:
            QMessageBox.warning(self, "Erro", "Avião não encontrado.")

    def alterar_aviao(self):
        sigla = self.sigla_input.text().strip()
        novo_modelo = self.modelo_input.text().strip()
        nova_qtd_assentos = self.assentos_input.text().strip()

        if not sigla or not novo_modelo or not nova_qtd_assentos:
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos.")
            return

        try:
            nova_qtd_assentos = int(nova_qtd_assentos)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Quantidade de assentos deve ser um número válido.")
            return

        metodos_gerente = MetodosGerente()
        sucesso = metodos_gerente.alterar_aviao(sigla, novo_modelo, nova_qtd_assentos)

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Avião alterado com sucesso!")
            self.sigla_input.clear()
            self.modelo_input.clear()
            self.assentos_input.clear()
            self.aviao_info_label.setText("Informações do avião a serem exibidas aqui")
        else:
            QMessageBox.critical(self, "Erro", "Erro ao alterar o avião.")


class TelaVoos_Remover(QMainWindow):
    def __init__(self, conn = psycopg2.connect(dbname='credenciais', user='poodois',  password='1234', host='localhost', port=5432)):
        super().__init__()
        self.setWindowTitle("Removendo Voos - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        self.conn = conn  # Conexão com o banco de dados

        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)  # Logo centralizada
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Adicionar a frase "Remover Voo" abaixo da logo
        self.remove_voo_label = QLabel("Remover Voo")
        self.remove_voo_label.setFont(montserrat_bold)
        self.remove_voo_label.setAlignment(Qt.AlignCenter)
        self.remove_voo_label.setStyleSheet("color: #333333; margin-top: 10px;")
        self.logo_layout.addWidget(self.remove_voo_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Entrada de sigla e botão de busca
        self.sigla_container = QWidget()
        self.sigla_layout = QVBoxLayout(self.sigla_container)
        self.sigla_layout.setSpacing(10)
        self.sigla_container.setContentsMargins(100, 10, 100, 10)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Sigla do Voo")
        self.sigla_input.setStyleSheet("border: 1px solid #cccccc; padding: 5px; border-radius: 3px;")
        self.sigla_layout.addWidget(self.sigla_input)

        self.buscar_button = QPushButton("Buscar Voo")
        self.buscar_button.setFixedSize(200, 50)
        self.buscar_button.setStyleSheet(button_style)
        self.buscar_button.clicked.connect(self.buscar_voo)
        self.sigla_layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.sigla_container)

        # Contêiner 3: Informações do voo
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.voo_info_label = QLabel("Informações do voo a serem exibidas aqui")
        self.voo_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 10px; border-radius: 3px;")
        self.voo_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.voo_info_label)

        self.layout.addWidget(self.info_container)

        # Contêiner 4: Botões de remover e voltar
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.remover_reserva_voo_button = QPushButton("Remover Voo")
        self.remover_reserva_voo_button.setFixedSize(200, 50)
        self.remover_reserva_voo_button.setStyleSheet(button_style)
        self.remover_reserva_voo_button.setFont(montserrat_bold)
        self.remover_reserva_voo_button.clicked.connect(self.remover_reserva_voo)
        self.button_layout.addWidget(self.remover_reserva_voo_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)

    def buscar_voo(self):
        """Busca informações do voo pela sigla e exibe as informações"""
        sigla = self.sigla_input.text().strip()
        if sigla:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("SELECT * FROM voos WHERE sigla = %s;", (sigla,))
                    voo = cur.fetchone()
                    if voo:
                        voo_info = f"Sigla: {voo[0]}\nOrigem: {voo[1]}\nDestino: {voo[2]}\nData: {voo[3]}"
                        self.voo_info_label.setText(voo_info)
                    else:
                        self.voo_info_label.setText("Voo não encontrado.")
            except Exception as e:
                self.voo_info_label.setText(f"Erro ao buscar voo: {str(e)}")
        else:
            self.voo_info_label.setText("Por favor, insira a sigla do voo.")

    def remover_reserva_voo(self):
        """Remove o voo usando a sigla informada"""
        sigla = self.sigla_input.text().strip()
        if sigla:
            sucesso, mensagem = self.excluir_voo(sigla)
            self.voo_info_label.setText(mensagem)
            if sucesso:
                self.sigla_input.clear()  # Limpa o campo de sigla após remoção
        else:
            self.voo_info_label.setText("Por favor, insira a sigla do voo.")

    def excluir_voo(self, sigla: str) -> tuple:
        """Exclui um voo pela sigla."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM voos WHERE sigla = %s;",
                    (sigla,)
                )
                self.conn.commit()
                if cur.rowcount > 0:
                    return True, "Voo excluído com sucesso."
                return False, "Voo não encontrado."
        except Exception as e:
            return False, f"Erro ao excluir voo: {str(e)}"

class TelaAvioes_Remover(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remover Avião - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Título "Remover Avião"
        self.remove_aviao_label = QLabel("Remover Avião")
        self.remove_aviao_label.setFont(montserrat_bold)
        self.remove_aviao_label.setAlignment(Qt.AlignCenter)
        self.remove_aviao_label.setStyleSheet("color: #333333; margin-top: 10px;")
        self.layout.addWidget(self.remove_aviao_label)

        # Entrada da sigla do avião
        self.sigla_container = QWidget()
        self.sigla_layout = QVBoxLayout(self.sigla_container)
        self.sigla_layout.setSpacing(10)
        self.sigla_container.setContentsMargins(100, 10, 100, 10)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Sigla do Avião")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.sigla_layout.addWidget(self.sigla_input)

        self.buscar_button = QPushButton("Buscar Avião")
        self.buscar_button.setFixedSize(200, 50)
        self.buscar_button.setStyleSheet(button_style)
        self.buscar_button.clicked.connect(self.buscar_aviao)
        self.sigla_layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.sigla_container)

        # Exibição das informações do avião
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.aviao_info_label = QLabel("Informações do avião a serem exibidas aqui")
        self.aviao_info_label.setStyleSheet(line_edit_style)
        self.aviao_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.aviao_info_label)

        self.layout.addWidget(self.info_container)

        # Botões de remover e voltar
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.remover_aviao_button = QPushButton("Remover Avião")
        self.remover_aviao_button.setFixedSize(200, 50)
        self.remover_aviao_button.setStyleSheet(button_style)
        self.remover_aviao_button.setFont(montserrat_bold)
        self.remover_aviao_button.clicked.connect(self.remover_aviao)
        self.button_layout.addWidget(self.remover_aviao_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)

    def buscar_aviao(self):
        """Busca informações do avião pela sigla."""
        sigla = self.sigla_input.text().strip()
        if not sigla:
            QMessageBox.warning(self, "Atenção", "Digite a sigla do avião.")
            return

        metodos_gerente = MetodosGerente()
        aviao = metodos_gerente.buscar_aviao_por_sigla(sigla)

        if aviao:
            self.aviao_info_label.setText(
                f"ID: {aviao[0]}\nSigla: {aviao[1]}\nModelo: {aviao[2]}\nAssentos: {aviao[3]}"
            )
            self.sigla_input.setReadOnly(True)  # Bloquear edição após busca bem-sucedida
        else:
            self.aviao_info_label.setText("Avião não encontrado.")
            self.sigla_input.setReadOnly(False)

    def remover_aviao(self):
        """Remove o avião baseado na sigla informada."""
        sigla = self.sigla_input.text().strip()
        if not sigla:
            QMessageBox.warning(self, "Atenção", "Digite a sigla do avião para remover.")
            return

        resposta = QMessageBox.question(
            self, "Confirmação", f"Tem certeza que deseja remover o avião com sigla '{sigla}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            metodos_gerente = MetodosGerente()
            sucesso = metodos_gerente.excluir_aviao(sigla)

            if sucesso:
                QMessageBox.information(self, "Sucesso", "Avião removido com sucesso!")
                self.aviao_info_label.setText("Informações do avião a serem exibidas aqui")
                self.sigla_input.clear()
                self.sigla_input.setReadOnly(False)
            else:
                QMessageBox.critical(self, "Erro", "Erro ao remover o avião.")


class TelaVoos_Listar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Voos - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Conexão com o banco de dados
        self.conn = psycopg2.connect("dbname=credenciais user=poodois password=1234 host=localhost")
        
        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Contêiner "Lista de Voos"
        self.label_container = QLabel("Lista de Voos")
        self.label_container.setFont(montserrat_bold)
        self.label_container.setAlignment(Qt.AlignCenter)
        self.label_container.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.label_container, alignment=Qt.AlignCenter)

        # Contêiner 3: Informações dos voos disponíveis
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        button_style = """
            QPushButton {
                background-color: #f1f1f1;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffcccc;  /* Vermelho claro /
            }
            QPushButton:pressed {
                background-color: #cce7ff;  / Azul claro */
            }
        """
        # Criação de uma label para mostrar as informações dos voos
        self.voo_info_label = QLabel("Informações do voo a serem exibidas aqui")
        self.voo_info_label.setStyleSheet(button_style)
        self.voo_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.voo_info_label)

        self.layout.addWidget(self.info_container)

        # Contêiner com o botão "Voltar"
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)

        # Chamar o método para listar os voos ao inicializar
        self.listar_voos()

    def listar_voos(self) -> None:
        """Atualiza a label com a lista de voos cadastrados no banco de dados."""
        try:
            # Consultar os voos no banco de dados
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, sigla, origem, destino, modelo_aviao FROM voos;")
                voos = cur.fetchall()
            
            # Formatar os dados dos voos para exibição
            voo_info = ""
            for voo in voos:
                voo_info += f"ID: {voo[0]} | Sigla: {voo[1]} | Origem: {voo[2]} | Destino: {voo[3]} | Modelo: {voo[4]}\n"

            # Atualizar a label com as informações dos voos
            self.voo_info_label.setText(voo_info if voo_info else "Nenhum voo cadastrado.")
        except Exception as e:
            self.voo_info_label.setText(f"Erro ao carregar os voos: {str(e)}")


class TelaAvioes_Listar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Aviões - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Contêiner "Lista de Aviões"
        self.label_container = QLabel("Lista de Aviões")
        self.label_container.setFont(montserrat_bold)
        self.label_container.setAlignment(Qt.AlignCenter)
        self.label_container.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.label_container, alignment=Qt.AlignCenter)

        # Contêiner de informações dos aviões disponíveis
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.aviao_info_label = QLabel()
        self.aviao_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.aviao_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.aviao_info_label)

        self.layout.addWidget(self.info_container)

        # Botão "Voltar"
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)

        # Carregar dados dos aviões
        self.carregar_lista_avioes()

    def carregar_lista_avioes(self):
        """Carrega a lista de aviões cadastrados e exibe na interface."""
        try:
            metodos_gerente = MetodosGerente()
            avioes = metodos_gerente.listar_avioes()
            if avioes:
                info_text = "ID | Sigla | Modelo | Assentos\n"
                info_text += "\n".join([f"{aviao[0]} | {aviao[1]} | {aviao[2]} | {aviao[3]}" for aviao in avioes])
            else:
                info_text = "Nenhum avião cadastrado."

            self.aviao_info_label.setText(info_text)
        except Exception as e:
            self.aviao_info_label.setText(f"Erro ao carregar aviões: {str(e)}")


class TelaVoos_Marcar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Marcar Voo - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = "./src/fonts/Montserrat-Bold.ttf"  # Atualize o caminho da fonte
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 1. Contêiner com o logo (centralizado)
        self.logo_container = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_container)
        self.logo_layout.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel(self.logo_container)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label)
        self.layout.addWidget(self.logo_container)

        # 2. Contêiner "Marcar Voo"
        self.label_container = QLabel("Marcar Voo")
        self.label_container.setFont(montserrat_bold)
        self.label_container.setAlignment(Qt.AlignCenter)
        self.label_container.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.label_container, alignment=Qt.AlignCenter)

        # 3. Contêiner de entrada para sigla
        self.sigla_container = QWidget()
        self.sigla_layout = QVBoxLayout(self.sigla_container)
        self.sigla_container.setContentsMargins(100, 10, 100, 10)
        self.sigla_layout.setSpacing(10)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Sigla")
        self.sigla_input.setStyleSheet("border: 1px solid #cccccc; padding: 5px; border-radius: 3px;")
        self.sigla_layout.addWidget(self.sigla_input)

        self.buscar_button = QPushButton("Buscar Voo")
        self.buscar_button.setFixedSize(200, 50)
        self.buscar_button.setStyleSheet(button_style)
        self.sigla_layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.sigla_container)

        # 4. Contêiner 3: Informações do voo
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.voo_info_label = QLabel("Informações do voo a serem exibidas aqui")
        self.voo_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.voo_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.voo_info_label)

        self.layout.addWidget(self.info_container)

        # 5. Contêiner com os botões "Marcar Voo" e "Voltar"
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        # Botão "Marcar Voo"
        self.confirmar_voo_button = QPushButton("Marcar Voo")
        self.confirmar_voo_button.setFixedSize(200, 50)
        self.confirmar_voo_button.setStyleSheet(button_style)
        self.confirmar_voo_button.setFont(montserrat_bold)
        self.confirmar_voo_button.clicked.connect(self.close)  # Implementar funcionalidade de marcação
        self.button_layout.addWidget(self.confirmar_voo_button)

        # Botão "Voltar"
        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.clicked.connect(self.close)  # Substituir por lógica de voltar
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)








class TelaAtendente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Layout da esquerda (logo e botões)
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(0)

        # Logo
        self.logo_label = QLabel(self)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        # Adicionar logo ao layout
        self.left_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)

        # Widget para centralizar botões
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Botões
        self.bt_clientes = QPushButton("Passageiros")
        self.bt_clientes.setFixedSize(200, 50)
        self.bt_clientes.setStyleSheet(button_style)
        self.bt_clientes.setFont(montserrat_bold)
        self.bt_clientes.clicked.connect(self.mostrar_tela_passageiros)

        self.bt_reservas = QPushButton("Reservas")
        self.bt_reservas.setFixedSize(200, 50)
        self.bt_reservas.setStyleSheet(button_style)
        self.bt_reservas.setFont(montserrat_bold)
        self.bt_reservas.clicked.connect(self.mostrar_tela_reservas)

        self.bt_chat = QPushButton("Chat")
        self.bt_chat.setFixedSize(200, 50)
        self.bt_chat.setStyleSheet(button_style)
        self.bt_chat.setFont(montserrat_bold)
        self.bt_chat.clicked.connect(self.mostrar_tela_chat_atendente)

        self.bt_sair = QPushButton("Sair")
        self.bt_sair.setFixedSize(200, 50)
        self.bt_sair.setStyleSheet(button_style)
        self.bt_sair.setFont(montserrat_bold)
        self.bt_sair.clicked.connect(self.mostrar_tela_inicial) 

        button_layout.addWidget(self.bt_clientes)
        button_layout.addWidget(self.bt_reservas)
        button_layout.addWidget(self.bt_sair)

        # Espaçador abaixo dos botões
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addSpacerItem(spacer)

        # Adicionar widget ao layout esquerdo
        self.left_layout.addWidget(button_widget, alignment=Qt.AlignTop)
        self.layout.addLayout(self.left_layout)

        # StackedWidget para trocar entre telas
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Placeholder inicial
        self.placeholder_widget = QWidget()
        self.stacked_widget.addWidget(self.placeholder_widget)

    def mostrar_tela_passageiros(self):
        self.tela_passageiros = TelaPassageiros()
        self.tela_passageiros.show()
    
    def mostrar_tela_reservas(self):
        self.tela_reservas = TelaReservas()
        self.tela_reservas.show()
    
    def mostrar_tela_inicial(self):
        self.tela_inicial = Tela()
        self.tela_inicial.show()
    
    def mostrar_tela_chat_atendente(self):
        self.tela_chat_atendente = TelaChat_Atendente()
        self.tela_chat_atendente.show()


class TelaChat_Atendente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = "path/to/your/font.ttf"  # Substitua pelo caminho correto da sua fonte
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        self.title_label = QLabel("Chat")
        self.title_label.setFont(montserrat_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Caixa de Mensagens
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.messages_container)
        self.scroll_area.setStyleSheet("background-color: #f5f5f5; border-radius: 10px; padding: 10px;")

        self.layout.addWidget(self.scroll_area)

        # Contêiner 3: Campo de mensagem e botão
        self.input_widget = QWidget()
        self.input_layout = QHBoxLayout(self.input_widget)
        self.input_layout.setContentsMargins(50, 20, 50, 0)
        self.input_layout.setSpacing(10)

        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Digite sua mensagem...")
        self.message_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc;")
        self.input_layout.addWidget(self.message_input)

        self.bt_enviar = QPushButton("Enviar")
        self.bt_enviar.setFixedSize(100, 40)
        self.bt_enviar.setStyleSheet(button_style)
        self.bt_enviar.setFont(montserrat_bold)
        self.input_layout.addWidget(self.bt_enviar)

        self.layout.addWidget(self.input_widget)

        # Inicializar a conexão
        self.usuario_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usuario_socket.connect((SERVER_HOST, SERVER_PORT))

        # Criar e iniciar thread para receber mensagens
        self.thread_recebida = threading.Thread(target=self.receber_mensagens, args=(self.usuario_socket,))
        self.thread_recebida.start()

        # Conectar o botão de enviar
        self.bt_enviar.clicked.connect(self.enviar_mensagem)

    def receber_mensagens(self, usuario_socket):
        while True:
            try:
                mensagem = usuario_socket.recv(1024).decode('utf-8')
                if mensagem:
                    self.adicionar_mensagem(mensagem, recebido=True)
            except:
                print("[ERRO] Conexão com o servidor perdida.")
                usuario_socket.close()
                break

    def adicionar_mensagem(self, mensagem, recebido):
        """Adicionar mensagem na interface com cores diferentes para enviadas e recebidas."""
        label = QLabel(mensagem)
        if recebido:
            label.setStyleSheet("background-color: #e0e0e0; border-radius: 10px; padding: 10px;")
        else:
            label.setStyleSheet("background-color: #add8e6; color: black; border-radius: 10px; padding: 10px;")
        label.setWordWrap(True)
        self.messages_layout.addWidget(label)

    def enviar_mensagem(self):
        """Enviar mensagem digitada pelo usuário."""
        mensagem = self.message_input.text()
        if mensagem:
            self.adicionar_mensagem(mensagem, recebido=False)
            self.usuario_socket.send(mensagem.encode('utf-8'))
            self.message_input.clear()




class TelaPassageiros(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Clientes - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Layout da esquerda
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(20)

        # Widget do logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.left_layout.addWidget(self.logo_widget)

        # Widget dos botões
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(15)
        self.button_layout.setAlignment(Qt.AlignTop)

        # Botões
        button_width = 200
        button_height = 50

        self.bt_cadastrar = QPushButton("Cadastrar")
        self.bt_cadastrar.setFixedSize(button_width, button_height)
        self.bt_cadastrar.setStyleSheet(button_style)
        self.bt_cadastrar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_cadastrar)
        self.bt_cadastrar.clicked.connect(self.mostrar_tela_cadastrar_passageiro)

        self.bt_alterar = QPushButton("Alterar")
        self.bt_alterar.setFixedSize(button_width, button_height)
        self.bt_alterar.setStyleSheet(button_style)
        self.bt_alterar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_alterar)
        self.bt_alterar.clicked.connect(self.mostrar_tela_alterar_passageiro)

        self.bt_remover = QPushButton("Remover")
        self.bt_remover.setFixedSize(button_width, button_height)
        self.bt_remover.setStyleSheet(button_style)
        self.bt_remover.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_remover)
        self.bt_remover.clicked.connect(self.mostrar_tela_remover_passageiro)

        self.bt_listar = QPushButton("Listar")
        self.bt_listar.setFixedSize(button_width, button_height)
        self.bt_listar.setStyleSheet(button_style)
        self.bt_listar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_listar)
        self.bt_listar.clicked.connect(self.mostrar_tela_listar_passageiro)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.button_layout.addWidget(self.bt_voltar)

        # Espaçador abaixo dos botões
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button_layout.addSpacerItem(spacer)

        # Adicionar widget dos botões ao layout esquerdo
        self.left_layout.addWidget(self.button_widget)

        # Adicionar layout esquerdo ao layout principal
        self.layout.addLayout(self.left_layout)

        # Placeholder para conteúdos adicionais
        self.placeholder_widget = QWidget()
        self.layout.addWidget(self.placeholder_widget)

    def mostrar_tela_cadastrar_passageiro(self):
        self.tela_cadastrar_passageiro = TelaPassageiros_Cadastrar()
        self.tela_cadastrar_passageiro.show()
        self.close()
    def mostrar_tela_alterar_passageiro(self):
        self.tela_alterar_passageiro = TelaPassageiros_Alterar()
        self.tela_alterar_passageiro.show()
        self.close()
    def mostrar_tela_remover_passageiro(self):
        self.tela_remover_passageiro = TelaPassageiros_Remover()
        self.tela_remover_passageiro.show()
        self.close()
    def mostrar_tela_listar_passageiro(self):
        self.tela_listar_passageiro = TelaPassageiros_Listar()
        self.tela_listar_passageiro.show()
        self.close()

class TelaReservas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Reservas - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Layout da esquerda
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(20)  # Espaçamento entre logo e botões

        # Widget do logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.left_layout.addWidget(self.logo_widget)

        # Widget dos botões
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(15)
        self.button_layout.setAlignment(Qt.AlignTop)

        # Botões
        button_width = 200
        button_height = 50

        self.bt_reservar = QPushButton("Reservar")
        self.bt_reservar.setFixedSize(button_width, button_height)
        self.bt_reservar.setStyleSheet(button_style)
        self.bt_reservar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_reservar)
        self.bt_reservar.clicked.connect(self.mostrar_tela_reservas_reservar)

        self.bt_cancelar = QPushButton("Remover")
        self.bt_cancelar.setFixedSize(button_width, button_height)
        self.bt_cancelar.setStyleSheet(button_style)
        self.bt_cancelar.setFont(montserrat_bold)
        self.button_layout.addWidget(self.bt_cancelar)
        self.bt_cancelar.clicked.connect(self.mostrar_tela_reservas_remover)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.button_layout.addWidget(self.bt_voltar)

        # Espaçador abaixo dos botões
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button_layout.addSpacerItem(spacer)

        # Adicionar widget dos botões ao layout esquerdo
        self.left_layout.addWidget(self.button_widget)

        # Adicionar layout esquerdo ao layout principal
        self.layout.addLayout(self.left_layout)

        # Placeholder para conteúdos adicionais
        self.placeholder_widget = QWidget()
        self.layout.addWidget(self.placeholder_widget)
    
    def mostrar_tela_reservas_reservar(self):
        self.tela_reservas_reservar = TelaReservas_Reservar()
        self.tela_reservas_reservar.show()
        self.close()
    
    def mostrar_tela_reservas_remover(self):
        self.tela_reservas_remover = TelaReservas_Remover()
        self.tela_reservas_remover.show()
        self.close()


class TelaPassageiros_Cadastrar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastrar Cliente - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Inicializar conexão com o banco de dados
        self.backend = CadastroClientes()

        # Carregar a fonte Montserrat
        if os.path.exists("font_path"):
            QFontDatabase.addApplicationFont("font_path")
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo e frase "Cadastrando Clientes"
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        self.title_label = QLabel("Cadastrar Passageiro")
        self.title_label.setFont(montserrat_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Campos de entrada
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        self.form_layout.setContentsMargins(50, 20, 50, 0)
        self.form_layout.setSpacing(20)

        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Nome")
        self.nome_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.nome_input)

        self.cpf_input = QLineEdit(self)
        self.cpf_input.setPlaceholderText("CPF")
        self.cpf_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.cpf_input)

        self.telefone_input = QLineEdit(self)
        self.telefone_input.setPlaceholderText("Telefone")
        self.telefone_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.telefone_input)

        self.layout.addWidget(self.form_widget)

        # Contêiner 3: Botões
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 30, 0, 0)
        self.buttons_layout.setSpacing(20)

        button_width = 200
        button_height = 50

        self.bt_cadastrar = QPushButton("Cadastrar")
        self.bt_cadastrar.setFixedSize(button_width, button_height)
        self.bt_cadastrar.setStyleSheet(button_style)
        self.bt_cadastrar.setFont(montserrat_bold)
        self.bt_cadastrar.clicked.connect(self.cadastrar_cliente)  # Conecta ao método de cadastro
        self.buttons_layout.addWidget(self.bt_cadastrar, alignment=Qt.AlignCenter)

        # Botão "Voltar"
        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)  # Conecta ao método de fechar a janela
        self.buttons_layout.addWidget(self.bt_voltar, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.buttons_widget)

    def cadastrar_cliente(self):
        """
        Método chamado ao clicar no botão "Cadastrar".
        Faz o cadastro do cliente no banco de dados.
        """
        nome = self.nome_input.text().strip()
        cpf = self.cpf_input.text().strip()
        telefone = self.telefone_input.text().strip()

        if not nome or not cpf or not telefone:
            self.show_message("Erro", "Todos os campos devem ser preenchidos!")
            return

        sucesso, mensagem = self.backend.cadastrar_cliente(nome, cpf, telefone)
        self.show_message("Resultado do Cadastro", mensagem)

        if sucesso:
            # Limpar os campos após o cadastro bem-sucedido
            self.nome_input.clear()
            self.cpf_input.clear()
            self.telefone_input.clear()

    def show_message(self, titulo, mensagem):
        """
        Exibe uma mensagem em uma janela modal.
        """
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

class TelaPassageiros_Alterar(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alterar Passageiro - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = "./src/fonts/Montserrat-Bold.ttf"
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Configuração de CPF
        self.cpf_input = QLineEdit()
        self.cpf_input.setPlaceholderText("Digite o CPF do passageiro")
        self.cpf_input.setStyleSheet(line_edit_style)
        self.layout.addWidget(self.cpf_input)

        # Botão Buscar Passageiro
        self.buscar_button = QPushButton("Buscar Passageiro")
        self.buscar_button.setFixedSize(200, 50)
        self.buscar_button.setFont(montserrat_bold)
        self.buscar_button.setStyleSheet(button_style)
        self.layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)
        self.buscar_button.clicked.connect(self.buscar_passageiro)

        # Informações do passageiro
        self.passageiro_info_label = QLabel("Informações do passageiro serão exibidas aqui")
        self.passageiro_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.layout.addWidget(self.passageiro_info_label)

        # Campos de edição
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Digite o nome do passageiro")
        self.layout.addWidget(self.nome_input)

        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("Digite o telefone do passageiro")
        self.layout.addWidget(self.telefone_input)

        # Botão Alterar Passageiro
        self.alterar_button = QPushButton("Alterar Passageiro")
        self.alterar_button.setFixedSize(200, 50)
        self.alterar_button.setFont(montserrat_bold)
        self.alterar_button.setStyleSheet(button_style)
        self.layout.addWidget(self.alterar_button, alignment=Qt.AlignCenter)
        self.alterar_button.clicked.connect(self.alterar_passageiro)

        # Botão Voltar
        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.layout.addWidget(self.voltar_button, alignment=Qt.AlignCenter)
        self.voltar_button.clicked.connect(self.close)

    def buscar_passageiro(self):
        cpf = self.cpf_input.text().strip()
        if not cpf:
            QMessageBox.warning(self, "Erro", "Digite o CPF do passageiro.")
            return
        
        db = CadastroClientes()

        cliente = db.buscar_cliente_por_cpf(cpf)
        if cliente:
            _, nome, cpf, telefone = cliente
            self.passageiro_info_label.setText(f"Nome: {nome}\nTelefone: {telefone}")
            self.nome_input.setText(nome)
            self.telefone_input.setText(telefone)
        else:
            QMessageBox.warning(self, "Erro", "Passageiro não encontrado.")
            self.passageiro_info_label.setText("")

    def alterar_passageiro(self):
        nome = self.nome_input.text().strip()
        telefone = self.telefone_input.text().strip()
        cpf = self.cpf_input.text().strip()

        if not nome or not telefone or not cpf:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        db = CadastroClientes()

        sucesso, mensagem = db.alterar_cliente(cpf, nome, telefone)
        if sucesso:
            QMessageBox.information(self, "Sucesso", "Dados do passageiro alterados com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", mensagem)



class TelaPassageiros_Remover(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Removendo Passageiros - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)  # Logo centralizada
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Adicionar a frase "Remover Passageiro" abaixo da logo
        self.remove_passageiro_label = QLabel("Remover Passageiro")
        self.remove_passageiro_label.setFont(montserrat_bold)
        self.remove_passageiro_label.setAlignment(Qt.AlignCenter)
        self.remove_passageiro_label.setStyleSheet("color: #333333; margin-top: 10px;")
        self.logo_layout.addWidget(self.remove_passageiro_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner 2: Entrada de CPF e botão de busca
        self.cpf_container = QWidget()
        self.cpf_layout = QVBoxLayout(self.cpf_container)
        self.cpf_layout.setSpacing(10)
        self.cpf_container.setContentsMargins(100, 10, 100, 10)

        self.cpf_input = QLineEdit()
        self.cpf_input.setPlaceholderText("CPF do Passageiro")
        self.cpf_input.setStyleSheet(line_edit_style)
        self.cpf_layout.addWidget(self.cpf_input)

        self.buscar_button = QPushButton("Buscar Passageiro")
        self.buscar_button.setFixedSize(200, 50)
        self.buscar_button.setStyleSheet(button_style)
        self.cpf_layout.addWidget(self.buscar_button, alignment=Qt.AlignCenter)
        self.buscar_button.clicked.connect(self.buscar_passageiro)

        self.layout.addWidget(self.cpf_container)

        # Contêiner 3: Informações do passageiro
        self.info_container = QWidget()
        self.info_layout = QVBoxLayout(self.info_container)
        self.info_container.setContentsMargins(100, 10, 100, 10)
        self.info_layout.setSpacing(10)

        self.passageiro_info_label = QLabel("Informações do passageiro a serem exibidas aqui")
        self.passageiro_info_label.setStyleSheet("border: 1px solid #cccccc; padding: 10px; border-radius: 3px;")
        self.passageiro_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_layout.addWidget(self.passageiro_info_label)

        self.layout.addWidget(self.info_container)

        # Contêiner 4: Botões de remover e voltar
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.remover_passageiro_button = QPushButton("Remover Passageiro")
        self.remover_passageiro_button.setFixedSize(200, 50)
        self.remover_passageiro_button.setStyleSheet(button_style)
        self.remover_passageiro_button.setFont(montserrat_bold)
        self.remover_passageiro_button.clicked.connect(self.remover_passageiro)
        self.button_layout.addWidget(self.remover_passageiro_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)
    
    def buscar_passageiro(self):
        cpf = self.cpf_input.text().strip()
        
        if not cpf:
            QMessageBox.warning(self, "Erro", "Digite o CPF do passageiro.")
            return

        try:
            db = CadastroClientes()
            cliente = db.buscar_cliente_por_cpf(cpf)

            if cliente:
                _, nome, cpf, telefone = cliente
                self.passageiro_info_label.setText(f"Nome: {nome}\nCPF: {cpf}\nTelefone: {telefone}")
            else:
                QMessageBox.warning(self, "Erro", "Passageiro não encontrado.")
                self.passageiro_info_label.setText("Informações do passageiro a serem exibidas aqui")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar passageiro: {str(e)}")

    def remover_passageiro(self):
        cpf = self.cpf_input.text().strip()

        if not cpf:
            QMessageBox.warning(self, "Erro", "Por favor, informe o CPF do passageiro.")
            return

        resposta = QMessageBox.question(
            self, 
            "Confirmação", 
            f"Tem certeza que deseja remover o passageiro com CPF {cpf}?", 
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            db = CadastroClientes()
            sucesso, mensagem = db.excluir_cliente(cpf)

            if sucesso:
                QMessageBox.information(self, "Sucesso", "Passageiro removido com sucesso!")
                self.cpf_input.clear()
                self.passageiro_info_label.setText("Informações do passageiro a serem exibidas aqui")
            else:
                QMessageBox.warning(self, "Erro", mensagem)

class TelaPassageiros_Listar(QMainWindow):
    def __init__(self, db_config=None):
        if db_config is None:
            db_config = {
                'dbname': 'credenciais',
                'user': 'poodois',
                'password': '1234',
                'host': 'localhost',
                'port': 5432
            }

        super().__init__()
        self.setWindowTitle("Lista de Passageiros - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Conectar ao banco de dados para obter a lista de clientes
        self.cadastro_clientes = ListarClientes(db_config)  # Instancia a classe de ListarClientes
        self.clientes = self.cadastro_clientes.listar_clientes()  # Busca os clientes cadastrados

        # Carregar a fonte Montserrat
        font_path = os.path.abspath("./src/fonts/Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)  # Logo centralizada
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Contêiner "Lista de Passageiros"
        self.label_container = QLabel("Lista de Passageiros")
        self.label_container.setFont(montserrat_bold)
        self.label_container.setAlignment(Qt.AlignCenter)
        self.label_container.setStyleSheet("color: #333333; margin-top: 20px;")
        self.layout.addWidget(self.label_container, alignment=Qt.AlignCenter)

        # Tabela de clientes
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(4)  # Quatro colunas: ID, Nome, CPF, Telefone
        self.tabela_clientes.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Telefone"])
        self.tabela_clientes.setSelectionMode(QAbstractItemView.NoSelection)  # Desativa seleção de células
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Impede edição das células
        self.tabela_clientes.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                font-size: 12px;
                color: #333333;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::horizontalHeader {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QTableWidget::verticalHeader {
                background-color: #f1f1f1;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #4CAF50;
                border-radius: 5px;
            }
        """)

        # Populando a tabela com dados
        self.atualizar_tabela()

        # Scroll para a tabela
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.tabela_clientes)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Contêiner com o botão "Voltar"
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)  
        self.voltar_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.button_container)

    def atualizar_tabela(self):
        """Atualiza os dados na tabela de clientes"""
        if self.clientes:
            self.tabela_clientes.setRowCount(len(self.clientes))
            for i, cliente in enumerate(self.clientes):
                self.tabela_clientes.setItem(i, 0, QTableWidgetItem(str(cliente[0])))  # ID
                self.tabela_clientes.setItem(i, 1, QTableWidgetItem(cliente[1]))  # Nome
                self.tabela_clientes.setItem(i, 2, QTableWidgetItem(cliente[2]))  # CPF
                self.tabela_clientes.setItem(i, 3, QTableWidgetItem(cliente[3]))  # Telefone
        else:
            # Se não houver clientes, exibe uma linha vazia com uma mensagem
            self.tabela_clientes.setRowCount(1)
            self.tabela_clientes.setItem(0, 0, QTableWidgetItem("Nenhum cliente cadastrado"))
            for col in range(1, 4):
                self.tabela_clientes.setItem(0, col, QTableWidgetItem(""))


class TelaReservas_Reservar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reservar Voo - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Backend connection
        self.backend = BackendReservas()

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Contêiner: Lista de voos disponíveis
        self.voos_container = QWidget()
        self.voos_layout = QVBoxLayout(self.voos_container)
        self.voos_layout.setContentsMargins(100, 10, 100, 10)
        self.voos_layout.setSpacing(15)

        self.voos_label = QLabel("Voos disponíveis")
        self.voos_label.setFont(montserrat_bold)
        self.voos_label.setAlignment(Qt.AlignCenter)
        self.voos_layout.addWidget(self.voos_label)

        self.voos_lista_label = QLabel()
        self.voos_lista_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.voos_lista_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.voos_layout.addWidget(self.voos_lista_label)

        self.layout.addWidget(self.voos_container)

        # Atualizar lista de voos disponíveis
        self.atualizar_lista_voos()

        # Contêiner: Seleção do voo
        self.selecao_voo_container = QWidget()
        self.selecao_voo_layout = QVBoxLayout(self.selecao_voo_container)
        self.selecao_voo_layout.setContentsMargins(100, 10, 100, 10)
        self.selecao_voo_layout.setSpacing(15)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Sigla do voo para reserva")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.selecao_voo_layout.addWidget(self.sigla_input)

        self.layout.addWidget(self.selecao_voo_container)

        # Contêiner: Botões "Reservar Voo" e "Voltar"
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.buttons_layout.setSpacing(20)

        self.reservar_button = QPushButton("Reservar Voo")
        self.reservar_button.setFixedSize(200, 50)
        self.reservar_button.setFont(montserrat_bold)
        self.reservar_button.setStyleSheet(button_style)
        self.reservar_button.clicked.connect(self.reservar_voo)
        self.buttons_layout.addWidget(self.reservar_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.buttons_container)

    def atualizar_lista_voos(self):
        voos = self.backend.listar_voos()
        if voos:
            texto_voos = "\n".join(
                [f"Sigla: {voo[0]}, Origem: {voo[1]}, Destino: {voo[2]}, Modelo: {voo[3]}, Assentos disponíveis: {voo[4]}" for voo in voos]
            )
        else:
            texto_voos = "Nenhum voo disponível."
        self.voos_lista_label.setText(texto_voos)

    def reservar_voo(self):
        sigla = self.sigla_input.text().strip()

        if not sigla:
            self.voos_lista_label.setText("Por favor, insira uma sigla válida.")
            return

        mensagem = self.backend.reservar_voo(sigla, 1)
        self.voos_lista_label.setText(mensagem)
        self.atualizar_lista_voos()

    def closeEvent(self, event):
        self.backend.close_connection()
        super().closeEvent(event)




class TelaReservas_Remover(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remover Reserva - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Backend connection
        self.backend = BackendRemoverReservas()

        # Carregar a fonte Montserrat
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)

        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")

        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Contêiner: Lista de voos disponíveis
        self.voos_container = QWidget()
        self.voos_layout = QVBoxLayout(self.voos_container)
        self.voos_layout.setContentsMargins(100, 10, 100, 10)
        self.voos_layout.setSpacing(15)

        self.voos_label = QLabel("Voos disponíveis")
        self.voos_label.setFont(montserrat_bold)
        self.voos_label.setAlignment(Qt.AlignCenter)
        self.voos_layout.addWidget(self.voos_label)

        self.voos_lista_label = QLabel()
        self.voos_lista_label.setStyleSheet("border: 1px solid #cccccc; padding: 8px; border-radius: 5px;")
        self.voos_lista_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.voos_layout.addWidget(self.voos_lista_label)

        self.layout.addWidget(self.voos_container)

        # Atualizar lista de voos disponíveis
        self.atualizar_lista_voos()

        # Contêiner: Seleção do voo
        self.selecao_voo_container = QWidget()
        self.selecao_voo_layout = QVBoxLayout(self.selecao_voo_container)
        self.selecao_voo_layout.setContentsMargins(100, 10, 100, 10)
        self.selecao_voo_layout.setSpacing(15)

        self.sigla_input = QLineEdit()
        self.sigla_input.setPlaceholderText("Sigla do voo para reserva")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.selecao_voo_layout.addWidget(self.sigla_input)

        self.layout.addWidget(self.selecao_voo_container)

        # Contêiner: Botões "Reservar Voo" e "Voltar"
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        self.buttons_layout.setSpacing(20)

        self.reservar_button = QPushButton("Remover Reserva do Voo")
        self.reservar_button.setFixedSize(200, 50)
        self.reservar_button.setFont(montserrat_bold)
        self.reservar_button.setStyleSheet(button_style)
        self.reservar_button.clicked.connect(self.remover_reserva_voo)
        self.buttons_layout.addWidget(self.reservar_button)

        self.voltar_button = QPushButton("Voltar")
        self.voltar_button.setFixedSize(200, 50)
        self.voltar_button.setFont(montserrat_bold)
        self.voltar_button.setStyleSheet(button_style)
        self.voltar_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.voltar_button)

        self.layout.addWidget(self.buttons_container)

    def atualizar_lista_voos(self):
        voos = self.backend.listar_voos()
        if voos:
            texto_voos = "\n".join(
                [f"Sigla: {voo[0]}, Origem: {voo[1]}, Destino: {voo[2]}, Modelo: {voo[3]}, Assentos disponíveis: {voo[4]}" for voo in voos]
            )
        else:
            texto_voos = "Nenhum voo disponível."
        self.voos_lista_label.setText(texto_voos)

    def remover_reserva_voo(self):
        sigla = self.sigla_input.text().strip()

        if not sigla:
            self.voos_lista_label.setText("Por favor, insira uma sigla válida.")
            return

        mensagem = self.backend.remover_reserva_voo(sigla, 1)
        self.voos_lista_label.setText(mensagem)
        self.atualizar_lista_voos()

    def closeEvent(self, event):
        self.backend.close_connection()
        super().closeEvent(event)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())

    import psycopg2

class GerenciadorDeReservas:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)

    def listar_voos(self):
        """Retorna todos os voos disponíveis no banco."""
        try:
            self.cursor.execute("SELECT * FROM voos;")
            voos = self.cursor.fetchall()
            return voos
        except Exception as e:
            print("Erro ao listar voos:", e)
            return []

    def adicionar_voo(self, sigla, origem, destino, modelo_aviao):
        """Adiciona um novo voo ao banco."""
        try:
            self.cursor.execute(
                "INSERT INTO voos (sigla, origem, destino, modelo_aviao) VALUES (%s, %s, %s, %s);",
                (sigla, origem, destino, modelo_aviao)
            )
            self.conn.commit()
            print("Voo adicionado com sucesso.")
        except Exception as e:
            print("Erro ao adicionar voo:", e)

    def remover_reserva_voo(self, id_voo):
        """Remove um voo do banco com base no ID."""
        try:
            self.cursor.execute("DELETE FROM voos WHERE id = %s;", (id_voo,))
            self.conn.commit()
            print("Voo removido com sucesso.")
        except Exception as e:
            print("Erro ao remover voo:", e)

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("Erro ao fechar a conexão:", e)
