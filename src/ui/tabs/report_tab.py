"""Aba para gerar relatórios e documentos"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFormLayout, QMessageBox, QFileDialog,
    QProgressBar
)
from PySide6.QtCore import Qt
from src.database.storage import DataStorage
from src.documents.report_generator import ReportGenerator
from pathlib import Path


class ReportTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self.generator = ReportGenerator(storage)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Company info section
        company_layout = QFormLayout()
        self.company_name = QLineEdit()
        self.company_cnpj = QLineEdit()
        self.company_address = QLineEdit()
        self.responsible_name = QLineEdit()

        company_layout.addRow("Razão Social:", self.company_name)
        company_layout.addRow("CNPJ:", self.company_cnpj)
        company_layout.addRow("Endereço:", self.company_address)
        company_layout.addRow("Responsável:", self.responsible_name)

        layout.addLayout(company_layout)

        # Report options
        options_layout = QFormLayout()
        self.scope_text = QTextEdit()
        self.scope_text.setPlaceholderText("Descreva o escopo da avaliação...")
        options_layout.addRow("Escopo da Avaliação:", self.scope_text)

        layout.addLayout(options_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        pgr_btn = QPushButton("Gerar PGR (DOCX)")
        pdf_btn = QPushButton("Gerar Relatório (PDF)")

        pgr_btn.clicked.connect(self._generate_pgr)
        pdf_btn.clicked.connect(self._generate_pdf)

        buttons_layout.addWidget(pgr_btn)
        buttons_layout.addWidget(pdf_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Status
        self.status_label = QLabel("Pronto para gerar documentos")
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        layout.addStretch()
        self.setLayout(layout)

    def _generate_pgr(self):
        """Gera documento PGR em formato DOCX"""
        if not self._validate_input():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar PGR", "", "Word Documents (*.docx)"
        )

        if file_path:
            try:
                self.status_label.setText("Gerando PGR...")
                self.progress.setVisible(True)
                self.progress.setValue(50)

                company_info = {
                    "name": self.company_name.text(),
                    "cnpj": self.company_cnpj.text(),
                    "address": self.company_address.text(),
                    "responsible": self.responsible_name.text()
                }

                self.generator.generate_pgr(
                    file_path,
                    company_info,
                    self.scope_text.toPlainText()
                )

                self.progress.setValue(100)
                QMessageBox.information(self, "Sucesso", f"PGR gerado com sucesso:\n{file_path}")
                self.status_label.setText("PGR gerado com sucesso")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao gerar PGR: {e}")
                self.status_label.setText("Erro ao gerar PGR")
            finally:
                self.progress.setVisible(False)

    def _generate_pdf(self):
        """Gera relatório de análise de riscos em PDF"""
        if not self._validate_input():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Relatório", "", "PDF Files (*.pdf)"
        )

        if file_path:
            try:
                self.status_label.setText("Gerando PDF...")
                self.progress.setVisible(True)
                self.progress.setValue(50)

                company_info = {
                    "name": self.company_name.text(),
                    "cnpj": self.company_cnpj.text(),
                    "address": self.company_address.text(),
                    "responsible": self.responsible_name.text()
                }

                self.generator.generate_pdf_report(
                    file_path,
                    company_info,
                    self.scope_text.toPlainText()
                )

                self.progress.setValue(100)
                QMessageBox.information(self, "Sucesso", f"Relatório gerado com sucesso:\n{file_path}")
                self.status_label.setText("Relatório gerado com sucesso")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório: {e}")
                self.status_label.setText("Erro ao gerar relatório")
            finally:
                self.progress.setVisible(False)

    def _validate_input(self):
        """Valida dados de entrada"""
        if not self.company_name.text():
            QMessageBox.warning(self, "Aviso", "Preencha o nome da empresa")
            return False
        if not self.scope_text.toPlainText():
            QMessageBox.warning(self, "Aviso", "Preencha o escopo da avaliação")
            return False
        if not self.storage.get_all_assessments():
            QMessageBox.warning(self, "Aviso", "Crie avaliações de risco antes de gerar documentos")
            return False
        return True
