"""Aba para gerenciar perigos identificados"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox,
    QTextEdit, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from src.models.risk import Hazard, RiskCategory
from src.database.storage import DataStorage
import uuid


class HazardDialog(QDialog):
    """Diálogo para adicionar/editar perigos"""

    def __init__(self, parent=None, hazard=None):
        super().__init__(parent)
        self.hazard = hazard
        self.setWindowTitle("Perigo Identificado")
        self.setGeometry(150, 150, 500, 400)
        self._setup_ui()

        if hazard:
            self._load_hazard(hazard)

    def _setup_ui(self):
        layout = QFormLayout()

        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.value for cat in RiskCategory])

        self.description_input = QTextEdit()
        self.location_input = QLineEdit()
        self.exposed_input = QTextEdit()

        layout.addRow("Categoria de Risco:", self.category_combo)
        layout.addRow("Descrição do Perigo:", self.description_input)
        layout.addRow("Localização:", self.location_input)
        layout.addRow("Pessoas Expostas:", self.exposed_input)

        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        cancel_btn = QPushButton("Cancelar")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addRow(buttons_layout)
        self.setLayout(layout)

    def _load_hazard(self, hazard):
        """Carrega dados do perigo no formulário"""
        self.category_combo.setCurrentText(hazard.category.value)
        self.description_input.setText(hazard.description)
        self.location_input.setText(hazard.location)
        self.exposed_input.setText(hazard.exposed_people)

    def get_hazard(self):
        """Retorna objeto Hazard com os dados do formulário"""
        category = RiskCategory(self.category_combo.currentText())

        if self.hazard:
            self.hazard.category = category
            self.hazard.description = self.description_input.toPlainText()
            self.hazard.location = self.location_input.text()
            self.hazard.exposed_people = self.exposed_input.toPlainText()
            return self.hazard
        else:
            return Hazard(
                id=str(uuid.uuid4()),
                category=category,
                description=self.description_input.toPlainText(),
                location=self.location_input.text(),
                exposed_people=self.exposed_input.toPlainText()
            )


class HazardTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        self._load_hazards()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar Perigo")
        edit_btn = QPushButton("Editar Selecionado")
        delete_btn = QPushButton("Remover Selecionado")

        add_btn.clicked.connect(self._add_hazard)
        edit_btn.clicked.connect(self._edit_hazard)
        delete_btn.clicked.connect(self._delete_hazard)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Categoria", "Descrição", "Localização", "Pessoas Expostas"])
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_hazards(self):
        """Carrega perigos na tabela"""
        hazards = self.storage.get_all_hazards()
        self.table.setRowCount(len(hazards))

        for row, hazard in enumerate(hazards):
            self.table.setItem(row, 0, QTableWidgetItem(hazard.id[:8]))
            self.table.setItem(row, 1, QTableWidgetItem(hazard.category.value))
            self.table.setItem(row, 2, QTableWidgetItem(hazard.description[:50]))
            self.table.setItem(row, 3, QTableWidgetItem(hazard.location))
            self.table.setItem(row, 4, QTableWidgetItem(hazard.exposed_people[:30]))

    def _add_hazard(self):
        dialog = HazardDialog(self)
        if dialog.exec() == QDialog.Accepted:
            hazard = dialog.get_hazard()
            self.storage.save_hazard(hazard)
            self._load_hazards()

    def _edit_hazard(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um perigo para editar")
            return

        hazard_id = self.table.item(current_row, 0).text()
        hazard = self.storage.get_hazard(hazard_id)

        if hazard:
            dialog = HazardDialog(self, hazard)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_hazard()
                self.storage.save_hazard(updated)
                self._load_hazards()

    def _delete_hazard(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um perigo para remover")
            return

        hazard_id = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", "Remover este perigo?")

        if reply == QMessageBox.Yes:
            self.storage.delete_hazard(hazard_id)
            self._load_hazards()
