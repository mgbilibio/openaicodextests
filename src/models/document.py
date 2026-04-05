"""Modelos para geração de documentos"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CompanyInfo:
    """Informações da empresa"""
    name: str
    cnpj: str
    address: str
    city: str
    state: str
    phone: str
    email: Optional[str] = None
    responsible: Optional[str] = None
    responsible_role: Optional[str] = None


@dataclass
class DocumentMetadata:
    """Metadados de um documento"""
    title: str
    version: str
    created_at: datetime
    created_by: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    company_info: Optional[CompanyInfo] = None


@dataclass
class RiskReport:
    """Relatório de análise de riscos (PGR / Laudo)"""
    metadata: DocumentMetadata
    scope: str  # Descrição do escopo
    methodology: str  # "ISO 31010"
    environments_assessed: List[str]
    total_hazards: int
    total_risks: int
    risks_by_level: dict  # {"Insignificante": 0, "Aceitável": 5, ...}
    recommendations: List[str]
    follow_up_date: Optional[str] = None
