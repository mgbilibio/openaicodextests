"""Janela principal da aplicação"""

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel
)
from PySide6.QtCore import Qt

from src.ui.tabs.environment_tab import EnvironmentTab
from src.ui.tabs.hazard_tab import HazardTab
from src.ui.tabs.activity_tab import ActivityTab
from src.ui.tabs.risk_assessment_tab import RiskAssessmentTab
from src.ui.tabs.control_plan_tab import ControlPlanTab
from src.ui.tabs.equipment_tab import EquipmentTab
from src.ui.tabs.ergonomic_tab import ErgonomicTab
from src.ui.tabs.report_tab import ReportTab
from src.database.storage import DataStorage


class MainWindow(QMainWindow):
    def __init__(self, data_dir: Path):
        super().__init__()
        self.setWindowTitle("Gestão de Riscos e Segurança do Trabalho")
        self.setGeometry(100, 100, 1200, 700)

        self.data_dir = data_dir
        self.storage = DataStorage(data_dir)

        self._setup_ui()

    def _setup_ui(self):
        """Configura a interface principal"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Header
        header = QLabel("Sistema de Gestão de Riscos - ISO 31010 / NRs Brasileiras")
        header.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(EnvironmentTab(self.storage), "Ambientes")
        tabs.addTab(HazardTab(self.storage), "Perigos")
        tabs.addTab(ActivityTab(self.storage), "Atividades")
        tabs.addTab(RiskAssessmentTab(self.storage), "Avaliação de Riscos")
        tabs.addTab(ControlPlanTab(self.storage), "Plano de Ações")
        tabs.addTab(EquipmentTab(self.storage), "Ferramentas e EPIs")
        tabs.addTab(ErgonomicTab(self.storage), "Análise Postural")
        tabs.addTab(ReportTab(self.storage), "Gerar Documentos")

        layout.addWidget(tabs)

        # Footer
        footer_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar Dados")
        save_btn.clicked.connect(self.storage.save_all)
        footer_layout.addStretch()
        footer_layout.addWidget(save_btn)

        layout.addLayout(footer_layout)

        central_widget.setLayout(layout)
