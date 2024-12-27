import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt

class Tela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Gerenciador da Companhia Aérea")
        self.setFixedSize(1000, 500)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        # Carregar a fonte personalizada
        font_path = os.path.abspath("./src/fonts/Montserrat-SemiBold.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)
            montserrat_bold = QFont("Montserrat", 10, QFont.Bold)
        else:
            montserrat_bold = QFont("Arial", 10, QFont.Bold)

        self.setStyleSheet("background-color: white;")

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(50, -100, 10, 175)
        layout.setSpacing(10)

        top_layout = QHBoxLayout()

        # Criar um QLabel para exibir a imagem superior
        self.label = QLabel(self)
        image_path = os.path.abspath("./src/images/image.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            resized_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(resized_pixmap)
        else:
            self.label.setText("Imagem não encontrada.")
        
        top_layout.addWidget(self.label, alignment=Qt.AlignLeft)

        layout.addLayout(top_layout)

        # Criar um QLabel para exibir o texto de boas-vindas
        welcome_label = QLabel(self)
        welcome_label.setText("<b>Bem-vindo ao sistema gerenciador da Delta Airlines</b>")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px;")
        welcome_label.setFont(montserrat_bold)
        layout.addWidget(welcome_label)

        # Diminuir a distância entre os widgets
        layout.addSpacing(-25)

        # Estilo para os botões
        button_style = """
            QPushButton {
                background-color: lightgray;
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

        # Botões
        bt_login = QPushButton("Login")
        bt_login.setFixedSize(200, 50)
        bt_login.setStyleSheet(button_style)
        bt_login.setFont(montserrat_bold)
        layout.addWidget(bt_login, alignment=Qt.AlignHCenter)

        bt_cadastrar = QPushButton("Cadastro")
        bt_cadastrar.setFixedSize(200, 50)
        bt_cadastrar.setStyleSheet(button_style)
        bt_cadastrar.setFont(montserrat_bold)
        layout.addWidget(bt_cadastrar, alignment=Qt.AlignHCenter)

        # Configurar layout principal
        self.setLayout(layout)

        # Criar um QLabel para sobrepor a imagem no canto inferior direito
        self.bottom_image_label = QLabel(self)
        bottom_image_path = os.path.abspath("./src/images/aviao.png")
        if os.path.exists(bottom_image_path):
            pixmap = QPixmap(bottom_image_path)
            resized_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ajuste para 300x300
            self.bottom_image_label.setPixmap(resized_pixmap)
        else:
            self.bottom_image_label.setText("Imagem não encontrada.")

    def resizeEvent(self, event):
        self.bottom_image_label.setGeometry(
            self.width() - 300,  # X (direita)
            self.height() - 235,  # Y (baixo)
            300, 300 
        )
        super().resizeEvent(event)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())