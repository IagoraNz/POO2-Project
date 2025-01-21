    def confirmar_voo(self):
        sigla = self.sigla_input.text().strip()
        if not sigla:
            QMessageBox.warning(self, "Erro", "Digite a sigla do voo.")
            return

        backend = BackendReservas()
        voo = backend.verificar_voo(sigla)
        if voo:
            assentos_livres = backend.contar_assentos_livres(sigla)
            QMessageBox.information(
                self,
                "Sucesso",
                f"Voo encontrado: {voo[1]} - {voo[2]} -> {voo[3]} ({voo[4]})\nAssentos livres: {assentos_livres}"
            )
        else:
            QMessageBox.warning(self, "Erro", "Voo não encontrado.")
        backend.fechar_conexao()