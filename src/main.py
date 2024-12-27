import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from backend.back import Autenticacao

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

            self.confirma_senha_input = QLineEdit(self)
            self.confirma_senha_input.setPlaceholderText("Confirmar Senha")
            self.confirma_senha_input.setEchoMode(QLineEdit.Password)
            self.confirma_senha_input.setStyleSheet(line_edit_style)
            self.layout.addWidget(self.confirma_senha_input, alignment=Qt.AlignHCenter)

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
        confirma_senha = self.confirma_senha_input.text()

        if senha != confirma_senha:
            print("As senhas não coincidem!")
            return
        
        if len(senha) < 8:
            print("A senha deve ter no mínimo 8 dígitos")
            return

        if self.auth.cadastro(usuario, senha):
            print(f"Usuário {usuario} cadastrado com sucesso!")
            self.voltar_tela_inicial()
        else:
            print(f"Erro: Usuário {usuario} já existe.")

    def voltar_tela_inicial(self):
        # Limpar os campos de cadastro
        self.usuario_input.setText("")
        self.senha_input.setText("")
        self.confirma_senha_input.setText("")

        # Remover os campos de cadastro
        self.layout.itemAt(5).widget().setVisible(False)
        self.layout.itemAt(6).widget().setVisible(False)
        self.layout.itemAt(7).widget().setVisible(False)
        self.layout.itemAt(8).widget().setVisible(False)

        # Recriar a tela inicial
        self.welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        self.layout.itemAt(3).widget().setVisible(True)
        self.layout.itemAt(4).widget().setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())