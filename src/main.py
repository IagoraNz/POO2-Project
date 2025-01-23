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

# Caminho para a fonte personalizada
font_path = os.path.abspath("./src/fonts/Montserrat-SemiBold.ttf")

# Estilo dos botões
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

# Estilo do plano de fundo
background_style = """
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
"""

# Estilo dos campos de texto
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
    """
    Summary:
        Classe principal da interface gráfica da aplicação. Contendo login, cadastro e redirecionamentos
    
    Attributes:
        QWidget (QWidget): Classe base para todos os widgets
        
    Methods:
        mostrar_formulario_cadastro: Exibe o formulário de cadastro de um novo usuário
        voltar_inicial_pelo_cadastro: Volta à tela inicial após o cadastro
        efetuar_cadastro: Realiza o cadastro de um novo usuário
        voltar_tela_inicial: Retorna à tela inicial após o cadastro
        mostrar_formulario_login: Exibe o formulário de login
        efetuar_login: Realiza a autenticação do usuário
        mostrar_tela_home: Exibe a tela principal do Gerente
        mostrar_tela_home2: Exibe a tela principal do At
    """

    def __init__(self, user=None, senha=None):
        """
        Inicializa a interface gráfica.

        Args:
            user (str, optional): Usuário para autenticação. Default é None.
            senha (str, optional): Senha para autenticação. Default é None.
        """
        super().__init__()
        self.setWindowTitle("DELTA")
        self.setFixedSize(1000, 500)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        # Carregar fonte personalizada ou usar fonte padrão
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        self.setStyleSheet("background-color: white;")

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 0, 10, 175)
        self.layout.setSpacing(10)

        # Layout para a imagem da logomarca
        self.image_layout = QHBoxLayout()
        self.image_layout.setContentsMargins(0, 35, 0, 0)
        self.image_layout.setSpacing(0)

        # Adicionar logomarca
        self.label = QLabel(self)
        image_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(resized_pixmap)
        else:
            self.label.setText("Imagem não encontrada.")
        self.image_layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addLayout(self.image_layout)

        # Texto de boas-vindas
        self.welcome_label = QLabel(self)
        self.welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 20px;")
        self.welcome_label.setFont(montserrat_bold)
        self.layout.addWidget(self.welcome_label)

        # Espaçamento entre widgets
        self.layout.addSpacing(-25)

        # Botão de login
        bt_login = QPushButton("Login")
        bt_login.setFixedSize(200, 50)
        bt_login.setStyleSheet(button_style)
        bt_login.setFont(montserrat_bold)
        bt_login.clicked.connect(self.mostrar_formulario_login)
        self.layout.addWidget(bt_login, alignment=Qt.AlignHCenter)

        # Botão de cadastro
        bt_cadastrar = QPushButton("Cadastro")
        bt_cadastrar.setFixedSize(200, 50)
        bt_cadastrar.setStyleSheet(button_style)
        bt_cadastrar.setFont(montserrat_bold)
        bt_cadastrar.clicked.connect(self.mostrar_formulario_cadastro)
        self.layout.addWidget(bt_cadastrar, alignment=Qt.AlignHCenter)

        # Imagem no canto inferior direito
        self.bottom_image_label = QLabel(self)
        bottom_image_path = os.path.abspath("./src/images/aviao.png")
        if os.path.exists(bottom_image_path):
            pixmap = QPixmap(bottom_image_path)
            resized_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.bottom_image_label.setPixmap(resized_pixmap)
        else:
            self.bottom_image_label.setText("Imagem não encontrada.")

        # Autenticação do usuário
        self.auth = Autenticacao(user, senha)

        # Configurar layout principal
        self.setLayout(self.layout)

    def resizeEvent(self, event) -> None:
        """
        Summary:
            Mantém a imagem posicionada no canto inferior direito ao redimensionar a janela.

        Args:
            event (QResizeEvent): Evento de redimensionamento.
            
        Returns:
            None
        """
        self.bottom_image_label.setGeometry(
            self.width() - 300,
            self.height() - 235,
            300, 300
        )
        super().resizeEvent(event)

    def mostrar_formulario_cadastro(self) -> None:
        """
        Summary:
            Exibe o formulário de cadastro, ocultando a tela de boas-vindas.
        
        Args:
            None
            
        Returns:
            None
        """
        self.welcome_label.setText("")
        self.layout.itemAt(3).widget().setVisible(False)
        self.layout.itemAt(4).widget().setVisible(False)

        # Criação dos campos de entrada (se ainda não existirem)
        if not hasattr(self, 'usuario_input'):
            tipo_funcionario_label = QLabel("Digite 1 para Gerente ou 2 para Atendente.", self)
            tipo_funcionario_label.setAlignment(Qt.AlignHCenter)
            tipo_funcionario_label.setStyleSheet("color: darkgray;")
            self.layout.addWidget(tipo_funcionario_label, alignment=Qt.AlignHCenter)

            self.usuario_input = QLineEdit(self)
            self.usuario_input.setPlaceholderText("Usuário")
            self.usuario_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.usuario_input, alignment=Qt.AlignHCenter)

            self.senha_input = QLineEdit(self)
            self.senha_input.setPlaceholderText("Senha")
            self.senha_input.setEchoMode(QLineEdit.Password)
            self.senha_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.senha_input, alignment=Qt.AlignHCenter)

            self.tipo_input = QLineEdit(self)
            self.tipo_input.setPlaceholderText("Tipo de Funcionário")
            self.tipo_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.tipo_input, alignment=Qt.AlignHCenter)

            bt_efetuar_cadastro = QPushButton("Efetuar Cadastro")
            bt_efetuar_cadastro.setFixedSize(200, 50)
            bt_efetuar_cadastro.setStyleSheet(button_style)
            bt_efetuar_cadastro.setFont(QFont("Montserrat", 10, QFont.Bold))
            bt_efetuar_cadastro.clicked.connect(self.efetuar_cadastro)
            bt_efetuar_cadastro.clicked.connect(self.voltar_inicial_pelo_cadastro)
            self.layout.addWidget(bt_efetuar_cadastro, alignment=Qt.AlignHCenter)

        # Tornar os campos de cadastro visíveis
        self.layout.itemAt(5).widget().setVisible(True)
        self.layout.itemAt(6).widget().setVisible(True)
        self.layout.itemAt(7).widget().setVisible(True)
        self.layout.itemAt(8).widget().setVisible(True)
        self.layout.itemAt(9).widget().setVisible(True)
        
    def voltar_inicial_pelo_cadastro(self) -> None:
        """
        Summary:
            Retorna à tela inicial após o cadastro.
            
        Args:
            None
            
        Returns:
            None
        """
        # Limpar os campos de cadastro
        if hasattr(self, 'usuario_input') and self.usuario_input.isVisible():
            if self.usuario_input.text():
                self.usuario_input.setText("")
            if hasattr(self, 'senha_input') and self.senha_input.text():
                self.senha_input.setText("")
            if hasattr(self, 'tipo_input') and self.tipo_input.isVisible() and self.tipo_input.text():
                self.tipo_input.setText("")

        # Remover os campos de login
        self.layout.itemAt(5).widget().setVisible(False)
        self.layout.itemAt(6).widget().setVisible(False)
        self.layout.itemAt(7).widget().setVisible(False)
        self.layout.itemAt(8).widget().setVisible(False)
        self.layout.itemAt(9).widget().setVisible(False)

        # Limpar a tela de boas-vindas e botões
        self.welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        self.layout.itemAt(3).widget().setVisible(True)
        self.layout.itemAt(4).widget().setVisible(True)
        
        # Fechar a tela atual e abrir a tela inicial
        self.close()
        self.tela_inicial = Tela()  # Crie uma nova instância da tela inicial
        self.tela_inicial.show()
        
    def efetuar_cadastro(self) -> None:
        """
        Summary:
            Realiza o cadastro de um novo usuário no sistema, validando os campos de entrada.
        
        Args:
            None
            
        Returns:
            None
        """
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()
        tipo = self.tipo_input.text()

        # Verifica se todos os campos foram preenchidos
        if not usuario or not senha or not tipo:
            print("Todos os campos devem ser preenchidos!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Todos os campos devem ser preenchidos!")
            msg.exec_()
            return

        # Verifica se a senha tem o mínimo de 8 caracteres
        if len(senha) < 8:
            print("A senha deve ter no mínimo 8 dígitos")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("A senha deve ter no mínimo 8 dígitos! Tente novamente...")
            msg.exec_()
            return

        # Verifica se o tipo de usuário é válido
        if tipo not in ["1", "2"]:
            print("Tipo de usuário inválido! Deve ser 1 (Gerente) ou 2 (Atendente)")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Tipo de usuário inválido! Deve ser 1 (Gerente) ou 2 (Atendente)")
            msg.exec_()
            return

        # Realiza o cadastro através da classe de autenticação
        if self.auth.cadastro(usuario, senha, tipo):
            print(f"Usuário {usuario} cadastrado com sucesso!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Sucesso")
            msg.setText(f"Usuário {usuario} cadastrado com sucesso!")
            msg.exec_()
            self.voltar_tela_inicial()
        else:
            # Exibe mensagem de erro caso o usuário já exista
            print(f"Erro: Usuário {usuario} já existe.")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Erro")
            msg.setText(f"Erro: Usuário {usuario} já existe.")
            msg.exec_()

    def voltar_tela_inicial(self) -> None:
        """
        Summary:
            Retorna à tela inicial após o cadastro.

        Args:
            None
            
        Returns:
            None
        """
        # Limpar os campos de cadastro
        self.usuario_input.setText("")
        self.senha_input.setText("")
        self.tipo_input.setText("")

        # Remover os campos de cadastro
        self.layout.itemAt(5).widget().setVisible(False)
        self.layout.itemAt(6).widget().setVisible(False)
        self.layout.itemAt(7).widget().setVisible(False)
        self.layout.itemAt(8).widget().setVisible(False)

        # Reexibir a tela inicial
        self.welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        self.layout.itemAt(3).widget().setVisible(True)
        self.layout.itemAt(4).widget().setVisible(True)

    def mostrar_formulario_login(self) -> None:
        """
        Summary:
            Exibe o formulário de login, com campos para usuário e senha.
        
        Args:
            None
            
        Returns:
            None
        """
        # Limpar a tela de boas-vindas e botões
        self.welcome_label.setText("")
        self.layout.itemAt(3).widget().setVisible(False)
        self.layout.itemAt(4).widget().setVisible(False)

        # Criar os campos de login, caso ainda não existam
        if not hasattr(self, 'login_usuario_input'):
            # Campo de entrada para o usuário
            self.login_usuario_input = QLineEdit(self)
            self.login_usuario_input.setPlaceholderText("Usuário")
            self.login_usuario_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.login_usuario_input, alignment=Qt.AlignHCenter)

            # Campo de entrada para a senha
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

        # Exibir o formulário de login
        self.layout.itemAt(5).widget().setVisible(True)
        self.layout.itemAt(6).widget().setVisible(True)
        self.layout.itemAt(7).widget().setVisible(True)

    def efetuar_login(self) -> None:
        """
        Realiza a autenticação do usuário.

        Args:
            None
            
        Returns:
            None
        """
        usuario = self.login_usuario_input.text()
        senha = self.login_senha_input.text()

        # Verifica se os campos foram preenchidos
        if not usuario or not senha:
            print("Todos os campos devem ser preenchidos!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Todos os campos devem ser preenchidos!")
            msg.exec_()
            return

        # Verifica a autenticidade do login
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
            # Login inválido
            print("Usuário ou senha incorretos!")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Inválido")
            msg.setText("Usuário ou senha incorretos! Tente novamente...")
            msg.exec_()

    def mostrar_tela_home(self) -> None:
        """
        Summary:
            Exibe a tela principal do Gerente.
        
        Args:
            None
            
        Returns:
            None
        """
        self.tela_gerente = TelaGerente()
        self.tela_gerente.show()
        self.close()

    def mostrar_tela_home2(self) -> None:
        """
        Summary:
            Exibe a tela principal do Atendente.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_atendente = TelaAtendente()
        self.tela_atendente.show()
        self.close()

class TelaGerente(QMainWindow):
    """
    Summary:
        Classe responsável pela tela de gerenciamento para o gerente
    
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos

    Methods:
        mostrar_tela_voos: Exibe a tela de gerenciamento de voos
        mostrar_tela_avioes: Exibe a tela de gerenciamento de aviões
        mostrar_tela_inicial: Retorna à tela inicial do sistema
        mostrar_tela_chat_gerente: Exibe a tela de chat para o gerente
        mostrar_tela_marcar_voo: Exibe a tela para marcar
    """

    def __init__(self):
        """
        Inicializa a tela do gerente. Configura o layout principal, estilos, e os botões de navegação. Além disso 
        define também o logo da empresa e o espaço para alternar entre telas.
        """
        super().__init__()
        self.setWindowTitle("Gerenciamento - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat, com fallback para Arial
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        # Configuração do layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Configuração do layout da esquerda
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(20, 35, 0, 0)
        self.left_layout.setSpacing(0)

        # Adiciona o logo
        self.logo_label = QLabel(self)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.left_layout.addWidget(self.logo_label, alignment=Qt.AlignTop)

        # Widget centralizador para botões
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(400, 80, 0, 0)
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)

        # Botões de navegação
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

        self.bt_marcar_voo = QPushButton("Marcar Voo")
        self.bt_marcar_voo.setFixedSize(200, 50)
        self.bt_marcar_voo.setStyleSheet(button_style)
        self.bt_marcar_voo.setFont(montserrat_bold)
        self.bt_marcar_voo.clicked.connect(self.mostrar_tela_marcar_voo)

        self.bt_sair = QPushButton("Sair")
        self.bt_sair.setFixedSize(200, 50)
        self.bt_sair.setStyleSheet(button_style)
        self.bt_sair.setFont(montserrat_bold)
        self.bt_sair.clicked.connect(self.mostrar_tela_inicial)

        # Adicionar botões ao layout
        button_layout.addWidget(self.bt_voos)
        button_layout.addWidget(self.bt_avioes)
        button_layout.addWidget(self.bt_chat)
        button_layout.addWidget(self.bt_marcar_voo)
        button_layout.addWidget(self.bt_sair)

        # Adiciona um espaçador abaixo dos botões
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addSpacerItem(spacer)

        # Adiciona o widget dos botões ao layout esquerdo
        self.left_layout.addWidget(button_widget, alignment=Qt.AlignTop)
        self.layout.addLayout(self.left_layout)

        # Configuração do espaço para alternância entre telas
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Placeholder inicial
        self.placeholder_widget = QWidget()
        self.stacked_widget.addWidget(self.placeholder_widget)

    def mostrar_tela_voos(self) -> None:
        """
        Summary:
            Exibe a tela de gerenciamento de voos.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_voos = TelaVoos()
        self.tela_voos.show()

    def mostrar_tela_avioes(self) -> None:
        """
        Summary:
            Exibe a tela de gerenciamento de aviões.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_avioes = TelaAvioes()
        self.tela_avioes.show()

    def mostrar_tela_inicial(self) -> None:
        """
        Summary:
            Retorna à tela inicial do sistema.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_inicial = Tela()
        self.tela_inicial.show()

    def mostrar_tela_chat_gerente(self) -> None:
        """
        Summary:
            Exibe a tela de chat para o gerente.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_chat_gerente = TelaChat_Gerente()
        self.tela_chat_gerente.show()

    def mostrar_tela_marcar_voo(self):
        self.tela_marcar_voo = TelaMarcarVoo_Gerente()
        self.tela_marcar_voo.show()

# Variáveis globais para a conexão com o servidor
SERVER_HOST = '26.7.161.228'
SERVER_PORT = 5555

class TelaChat_Gerente(QMainWindow):
    """
    Summary:
        Classe responsável pela tela de chat para o gerente. Esta classe permite ao gerente enviar e receber mensagens em tempo real
        através de uma conexão socket com o servidor.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        _configurar_logo_e_titulo: Configura o contêiner com o logo e o título
        _configurar_caixa_de_mensagens: Configura o contêiner para exibição das mensagens
        _configurar_input_e_botao: Configura o campo de entrada e o botão de envio
        receber_mensagens: Thread responsável por receber mensagens do servidor
        exibir_mensagem: Exibe uma mensagem na caixa de mensagens
        enviar_mensagem: Envia a mensagem digitada pelo usuário ao servidor
    """

    def __init__(self):
        """
        Inicializa a interface de chat do gerente. Configura o layout principal, componentes visuais (logo, campo de mensagens, botão de envio)
        e a conexão socket com o servidor.
        """
        super().__init__()
        self.setWindowTitle("Chat - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat ou utilizar Arial como alternativa
        font_path = "path/to/your/font.ttf"  # Substitua pelo caminho correto da sua fonte
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Configurar layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo e título
        self._configurar_logo_e_titulo(montserrat_bold)

        # Contêiner 2: Caixa de mensagens
        self._configurar_caixa_de_mensagens()

        # Contêiner 3: Campo de entrada e botão de envio
        self._configurar_input_e_botao(montserrat_bold)

        # Inicializar conexão socket
        self.usuario_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.usuario_socket.connect((SERVER_HOST, SERVER_PORT))
        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao servidor: {e}")
            self.close()  # Fecha a janela se não for possível conectar

        # Iniciar thread para receber mensagens
        self.thread_recebida = threading.Thread(target=self.receber_mensagens, args=(self.usuario_socket,))
        self.thread_recebida.daemon = True
        self.thread_recebida.start()

        # Conectar botão de envio
        self.bt_enviar.clicked.connect(self.enviar_mensagem)

    def _configurar_logo_e_titulo(self, fonte_bold) -> None:
        """
        Summary:
            Configura o contêiner com o logo e o título.

        Args:
            fonte_bold (QFont): Fonte em negrito para o título.
            
        Returns:
            None
        """
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        # Adiciona o logo
        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # Adiciona o título
        self.title_label = QLabel("Chat")
        self.title_label.setFont(fonte_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

    def _configurar_caixa_de_mensagens(self) -> None:
        """
        Summary:
            Configura o contêiner para exibição das mensagens.
            
        Args:
            None
            
        Returns:
            None
        """
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(50, 20, 50, 0)
        self.messages_layout.setSpacing(10)

        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.messages_box.setStyleSheet(
            "background-color: #f5f5f5; padding: 15px; border-radius: 10px; border: 1px solid #ccc; height: 300px;"
        )
        self.messages_layout.addWidget(self.messages_box)

        self.layout.addWidget(self.messages_widget)

    def _configurar_input_e_botao(self, fonte_bold) -> None:
        """
        Summary:
            Configura o campo de entrada e o botão de envio.

        Args:
            fonte_bold (QFont): Fonte em negrito para o botão de envio.
            
        Returns:
            None
        """
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
        self.bt_enviar.setFont(fonte_bold)
        self.input_layout.addWidget(self.bt_enviar)

        self.layout.addWidget(self.input_widget)

    def receber_mensagens(self, usuario_socket) -> None:
        """
        Summary:
            Thread responsável por receber mensagens do servidor.

        Args:
            usuario_socket (socket): Socket de comunicação com o servidor.
            
        Returns:
            None
        """
        while True:
            try:
                mensagem = usuario_socket.recv(1024).decode("utf-8")
                if mensagem:
                    self.exibir_mensagem(mensagem, enviado=False)
            except Exception as e:
                print(f"[ERRO] Conexão com o servidor perdida: {e}")
                usuario_socket.close()
                break

    def exibir_mensagem(self, mensagem, enviado) -> None:
        """
        Summary:
            Exibe uma mensagem na caixa de mensagens.

        Args:
            mensagem (str): Mensagem a ser exibida.
            enviado (bool): Indica se a mensagem foi enviada pelo usuário.
            
        Returns:
            None
        """
        cor = "#003d79" if enviado else "black"
        self.messages_box.append(f'<p style="color: {cor};">{mensagem}</p>')

    def enviar_mensagem(self) -> None:
        """
        Summary:
            Envia a mensagem digitada pelo usuário ao servidor.
        
        Args:
            None
            
        Returns:
            None    
        """
        mensagem = self.message_input.text()
        if mensagem.lower() == "sair":
            print("[DESCONECTANDO] Encerrando a conexão.")
            self.usuario_socket.close()
            self.close()  # Fecha a janela
        elif mensagem:
            self.usuario_socket.send(mensagem.encode("utf-8"))
            self.exibir_mensagem(mensagem, enviado=True)
            self.message_input.clear()  # Limpa o campo de entrada

class TelaChat_Gerente(QMainWindow):
    """
    Summary:
        Classe responsável pela tela de chat para o gerente. Esta classe permite ao gerente enviar e receber mensagens em tempo real
        através de uma conexão socket com o servidor.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        _configurar_logo_e_titulo: Configura o contêiner com o logo e o título
        _configurar_caixa_de_mensagens: Configura o contêiner para exibição das mensagens
        _configurar_input_e_botao: Configura o campo de entrada e o botão de envio
        receber_mensagens: Thread responsável por receber mensagens do servidor
        exibir_mensagem: Exibe uma mensagem na caixa de mensagens
        enviar_mensagem: Envia a mensagem digitada pelo usuário ao servidor
    """

    def __init__(self):
        """
        Inicializa a interface de chat do gerente. Configura o layout principal, componentes visuais (logo, campo de mensagens, botão de envio)
        e a conexão socket com o servidor.
        """
        super().__init__()
        self.setWindowTitle("Chat - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Carregar a fonte Montserrat ou utilizar Arial como alternativa
        font_path = "path/to/your/font.ttf"  # Substitua pelo caminho correto da sua fonte
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 14, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 14, QFont.Bold)

        # Configurar layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Contêiner 1: Logo e título
        self._configurar_logo_e_titulo(montserrat_bold)

        # Contêiner 2: Caixa de mensagens
        self._configurar_caixa_de_mensagens()

        # Contêiner 3: Campo de entrada e botão de envio
        self._configurar_input_e_botao(montserrat_bold)

        # Inicializar conexão socket
        self.usuario_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.usuario_socket.connect((SERVER_HOST, SERVER_PORT))
        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao servidor: {e}")
            self.close()  # Fecha a janela se não for possível conectar

        # Iniciar thread para receber mensagens
        self.thread_recebida = threading.Thread(target=self.receber_mensagens, args=(self.usuario_socket,))
        self.thread_recebida.daemon = True
        self.thread_recebida.start()

        # Conectar botão de envio
        self.bt_enviar.clicked.connect(self.enviar_mensagem)

    def _configurar_logo_e_titulo(self, fonte_bold) -> None:
        """
        Summary:
            Configura o contêiner com o logo e o título.

        Args:
            fonte_bold (QFont): Fonte em negrito para o título.
            
        Returns:
            None
        """
        self.logo_widget = QWidget()
        self.logo_layout = QVBoxLayout(self.logo_widget)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(10)

        # Adiciona o logo
        self.logo_label = QLabel(self.logo_widget)
        logo_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(resized_pixmap)
        else:
            self.logo_label.setText("Imagem não encontrada.")
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # Adiciona o título
        self.title_label = QLabel("Chat")
        self.title_label.setFont(fonte_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

    def _configurar_caixa_de_mensagens(self) -> None:
        """
        Summary:
            Configura o contêiner para exibição das mensagens.
        
        Args:
            None
            
        Returns:
            None    
        """
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(50, 20, 50, 0)
        self.messages_layout.setSpacing(10)

        self.messages_box = QTextEdit()
        self.messages_box.setReadOnly(True)
        self.messages_box.setStyleSheet(
            "background-color: #f5f5f5; padding: 15px; border-radius: 10px; border: 1px solid #ccc; height: 300px;"
        )
        self.messages_layout.addWidget(self.messages_box)

        self.layout.addWidget(self.messages_widget)

    def _configurar_input_e_botao(self, fonte_bold) -> None:
        """
        Summary:
            Configura o campo de entrada e o botão de envio.

        Args:
            fonte_bold (QFont): Fonte em negrito para o botão de envio.
            
        Returns:
            None
        """
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
        self.bt_enviar.setFont(fonte_bold)
        self.input_layout.addWidget(self.bt_enviar)

        self.layout.addWidget(self.input_widget)

    def receber_mensagens(self, usuario_socket) -> None:
        """
        Summary:
            Thread responsável por receber mensagens do servidor.

        Args:
            usuario_socket (socket): Socket de comunicação com o servidor.
            
        Returns:
            None
        """
        while True:
            try:
                mensagem = usuario_socket.recv(1024).decode("utf-8")
                if mensagem:
                    self.exibir_mensagem(mensagem, enviado=False)
            except Exception as e:
                print(f"[ERRO] Conexão com o servidor perdida: {e}")
                usuario_socket.close()
                break

    def exibir_mensagem(self, mensagem, enviado) -> None:
        """
        Summary:
            Exibe uma mensagem na caixa de mensagens.

        Args:
            mensagem (str): Mensagem a ser exibida.
            enviado (bool): Indica se a mensagem foi enviada pelo usuário.
            
        Returns:
            None
        """
        cor = "#003d79" if enviado else "black"
        self.messages_box.append(f'<p style="color: {cor};">{mensagem}</p>')

    def enviar_mensagem(self) -> None:
        """
        Summary:
            Envia a mensagem digitada pelo usuário ao servidor.
            
        Args:
            None
            
        Returns:
            None
        """
        mensagem = self.message_input.text()
        if mensagem.lower() == "sair":
            print("[DESCONECTANDO] Encerrando a conexão.")
            self.usuario_socket.close()
            self.close()  # Fecha a janela
        elif mensagem:
            self.usuario_socket.send(mensagem.encode("utf-8"))
            self.exibir_mensagem(mensagem, enviado=True)
            self.message_input.clear()  # Limpa o campo de entrada

class TelaMarcarVoo_Gerente(QMainWindow):
    """ 
    Summary:
        Classe responsável pela interface de marcação de voos pelo gerente da companhia aérea Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        __init__: Inicializa a interface de marcação de voos e configura o layout principal, widgets e botões associados.
    """
    def __init__(self):
        """
        Inicializa a interface de marcação de voos.
        """
        super().__init__()

        self.setWindowTitle("Marcar Voo - Delta Airlines")
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

        # Contêiner: Logo e título
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

        self.title_label = QLabel("Marcar Voo")
        self.title_label.setFont(montserrat_bold)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.logo_layout.addWidget(self.title_label)

        self.layout.addWidget(self.logo_widget)

        # Contêiner: Campo de entrada
        self.sigla_input = QLineEdit(self)
        self.sigla_input.setPlaceholderText("Digite a sigla do voo")
        self.sigla_input.setStyleSheet(line_edit_style)
        self.layout.addWidget(self.sigla_input, alignment=Qt.AlignCenter)

        # Contêiner: Botões
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(10)  # Ajuste para aproximar os botões

        self.bt_marcar = QPushButton("Marcar Voo")
        self.bt_marcar.setFixedSize(200, 50)
        self.bt_marcar.setStyleSheet(button_style)
        self.bt_marcar.setFont(montserrat_bold)
        self.bt_marcar.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.bt_marcar, alignment=Qt.AlignCenter)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(200, 50)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.bt_voltar, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.buttons_widget)

class TelaVoos(QMainWindow):
    """
    Summary:
        Classe responsável pela interface de gerenciamento de voos da companhia aérea Delta Airlines.

    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        __init__: Inicializa a interface de gerenciamento de voos e configura o layout principal, widgets e botões associados.
        mostrar_tela_cadastrar_voo: Exibe a tela de cadastro de voos
        mostrar_tela_alterar_voo: Exibe a tela de alteração de voos
        mostrar_tela_remover_reserva_voo: Exibe a tela de remoção de reservas de voos
        mostrar_tela_listar_voo: Exibe a tela de listagem
    """

    def __init__(self):
        """
        Inicializa a interface de gerenciamento de voos. Define o layout principal, os widgets e as ações associadas aos botões.
        """
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

        # Logo da companhia aérea
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
        self.button_layout.setContentsMargins(400, 55, 0, 0)
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
    
    def mostrar_tela_cadastrar_voo(self) -> None:
        """
        Summary:
            Exibe a tela de cadastro de voos.

        Args:
            None
            
        Returns:
            None
        """
        if not hasattr(self, 'cadastro_voos'):
            self.cadastro_voos = CadastroVoos()
        self.tela_cadastrar_voo = TelaVoos_Cadastrar(self.cadastro_voos)
        self.tela_cadastrar_voo.show()

    def mostrar_tela_alterar_voo(self) -> None:
        """
        Summary:
            Exibe a tela de alteração de voos.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_alterar_voo = TelaVoos_Alterar()
        self.tela_alterar_voo.show()
    
    def mostrar_tela_remover_reserva_voo(self) -> None:
        """
        Summary:
            Exibe a tela de remoção de reservas de voos.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_remover_reserva_voo = TelaVoos_Remover()
        self.tela_remover_reserva_voo.show()
    
    def mostrar_tela_listar_voo(self) -> None:
        """
        Summary:
            Exibe a tela de listagem de voos.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_listar_voo = TelaVoos_Listar()
        self.tela_listar_voo.show()

