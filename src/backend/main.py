import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
# from back import *

class Tela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema Gerenciador da Companhia Aérea')
        layout = QVBoxLayout()
        
        # bt_cadastrar = QPushButton("Cadastro")
        # bt_cadastrar.setFixedSize(200, 50)
        # layout.addWidget(bt_cadastrar)
        
        # bt_login = QPushButton("Login")
        # bt_login.setFixedSize(200, 50)
        # layout.addWidget(bt_login)
        
        # Adicionar os botões aqui
        
        # Definindo o layout
        self.setLayout(layout)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())