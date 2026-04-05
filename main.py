#!/usr/bin/env python3
"""
App de Gestão de Riscos e Segurança do Trabalho
Baseado em ISO 31010 e NRs Brasileiras
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Configurar diretórios de dados
    data_dir = Path.home() / ".occupational_health_app"
    data_dir.mkdir(exist_ok=True)

    window = MainWindow(data_dir)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