class TelaAvioes(QMainWindow):
    """
    Summary:
        Classe responsável pela interface gráfica de gerenciamento de aviões. Contém botões para cadastrar, alterar, remover e listar aviões.
    
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        __init__: Inicializa a tela de gerenciamento de aviões, configurando o layout e os botões de interação.
        mostrar_tela_cadastar_aviao: Exibe a tela de cadastro de avião
        mostrar_tela_alterar_aviao: Exibe a tela de alteração de avião
        mostrar_tela_remover_aviao: Exibe a tela de remoção de avião
        mostrar_tela_listar_aviao: Exibe a tela de listagem de aviões
    """

    def __init__(self):
        """
        Inicializa a tela de gerenciamento de aviões, configurando o layout e os botões de interação.
        """
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
        self.button_layout.setContentsMargins(400, 60, 0, 0)
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

    def mostrar_tela_cadastar_aviao(self) -> None:
        """
        Summary:
            Exibe a tela de cadastro de avião.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_cadastrar_aviao = TelaAvioes_Cadastrar()
        self.tela_cadastrar_aviao.show()

    def mostrar_tela_alterar_aviao(self) -> None:
        """
        Summary:
            Exibe a tela de alteração de avião.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_alterar_aviao = TelaAvioes_Alterar()
        self.tela_alterar_aviao.show()

    def mostrar_tela_remover_aviao(self) -> None:
        """
        Summary:
            Exibe a tela de remoção de avião.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_remover_aviao = TelaAvioes_Remover()
        self.tela_remover_aviao.show()

    def mostrar_tela_listar_aviao(self) -> None:
        """
        Summary:
            Exibe a tela de listagem de aviões.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_listar_aviao = TelaAvioes_Listar()
        self.tela_listar_aviao.show()
    
