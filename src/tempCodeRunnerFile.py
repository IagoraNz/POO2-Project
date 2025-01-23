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

        if not sigla or not origem or not destino or not modelo:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        sucesso, mensagem = self.cadastro_voos.cadastrar_voo(sigla, origem, destino, modelo)
        QMessageBox.information(self, "Resultado", mensagem)