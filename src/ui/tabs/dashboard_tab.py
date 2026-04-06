"""Aba de Dashboard com gráficos e estatísticas"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QComboBox, QPushButton, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from src.database.storage import DataStorage
from src.analytics.risk_analytics import RiskAnalytics


class DashboardTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self.analytics = RiskAnalytics(storage)

        # Configurar estilo
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = '#f8f9fa'
        plt.rcParams['font.family'] = 'Segoe UI'
        plt.rcParams['font.size'] = 9

        self._setup_ui()
        self._update_dashboard()

    def _setup_ui(self):
        """Setup interface principal"""
        main_layout = QVBoxLayout()

        # Header com título e filtros
        header = QHBoxLayout()
        title = QLabel("📊 Dashboard de Riscos")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)

        header.addWidget(title)
        header.addStretch()

        # Botão de atualizar
        refresh_btn = QPushButton("🔄 Atualizar")
        refresh_btn.clicked.connect(self._update_dashboard)
        header.addWidget(refresh_btn)

        main_layout.addLayout(header)

        # Sumário executivo (KPIs)
        kpi_layout = self._create_kpi_section()
        main_layout.addLayout(kpi_layout)

        # Gráficos em grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        # Gráfico 1: Distribuição de Riscos (Pie)
        self.fig_distribution = Figure(figsize=(4, 3), dpi=100)
        self.canvas_distribution = FigureCanvasQTAgg(self.fig_distribution)
        scroll_layout.addWidget(QLabel("Distribuição de Riscos"), 0, 0)
        scroll_layout.addWidget(self.canvas_distribution, 1, 0)

        # Gráfico 2: Riscos por Severidade (Bar)
        self.fig_severity = Figure(figsize=(4, 3), dpi=100)
        self.canvas_severity = FigureCanvasQTAgg(self.fig_severity)
        scroll_layout.addWidget(QLabel("Riscos por Severidade"), 0, 1)
        scroll_layout.addWidget(self.canvas_severity, 1, 1)

        # Gráfico 3: Riscos por Categoria (Bar)
        self.fig_category = Figure(figsize=(4, 3), dpi=100)
        self.canvas_category = FigureCanvasQTAgg(self.fig_category)
        scroll_layout.addWidget(QLabel("Riscos por Categoria"), 2, 0)
        scroll_layout.addWidget(self.canvas_category, 3, 0)

        # Gráfico 4: Ações Corretivas por Status (Bar)
        self.fig_controls = Figure(figsize=(4, 3), dpi=100)
        self.canvas_controls = FigureCanvasQTAgg(self.fig_controls)
        scroll_layout.addWidget(QLabel("Ações Corretivas por Status"), 2, 1)
        scroll_layout.addWidget(self.canvas_controls, 3, 1)

        # Gráfico 5: Matriz de Riscos (Heatmap)
        self.fig_matrix = Figure(figsize=(5, 4), dpi=100)
        self.canvas_matrix = FigureCanvasQTAgg(self.fig_matrix)
        scroll_layout.addWidget(QLabel("Matriz de Riscos (Severidade x Probabilidade)"), 4, 0, 1, 2)
        scroll_layout.addWidget(self.canvas_matrix, 5, 0, 1, 2)

        # Gráfico 6: Riscos por Ambiente (Bar)
        self.fig_environment = Figure(figsize=(5, 3), dpi=100)
        self.canvas_environment = FigureCanvasQTAgg(self.fig_environment)
        scroll_layout.addWidget(QLabel("Riscos por Ambiente"), 6, 0, 1, 2)
        scroll_layout.addWidget(self.canvas_environment, 7, 0, 1, 2)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def _create_kpi_section(self) -> QGridLayout:
        """Cria seção de KPIs"""
        layout = QGridLayout()
        layout.setSpacing(15)

        summary = self.analytics.get_executive_summary()

        kpis = [
            ("🏢 Ambientes", summary['environments'], "#667eea"),
            ("⚠️ Perigos", summary['hazards'], "#764ba2"),
            ("📋 Atividades", summary['activities'], "#f093fb"),
            ("📊 Riscos", summary['assessments'], "#4facfe"),
            ("✅ Ações", summary['controls'], "#43e97b"),
            ("🛡️ EPIs", summary['epis'], "#fa709a"),
            ("🔧 Ferramentas", summary['tools'], "#30cfd0"),
        ]

        row = 0
        col = 0
        for label, value, color in kpis:
            kpi_frame = QFrame()
            kpi_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 8px;
                    padding: 10px;
                }}
            """)

            kpi_layout = QVBoxLayout(kpi_frame)

            title_label = QLabel(label)
            title_font = QFont()
            title_font.setPointSize(10)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet("color: white;")

            value_label = QLabel(str(value))
            value_font = QFont()
            value_font.setPointSize(16)
            value_font.setBold(True)
            value_label.setFont(value_font)
            value_label.setStyleSheet("color: white;")

            kpi_layout.addWidget(title_label)
            kpi_layout.addWidget(value_label)
            kpi_layout.addStretch()

            layout.addWidget(kpi_frame, row, col)

            col += 1
            if col >= 7:
                col = 0
                row += 1

        layout.addStretch()
        return layout

    def _update_dashboard(self):
        """Atualiza todos os gráficos"""
        # Limpar figuras
        for fig in [self.fig_distribution, self.fig_severity, self.fig_category,
                    self.fig_controls, self.fig_matrix, self.fig_environment]:
            fig.clear()

        # Gráfico 1: Distribuição de Riscos
        self._plot_distribution()

        # Gráfico 2: Riscos por Severidade
        self._plot_severity()

        # Gráfico 3: Riscos por Categoria
        self._plot_category()

        # Gráfico 4: Ações Corretivas
        self._plot_controls()

        # Gráfico 5: Matriz de Riscos
        self._plot_risk_matrix()

        # Gráfico 6: Riscos por Ambiente
        self._plot_environment()

        # Atualizar canvas
        for canvas in [self.canvas_distribution, self.canvas_severity,
                       self.canvas_category, self.canvas_controls,
                       self.canvas_matrix, self.canvas_environment]:
            canvas.draw()

    def _plot_distribution(self):
        """Gráfico pizza de distribuição"""
        data = self.analytics.get_risk_distribution()

        if not data:
            return

        colors = ['#43e97b', '#fa709a', '#fee140', '#30cfd0', '#ff6b6b']
        ax = self.fig_distribution.add_subplot(111)

        wedges, texts, autotexts = ax.pie(
            data.values(),
            labels=data.keys(),
            autopct='%1.1f%%',
            colors=colors[:len(data)],
            startangle=90
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        for text in texts:
            text.set_fontsize(9)

        ax.set_title("Distribuição de Riscos", fontweight='bold', pad=20)
        self.fig_distribution.tight_layout()

    def _plot_severity(self):
        """Gráfico de barras por severidade"""
        data = self.analytics.get_risks_by_severity()

        if not data:
            return

        ax = self.fig_severity.add_subplot(111)

        colors = ['#43e97b', '#fee140', '#fa709a', '#ff6b6b', '#c92127']
        bars = ax.bar(range(len(data)), list(data.values()), color=colors[:len(data)])

        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data.keys(), rotation=45, ha='right', fontsize=8)
        ax.set_ylabel("Quantidade", fontsize=9)
        ax.set_title("Riscos por Severidade", fontweight='bold', pad=20)

        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8)

        self.fig_severity.tight_layout()

    def _plot_category(self):
        """Gráfico de barras por categoria"""
        data = self.analytics.get_risks_by_hazard_category()

        if not data:
            return

        ax = self.fig_category.add_subplot(111)

        bars = ax.barh(list(data.keys()), list(data.values()), color='#4facfe')

        ax.set_xlabel("Quantidade", fontsize=9)
        ax.set_title("Riscos por Categoria de Perigo", fontweight='bold', pad=20)
        ax.set_yticklabels(list(data.keys()), fontsize=8)

        # Adicionar valores nas barras
        for i, (bar, value) in enumerate(zip(ax.patches, data.values())):
            ax.text(value, bar.get_y() + bar.get_height()/2.,
                   f' {int(value)}',
                   ha='left', va='center', fontsize=8)

        self.fig_category.tight_layout()

    def _plot_controls(self):
        """Gráfico de ações corretivas"""
        data = self.analytics.get_controls_by_status()

        if not data:
            return

        ax = self.fig_controls.add_subplot(111)

        colors = ['#43e97b', '#4facfe', '#fee140', '#ff6b6b']
        color_map = {
            'Planejado': colors[0],
            'Em Execução': colors[1],
            'Concluído': colors[2],
            'Atrasado': colors[3],
            'Cancelado': '#999'
        }

        bar_colors = [color_map.get(status, '#ccc') for status in data.keys()]
        bars = ax.bar(range(len(data)), list(data.values()), color=bar_colors)

        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data.keys(), rotation=45, ha='right', fontsize=8)
        ax.set_ylabel("Quantidade", fontsize=9)
        ax.set_title("Ações Corretivas por Status", fontweight='bold', pad=20)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8)

        self.fig_controls.tight_layout()

    def _plot_risk_matrix(self):
        """Heatmap de matriz de riscos"""
        matrix = self.analytics.get_risk_matrix()
        severities, probabilities = self.analytics.get_matrix_labels()

        if not matrix or not any(any(row) for row in matrix):
            return

        ax = self.fig_matrix.add_subplot(111)

        # Criar heatmap
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto')

        # Configurar labels
        ax.set_xticks(range(len(probabilities)))
        ax.set_yticks(range(len(severities)))
        ax.set_xticklabels(probabilities, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(severities, fontsize=9)

        ax.set_xlabel("Probabilidade", fontsize=10, fontweight='bold')
        ax.set_ylabel("Severidade", fontsize=10, fontweight='bold')
        ax.set_title("Matriz de Riscos", fontweight='bold', pad=20)

        # Adicionar valores nas células
        for i in range(len(severities)):
            for j in range(len(probabilities)):
                value = int(matrix[i][j])
                if value > 0:
                    text_color = 'white' if matrix[i][j] > max(max(row) for row in matrix) / 2 else 'black'
                    ax.text(j, i, str(value),
                           ha="center", va="center", color=text_color,
                           fontsize=10, fontweight='bold')

        # Colorbar
        cbar = self.fig_matrix.colorbar(im, ax=ax)
        cbar.set_label('Quantidade', fontsize=9)

        self.fig_matrix.tight_layout()

    def _plot_environment(self):
        """Gráfico de riscos por ambiente"""
        data = self.analytics.get_risks_by_environment()

        if not data:
            return

        ax = self.fig_environment.add_subplot(111)

        bars = ax.bar(range(len(data)), list(data.values()), color='#30cfd0')

        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data.keys(), rotation=45, ha='right', fontsize=9)
        ax.set_ylabel("Quantidade de Riscos", fontsize=10)
        ax.set_title("Riscos por Ambiente", fontweight='bold', pad=20)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)

        self.fig_environment.tight_layout()