class TelaVoos_Cadastrar(QMainWindow):
    """
    Tela para cadastro de voos na aplicação Delta Airlines.

    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        __init__: Inicializa a tela de cadastro de voos, configurando o layout e os botões de interação.
        cadastrar_voo: Realiza o cadastro de um novo voo, validando todos os campos.
    """

    def __init__(self, cadastro_voos):
        """
        Summary:
            Inicializa a tela de cadastro de voos.

        Args:
            cadastro_voos (CadastroVoos): Instância da classe CadastroVoos
        """
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

        self.nome_aviao_input = QLineEdit(self)
        self.nome_aviao_input.setPlaceholderText("Sigla do Avião")
        self.nome_aviao_input.setStyleSheet(line_edit_style)
        self.form_layout.addWidget(self.nome_aviao_input)

        self.sigla_input = QLineEdit(self)
        self.sigla_input.setPlaceholderText("Sigla do Voo")
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
        self.bt_cadastrar.clicked.connect(self.cadastrar_voo)
        self.buttons_layout.addWidget(self.bt_cadastrar, alignment=Qt.AlignCenter)

        self.bt_voltar = QPushButton("Voltar")
        self.bt_voltar.setFixedSize(button_width, button_height)
        self.bt_voltar.setStyleSheet(button_style)
        self.bt_voltar.setFont(montserrat_bold)
        self.bt_voltar.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.bt_voltar, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.buttons_widget)

    def cadastrar_voo(self) -> None:
        """
        Realiza o cadastro de um novo voo, validando todos os campos.

        Args:
            None
            
        Returns:
            None
            
        Raises:
            QMessageBox.warning: Exibe uma mensagem de erro caso algum campo não seja preenchido.
            QMessageBox.information: Exibe uma mensagem de sucesso após o cadastro do voo.
        """
        sigla_voo = self.sigla_input.text()
        origem = self.origem_input.text()
        destino = self.destino_input.text()
        modelo = self.modelo_input.text()
        nome_aviao = self.nome_aviao_input.text()

        # Validar se todos os campos estão preenchidos
        if not sigla_voo or not origem or not destino or not modelo or not nome_aviao:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        # Verificar se o avião existe no cadastro
        quantidade_assentos = self.cadastro_voos.buscar_assentos_por_aviao(nome_aviao)
        if quantidade_assentos is None:
            QMessageBox.warning(self, "Erro", f"Avião com sigla '{nome_aviao}' não encontrado.")
            return

        # Realizar o cadastro do voo
        sucesso, mensagem = self.cadastro_voos.cadastrar_voo(sigla_voo, origem, destino, modelo, quantidade_assentos)
        QMessageBox.information(self, "Resultado", mensagem)

