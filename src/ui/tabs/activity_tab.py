"""Aba para gerenciar atividades de trabalho"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox,
    QTextEdit, QFormLayout, QMessageBox, QSpinBox, QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt
from src.models.risk import WorkActivity
from src.database.storage import DataStorage
import uuid


class ActivityDialog(QDialog):
    """Diálogo para adicionar/editar atividades"""

    def __init__(self, parent=None, storage=None, activity=None):
        super().__init__(parent)
        self.activity = activity
        self.storage = storage
        self.setWindowTitle("Atividade de Trabalho")
        self.setGeometry(150, 150, 550, 500)
        self._setup_ui()

        if activity:
            self._load_activity(activity)

    def _setup_ui(self):
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.description_input = QTextEdit()

        # Environment selection
        self.environment_combo = QComboBox()
        if self.storage:
            for env in self.storage.get_all_environments():
                self.environment_combo.addItem(env.name, env.id)

        self.workers_spinbox = QSpinBox()
        self.workers_spinbox.setMinimum(1)
        self.workers_spinbox.setMaximum(1000)
        self.workers_spinbox.setValue(1)

        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Contínuo", "Intermitente", "Ocasional"])

        # Hazards selection
        self.hazards_list = QListWidget()
        if self.storage:
            for hazard in self.storage.get_all_hazards():
                item = QListWidget.QListWidgetItem(
                    f"{hazard.category.value} - {hazard.description[:40]}"
                )
                item.setData(Qt.UserRole, hazard.id)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.hazards_list.addItem(item)

        layout.addRow("Nome da Atividade:", self.name_input)
        layout.addRow("Descrição:", self.description_input)
        layout.addRow("Ambiente:", self.environment_combo)
        layout.addRow("Número de Trabalhadores:", self.workers_spinbox)
        layout.addRow("Frequência:", self.frequency_combo)
        layout.addRow("Perigos Associados:", self.hazards_list)

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

    def _load_activity(self, activity):
        """Carrega dados da atividade no formulário"""
        self.name_input.setText(activity.name)
        self.description_input.setText(activity.description)

        # Select environment
        for i in range(self.environment_combo.count()):
            if self.environment_combo.itemData(i) == activity.environment_id:
                self.environment_combo.setCurrentIndex(i)

        self.workers_spinbox.setValue(activity.workers)
        self.frequency_combo.setCurrentText(activity.frequency)

        # Select hazards
        for i in range(self.hazards_list.count()):
            item = self.hazards_list.item(i)
            hazard_id = item.data(Qt.UserRole)
            if hazard_id in activity.hazards:
                item.setCheckState(Qt.CheckState.Checked)

    def get_activity(self):
        """Retorna objeto WorkActivity com os dados do formulário"""
        # Get selected hazards
        hazards = []
        for i in range(self.hazards_list.count()):
            item = self.hazards_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                hazards.append(item.data(Qt.UserRole))

        if self.activity:
            self.activity.name = self.name_input.text()
            self.activity.description = self.description_input.toPlainText()
            self.activity.environment_id = self.environment_combo.currentData()
            self.activity.workers = self.workers_spinbox.value()
            self.activity.frequency = self.frequency_combo.currentText()
            self.activity.hazards = hazards
            return self.activity
        else:
            return WorkActivity(
                id=str(uuid.uuid4()),
                name=self.name_input.text(),
                description=self.description_input.toPlainText(),
                environment_id=self.environment_combo.currentData(),
                workers=self.workers_spinbox.value(),
                frequency=self.frequency_combo.currentText(),
                hazards=hazards
            )


class ActivityTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        self._load_activities()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Info
        info_label = QLabel(
            "Atividades e tarefas executadas nos ambientes, com associação a perigos identificados."
        )
        layout.addWidget(info_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar Atividade")
        edit_btn = QPushButton("Editar Selecionada")
        delete_btn = QPushButton("Remover Selecionada")

        add_btn.clicked.connect(self._add_activity)
        edit_btn.clicked.connect(self._edit_activity)
        delete_btn.clicked.connect(self._delete_activity)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Ambiente", "Frequência",
            "Trabalhadores", "Perigos Associados"
        ])
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_activities(self):
        """Carrega atividades na tabela"""
        activities = self.storage.get_all_activities()
        self.table.setRowCount(len(activities))

        for row, activity in enumerate(activities):
            env = self.storage.get_environment(activity.environment_id)
            env_name = env.name if env else "N/A"

            hazard_count = len(activity.hazards)

            self.table.setItem(row, 0, QTableWidgetItem(activity.id[:8]))
            self.table.setItem(row, 1, QTableWidgetItem(activity.name))
            self.table.setItem(row, 2, QTableWidgetItem(env_name))
            self.table.setItem(row, 3, QTableWidgetItem(activity.frequency))
            self.table.setItem(row, 4, QTableWidgetItem(str(activity.workers)))
            self.table.setItem(row, 5, QTableWidgetItem(f"{hazard_count} perigo(s)"))

    def _add_activity(self):
        if not self.storage.get_all_environments():
            QMessageBox.warning(self, "Aviso", "Cadastre ambientes antes de criar atividades")
            return

        dialog = ActivityDialog(self, self.storage)
        if dialog.exec() == QDialog.Accepted:
            activity = dialog.get_activity()
            self.storage.save_activity(activity)
            self._load_activities()

    def _edit_activity(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma atividade para editar")
            return

        activity_id = self.table.item(current_row, 0).text()
        activity = self.storage.get_activity(activity_id)

        if activity:
            dialog = ActivityDialog(self, self.storage, activity)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_activity()
                self.storage.save_activity(updated)
                self._load_activities()

    def _delete_activity(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma atividade para remover")
            return

        activity_id = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", "Remover esta atividade?")

        if reply == QMessageBox.Yes:
            self.storage.delete_activity(activity_id)
            self._load_activities()
