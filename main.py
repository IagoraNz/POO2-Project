import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

class Tela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema Gerenciador do Porto de Santos')
        
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