class TelaAvioes_Cadastrar(QMainWindow):
    """
    Summary:
        Classe responsável pela tela de cadastro de avião.

    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas de aplicativos
        
    Methods:
        __init__: Inicializa a tela de cadastro de avião, configurando o layout, campos de entrada, botões de ação e lógica de exibição da tela.
        cadastrar_aviao: Método para cadastrar um avião com os dados fornecidos nos campos de entrada.
    """

    def __init__(self):
        """
        Inicializa a tela de cadastro de avião. Configura a interface gráfica, incluindo fontes, layout, campos de entrada, 
        botões de ação, e lógica de exibição da tela.
        """
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

    def cadastrar_aviao(self) -> None:
        """
        Summary:
            Método para cadastrar um avião com os dados fornecidos nos campos de entrada.
            
        Args:
            None
            
        Returns:
            None
        """
        sigla = self.sigla_input.text().strip()
        modelo = self.modelo_input.text().strip()
        assentos = self.assentos_input.text().strip()

        # Validações
        if not sigla or not modelo or not assentos.isdigit():
            print("Preencha todos os campos corretamente.")
            return

        # Chamando o método de cadastro da classe MetodosGerente
        sucesso = self.gerente.cadastrar_aviao(sigla, modelo, int(assentos))

        # Exibindo mensagem de sucesso ou erro
        if sucesso:
            QMessageBox.information(self, "Sucesso", "Avião cadastrado com sucesso!")
            print("Avião cadastrado com sucesso!")
            self.sigla_input.clear()
            self.modelo_input.clear()
            self.assentos_input.clear()
        else:
            print("Erro ao cadastrar o avião. Verifique os dados.")

