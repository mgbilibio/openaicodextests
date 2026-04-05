"""Aba para gerenciar ambientes de trabalho"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QSpinBox,
    QComboBox, QTextEdit, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt
from src.models.risk import WorkEnvironment
from src.database.storage import DataStorage
import uuid


class EnvironmentDialog(QDialog):
    """Diálogo para adicionar/editar ambientes"""

    def __init__(self, parent=None, environment=None):
        super().__init__(parent)
        self.environment = environment
        self.setWindowTitle("Ambiente de Trabalho")
        self.setGeometry(150, 150, 500, 400)
        self._setup_ui()

        if environment:
            self._load_environment(environment)

    def _setup_ui(self):
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.location_input = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Escritório", "Produção", "Obra", "Comercial", "Administrativo", "Outro"])
        self.workers_spinbox = QSpinBox()
        self.workers_spinbox.setMinimum(1)
        self.workers_spinbox.setMaximum(10000)

        layout.addRow("Nome do Ambiente:", self.name_input)
        layout.addRow("Descrição:", self.description_input)
        layout.addRow("Localização:", self.location_input)
        layout.addRow("Tipo:", self.type_combo)
        layout.addRow("Número de Trabalhadores:", self.workers_spinbox)

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

    def _load_environment(self, environment):
        """Carrega dados do ambiente no formulário"""
        self.name_input.setText(environment.name)
        self.description_input.setText(environment.description)
        self.location_input.setText(environment.location)
        self.type_combo.setCurrentText(environment.type)
        self.workers_spinbox.setValue(environment.workers_count)

    def get_environment(self):
        """Retorna objeto WorkEnvironment com os dados do formulário"""
        if self.environment:
            self.environment.name = self.name_input.text()
            self.environment.description = self.description_input.toPlainText()
            self.environment.location = self.location_input.text()
            self.environment.type = self.type_combo.currentText()
            self.environment.workers_count = self.workers_spinbox.value()
            return self.environment
        else:
            return WorkEnvironment(
                id=str(uuid.uuid4()),
                name=self.name_input.text(),
                description=self.description_input.toPlainText(),
                location=self.location_input.text(),
                type=self.type_combo.currentText(),
                workers_count=self.workers_spinbox.value()
            )


class EnvironmentTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        self._load_environments()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar Ambiente")
        edit_btn = QPushButton("Editar Selecionado")
        delete_btn = QPushButton("Remover Selecionado")

        add_btn.clicked.connect(self._add_environment)
        edit_btn.clicked.connect(self._edit_environment)
        delete_btn.clicked.connect(self._delete_environment)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Tipo", "Localização", "Trabalhadores", "Descrição"])
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_environments(self):
        """Carrega ambientes na tabela"""
        environments = self.storage.get_all_environments()
        self.table.setRowCount(len(environments))

        for row, env in enumerate(environments):
            self.table.setItem(row, 0, QTableWidgetItem(env.id[:8]))
            self.table.setItem(row, 1, QTableWidgetItem(env.name))
            self.table.setItem(row, 2, QTableWidgetItem(env.type))
            self.table.setItem(row, 3, QTableWidgetItem(env.location))
            self.table.setItem(row, 4, QTableWidgetItem(str(env.workers_count)))
            self.table.setItem(row, 5, QTableWidgetItem(env.description[:50]))

    def _add_environment(self):
        dialog = EnvironmentDialog(self)
        if dialog.exec() == QDialog.Accepted:
            environment = dialog.get_environment()
            self.storage.save_environment(environment)
            self._load_environments()

    def _edit_environment(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um ambiente para editar")
            return

        environment_id = self.table.item(current_row, 0).text()
        environment = self.storage.get_environment(environment_id)

        if environment:
            dialog = EnvironmentDialog(self, environment)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_environment()
                self.storage.save_environment(updated)
                self._load_environments()

    def _delete_environment(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um ambiente para remover")
            return

        environment_id = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", "Remover este ambiente?")

        if reply == QMessageBox.Yes:
            self.storage.delete_environment(environment_id)
            self._load_environments()
