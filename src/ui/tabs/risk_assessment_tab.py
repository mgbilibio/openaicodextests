"""Aba para avaliação de riscos seguindo ISO 31010"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox,
    QTextEdit, QFormLayout, QMessageBox, QSpinBox
)
from PySide6.QtCore import Qt
from src.models.risk import RiskAssessment, RiskSeverity, RiskProbability
from src.database.storage import DataStorage
import uuid


class RiskAssessmentDialog(QDialog):
    """Diálogo para realizar avaliação de risco (ISO 31010)"""

    def __init__(self, parent=None, storage=None, assessment=None):
        super().__init__(parent)
        self.assessment = assessment
        self.storage = storage
        self.setWindowTitle("Avaliação de Risco - ISO 31010")
        self.setGeometry(100, 100, 600, 600)
        self._setup_ui()

        if assessment:
            self._load_assessment(assessment)

    def _setup_ui(self):
        layout = QFormLayout()

        # Hazard selection
        self.hazard_combo = QComboBox()
        if self.storage:
            for hazard in self.storage.get_all_hazards():
                self.hazard_combo.addItem(hazard.description, hazard.id)

        # Severity and Probability
        self.severity_combo = QComboBox()
        self.severity_combo.addItems([s.value for s in RiskSeverity])

        self.probability_combo = QComboBox()
        self.probability_combo.addItems([p.value for p in RiskProbability])

        # Control measures
        self.control_measures = QTextEdit()

        # Residual risk
        self.residual_severity = QComboBox()
        self.residual_severity.addItems(["Nenhuma"] + [s.value for s in RiskSeverity])

        self.residual_probability = QComboBox()
        self.residual_probability.addItems(["Nenhuma"] + [p.value for p in RiskProbability])

        # Others
        self.responsible = QLineEdit()
        self.deadline = QLineEdit()
        self.notes = QTextEdit()

        layout.addRow("Perigo:", self.hazard_combo)
        layout.addRow("Severidade:", self.severity_combo)
        layout.addRow("Probabilidade:", self.probability_combo)
        layout.addRow("Medidas de Controle:", self.control_measures)
        layout.addRow("Severidade Residual:", self.residual_severity)
        layout.addRow("Probabilidade Residual:", self.residual_probability)
        layout.addRow("Responsável:", self.responsible)
        layout.addRow("Prazo:", self.deadline)
        layout.addRow("Observações:", self.notes)

        # Risk level indicator
        self.risk_level_label = QLabel()
        layout.addRow("Nível de Risco:", self.risk_level_label)

        self.severity_combo.currentTextChanged.connect(self._update_risk_level)
        self.probability_combo.currentTextChanged.connect(self._update_risk_level)

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

    def _update_risk_level(self):
        """Atualiza o nível de risco na matriz ISO 31010"""
        try:
            severity = RiskSeverity(self.severity_combo.currentText())
            probability = RiskProbability(self.probability_combo.currentText())

            severity_scores = {
                RiskSeverity.INSIGNIFICANTE: 1,
                RiskSeverity.MENOR: 2,
                RiskSeverity.MODERADO: 3,
                RiskSeverity.MAIOR: 4,
                RiskSeverity.CATASTROFICO: 5,
            }

            probability_scores = {
                RiskProbability.RARO: 1,
                RiskProbability.IMPROVAVEL: 2,
                RiskProbability.POSSIVEL: 3,
                RiskProbability.PROVAVEL: 4,
                RiskProbability.MUITO_PROVAVEL: 5,
            }

            score = severity_scores[severity] * probability_scores[probability]

            if score <= 3:
                level = "Insignificante"
            elif score <= 6:
                level = "Aceitável"
            elif score <= 12:
                level = "Moderado"
            elif score <= 16:
                level = "Substancial"
            else:
                level = "Intolerável"

            self.risk_level_label.setText(f"{level} (score: {score})")
        except:
            pass

    def _load_assessment(self, assessment):
        """Carrega dados da avaliação no formulário"""
        # Find hazard in combo
        for i in range(self.hazard_combo.count()):
            if self.hazard_combo.itemData(i) == assessment.hazard_id:
                self.hazard_combo.setCurrentIndex(i)

        self.severity_combo.setCurrentText(assessment.severity.value)
        self.probability_combo.setCurrentText(assessment.probability.value)
        self.control_measures.setText(assessment.control_measures)
        self.responsible.setText(assessment.responsible or "")
        self.deadline.setText(assessment.deadline or "")
        self.notes.setText(assessment.notes)

    def get_assessment(self):
        """Retorna objeto RiskAssessment com os dados do formulário"""
        hazard_id = self.hazard_combo.currentData()
        severity = RiskSeverity(self.severity_combo.currentText())
        probability = RiskProbability(self.probability_combo.currentText())

        residual_sev = None
        if self.residual_severity.currentText() != "Nenhuma":
            residual_sev = RiskSeverity(self.residual_severity.currentText())

        residual_prob = None
        if self.residual_probability.currentText() != "Nenhuma":
            residual_prob = RiskProbability(self.residual_probability.currentText())

        if self.assessment:
            self.assessment.hazard_id = hazard_id
            self.assessment.severity = severity
            self.assessment.probability = probability
            self.assessment.control_measures = self.control_measures.toPlainText()
            self.assessment.residual_severity = residual_sev
            self.assessment.residual_probability = residual_prob
            self.assessment.responsible = self.responsible.text()
            self.assessment.deadline = self.deadline.text()
            self.assessment.notes = self.notes.toPlainText()
            return self.assessment
        else:
            return RiskAssessment(
                id=str(uuid.uuid4()),
                hazard_id=hazard_id,
                severity=severity,
                probability=probability,
                control_measures=self.control_measures.toPlainText(),
                residual_severity=residual_sev,
                residual_probability=residual_prob,
                responsible=self.responsible.text(),
                deadline=self.deadline.text(),
                notes=self.notes.toPlainText()
            )


class RiskAssessmentTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        self._load_assessments()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar Avaliação")
        edit_btn = QPushButton("Editar Selecionada")
        delete_btn = QPushButton("Remover Selecionada")

        add_btn.clicked.connect(self._add_assessment)
        edit_btn.clicked.connect(self._edit_assessment)
        delete_btn.clicked.connect(self._delete_assessment)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Perigo", "Severidade", "Probabilidade",
            "Nível", "Controles", "Responsável"
        ])
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_assessments(self):
        """Carrega avaliações na tabela"""
        assessments = self.storage.get_all_assessments()
        self.table.setRowCount(len(assessments))

        for row, assess in enumerate(assessments):
            hazard = self.storage.get_hazard(assess.hazard_id)
            hazard_desc = hazard.description[:30] if hazard else "N/A"

            self.table.setItem(row, 0, QTableWidgetItem(assess.id[:8]))
            self.table.setItem(row, 1, QTableWidgetItem(hazard_desc))
            self.table.setItem(row, 2, QTableWidgetItem(assess.severity.value))
            self.table.setItem(row, 3, QTableWidgetItem(assess.probability.value))
            self.table.setItem(row, 4, QTableWidgetItem(assess.get_risk_level()))
            self.table.setItem(row, 5, QTableWidgetItem(assess.control_measures[:40]))
            self.table.setItem(row, 6, QTableWidgetItem(assess.responsible or "N/A"))

    def _add_assessment(self):
        if not self.storage.get_all_hazards():
            QMessageBox.warning(self, "Aviso", "Adicione perigos antes de criar avaliações")
            return

        dialog = RiskAssessmentDialog(self, self.storage)
        if dialog.exec() == QDialog.Accepted:
            assessment = dialog.get_assessment()
            self.storage.save_assessment(assessment)
            self._load_assessments()

    def _edit_assessment(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma avaliação para editar")
            return

        assessment_id = self.table.item(current_row, 0).text()
        assessment = self.storage.get_assessment(assessment_id)

        if assessment:
            dialog = RiskAssessmentDialog(self, self.storage, assessment)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_assessment()
                self.storage.save_assessment(updated)
                self._load_assessments()

    def _delete_assessment(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma avaliação para remover")
            return

        assessment_id = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", "Remover esta avaliação?")

        if reply == QMessageBox.Yes:
            self.storage.delete_assessment(assessment_id)
            self._load_assessments()