class TelaVoos_Alterar(QMainWindow):
    """
    Summary:
        Classe responsável pela interface gráfica de alteração de voos.

    Args:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        buscar_voo_handler: Busca um voo no banco de dados a partir da sigla inform
        alterar_voo_handler: Altera as informações do voo no banco de dados.
        alterar_voo: Exibe a tela de alteração de voos.
    """
    def __init__(self, conn=None, parent=None):
        """
        Summary:
            Inicializa a tela de alteração de voos.
        
        Args:
            conn (psycopg2.connection, optional): Conexão com o banco de dados. Defaults to None.
            parent (QWidget, optional): Widget pai da janela. Defaults to None.
        """
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

    def buscar_voo_handler(self) -> None:
        """
        Summary: 
            Busca um voo no banco de dados a partir da sigla informada no campo de entrada.
        
        Args:
            None
            
        Returns:
            None
        """
        sigla = self.sigla_input.text().strip()
        if sigla:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("SELECT * FROM voos WHERE sigla = %s;", (sigla,))
                    voo = cur.fetchone()
                    if voo:
                        self.voo_info_label.setText(f"Informações do voo {sigla} encontradas.")
                        self.voo_info_label.setStyleSheet("color: green;")
                    else:
                        self.voo_info_label.setText(f"Informações do voo {sigla} não encontradas.")
                        self.voo_info_label.setStyleSheet("color: red;")
            except Exception as e:
                self.voo_info_label.setText(f"Erro ao buscar voo: {str(e)}")
        else:
            self.voo_info_label.setText("Por favor, insira a sigla do voo.")
        
    def alterar_voo_handler(self) -> None:
        """
        Summary:
            Altera as informações do voo no banco de dados.
        
        Args:
            None
            
        Returns:
            None
        """
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
        """ 
        Summary:
            Este método altera as informações de um voo no banco de dados.
            
        Args:
            sigla (str): Sigla do voo a ser alterado.
            origem (str): Origem do voo.
            destino (str): Destino do voo.
            modelo_aviao (str): Modelo do avião do voo.
            
        Returns:
            tuple (bool, str): Retorna uma tupla com um booleano indicando se a alteração foi bem sucedida e uma mensagem.
        
        Raises:
            Exception: Se ocorrer um erro ao alterar os dados do voo.
        """
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
    """
    Summary:
        Classe responsável pela interface gráfica de alteração de informações de um avião.
    
    Args:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        buscar_aviao: Busca um avião no sistema a partir da sigla informada.
        alterar_aviao: Altera as informações do avião no sistema.
    """
    def __init__(self):
        """
        Inicializa a tela de alteração de avião, configurando o layout e os campos de entrada para 
        busca e alteração das informações do avião.
        """
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

    def buscar_aviao(self) -> None:
        """
        Summary:
            Método que busca o avião com base na sigla fornecida pelo usuário.
        
        Args:
            None
            
        Returns:
            None
            
        Raises:
            QMessageBox.warning: Exibe uma mensagem de erro caso a sigla não seja fornecida.
            QMessageBox.warning: Exibe uma mensagem de erro caso o avião não seja encontrado.
        """
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

    def alterar_aviao(self) -> None:
        """
        Summary:
            Método que altera as informações do avião (modelo e quantidade de assentos) com base nos dados fornecidos.
        
        Args:
            None
            
        Returns:
            None
            
        Raises:
            QMessageBox.warning: Exibe uma mensagem de erro caso algum campo não seja preenchido.
            QMessageBox.information: Exibe uma mensagem de sucesso após a alteração do avião.
            QMessageBox.critical: Exibe uma mensagem de erro caso a alteração do avião falhe.
        """
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
    """
    Summary:
        Classe que representa a tela de remoção de voos na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        buscar_voo: Busca informações do voo pela sigla e exibe as informações.
        remover_reserva_voo: Remove um voo do banco de dados.
    """

    def __init__(self, conn = psycopg2.connect(dbname='credenciais', user='poodois', password='1234', host='localhost', port=5432)):
        """
        Summary:
            Inicializa a tela de remoção de voos, configurando o layout, campos de entrada, botões de ação e lógica de exibição da tela.
            
        Args:
            conn (psycopg2.connection, optional): Conexão com o banco de dados. Defaults to psycopg2.connect(dbname='credenciais', user='pood
            
        Returns:
            None
        """
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

    def buscar_voo(self) -> None:
        """
        Summary:
            Busca informações do voo pela sigla e exibe as informações.

        Args:
            None
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao buscar o voo.
        """
        sigla = self.sigla_input.text().strip()
        if sigla:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("SELECT * FROM voos WHERE sigla = %s;", (sigla,))
                    voo = cur.fetchone()
                    if voo:
                        voo_info = f"ID: {voo[0]}\nSigla: {voo[1]}\nOrigem: {voo[2]}\nDestino: {voo[3]}"
                        self.voo_info_label.setText(voo_info)
                    else:
                        self.voo_info_label.setText("Voo não encontrado.")
            except Exception as e:
                self.voo_info_label.setText(f"Erro ao buscar voo: {str(e)}")
        else:
            self.voo_info_label.setText("Por favor, insira a sigla do voo.")

    def remover_reserva_voo(self) -> None:
        """
        Summary:
            Remove o voo utilizando a sigla fornecida.

        Args:
            None
            
        Returns:
            None
        """
        sigla = self.sigla_input.text().strip()
        if sigla:
            sucesso, mensagem = self.excluir_voo(sigla)
            self.voo_info_label.setText(mensagem)
            if sucesso:
                self.sigla_input.clear()  # Limpa o campo de sigla após remoção
        else:
            self.voo_info_label.setText("Por favor, insira a sigla do voo.")

    def excluir_voo(self, sigla: str) -> tuple:
        """
        Summary:
            Exclui um voo pela sigla no banco de dados.

        Args:
            sigla (str): Sigla do voo a ser excluído.
            
        Returns:
            tuple (bool, str): Retorna uma tupla com um booleano indicando se a exclusão foi bem sucedida e uma mensagem.
            
        Raises:
            Exception: Se ocorrer um erro ao excluir o voo.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM voos WHERE sigla = %s;", (sigla,))
                self.conn.commit()
                if cur.rowcount > 0:
                    return True, "Voo excluído com sucesso."
                return False, "Voo não encontrado."
        except Exception as e:
            return False, f"Erro ao excluir voo: {str(e)}"

class TelaAvioes_Remover(QMainWindow):
    """
    Summary:
        Classe que representa a tela de remoção de aviões na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        buscar_aviao: Busca informações do avião pela sigla e exibe as informações.
        remover_aviao: Remove um avião do banco de dados.
    """

    def __init__(self):
        """
        Inicializa a tela de remoção de avião, configurando o layout, fontes, campos de entrada
        e botões necessários para buscar e remover um avião.
        """
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
        self.buscar_button.setFont(montserrat_bold)
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

    def buscar_aviao(self) -> None:
        """
        Summary:
            Busca informações do avião pela sigla e exibe as informações.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            QMessageBox.warning: Exibe uma mensagem de erro caso a sigla não seja fornecida.
            QMessageBox.warning: Exibe uma mensagem de erro caso o avião não seja encontrado.
        """
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

    def remover_aviao(self) -> None:
        """
        Summary:
            Remove um avião do banco de dados.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            QMessageBox.warning: Exibe uma mensagem de erro caso a sigla não seja fornecida.
            QMessageBox.question: Exibe uma mensagem de confirmação para a remoção do avião.
            QMessageBox.information: Exibe uma mensagem de sucesso após a remoção do avião.
            QMessageBox.critical: Exibe uma mensagem de erro caso a remoção do avião falhe.
        """
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
    """
    Summary:
        Classe que representa a tela de listagem de voos na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        carregar_lista_voos: Carrega a lista de voos cadastrados e exibe na interface.
    """
    def __init__(self):
        """Inicializa a tela para listar os voos cadastrados na Delta Airlines."""
        super().__init__()

        # Configurações da janela
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

        # Tabela de voos
        self.tabela_voos = QTableWidget()
        self.tabela_voos.setColumnCount(5)  # Cinco colunas: ID, Sigla, Origem, Destino, Modelo
        self.tabela_voos.setHorizontalHeaderLabels(["ID", "Sigla", "Origem", "Destino", "Modelo"])
        self.tabela_voos.setSelectionMode(QAbstractItemView.NoSelection)  # Desativa seleção de células
        self.tabela_voos.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Impede edição das células
        self.tabela_voos.setStyleSheet("""
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

        # Scroll para a tabela
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.tabela_voos)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

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

        # Carregar dados dos voos
        self.carregar_lista_voos()

    def carregar_lista_voos(self) -> None:
        """
        Summary:
            Carrega a lista de voos cadastrados e exibe na interface.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao carregar os voos.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, sigla, origem, destino, modelo_aviao FROM voos;")
                voos = cur.fetchall()

            if voos:
                self.tabela_voos.setRowCount(len(voos))
                for i, voo in enumerate(voos):
                    self.tabela_voos.setItem(i, 0, QTableWidgetItem(str(voo[0])))  # ID
                    self.tabela_voos.setItem(i, 1, QTableWidgetItem(voo[1]))  # Sigla
                    self.tabela_voos.setItem(i, 2, QTableWidgetItem(voo[2]))  # Origem
                    self.tabela_voos.setItem(i, 3, QTableWidgetItem(voo[3]))  # Destino
                    self.tabela_voos.setItem(i, 4, QTableWidgetItem(voo[4]))  # Modelo
            else:
                self.tabela_voos.setRowCount(1)
                self.tabela_voos.setItem(0, 0, QTableWidgetItem("Nenhum voo cadastrado"))
                for col in range(1, 5):
                    self.tabela_voos.setItem(0, col, QTableWidgetItem(""))
        except Exception as e:
            self.tabela_voos.setRowCount(1)
            self.tabela_voos.setItem(0, 0, QTableWidgetItem(f"Erro ao carregar voos: {str(e)}"))
            for col in range(1, 5):
                self.tabela_voos.setItem(0, col, QTableWidgetItem(""))

class TelaAvioes_Listar(QMainWindow):
    """
    Summary:
        Classe que representa a tela de listagem de aviões na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        carregar_lista_avioes: Carrega a lista de aviões cadastrados e exibe na interface.
    """
    def __init__(self):
        """Inicializa a tela para listar os aviões cadastrados na Delta Airlines."""
        super().__init__()

        # Configurações da janela
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

        # Tabela de aviões
        self.tabela_avioes = QTableWidget()
        self.tabela_avioes.setColumnCount(4)  # Quatro colunas: ID, Sigla, Modelo, Assentos
        self.tabela_avioes.setHorizontalHeaderLabels(["ID", "Sigla", "Modelo", "Assentos"])
        self.tabela_avioes.setSelectionMode(QAbstractItemView.NoSelection)  # Desativa seleção de células
        self.tabela_avioes.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Impede edição das células
        self.tabela_avioes.setStyleSheet("""
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

        # Scroll para a tabela
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.tabela_avioes)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

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

    def carregar_lista_avioes(self) -> None:
        """
        Summary:
            Carrega a lista de aviões cadastrados e exibe na interface.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao carregar os aviões.
        """
        try:
            metodos_gerente = MetodosGerente()
            avioes = metodos_gerente.listar_avioes()
            if avioes:
                self.tabela_avioes.setRowCount(len(avioes))
                for i, aviao in enumerate(avioes):
                    self.tabela_avioes.setItem(i, 0, QTableWidgetItem(str(aviao[0])))  # ID
                    self.tabela_avioes.setItem(i, 1, QTableWidgetItem(aviao[1]))  # Sigla
                    self.tabela_avioes.setItem(i, 2, QTableWidgetItem(aviao[2]))  # Modelo
                    self.tabela_avioes.setItem(i, 3, QTableWidgetItem(str(aviao[3])))  # Assentos
            else:
                self.tabela_avioes.setRowCount(1)
                self.tabela_avioes.setItem(0, 0, QTableWidgetItem("Nenhum avião cadastrado"))
                for col in range(1, 4):
                    self.tabela_avioes.setItem(0, col, QTableWidgetItem(""))
        except Exception as e:
            self.tabela_avioes.setRowCount(1)
            self.tabela_avioes.setItem(0, 0, QTableWidgetItem(f"Erro ao carregar aviões: {str(e)}"))
            for col in range(1, 4):
                self.tabela_avioes.setItem(0, col, QTableWidgetItem(""))

