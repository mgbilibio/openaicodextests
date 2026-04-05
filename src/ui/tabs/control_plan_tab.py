"""Aba para Plano de Controles e Ações Corretivas"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox,
    QTextEdit, QFormLayout, QMessageBox, QSpinBox, QDateEdit,
    QDoubleSpinBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from src.models.risk import ControlMeasure, ControlType, ControlStatus
from src.database.storage import DataStorage
import uuid
from datetime import datetime, date


class ControlMeasureDialog(QDialog):
    """Diálogo para adicionar/editar medidas de controle"""

    def __init__(self, parent=None, storage=None, control=None):
        super().__init__(parent)
        self.control = control
        self.storage = storage
        self.setWindowTitle("Medida de Controle")
        self.setGeometry(100, 100, 600, 700)
        self._setup_ui()

        if control:
            self._load_control(control)

    def _setup_ui(self):
        layout = QFormLayout()

        # Assessment selection
        self.assessment_combo = QComboBox()
        if self.storage:
            for assess in self.storage.get_all_assessments():
                hazard = self.storage.get_hazard(assess.hazard_id)
                hazard_text = hazard.description[:40] if hazard else "N/A"
                self.assessment_combo.addItem(
                    f"[{assess.get_risk_level()}] {hazard_text}",
                    assess.id
                )

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Descrição detalhada da medida de controle...")

        # Control type
        self.type_combo = QComboBox()
        self.type_combo.addItems([ct.value for ct in ControlType])

        # Dates
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())

        self.deadline = QDateEdit()
        self.deadline.setDate(QDate.currentDate().addMonths(1))

        # Responsible
        self.responsible = QLineEdit()
        self.alternative_responsible = QLineEdit()

        # Budget
        self.estimated_cost = QDoubleSpinBox()
        self.estimated_cost.setMaximum(999999.99)
        self.estimated_cost.setValue(0.0)
        self.estimated_cost.setSuffix(" R$")

        self.actual_cost = QDoubleSpinBox()
        self.actual_cost.setMaximum(999999.99)
        self.actual_cost.setValue(0.0)
        self.actual_cost.setSuffix(" R$")

        self.supplier = QLineEdit()

        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems([s.value for s in ControlStatus])

        # Progress
        self.progress_spinbox = QSpinBox()
        self.progress_spinbox.setMinimum(0)
        self.progress_spinbox.setMaximum(100)
        self.progress_spinbox.setValue(0)
        self.progress_spinbox.setSuffix(" %")

        # Effectiveness
        self.expected_reduction = QSpinBox()
        self.expected_reduction.setMinimum(0)
        self.expected_reduction.setMaximum(100)
        self.expected_reduction.setValue(50)
        self.expected_reduction.setSuffix(" %")

        self.actual_reduction = QSpinBox()
        self.actual_reduction.setMinimum(0)
        self.actual_reduction.setMaximum(100)
        self.actual_reduction.setValue(0)
        self.actual_reduction.setSuffix(" %")

        self.verified_combo = QComboBox()
        self.verified_combo.addItems(["Não Verificado", "Verificado"])

        self.verified_by = QLineEdit()
        self.notes = QTextEdit()

        layout.addRow("Risco a Controlar:", self.assessment_combo)
        layout.addRow("Descrição da Medida:", self.description_input)
        layout.addRow("Tipo de Controle:", self.type_combo)
        layout.addRow("Data Início:", self.start_date)
        layout.addRow("Prazo:", self.deadline)
        layout.addRow("Responsável Principal:", self.responsible)
        layout.addRow("Responsável Alternativo:", self.alternative_responsible)
        layout.addRow("Custo Estimado:", self.estimated_cost)
        layout.addRow("Custo Real:", self.actual_cost)
        layout.addRow("Fornecedor:", self.supplier)
        layout.addRow("Status:", self.status_combo)
        layout.addRow("Progresso:", self.progress_spinbox)
        layout.addRow("Redução Esperada:", self.expected_reduction)
        layout.addRow("Redução Real:", self.actual_reduction)
        layout.addRow("Verificação:", self.verified_combo)
        layout.addRow("Verificado Por:", self.verified_by)
        layout.addRow("Observações:", self.notes)

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

    def _load_control(self, control):
        """Carrega dados da medida no formulário"""
        # Find assessment
        for i in range(self.assessment_combo.count()):
            if self.assessment_combo.itemData(i) == control.assessment_id:
                self.assessment_combo.setCurrentIndex(i)

        self.description_input.setText(control.description)
        self.type_combo.setCurrentText(control.control_type.value)

        # Dates
        start = datetime.strptime(control.start_date, '%Y-%m-%d').date()
        deadline = datetime.strptime(control.deadline, '%Y-%m-%d').date()
        self.start_date.setDate(QDate(start.year, start.month, start.day))
        self.deadline.setDate(QDate(deadline.year, deadline.month, deadline.day))

        self.responsible.setText(control.responsible)
        if control.alternative_responsible:
            self.alternative_responsible.setText(control.alternative_responsible)

        self.estimated_cost.setValue(control.estimated_cost)
        self.actual_cost.setValue(control.actual_cost)
        if control.supplier:
            self.supplier.setText(control.supplier)

        self.status_combo.setCurrentText(control.status.value)
        self.progress_spinbox.setValue(control.progress_percent)
        self.expected_reduction.setValue(control.expected_reduction_percent)
        if control.actual_reduction_percent:
            self.actual_reduction.setValue(control.actual_reduction_percent)

        status = "Verificado" if control.verified else "Não Verificado"
        self.verified_combo.setCurrentText(status)
        if control.verified_by:
            self.verified_by.setText(control.verified_by)

        self.notes.setText(control.notes)

    def get_control(self):
        """Retorna objeto ControlMeasure com os dados do formulário"""
        start_qdate = self.start_date.date()
        deadline_qdate = self.deadline.date()

        start_str = f"{start_qdate.year}-{start_qdate.month:02d}-{start_qdate.day:02d}"
        deadline_str = f"{deadline_qdate.year}-{deadline_qdate.month:02d}-{deadline_qdate.day:02d}"

        verified = self.verified_combo.currentText() == "Verificado"
        verified_by = self.verified_by.text() if verified else None

        if self.control:
            self.control.assessment_id = self.assessment_combo.currentData()
            self.control.description = self.description_input.toPlainText()
            self.control.control_type = ControlType(self.type_combo.currentText())
            self.control.start_date = start_str
            self.control.deadline = deadline_str
            self.control.responsible = self.responsible.text()
            self.control.alternative_responsible = self.alternative_responsible.text() or None
            self.control.estimated_cost = self.estimated_cost.value()
            self.control.actual_cost = self.actual_cost.value()
            self.control.supplier = self.supplier.text() or None
            self.control.status = ControlStatus(self.status_combo.currentText())
            self.control.progress_percent = self.progress_spinbox.value()
            self.control.expected_reduction_percent = self.expected_reduction.value()
            self.control.actual_reduction_percent = self.actual_reduction.value()
            self.control.verified = verified
            self.control.verified_by = verified_by
            self.control.notes = self.notes.toPlainText()
            return self.control
        else:
            return ControlMeasure(
                id=str(uuid.uuid4()),
                assessment_id=self.assessment_combo.currentData(),
                description=self.description_input.toPlainText(),
                control_type=ControlType(self.type_combo.currentText()),
                start_date=start_str,
                deadline=deadline_str,
                responsible=self.responsible.text(),
                alternative_responsible=self.alternative_responsible.text() or None,
                estimated_cost=self.estimated_cost.value(),
                actual_cost=self.actual_cost.value(),
                supplier=self.supplier.text() or None,
                status=ControlStatus(self.status_combo.currentText()),
                progress_percent=self.progress_spinbox.value(),
                expected_reduction_percent=self.expected_reduction.value(),
                actual_reduction_percent=self.actual_reduction.value(),
                verified=verified,
                verified_by=verified_by,
                notes=self.notes.toPlainText()
            )


class ControlPlanTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        self._load_controls()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Info
        info_label = QLabel(
            "Planejamento e acompanhamento de ações corretivas para redução de riscos"
        )
        layout.addWidget(info_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar Ação")
        edit_btn = QPushButton("Editar Selecionada")
        delete_btn = QPushButton("Remover Selecionada")
        refresh_btn = QPushButton("Atualizar")

        add_btn.clicked.connect(self._add_control)
        edit_btn.clicked.connect(self._edit_control)
        delete_btn.clicked.connect(self._delete_control)
        refresh_btn.clicked.connect(self._load_controls)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Prioridade", "Status", "Descrição", "Tipo", "Responsável",
            "Prazo", "Progresso", "Custo Est.", "Custo Real", "Verificado"
        ])
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)

        # Summary
        summary_layout = QHBoxLayout()
        self.summary_label = QLabel()
        summary_layout.addWidget(self.summary_label)
        summary_layout.addStretch()
        layout.addLayout(summary_layout)

        self.setLayout(layout)

    def _load_controls(self):
        """Carrega medidas de controle na tabela"""
        controls = self.storage.get_all_control_measures()
        self.table.setRowCount(len(controls))

        completed = 0
        overdue = 0
        in_progress = 0
        total_budget = 0.0
        total_spent = 0.0

        for row, control in enumerate(controls):
            priority = control.get_priority()
            status = control.status.value
            control_type = control.control_type.value

            if control.status == ControlStatus.CONCLUIDO:
                completed += 1
            elif control.is_overdue():
                overdue += 1
            elif control.status == ControlStatus.EM_EXECUCAO:
                in_progress += 1

            total_budget += control.estimated_cost
            total_spent += control.actual_cost

            self.table.setItem(row, 0, QTableWidgetItem(priority))
            self.table.setItem(row, 1, QTableWidgetItem(status))
            self.table.setItem(row, 2, QTableWidgetItem(control.description[:40]))
            self.table.setItem(row, 3, QTableWidgetItem(control_type))
            self.table.setItem(row, 4, QTableWidgetItem(control.responsible))
            self.table.setItem(row, 5, QTableWidgetItem(control.deadline))
            self.table.setItem(row, 6, QTableWidgetItem(f"{control.progress_percent}%"))

            cost_est = f"R$ {control.estimated_cost:,.2f}"
            cost_real = f"R$ {control.actual_cost:,.2f}"
            self.table.setItem(row, 7, QTableWidgetItem(cost_est))
            self.table.setItem(row, 8, QTableWidgetItem(cost_real))

            verified = "✓ Sim" if control.verified else "✗ Não"
            self.table.setItem(row, 9, QTableWidgetItem(verified))

            # Color by priority
            if "Crítica" in priority:
                for col in range(10):
                    item = self.table.item(row, col)
                    item.setBackground(QColor(255, 200, 200))

        # Update summary
        total_actions = len(controls)
        summary_text = (
            f"Total: {total_actions} | Concluídas: {completed} | "
            f"Em Progresso: {in_progress} | Atrasadas: {overdue} | "
            f"Orçamento: R$ {total_budget:,.2f} | Gasto: R$ {total_spent:,.2f}"
        )
        self.summary_label.setText(summary_text)

    def _add_control(self):
        if not self.storage.get_all_assessments():
            QMessageBox.warning(self, "Aviso", "Crie avaliações de risco antes de planejar ações")
            return

        dialog = ControlMeasureDialog(self, self.storage)
        if dialog.exec() == QDialog.Accepted:
            control = dialog.get_control()
            self.storage.save_control_measure(control)
            self._load_controls()

    def _edit_control(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma ação para editar")
            return

        # Get control ID from description cell
        description = self.table.item(current_row, 2).text()
        controls = self.storage.get_all_control_measures()

        control = None
        for c in controls:
            if description in c.description:
                control = c
                break

        if control:
            dialog = ControlMeasureDialog(self, self.storage, control)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_control()
                self.storage.save_control_measure(updated)
                self._load_controls()

    def _delete_control(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma ação para remover")
            return

        description = self.table.item(current_row, 2).text()
        reply = QMessageBox.question(self, "Confirmar", "Remover esta ação corretiva?")

        if reply == QMessageBox.Yes:
            controls = self.storage.get_all_control_measures()
            for c in controls:
                if description in c.description:
                    self.storage.delete_control_measure(c.id)
                    self._load_controls()
                    break
