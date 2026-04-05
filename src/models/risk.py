"""Modelos de dados para análise de riscos ISO 31010"""

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Optional, List
from datetime import datetime


class RiskCategory(Enum):
    """Categorias de riscos conforme NRs"""
    FISICO = "Físico"
    QUIMICO = "Químico"
    BIOLOGICO = "Biológico"
    ERGONOMICO = "Ergonômico"
    PSICOSSOCIAL = "Psicossocial"
    MECANICO = "Mecânico"
    ELETRICO = "Elétrico"
    TERMICO = "Térmico"
    RADIACAO = "Radiação"
    PRESSAO = "Pressão"


class RiskSeverity(Enum):
    """Níveis de severidade (ISO 31010)"""
    INSIGNIFICANTE = "Insignificante"
    MENOR = "Menor"
    MODERADO = "Moderado"
    MAIOR = "Maior"
    CATASTROFICO = "Catastrófico"


class RiskProbability(Enum):
    """Níveis de probabilidade (ISO 31010)"""
    RARO = "Raro"
    IMPROVAVEL = "Improvável"
    POSSIVEL = "Possível"
    PROVAVEL = "Provável"
    MUITO_PROVAVEL = "Muito Provável"


@dataclass
class Hazard:
    """Perigo identificado no ambiente"""
    id: str
    category: RiskCategory
    description: str
    location: str
    exposed_people: str  # Descrição de quem está exposto
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class RiskAssessment:
    """Avaliação de risco com metodologia ISO 31010"""
    id: str
    hazard_id: str
    severity: RiskSeverity
    probability: RiskProbability
    control_measures: str
    residual_severity: Optional[RiskSeverity] = None
    residual_probability: Optional[RiskProbability] = None
    responsible: Optional[str] = None
    deadline: Optional[str] = None
    status: str = "Aberto"  # Aberto, Em Andamento, Concluído
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def get_risk_level(self) -> str:
        """Calcula nível de risco baseado em matriz (severidade x probabilidade)"""
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

        score = severity_scores[self.severity] * probability_scores[self.probability]

        if score <= 3:
            return "Insignificante"
        elif score <= 6:
            return "Aceitável"
        elif score <= 12:
            return "Moderado"
        elif score <= 16:
            return "Substancial"
        else:
            return "Intolerável"

    def to_dict(self):
        return asdict(self)


@dataclass
class WorkActivity:
    """Atividade ou tarefa executada no ambiente"""
    id: str
    name: str
    description: str
    environment_id: str
    workers: int
    frequency: str  # Contínuo, Intermitente, Ocasional
    hazards: List[str] = field(default_factory=list)  # IDs dos perigos
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class WorkEnvironment:
    """Ambiente ou setor de trabalho"""
    id: str
    name: str
    description: str
    location: str
    type: str  # Escritório, Produção, Obra, etc.
    workers_count: int
    activities: List[str] = field(default_factory=list)  # IDs das atividades
    hazards: List[str] = field(default_factory=list)  # IDs dos perigos
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
