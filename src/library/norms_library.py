"""Módulo de Biblioteca de Normas com busca FTS5"""

import sqlite3
import unicodedata
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Resultado de busca em normas"""
    norm_id: str
    norm_title: str
    section: str
    article: str
    content: str
    excerpt: str  # Trecho com contexto
    word_before: int
    word_after: int


class NormsLibrary:
    """Biblioteca de normas brasileiras com busca FTS5"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Inicializa banco de dados com FTS5"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de metadados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS norms (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                version TEXT,
                publication_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de conteúdo com FTS5
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS norm_content_fts
            USING fts5(
                norm_id UNINDEXED,
                section,
                article,
                content,
                content='norm_content',
                content_rowid='rowid'
            )
        ''')

        # Tabela auxiliar para armazenar conteúdo original
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS norm_content (
                rowid INTEGER PRIMARY KEY,
                norm_id TEXT,
                section TEXT,
                article TEXT,
                content TEXT,
                FOREIGN KEY(norm_id) REFERENCES norms(id)
            )
        ''')

        conn.commit()
        conn.close()

    def _normalize_text(self, text: str) -> str:
        """Normaliza texto removendo acentos e convertendo para minúsculas"""
        # Remove acentos
        nfd = unicodedata.normalize('NFD', text)
        normalized = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
        # Minúsculas
        return normalized.lower()

    def add_norm(self, norm_id: str, title: str, description: str = "",
                 version: str = "", publication_date: str = "") -> bool:
        """Adiciona uma norma ao banco"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO norms
                (id, title, description, version, publication_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (norm_id, title, description, version, publication_date))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao adicionar norma: {e}")
            return False

    def add_content(self, norm_id: str, section: str, article: str,
                   content: str) -> bool:
        """Adiciona conteúdo de uma norma para indexação"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Inserir na tabela original
            cursor.execute('''
                INSERT INTO norm_content (norm_id, section, article, content)
                VALUES (?, ?, ?, ?)
            ''', (norm_id, section, article, content))

            # Normalizar e inserir no FTS5
            normalized_content = self._normalize_text(content)
            cursor.execute('''
                INSERT INTO norm_content_fts (norm_id, section, article, content)
                VALUES (?, ?, ?, ?)
            ''', (norm_id, section, article, normalized_content))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao adicionar conteúdo: {e}")
            return False

    def search(self, query: str, words_before: int = 200,
               words_after: int = 200) -> List[SearchResult]:
        """Busca em normas e retorna trechos com contexto"""
        try:
            # Normalizar query
            normalized_query = self._normalize_text(query)

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Busca FTS5 com normalização
            cursor.execute('''
                SELECT DISTINCT
                    nc.norm_id,
                    n.title,
                    nc.section,
                    nc.article,
                    nc.content
                FROM norm_content_fts ncf
                JOIN norm_content nc ON ncf.rowid = nc.rowid
                JOIN norms n ON nc.norm_id = n.id
                WHERE norm_content_fts MATCH ?
                LIMIT 20
            ''', (normalized_query,))

            results = []
            for row in cursor.fetchall():
                # Extrair trecho com contexto
                excerpt = self._extract_excerpt(
                    row['content'],
                    normalized_query,
                    words_before,
                    words_after
                )

                result = SearchResult(
                    norm_id=row['norm_id'],
                    norm_title=row['title'],
                    section=row['section'],
                    article=row['article'],
                    content=row['content'],
                    excerpt=excerpt,
                    word_before=words_before,
                    word_after=words_after
                )
                results.append(result)

            conn.close()
            return results

        except Exception as e:
            print(f"Erro ao buscar: {e}")
            return []

    def _extract_excerpt(self, content: str, query: str,
                        words_before: int, words_after: int) -> str:
        """Extrai trecho com N palavras antes e depois do termo"""
        words = content.split()
        query_words = query.split()

        # Encontrar a posição do termo na lista de palavras
        match_idx = -1
        for i in range(len(words) - len(query_words) + 1):
            if self._normalize_text(' '.join(words[i:i+len(query_words)])) == query:
                match_idx = i
                break

        if match_idx == -1:
            # Se não encontrar match exato, retornar primeiras X palavras
            return ' '.join(words[:min(words_before + len(query_words) + words_after, len(words))]) + "..."

        # Calcular índices
        start_idx = max(0, match_idx - words_before)
        end_idx = min(len(words), match_idx + len(query_words) + words_after)

        # Extrair trecho
        excerpt_words = words[start_idx:end_idx]
        excerpt = ' '.join(excerpt_words)

        # Adicionar reticências se necessário
        if start_idx > 0:
            excerpt = "..." + excerpt
        if end_idx < len(words):
            excerpt = excerpt + "..."

        # Destacar o termo de busca
        for query_word in query_words:
            pattern_normal = query_word
            for word in excerpt_words:
                if self._normalize_text(word) == self._normalize_text(query_word):
                    excerpt = excerpt.replace(word, f"<mark>{word}</mark>", 1)

        return excerpt

    def get_all_norms(self) -> List[Dict]:
        """Retorna todas as normas cadastradas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM norms ORDER BY title')
            norms = [dict(row) for row in cursor.fetchall()]

            conn.close()
            return norms
        except Exception as e:
            print(f"Erro ao buscar normas: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Retorna estatísticas da biblioteca"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM norms')
            norm_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM norm_content')
            content_count = cursor.fetchone()[0]

            cursor.execute('SELECT SUM(LENGTH(content)) FROM norm_content')
            total_size = cursor.fetchone()[0] or 0

            conn.close()

            return {
                'total_norms': norm_count,
                'total_articles': content_count,
                'total_chars': total_size,
                'total_words': total_size // 5  # Aproximado
            }
        except Exception as e:
            print(f"Erro ao calcular estatísticas: {e}")
            return {}
