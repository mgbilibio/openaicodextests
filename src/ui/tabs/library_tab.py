"""Aba para Biblioteca de Normas com Busca FTS5"""

import json
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QObject, Slot
from PySide6.QtWebEngineCore import QWebEngineScript
from src.library.norms_library import NormsLibrary
from src.library.populate_norms import populate_norms


class SearchBridge(QObject):
    """Bridge entre JavaScript e Python"""

    def __init__(self, library: NormsLibrary):
        super().__init__()
        self.library = library

    @Slot(str, int, int)
    def search(self, query: str, words_before: int, words_after: int):
        """Realiza busca e retorna resultados"""
        try:
            # Buscar nos normas
            results = self.library.search(query, words_before, words_after)

            # Converter para JSON
            results_json = []
            for result in results:
                results_json.append({
                    'norm_id': result.norm_id,
                    'norm_title': result.norm_title,
                    'section': result.section,
                    'article': result.article,
                    'excerpt': result.excerpt
                })

            # Passar para JavaScript
            results_str = json.dumps(results_json)
            self.window.page().runJavaScript(
                f"displayResults({results_str}, '{query}')"
            )

        except Exception as e:
            error_msg = str(e).replace("'", "\\'")
            self.window.page().runJavaScript(
                f"displayError('{error_msg}')"
            )

    def set_window(self, window):
        """Define a janela web"""
        self.window = window


class LibraryTab(QWidget):
    def __init__(self, data_dir: Path):
        super().__init__()
        self.data_dir = data_dir
        self.library_dir = data_dir / "library"
        self.db_path = self.library_dir / "norms.db"

        # Inicializar biblioteca
        self._init_library()

        # Setup UI
        self._setup_ui()

    def _init_library(self):
        """Inicializa banco de dados com normas"""
        self.library_dir.mkdir(exist_ok=True)

        # Se banco não existe, popular com normas
        if not self.db_path.exists():
            populate_norms(self.db_path)

        self.library = NormsLibrary(self.db_path)

    def _setup_ui(self):
        """Setup interface com WebView"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Criar QWebEngineView
        self.web_view = QWebEngineView()

        # Criar bridge para comunicação Python-JS
        self.bridge = SearchBridge(self.library)
        self.web_view.page().javaScriptConsoleMessage

        # Registrar objeto bridge
        self.web_view.page().profiles[0].defaultProfile.downloadRequested.connect(self._on_download)

        # Carregar página HTML
        html_path = Path(__file__).parent.parent / "library" / "search_page.html"
        self.web_view.setUrl(QUrl.fromLocalFile(str(html_path)))

        # Injetar script para registrar bridge
        script = QWebEngineScript()
        script.setSourceCode("""
            window.searchBridge = new QWebChannel.objects.searchBridge;
        """)
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        self.web_view.page().scripts().insert(script)

        # Adicionar bridge manualmente via contexto
        self.web_view.page().setWebChannel(self._get_web_channel())

        layout.addWidget(self.web_view)
        self.setLayout(layout)

        # Buscar estatísticas e passar para JavaScript
        self._load_stats()

    def _get_web_channel(self):
        """Cria QWebChannel para comunicação"""
        from PySide6.QtWebChannel import QWebChannel

        channel = QWebChannel()
        self.bridge.set_window(self.web_view)
        channel.registerObject('searchBridge', self.bridge)
        return channel

    def _load_stats(self):
        """Carrega e exibe estatísticas da biblioteca"""
        try:
            stats = self.library.get_statistics()

            # Converter para JSON e passar para JavaScript
            stats_json = json.dumps(stats)
            self.web_view.page().runJavaScript(
                f"updateStats({stats_json})"
            )
        except Exception as e:
            print(f"Erro ao carregar estatísticas: {e}")

    def _on_download(self, download):
        """Handle downloads"""
        pass