class TelaAtendente(QMainWindow):
    """ 
    Summary:
        Classe que representa a tela principal do atendente na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        mostrar_tela_passageiros: Exibe a tela de gerenciamento de passageiros.
        mostrar_tela_reservas: Exibe a tela de gerenciamento de reservas.
        mostrar_tela_inicial: Exibe a tela inicial do sistema.
        mostrar_tela_chat_atendente: Exibe a tela de chat do atendente.
    """

    def __init__(self):
        """Inicializa a tela principal do atendente e configura o layout e os botões de navegação."""
        super().__init__()
        self.setWindowTitle("Atendimento - Delta Airlines")
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
        button_layout.setContentsMargins(400, 90, 0, 0)
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

    def mostrar_tela_passageiros(self) -> None:
        """ 
        Summary:
            Exibe a tela de gerenciamento de passageiros.
        
        Args:
            None
            
        Returns:
            None    
        """
        self.tela_passageiros = TelaPassageiros()
        self.tela_passageiros.show()
    
    def mostrar_tela_reservas(self) -> None:
        """
        Summary:
            Exibe a tela de gerenciamento de reservas.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_reservas = TelaReservas()
        self.tela_reservas.show()
    
    def mostrar_tela_inicial(self) -> None:
        """
        Summary:
            Exibe a tela inicial do sistema.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_inicial = Tela()
        self.tela_inicial.show()
    
    def mostrar_tela_chat_atendente(self) -> None:
        """
        Summary:
            Exibe a tela de chat do atendente.
        
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_chat_atendente = TelaChat_Atendente()
        self.tela_chat_atendente.show()

class TelaChat_Atendente(QMainWindow):
    """ 
    Summary:
        Classe que representa a tela de chat do atendente na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        receber_mensagens: Recebe e exibe mensagens enviadas ao atendente através do socket.
        exibir_mensagem: Exibe uma mensagem na caixa de mensagens com a cor apropriada.
        enviar_mensagem: Envia a mensagem digitada pelo atendente para o servidor.  
    """

    def __init__(self):
        """Inicializa a tela de chat do atendente, configurando os componentes da interface gráfica."""
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

    def receber_mensagens(self, usuario_socket) -> None:
        """ 
        Summary:
            Recebe e exibe mensagens enviadas ao atendente através do socket.
            
        Args:
            usuario_socket (socket): Socket do usuário para receber mensagens.
            
        Returns:
            None
        """
        while True:
            try:
                mensagem = usuario_socket.recv(1024).decode("utf-8")
                if mensagem:
                    self.exibir_mensagem(mensagem, enviado=False)
            except:
                print("[ERRO] Conexão com o servidor perdida.")
                usuario_socket.close()
                break

    def exibir_mensagem(self, mensagem, enviado) -> None:
        """ 
        Summary:
            Exibe uma mensagem na caixa de mensagens com a cor apropriada.
            
        Args:
            mensagem (str): Mensagem a ser exibida.
            enviado (bool): Indica se a mensagem foi enviada pelo atendente.
            
        Returns:
            None
        """
        cor = "#003d79" if enviado else "black"
        self.messages_box.append(f'<p style="color: {cor};">{mensagem}</p>')

    def enviar_mensagem(self) -> None:
        """ 
        Summary:
            Envia a mensagem digitada pelo atendente para o servidor.
            
        Args:
            None
            
        Returns:
            None
        """
        mensagem = self.message_input.text()
        if mensagem.lower() == "sair":
            print("[DESCONECTANDO] Encerrando a conexão.")
            self.usuario_socket.close()
            self.close()  # Fecha a janela
        elif mensagem:
            self.usuario_socket.send(mensagem.encode("utf-8"))
            self.exibir_mensagem(mensagem, enviado=True)
            self.message_input.clear()  # Limpa o campo de entrada

class TelaPassageiros(QMainWindow):
    """
    Summary:
        Classe que representa a tela de gerenciamento de passageiros na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        mostrar_tela_cadastrar_passageiro: Exibe a tela de cadastro de passageiros.
        mostrar_tela_alterar_passageiro: Exibe a tela de alteração de dados de passageiros.
        mostrar_tela_remover_passageiro: Exibe a tela de remoção de passageiros.
        mostrar_tela_listar_passageiro: Exibe a tela de listagem de passageiros.
    """
    def __init__(self):
        """
        Inicializa a tela de gerenciamento de passageiros, configurando o layout
        e adicionando os botões de ação.
        """
        super().__init__()
        self.setWindowTitle("Atendimento de clientes - Delta Airlines")
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
        self.button_layout.setContentsMargins(400, 70, 0, 0)
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

    def mostrar_tela_cadastrar_passageiro(self) -> None:
        """
        Summary:
            Exibe a tela de cadastro de passageiros.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_cadastrar_passageiro = TelaPassageiros_Cadastrar()
        self.tela_cadastrar_passageiro.show()
        self.close()

    def mostrar_tela_alterar_passageiro(self) -> None:
        """
        Summary:
            Exibe a tela de alteração de dados de passageiros.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_alterar_passageiro = TelaPassageiros_Alterar()
        self.tela_alterar_passageiro.show()
        self.close()

    def mostrar_tela_remover_passageiro(self) -> None:
        """
        Summary:
            Exibe a tela de remoção de passageiros.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_remover_passageiro = TelaPassageiros_Remover()
        self.tela_remover_passageiro.show()
        self.close()

    def mostrar_tela_listar_passageiro(self) -> None:
        """
        Summary:
            Exibe a tela de listagem de passageiros.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_listar_passageiro = TelaPassageiros_Listar()
        self.tela_listar_passageiro.show()
        self.close()

class TelaReservas(QMainWindow):
    """
    Summary:
        Classe que representa a tela de gerenciamento de reservas na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        mostrar_tela_reservas_reservar: Exibe a tela para realizar uma nova reserva.
        mostrar_tela_reservas_remover: Exibe a tela para remover uma reserva existente
    """
    def __init__(self):
        """
        Inicializa a tela de gerenciamento de reservas, configurando o layout
        e adicionando os botões de ação.
        """
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
        self.button_layout.setContentsMargins(400, 120, 0, 0)
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

    def mostrar_tela_reservas_reservar(self) -> None:
        """
        Summary:
            Exibe a tela para realizar uma nova reserva.
            
        Args:
            None
            
        Returns:
            None
        """
        self.tela_reservas_reservar = TelaReservas_Reservar()
        self.tela_reservas_reservar.show()
        self.close()

    def mostrar_tela_reservas_remover(self) -> None:
        """
        Summary:
            Exibe a tela para remover uma reserva existente.
            
        Args:
            None
            
        Returns:
            None  
        """
        self.tela_reservas_remover = TelaReservas_Remover()
        self.tela_reservas_remover.show()
        self.close()

class TelaPassageiros_Cadastrar(QMainWindow):
    """
    Summary:
        Classe que representa a tela de cadastro de passageiros na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        cadastrar_passageiro: Cadastra um novo passageiro no sistema.
        show_message: Exibe uma mensagem em uma janela modal
    """
    def __init__(self):
        """
        Inicializa a interface da tela de cadastro de cliente.
        Configura o layout, carrega fontes, logo e campos para o cadastro.
        """
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

    def cadastrar_cliente(self) -> None:
        """
        Summary:
            Cadastra um novo passageiro no sistema. Coleta os dados dos campos de entrada
            
        Args:
            None
            
        Returns:
            None  
            
        Raises:
            Exception: Se ocorrer um erro ao cadastrar o passageiro.
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

    def show_message(self, titulo, mensagem) -> None:
        """
        Summary:
            Exibe uma mensagem em uma janela modal.
            
        Args:
            titulo (str): Título da mensagem.
            mensagem (str): Conteúdo da mensagem.
            
        Returns:
            None
        """
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

