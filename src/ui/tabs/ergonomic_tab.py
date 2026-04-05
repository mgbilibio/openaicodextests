"""Aba para Análise Ergonômica e Postural (NR-17)"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox,
    QTextEdit, QFormLayout, QMessageBox, QSpinBox, QDateEdit,
    QCheckBox, QProgressBar
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from src.models.ergonomics import PosturalAssessment, ForceLevel, RiskLevel
from src.database.storage import DataStorage
import uuid
from datetime import datetime, date


class PosturalAssessmentDialog(QDialog):
    """Diálogo para avaliação postural RULA"""

    def __init__(self, parent=None, storage=None, assessment=None):
        super().__init__(parent)
        self.assessment = assessment
        self.storage = storage
        self.setWindowTitle("Análise Ergonômica - Avaliação Postural RULA")
        self.setGeometry(50, 50, 800, 900)
        self._setup_ui()

        if assessment:
            self._load_assessment(assessment)

    def _setup_ui(self):
        layout = QFormLayout()

        # Activity selection
        self.activity_combo = QComboBox()
        if self.storage:
            for activity in self.storage.get_all_activities():
                self.activity_combo.addItem(activity.name, activity.id)

        # Assessment info
        self.assessor_input = QLineEdit()
        self.assessment_date = QDateEdit()
        self.assessment_date.setDate(QDate.currentDate())

        # ===== Membros Superiores =====
        layout.addRow(QLabel("<b>MEMBROS SUPERIORES (Braço/Pulso)</b>"), QLabel())

        self.shoulder_combo = QComboBox()
        self.shoulder_combo.addItems(["Neutro", "Ligeiramente Elevado", "Elevado"])

        self.shoulder_abduction_check = QCheckBox("Abdução de ombro presente")
        self.elbow_flexion = QSpinBox()
        self.elbow_flexion.setMinimum(0)
        self.elbow_flexion.setMaximum(180)
        self.elbow_flexion.setValue(90)
        self.elbow_flexion.setSuffix("°")

        self.elbow_away_check = QCheckBox("Cotovelo afastado do corpo")

        self.wrist_extension = QSpinBox()
        self.wrist_extension.setMinimum(-30)
        self.wrist_extension.setMaximum(60)
        self.wrist_extension.setValue(0)
        self.wrist_extension.setSuffix("°")

        self.wrist_deviation_combo = QComboBox()
        self.wrist_deviation_combo.addItems(["Nenhuma", "Radial", "Ulnar"])

        self.wrist_rotation_check = QCheckBox("Rotação de pulso presente")

        layout.addRow("Posição do Ombro:", self.shoulder_combo)
        layout.addRow("", self.shoulder_abduction_check)
        layout.addRow("Flexão do Cotovelo:", self.elbow_flexion)
        layout.addRow("", self.elbow_away_check)
        layout.addRow("Extensão do Pulso:", self.wrist_extension)
        layout.addRow("Desvio de Pulso:", self.wrist_deviation_combo)
        layout.addRow("", self.wrist_rotation_check)

        # ===== Pescoço e Tronco =====
        layout.addRow(QLabel("<b>PESCOÇO E TRONCO</b>"), QLabel())

        self.neck_flexion = QSpinBox()
        self.neck_flexion.setMinimum(0)
        self.neck_flexion.setMaximum(90)
        self.neck_flexion.setValue(0)
        self.neck_flexion.setSuffix("°")

        self.neck_rotation_check = QCheckBox("Rotação de pescoço presente")
        self.neck_side_flexion_check = QCheckBox("Flexão lateral de pescoço")

        self.trunk_flexion = QSpinBox()
        self.trunk_flexion.setMinimum(0)
        self.trunk_flexion.setMaximum(60)
        self.trunk_flexion.setValue(0)
        self.trunk_flexion.setSuffix("°")

        self.trunk_rotation_check = QCheckBox("Rotação de tronco presente")
        self.trunk_side_flexion_check = QCheckBox("Flexão lateral de tronco")

        self.seated_properly_check = QCheckBox("Posição sentada correta", True)
        self.feet_support_check = QCheckBox("Pés apoiados corretamente", True)

        layout.addRow("Flexão de Pescoço:", self.neck_flexion)
        layout.addRow("", self.neck_rotation_check)
        layout.addRow("", self.neck_side_flexion_check)
        layout.addRow("Flexão de Tronco:", self.trunk_flexion)
        layout.addRow("", self.trunk_rotation_check)
        layout.addRow("", self.trunk_side_flexion_check)
        layout.addRow("", self.seated_properly_check)
        layout.addRow("", self.feet_support_check)

        # ===== Força e Repetição =====
        layout.addRow(QLabel("<b>FORÇA, CARGA E REPETIÇÃO</b>"), QLabel())

        self.force_level_combo = QComboBox()
        self.force_level_combo.addItems([f.value for f in ForceLevel])

        self.force_duration_combo = QComboBox()
        self.force_duration_combo.addItems(["Ocasional", "Frequente (>2/min)", "Repetitivo"])

        self.static_posture = QSpinBox()
        self.static_posture.setMaximum(480)
        self.static_posture.setValue(0)
        self.static_posture.setSuffix(" min")

        self.activity_frequency_combo = QComboBox()
        self.activity_frequency_combo.addItems(["Ocasional", "Frequente", "Contínuo"])

        self.repetitive_check = QCheckBox("Movimentos repetitivos")

        layout.addRow("Nível de Força/Carga:", self.force_level_combo)
        layout.addRow("Duração da Força:", self.force_duration_combo)
        layout.addRow("Postura Estática (duração):", self.static_posture)
        layout.addRow("Frequência de Atividade:", self.activity_frequency_combo)
        layout.addRow("", self.repetitive_check)

        # ===== Fatores Adicionais =====
        layout.addRow(QLabel("<b>FATORES ADICIONAIS</b>"), QLabel())

        self.stress_check = QCheckBox("Alto nível de estresse")
        self.visibility_check = QCheckBox("Visibilidade deficiente")
        self.support_check = QCheckBox("Suporte inadequado")

        layout.addRow("", self.stress_check)
        layout.addRow("", self.visibility_check)
        layout.addRow("", self.support_check)

        # ===== Resultados =====
        layout.addRow(QLabel("<b>RESULTADOS</b>"), QLabel())

        self.score_label = QLabel("Score RULA: -")
        self.risk_label = QLabel("Nível de Risco: -")
        self.score_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.risk_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        layout.addRow("", self.score_label)
        layout.addRow("", self.risk_label)

        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(100)
        layout.addRow("Recomendações:", self.recommendations_text)

        # ===== Follow-up =====
        self.followup_check = QCheckBox("Acompanhamento necessário")
        self.followup_date = QDateEdit()
        self.followup_date.setDate(QDate.currentDate().addMonths(3))

        layout.addRow("", self.followup_check)
        layout.addRow("Data de Acompanhamento:", self.followup_date)

        # Calculate button
        calculate_btn = QPushButton("Calcular Score RULA")
        calculate_btn.clicked.connect(self._calculate_rula)
        layout.addRow("", calculate_btn)

        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar Avaliação")
        cancel_btn = QPushButton("Cancelar")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addRow(buttons_layout)
        self.setLayout(layout)

    def _load_assessment(self, assessment):
        """Carrega dados da avaliação"""
        for i in range(self.activity_combo.count()):
            if self.activity_combo.itemData(i) == assessment.activity_id:
                self.activity_combo.setCurrentIndex(i)

        self.assessor_input.setText(assessment.assessor)
        date_obj = datetime.strptime(assessment.assessment_date, '%Y-%m-%d').date()
        self.assessment_date.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))

        self.shoulder_combo.setCurrentText(assessment.shoulder_elevation)
        self.shoulder_abduction_check.setChecked(assessment.shoulder_abduction)
        self.elbow_flexion.setValue(assessment.elbow_flexion)
        self.elbow_away_check.setChecked(assessment.elbow_away_from_body)
        self.wrist_extension.setValue(assessment.wrist_extension)
        self.wrist_deviation_combo.setCurrentText(assessment.wrist_deviation)
        self.wrist_rotation_check.setChecked(assessment.wrist_rotation)

        self.neck_flexion.setValue(assessment.neck_flexion)
        self.neck_rotation_check.setChecked(assessment.neck_rotation)
        self.neck_side_flexion_check.setChecked(assessment.neck_side_flexion)
        self.trunk_flexion.setValue(assessment.trunk_flexion)
        self.trunk_rotation_check.setChecked(assessment.trunk_rotation)
        self.trunk_side_flexion_check.setChecked(assessment.trunk_side_flexion)
        self.seated_properly_check.setChecked(assessment.seated_properly)
        self.feet_support_check.setChecked(assessment.feet_flat_or_footrest)

        self.force_level_combo.setCurrentText(assessment.force_level.value)
        self.force_duration_combo.setCurrentText(assessment.force_duration)
        self.static_posture.setValue(assessment.static_posture_min)
        self.activity_frequency_combo.setCurrentText(assessment.activity_frequency)
        self.repetitive_check.setChecked(assessment.repetitive_movements)

        self.stress_check.setChecked(assessment.high_stress)
        self.visibility_check.setChecked(assessment.poor_visibility)
        self.support_check.setChecked(assessment.inadequate_support)

        self.score_label.setText(f"Score RULA: {assessment.rula_final_score}")
        self.risk_label.setText(f"Nível de Risco: {assessment.risk_level.value}")
        self.recommendations_text.setText('\n'.join(assessment.recommendations))

        self.followup_check.setChecked(assessment.follow_up_needed)
        if assessment.follow_up_date:
            followup = datetime.strptime(assessment.follow_up_date, '%Y-%m-%d').date()
            self.followup_date.setDate(QDate(followup.year, followup.month, followup.day))

    def _calculate_rula(self):
        """Calcula score RULA e gera recomendações"""
        # Criar objeto temporário com dados do formulário
        temp = self._get_assessment_data()

        # Calcular score
        temp.calculate_rula_score()
        temp.generate_recommendations()

        # Atualizar labels
        self.score_label.setText(f"Score RULA: {temp.rula_final_score}/7")

        color = "green"
        if temp.rula_final_score <= 2:
            color = "green"
        elif temp.rula_final_score <= 4:
            color = "orange"
        else:
            color = "red"

        self.score_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {color};")
        self.risk_label.setText(f"Nível de Risco: {temp.risk_level.value}")
        self.risk_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {color};")

        # Atualizar recomendações
        recom_text = '\n'.join(temp.recommendations)
        if temp.suggested_positions:
            recom_text += "\n\nPosturas Sugeridas:\n" + '\n'.join(temp.suggested_positions)
        if temp.required_equipment:
            recom_text += "\n\nEquipamentos Necessários:\n" + '\n'.join(temp.required_equipment)

        self.recommendations_text.setText(recom_text)

    def _get_assessment_data(self) -> PosturalAssessment:
        """Extrai dados do formulário e cria PosturalAssessment"""
        qdate = self.assessment_date.date()
        date_str = f"{qdate.year}-{qdate.month:02d}-{qdate.day:02d}"

        return PosturalAssessment(
            id=self.assessment.id if self.assessment else str(uuid.uuid4()),
            activity_id=self.activity_combo.currentData(),
            assessment_date=date_str,
            assessor=self.assessor_input.text(),
            shoulder_elevation=self.shoulder_combo.currentText(),
            shoulder_abduction=self.shoulder_abduction_check.isChecked(),
            elbow_flexion=self.elbow_flexion.value(),
            elbow_away_from_body=self.elbow_away_check.isChecked(),
            wrist_extension=self.wrist_extension.value(),
            wrist_deviation=self.wrist_deviation_combo.currentText(),
            wrist_rotation=self.wrist_rotation_check.isChecked(),
            neck_flexion=self.neck_flexion.value(),
            neck_rotation=self.neck_rotation_check.isChecked(),
            neck_side_flexion=self.neck_side_flexion_check.isChecked(),
            trunk_flexion=self.trunk_flexion.value(),
            trunk_rotation=self.trunk_rotation_check.isChecked(),
            trunk_side_flexion=self.trunk_side_flexion_check.isChecked(),
            seated_properly=self.seated_properly_check.isChecked(),
            feet_flat_or_footrest=self.feet_support_check.isChecked(),
            force_level=ForceLevel(self.force_level_combo.currentText()),
            force_duration=self.force_duration_combo.currentText(),
            repetitive_movements=self.repetitive_check.isChecked(),
            static_posture_min=self.static_posture.value(),
            activity_frequency=self.activity_frequency_combo.currentText(),
            high_stress=self.stress_check.isChecked(),
            poor_visibility=self.visibility_check.isChecked(),
            inadequate_support=self.support_check.isChecked(),
            follow_up_needed=self.followup_check.isChecked(),
        )

    def get_assessment(self):
        """Retorna PosturalAssessment completo"""
        assessment = self._get_assessment_data()

        # Recalcular para salvar
        assessment.calculate_rula_score()
        assessment.generate_recommendations()

        if self.followup_check.isChecked():
            qdate = self.followup_date.date()
            assessment.follow_up_date = f"{qdate.year}-{qdate.month:02d}-{qdate.day:02d}"

        return assessment


class ErgonomicTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        self._load_assessments()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Info
        info = QLabel(
            "Avaliação Ergonômica - Análise Postural RULA conforme NR-17"
        )
        layout.addWidget(info)

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Nova Avaliação")
        edit_btn = QPushButton("Editar Selecionada")
        delete_btn = QPushButton("Remover Selecionada")
        refresh_btn = QPushButton("Atualizar")

        add_btn.clicked.connect(self._add_assessment)
        edit_btn.clicked.connect(self._edit_assessment)
        delete_btn.clicked.connect(self._delete_assessment)
        refresh_btn.clicked.connect(self._load_assessments)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Atividade", "Data", "Avaliador", "Score RULA",
            "Nível de Risco", "Prioridade", "Acompanhamento", "Recomendações"
        ])
        self.table.resizeColumnsToContents()

        layout.addWidget(self.table)

        # Summary
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

    def _load_assessments(self):
        """Carrega avaliações na tabela"""
        assessments = self.storage.get_all_postural_assessments()
        self.table.setRowCount(len(assessments))

        critical = 0
        urgent = 0
        investigation = 0
        acceptable = 0

        for row, assess in enumerate(assessments):
            activity = self.storage.get_activity(assess.activity_id)
            activity_name = activity.name if activity else "N/A"

            priority_text = assess.interventions_priority
            if assess.rula_final_score <= 2:
                acceptable += 1
            elif assess.rula_final_score <= 4:
                investigation += 1
                priority_text = "🟡 " + priority_text
            elif assess.rula_final_score <= 6:
                urgent += 1
                priority_text = "🟠 " + priority_text
            else:
                critical += 1
                priority_text = "🔴 " + priority_text

            followup = "✓" if assess.follow_up_needed else "✗"
            recom_preview = (assess.recommendations[0][:40] if assess.recommendations else "")

            self.table.setItem(row, 0, QTableWidgetItem(activity_name))
            self.table.setItem(row, 1, QTableWidgetItem(assess.assessment_date))
            self.table.setItem(row, 2, QTableWidgetItem(assess.assessor))
            self.table.setItem(row, 3, QTableWidgetItem(str(assess.rula_final_score)))
            self.table.setItem(row, 4, QTableWidgetItem(assess.risk_level.value))
            self.table.setItem(row, 5, QTableWidgetItem(priority_text))
            self.table.setItem(row, 6, QTableWidgetItem(followup))
            self.table.setItem(row, 7, QTableWidgetItem(recom_preview))

            # Color by risk
            if critical > 0 and assess.rula_final_score >= 7:
                for col in range(8):
                    self.table.item(row, col).setBackground(QColor(255, 150, 150))
            elif urgent > 0 and assess.rula_final_score >= 5:
                for col in range(8):
                    self.table.item(row, col).setBackground(QColor(255, 220, 150))

        # Update summary
        summary = (
            f"Total: {len(assessments)} | Aceitável: {acceptable} | "
            f"Investigação: {investigation} | Urgente: {urgent} | Crítica: {critical}"
        )
        self.summary_label.setText(summary)

    def _add_assessment(self):
        if not self.storage.get_all_activities():
            QMessageBox.warning(self, "Aviso", "Cadastre atividades antes de fazer avaliação ergonômica")
            return

        dialog = PosturalAssessmentDialog(self, self.storage)
        if dialog.exec() == QDialog.Accepted:
            assessment = dialog.get_assessment()
            self.storage.save_postural_assessment(assessment)
            self._load_assessments()

    def _edit_assessment(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma avaliação para editar")
            return

        # Find assessment by activity name
        activity_name = self.table.item(current_row, 0).text()
        assess = None
        for a in self.storage.get_all_postural_assessments():
            activity = self.storage.get_activity(a.activity_id)
            if activity and activity.name == activity_name:
                assess = a
                break

        if assess:
            dialog = PosturalAssessmentDialog(self, self.storage, assess)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_assessment()
                self.storage.save_postural_assessment(updated)
                self._load_assessments()

    def _delete_assessment(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma avaliação para remover")
            return

        activity_name = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", f"Remover avaliação de '{activity_name}'?")

        if reply == QMessageBox.Yes:
            for a in self.storage.get_all_postural_assessments():
                activity = self.storage.get_activity(a.activity_id)
                if activity and activity.name == activity_name:
                    self.storage.delete_postural_assessment(a.id)
                    self._load_assessments()
                    break
