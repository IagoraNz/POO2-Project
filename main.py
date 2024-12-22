import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QInputDialog

class Tela(QWidget):
    def __init__(self):
        self.setWindowTitle('Sistema Gerenciador do Porto de Santos')
        self.setGeometry(100, 100, 300, 300)
        
        # Inicializar aqui as classes necessárias
        
        # Layout
        layout = QVBoxLayout()
        
        # Adicionar os botões aqui
        
        # Definindo o layout
        self.setLayout(layout)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = Tela()
    tela.show()
    sys.exit(app.exec_())