class TelaPassageiros_Alterar(QMainWindow):
    """
    Summary:
        Classe que representa a tela de alteração de dados de um passageiro na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        buscar_passageiro: Busca as informações de um passageiro a partir do CPF.
        alterar_passageiro: Altera as informações de um passageiro no banco de dados.
    """
    def __init__(self):
        """
        Inicializa a interface de alteração de dados do passageiro.
        Configura o layout, os campos de entrada e os botões de ação.
        """
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

    def buscar_passageiro(self) -> None:
        """
        Summary:
            Busca as informações de um passageiro a partir do CPF.
            
        Args:
            None
            
        Returns:
            None
        """
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

    def alterar_passageiro(self) -> None:
        """
        Summary:
            Altera as informações de um passageiro no banco de dados.
            
        Args:
            None
            
        Returns:
            None  
            
        Raises:
            Exception: Se ocorrer um erro ao alterar os dados do passageiro.
        """
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
    """
    Summary:
        Classe que representa a tela de remoção de um passageiro na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        buscar_passageiro: Busca as informações de um passageiro a partir do CPF.
        remover_passageiro: Remove um passageiro do banco de dados.
    """
    def __init__(self):
        """
        Inicializa a interface de remoção de um passageiro.
        Configura o layout, os campos de entrada e os botões de ação.
        """
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
    
    def buscar_passageiro(self) -> None:
        """
        Summary:
            Busca as informações de um passageiro a partir do CPF.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao buscar o passageiro.
        """
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

    def remover_passageiro(self) -> None:
        """
        Summary:
            Remove um passageiro do banco de dados.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao remover o passageiro.
        """
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
    """
    Summary:
        Classe que representa a tela de listagem de passageiros na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        atualizar_tabela: Atualiza os dados na tabela de clientes.
    """
    def __init__(self, db_config=None):
        """
        Summary:
            Inicializa a interface da tela de listagem de clientes. Configura o layout, carrega fontes, logo e a tabela de clientes.
        
        Args:
            db_config (dict): Configurações para conexão com o banco de dados.
        """
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

    def atualizar_tabela(self) -> None:
        """
        Summary:
            Atualiza os dados na tabela de clientes.
            
        Args:
            None
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao atualizar a tabela.
        """
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
    """
    Summary:
        Classe responsável pela tela de reserva de voos. Permite que o usuário selecione um voo e faça a reserva.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        atualizar_lista_voos: Atualiza a lista de voos disponíveis exibida na tela.
        reservar_voo: Realiza a reserva de um voo com base na sigla fornecida pelo
    """
    def __init__(self):
        """
        Construtor da classe TelaReservas_Reservar. Inicializa a interface e os elementos da tela.
        """
        super().__init__()
        self.setWindowTitle("Reservar Voo - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Backend connection
        self.backend = BackendReservas()

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
        """
        Atualiza a lista de voos disponíveis exibida na tela.
        """
        voos = self.backend.listar_voos()
        if voos:
            texto_voos = "\n".join(
                [f"Sigla: {voo[0]}, Origem: {voo[1]}, Destino: {voo[2]}, Modelo: {voo[3]}, Assentos disponíveis: {voo[4]}" for voo in voos]
            )
        else:
            texto_voos = "Nenhum voo disponível."
        self.voos_lista_label.setText(texto_voos)

    def reservar_voo(self):
        """
        Realiza a reserva de um voo com base na sigla fornecida pelo usuário.
        """
        sigla = self.sigla_input.text().strip()

        if not sigla:
            self.voos_lista_label.setText("Por favor, insira uma sigla válida.")
            return

        mensagem = self.backend.reservar_voo(sigla, 1)
        self.voos_lista_label.setText(mensagem)
        self.atualizar_lista_voos()

    def closeEvent(self, event):
        """
        Fecha a conexão com o backend quando a janela é fechada.
        """
        self.backend.close_connection()
        super().closeEvent(event)

class TelaReservas_Remover(QMainWindow):
    """
    Summary:
        Classe que representa a tela de remoção de reservas na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        atualizar_lista_reservas: Atualiza a lista de reservas disponíveis na tela.
        remover_reserva_voo: Remove a reserva de um voo selecionado
    """

    def __init__(self):
        """
        Inicializa a interface gráfica da tela de remoção de reservas.
        Estabelece a conexão com o backend e configura o layout da tela.
        """
        super().__init__()
        self.setWindowTitle("Remover Reserva - Delta Airlines")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        # Conectar com o backend para remoção de reservas
        self.backend = BackendRemoverReservas()

        # Carregar a fonte Montserrat ou fallback para Arial
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

        # Contêiner: Botões "Remover Reserva do Voo" e "Voltar"
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

    def atualizar_lista_voos(self) -> None:
        """
        Summary:
            Atualiza a lista de voos disponíveis exibida na tela. Consulta o backend para obter a lista de voos.
            
        Args:
            None
            
        Returns:
            None
        """
        voos = self.backend.listar_voos()
        if voos:
            texto_voos = "\n".join(
                [f"Sigla: {voo[0]}, Origem: {voo[1]}, Destino: {voo[2]}, Modelo: {voo[3]}, Assentos disponíveis: {voo[4]}" for voo in voos]
            )
        else:
            texto_voos = "Nenhum voo disponível."
        self.voos_lista_label.setText(texto_voos)

    def remover_reserva_voo(self) -> None:
        """
        Summary:
            Remove a reserva de um voo selecionado. Consulta o backend para realizar a remoção da reserva.
            
        Args:
            None
            
        Returns:
            None
        """
        sigla = self.sigla_input.text().strip()

        if not sigla:
            self.voos_lista_label.setText("Por favor, insira uma sigla válida.")
            return

        mensagem = self.backend.remover_reserva_voo(sigla, 1)
        self.voos_lista_label.setText(mensagem)
        self.atualizar_lista_voos()

    def closeEvent(self, event) -> None:
        """
        Summary:
            Fecha a conexão com o backend quando a janela é fechada.
            
        Args:
            event (QCloseEvent): Evento de fechamento da janela.
            
        Returns:
            None
        """
        self.backend.close_connection()
        super().closeEvent(event)

class GerenciadorDeReservas:
    """
    Summary:
        Classe que gerencia as reservas de voos na aplicação Delta Airlines.
        
    Attributes:
        QMainWindow (QMainWindow): Classe base para janelas da aplicação.
        
    Methods:
        __init__: Inicializa a interface gráfica do gerenciador de reservas.
        abrir_tela_reservar: Abre a tela de reserva de voos.
        abrir_tela_remover: Abre a tela de remoção de reservas.
    """

    def __init__(self, dbname, user, password, host='localhost', port=5432):
        """
        Summary:
            Inicializa a conexão com o banco de dados.

        Args:
            dbname (str): Nome do banco de dados.
            user (str): Nome de usuário para autenticação.
            password (str): Senha do usuário.
            host (str): Endereço do servidor do banco de dados (padrão 'localhost').
            port (int): Porta de conexão ao banco de dados (padrão 5432).
        """
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

    def listar_voos(self) -> list:
        """
        Summary:
            Lista os voos disponíveis no banco de dados.
            
        Args:
            None
            
        Returns:
            list: Lista de voos disponíveis.
            
        Raises:
            Exception: Se ocorrer um erro ao listar os voos.
        """
        try:
            self.cursor.execute("SELECT * FROM voos;")
            voos = self.cursor.fetchall()
            return voos
        except Exception as e:
            print("Erro ao listar voos:", e)
            return []

    def adicionar_voo(self, sigla, origem, destino, modelo_aviao) -> None:
        """
        Summary:
            Adiciona um novo voo ao banco de dados.
            
        Args:
            sigla (str): Sigla do voo.
            origem (str): Aeroporto de origem.
            destino (str): Aeroporto de destino.
            modelo_aviao (str): Modelo do avião.
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao adicionar o voo.
        """
        try:
            self.cursor.execute(
                "INSERT INTO voos (sigla, origem, destino, modelo_aviao) VALUES (%s, %s, %s, %s);",
                (sigla, origem, destino, modelo_aviao)
            )
            self.conn.commit()
            print("Voo adicionado com sucesso.")
        except Exception as e:
            print("Erro ao adicionar voo:", e)

    def remover_reserva_voo(self, id_voo) -> None:
        """
        Summary:
            Remove a reserva de um voo no banco de dados.
            
        Args:
            id_voo (int): ID do voo a ser removido.
            
        Returns:
            None
            
        Raises:
            Exception: Se ocorrer um erro ao remover a reserva do voo.
        """
        try:
            self.cursor.execute("DELETE FROM voos WHERE id = %s;", (id_voo,))
            self.conn.commit()
            print("Voo removido com sucesso.")
        except Exception as e:
            print("Erro ao remover voo:", e)

    def fechar_conexao(self) -> None:
        """
        Summary:
            Fecha a conexão com o banco de dados.
            
        Args:
            None
            
        Returns:
            None
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("Erro ao fechar a conexão:", e)

# Código para rodar a aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())


