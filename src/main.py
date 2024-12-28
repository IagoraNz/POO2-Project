import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from backend.back import Autenticacao
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSizePolicy, QSpacerItem

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
        self.setWindowTitle("Sistema Gerenciador da Companhia Aérea")
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
            self.tipo_input.setPlaceholderText("Tipo de funcionário (1 - Gerente, 2 - Atendente)")
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
        self.left_layout.setContentsMargins(20, 35, 0, 0)  # Mantém as margens originais
        self.left_layout.setSpacing(0)  # Sem espaçamento entre widgets
        
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
        
        # Criar um widget auxiliar para centralizar os botões
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Sem margens internas no widget
        button_layout.setSpacing(15)  # Espaçamento entre botões
        button_layout.setAlignment(Qt.AlignCenter)  # Centraliza os botões verticalmente
        
        # Botões
        self.bt_voos = QPushButton("Voos")
        self.bt_voos.setFixedSize(200, 50)
        self.bt_voos.setStyleSheet(button_style)
        self.bt_voos.setFont(montserrat_bold)
        self.bt_voos.clicked.connect(self.mostrar_voos)
        
        self.bt_avioes = QPushButton("Aviões")
        self.bt_avioes.setFixedSize(200, 50)
        self.bt_avioes.setStyleSheet(button_style)
        self.bt_avioes.setFont(montserrat_bold)
        self.bt_avioes.clicked.connect(self.mostrar_avioes)
        
        # Adicionar os botões ao layout do widget de botões
        button_layout.addWidget(self.bt_voos)
        button_layout.addWidget(self.bt_avioes)
        
        # Adicionar espaçador abaixo dos botões para empurrá-los para cima
        spacer = QSpacerItem(20, 230, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addSpacerItem(spacer)
        
        # Adicionar o widget de botões ao layout esquerdo
        self.left_layout.addWidget(button_widget, alignment=Qt.AlignTop)  # Centraliza horizontalmente
        
        # Adicionar o layout esquerdo ao layout principal
        self.layout.addLayout(self.left_layout)
        
        # Tela interna (direita)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Placeholder inicial
        self.placeholder_widget = QWidget()
        self.stacked_widget.addWidget(self.placeholder_widget)
        
    def mostrar_voos(self):
        self.voos_widget = QWidget()
        voos_layout = QVBoxLayout(self.voos_widget)
        
        # Adicionar conteúdo específico para Voos
        voos_label = QLabel("Gerenciamento de Voos")
        voos_label.setFont(QFont("Montserrat", 12, QFont.Bold))
        voos_label.setAlignment(Qt.AlignCenter)
        voos_layout.addWidget(voos_label)
        self.stacked_widget.addWidget(self.voos_widget)
        self.stacked_widget.setCurrentWidget(self.voos_widget)
        
    def mostrar_avioes(self):
        self.avioes_widget = QWidget()
        avioes_layout = QVBoxLayout(self.avioes_widget)
        
        # Adicionar conteúdo específico para Aviões
        avioes_label = QLabel("Gerenciamento de Aviões")
        avioes_label.setFont(QFont("Montserrat", 12, QFont.Bold))
        avioes_label.setAlignment(Qt.AlignCenter)
        avioes_layout.addWidget(avioes_label)
        
        self.stacked_widget.addWidget(self.avioes_widget)
        self.stacked_widget.setCurrentWidget(self.avioes_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())