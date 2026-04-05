"""Aba para gerenciar Ferramentas e EPIs"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QTabWidget, QDialog, QLineEdit, QComboBox,
    QTextEdit, QFormLayout, QMessageBox, QSpinBox, QDateEdit,
    QDoubleSpinBox, QLabel
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from src.models.equipment import (
    EPI, Tool, EPIAssignment,
    EPICategory, ToolCategory, InspectionStatus
)
from src.database.storage import DataStorage
import uuid
from datetime import datetime, date


# ===== EPI Dialog =====

class EPIDialog(QDialog):
    """Diálogo para adicionar/editar EPIs"""

    def __init__(self, parent=None, storage=None, epi=None):
        super().__init__(parent)
        self.epi = epi
        self.storage = storage
        self.setWindowTitle("Equipamento de Proteção Individual")
        self.setGeometry(100, 100, 600, 600)
        self._setup_ui()

        if epi:
            self._load_epi(epi)

    def _setup_ui(self):
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems([c.value for c in EPICategory])

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(60)

        self.ca_number = QLineEdit()
        self.ca_number.setPlaceholderText("Ex: CA 12.345")

        self.ca_validity = QDateEdit()
        self.ca_validity.setDate(QDate.currentDate().addYears(3))

        self.manufacturer = QLineEdit()
        self.protection_level = QComboBox()
        self.protection_level.addItems(["Alto", "Médio", "Baixo"])

        self.cost_unit = QDoubleSpinBox()
        self.cost_unit.setMaximum(9999.99)
        self.cost_unit.setSuffix(" R$")

        self.quantity = QSpinBox()
        self.quantity.setMaximum(10000)
        self.quantity.setValue(0)

        self.reorder_point = QSpinBox()
        self.reorder_point.setMaximum(10000)
        self.reorder_point.setValue(10)

        self.supplier = QLineEdit()
        self.supplier_contact = QLineEdit()
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(60)

        layout.addRow("Nome do EPI:", self.name_input)
        layout.addRow("Categoria:", self.category_combo)
        layout.addRow("Descrição:", self.description_input)
        layout.addRow("Número CA:", self.ca_number)
        layout.addRow("Validade CA:", self.ca_validity)
        layout.addRow("Fabricante:", self.manufacturer)
        layout.addRow("Nível de Proteção:", self.protection_level)
        layout.addRow("Custo Unitário:", self.cost_unit)
        layout.addRow("Quantidade em Estoque:", self.quantity)
        layout.addRow("Ponto de Reposição:", self.reorder_point)
        layout.addRow("Fornecedor:", self.supplier)
        layout.addRow("Contato Fornecedor:", self.supplier_contact)
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

    def _load_epi(self, epi):
        """Carrega dados do EPI no formulário"""
        self.name_input.setText(epi.name)
        self.category_combo.setCurrentText(epi.category.value)
        self.description_input.setText(epi.description)
        self.ca_number.setText(epi.ca_number)

        validity = datetime.strptime(epi.ca_validity_date, '%Y-%m-%d').date()
        self.ca_validity.setDate(QDate(validity.year, validity.month, validity.day))

        self.manufacturer.setText(epi.manufacturer)
        self.protection_level.setCurrentText(epi.protection_level)
        self.cost_unit.setValue(epi.cost_unit)
        self.quantity.setValue(epi.quantity_in_stock)
        self.reorder_point.setValue(epi.reorder_point)
        self.supplier.setText(epi.supplier)
        if epi.supplier_contact:
            self.supplier_contact.setText(epi.supplier_contact)
        self.notes.setText(epi.notes)

    def get_epi(self):
        """Retorna objeto EPI"""
        qdate = self.ca_validity.date()
        validity_str = f"{qdate.year}-{qdate.month:02d}-{qdate.day:02d}"

        if self.epi:
            self.epi.name = self.name_input.text()
            self.epi.category = EPICategory(self.category_combo.currentText())
            self.epi.description = self.description_input.toPlainText()
            self.epi.ca_number = self.ca_number.text()
            self.epi.ca_validity_date = validity_str
            self.epi.manufacturer = self.manufacturer.text()
            self.epi.protection_level = self.protection_level.currentText()
            self.epi.cost_unit = self.cost_unit.value()
            self.epi.quantity_in_stock = self.quantity.value()
            self.epi.reorder_point = self.reorder_point.value()
            self.epi.supplier = self.supplier.text()
            self.epi.supplier_contact = self.supplier_contact.text() or None
            self.epi.notes = self.notes.toPlainText()
            return self.epi
        else:
            return EPI(
                id=str(uuid.uuid4()),
                name=self.name_input.text(),
                category=EPICategory(self.category_combo.currentText()),
                description=self.description_input.toPlainText(),
                ca_number=self.ca_number.text(),
                ca_validity_date=validity_str,
                manufacturer=self.manufacturer.text(),
                protection_level=self.protection_level.currentText(),
                cost_unit=self.cost_unit.value(),
                quantity_in_stock=self.quantity.value(),
                reorder_point=self.reorder_point.value(),
                supplier=self.supplier.text(),
                supplier_contact=self.supplier_contact.text() or None,
                notes=self.notes.toPlainText()
            )


# ===== Tools Dialog =====

class ToolDialog(QDialog):
    """Diálogo para adicionar/editar ferramentas"""

    def __init__(self, parent=None, storage=None, tool=None):
        super().__init__(parent)
        self.tool = tool
        self.storage = storage
        self.setWindowTitle("Ferramenta/Equipamento")
        self.setGeometry(100, 100, 550, 500)
        self._setup_ui()

        if tool:
            self._load_tool(tool)

    def _setup_ui(self):
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems([c.value for c in ToolCategory])

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(60)

        self.location_input = QLineEdit()
        self.responsible = QLineEdit()
        self.serial_number = QLineEdit()

        self.last_inspection = QDateEdit()
        self.last_inspection.setDate(QDate.currentDate())

        self.next_inspection = QDateEdit()
        self.next_inspection.setDate(QDate.currentDate().addMonths(6))

        self.inspection_status = QComboBox()
        self.inspection_status.addItems([s.value for s in InspectionStatus])

        self.inspector = QLineEdit()
        self.maintenance_interval = QSpinBox()
        self.maintenance_interval.setMaximum(3650)
        self.maintenance_interval.setValue(365)
        self.maintenance_interval.setSuffix(" dias")

        self.notes = QTextEdit()
        self.notes.setMaximumHeight(60)

        layout.addRow("Nome da Ferramenta:", self.name_input)
        layout.addRow("Categoria:", self.category_combo)
        layout.addRow("Descrição:", self.description_input)
        layout.addRow("Localização:", self.location_input)
        layout.addRow("Responsável:", self.responsible)
        layout.addRow("Número de Série:", self.serial_number)
        layout.addRow("Última Inspeção:", self.last_inspection)
        layout.addRow("Próxima Inspeção:", self.next_inspection)
        layout.addRow("Status da Inspeção:", self.inspection_status)
        layout.addRow("Inspetor:", self.inspector)
        layout.addRow("Intervalo de Manutenção:", self.maintenance_interval)
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

    def _load_tool(self, tool):
        """Carrega dados da ferramenta"""
        self.name_input.setText(tool.name)
        self.category_combo.setCurrentText(tool.category.value)
        self.description_input.setText(tool.description)
        self.location_input.setText(tool.location)
        self.responsible.setText(tool.responsible)
        if tool.serial_number:
            self.serial_number.setText(tool.serial_number)

        last = datetime.strptime(tool.last_inspection_date, '%Y-%m-%d').date()
        self.last_inspection.setDate(QDate(last.year, last.month, last.day))

        nxt = datetime.strptime(tool.next_inspection_date, '%Y-%m-%d').date()
        self.next_inspection.setDate(QDate(nxt.year, nxt.month, nxt.day))

        self.inspection_status.setCurrentText(tool.inspection_status.value)
        if tool.inspector:
            self.inspector.setText(tool.inspector)

        self.maintenance_interval.setValue(tool.maintenance_interval_days)
        self.notes.setText(tool.notes)

    def get_tool(self):
        """Retorna objeto Tool"""
        last_qdate = self.last_inspection.date()
        nxt_qdate = self.next_inspection.date()

        last_str = f"{last_qdate.year}-{last_qdate.month:02d}-{last_qdate.day:02d}"
        nxt_str = f"{nxt_qdate.year}-{nxt_qdate.month:02d}-{nxt_qdate.day:02d}"

        if self.tool:
            self.tool.name = self.name_input.text()
            self.tool.category = ToolCategory(self.category_combo.currentText())
            self.tool.description = self.description_input.toPlainText()
            self.tool.location = self.location_input.text()
            self.tool.responsible = self.responsible.text()
            self.tool.serial_number = self.serial_number.text() or None
            self.tool.last_inspection_date = last_str
            self.tool.next_inspection_date = nxt_str
            self.tool.inspection_status = InspectionStatus(self.inspection_status.currentText())
            self.tool.inspector = self.inspector.text() or None
            self.tool.maintenance_interval_days = self.maintenance_interval.value()
            self.tool.notes = self.notes.toPlainText()
            return self.tool
        else:
            return Tool(
                id=str(uuid.uuid4()),
                name=self.name_input.text(),
                category=ToolCategory(self.category_combo.currentText()),
                description=self.description_input.toPlainText(),
                location=self.location_input.text(),
                responsible=self.responsible.text(),
                last_inspection_date=last_str,
                next_inspection_date=nxt_str,
                inspection_status=InspectionStatus(self.inspection_status.currentText()),
                inspector=self.inspector.text() or None,
                maintenance_interval_days=self.maintenance_interval.value(),
                notes=self.notes.toPlainText(),
                serial_number=self.serial_number.text() or None
            )


# ===== Main Equipment Tab =====

class EquipmentTab(QWidget):
    def __init__(self, storage: DataStorage):
        super().__init__()
        self.storage = storage
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Tabs for EPIs and Tools
        tabs = QTabWidget()
        tabs.addTab(self._create_epi_tab(), "EPIs")
        tabs.addTab(self._create_tools_tab(), "Ferramentas")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def _create_epi_tab(self):
        """Cria aba de EPIs"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Info
        info = QLabel("Cadastro e gestão de Equipamentos de Proteção Individual")
        layout.addWidget(info)

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar EPI")
        edit_btn = QPushButton("Editar Selecionado")
        delete_btn = QPushButton("Remover Selecionado")

        add_btn.clicked.connect(self._add_epi)
        edit_btn.clicked.connect(self._edit_epi)
        delete_btn.clicked.connect(self._delete_epi)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.epi_table = QTableWidget()
        self.epi_table.setColumnCount(9)
        self.epi_table.setHorizontalHeaderLabels([
            "Nome", "Categoria", "CA", "Validade", "Nível", "Estoque",
            "Reposição", "Custo Unit.", "Status"
        ])
        self.epi_table.resizeColumnsToContents()

        layout.addWidget(self.epi_table)
        widget.setLayout(layout)

        self._load_epis()
        return widget

    def _create_tools_tab(self):
        """Cria aba de Ferramentas"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Info
        info = QLabel("Cadastro e inspeção de ferramentas e equipamentos de trabalho")
        layout.addWidget(info)

        # Buttons
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Adicionar Ferramenta")
        edit_btn = QPushButton("Editar Selecionada")
        delete_btn = QPushButton("Remover Selecionada")

        add_btn.clicked.connect(self._add_tool)
        edit_btn.clicked.connect(self._edit_tool)
        delete_btn.clicked.connect(self._delete_tool)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Table
        self.tools_table = QTableWidget()
        self.tools_table.setColumnCount(8)
        self.tools_table.setHorizontalHeaderLabels([
            "Nome", "Categoria", "Localização", "Responsável",
            "Status Inspeção", "Última Inspeção", "Próxima Inspeção", "Número Série"
        ])
        self.tools_table.resizeColumnsToContents()

        layout.addWidget(self.tools_table)
        widget.setLayout(layout)

        self._load_tools()
        return widget

    def _load_epis(self):
        """Carrega EPIs na tabela"""
        epis = self.storage.get_all_epis()
        self.epi_table.setRowCount(len(epis))

        for row, epi in enumerate(epis):
            status = ""
            if epi.is_ca_expired():
                status = "🔴 CA Vencida"
            elif epi.is_low_stock():
                status = "🟠 Estoque Baixo"
            else:
                status = "🟢 OK"

            self.epi_table.setItem(row, 0, QTableWidgetItem(epi.name))
            self.epi_table.setItem(row, 1, QTableWidgetItem(epi.category.value))
            self.epi_table.setItem(row, 2, QTableWidgetItem(epi.ca_number))
            self.epi_table.setItem(row, 3, QTableWidgetItem(epi.ca_validity_date))
            self.epi_table.setItem(row, 4, QTableWidgetItem(epi.protection_level))
            self.epi_table.setItem(row, 5, QTableWidgetItem(str(epi.quantity_in_stock)))
            self.epi_table.setItem(row, 6, QTableWidgetItem(str(epi.reorder_point)))
            self.epi_table.setItem(row, 7, QTableWidgetItem(f"R$ {epi.cost_unit:.2f}"))
            self.epi_table.setItem(row, 8, QTableWidgetItem(status))

            if "Vencida" in status:
                for col in range(9):
                    self.epi_table.item(row, col).setBackground(QColor(255, 200, 200))
            elif "Baixo" in status:
                for col in range(9):
                    self.epi_table.item(row, col).setBackground(QColor(255, 255, 200))

    def _load_tools(self):
        """Carrega ferramentas na tabela"""
        tools = self.storage.get_all_tools()
        self.tools_table.setRowCount(len(tools))

        for row, tool in enumerate(tools):
            status_text = tool.get_inspection_status_text()

            self.tools_table.setItem(row, 0, QTableWidgetItem(tool.name))
            self.tools_table.setItem(row, 1, QTableWidgetItem(tool.category.value))
            self.tools_table.setItem(row, 2, QTableWidgetItem(tool.location))
            self.tools_table.setItem(row, 3, QTableWidgetItem(tool.responsible))
            self.tools_table.setItem(row, 4, QTableWidgetItem(status_text))
            self.tools_table.setItem(row, 5, QTableWidgetItem(tool.last_inspection_date))
            self.tools_table.setItem(row, 6, QTableWidgetItem(tool.next_inspection_date))
            self.tools_table.setItem(row, 7, QTableWidgetItem(tool.serial_number or "N/A"))

            if "Vencida" in status_text or "Com Defeito" in status_text:
                for col in range(8):
                    self.tools_table.item(row, col).setBackground(QColor(255, 200, 200))
            elif "Precisa Reparo" in status_text:
                for col in range(8):
                    self.tools_table.item(row, col).setBackground(QColor(255, 255, 200))

    def _add_epi(self):
        dialog = EPIDialog(self, self.storage)
        if dialog.exec() == QDialog.Accepted:
            epi = dialog.get_epi()
            self.storage.save_epi(epi)
            self._load_epis()

    def _edit_epi(self):
        current_row = self.epi_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um EPI para editar")
            return

        epi_name = self.epi_table.item(current_row, 0).text()
        epi = None
        for e in self.storage.get_all_epis():
            if e.name == epi_name:
                epi = e
                break

        if epi:
            dialog = EPIDialog(self, self.storage, epi)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_epi()
                self.storage.save_epi(updated)
                self._load_epis()

    def _delete_epi(self):
        current_row = self.epi_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um EPI para remover")
            return

        epi_name = self.epi_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", f"Remover EPI '{epi_name}'?")

        if reply == QMessageBox.Yes:
            for e in self.storage.get_all_epis():
                if e.name == epi_name:
                    self.storage.delete_epi(e.id)
                    self._load_epis()
                    break

    def _add_tool(self):
        dialog = ToolDialog(self, self.storage)
        if dialog.exec() == QDialog.Accepted:
            tool = dialog.get_tool()
            self.storage.save_tool(tool)
            self._load_tools()

    def _edit_tool(self):
        current_row = self.tools_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma ferramenta para editar")
            return

        tool_name = self.tools_table.item(current_row, 0).text()
        tool = None
        for t in self.storage.get_all_tools():
            if t.name == tool_name:
                tool = t
                break

        if tool:
            dialog = ToolDialog(self, self.storage, tool)
            if dialog.exec() == QDialog.Accepted:
                updated = dialog.get_tool()
                self.storage.save_tool(updated)
                self._load_tools()

    def _delete_tool(self):
        current_row = self.tools_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma ferramenta para remover")
            return

        tool_name = self.tools_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirmar", f"Remover ferramenta '{tool_name}'?")

        if reply == QMessageBox.Yes:
            for t in self.storage.get_all_tools():
                if t.name == tool_name:
                    self.storage.delete_tool(t.id)
                    self._load_tools()
                    break
