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


class ControlType(Enum):
    """Tipos de medidas de controle"""
    ELIMINACAO = "Eliminação"
    SUBSTITUICAO = "Substituição"
    CONTROLE_ADMINISTRATIVO = "Controle Administrativo"
    EPI = "EPE (Equipamento de Proteção Individual)"
    MONITORAMENTO = "Monitoramento/Vigilância"


class ControlStatus(Enum):
    """Status de uma medida de controle"""
    PLANEJADO = "Planejado"
    EM_EXECUCAO = "Em Execução"
    CONCLUIDO = "Concluído"
    ATRASADO = "Atrasado"
    CANCELADO = "Cancelado"


@dataclass
class ControlMeasure:
    """Medida de controle/ação corretiva"""
    id: str
    assessment_id: str  # Link para RiskAssessment

    # Descrição
    description: str
    control_type: ControlType

    # Planejamento
    start_date: str  # formato YYYY-MM-DD
    deadline: str  # formato YYYY-MM-DD
    responsible: str
    alternative_responsible: Optional[str] = None

    # Orçamento
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    supplier: Optional[str] = None

    # Execução
    status: ControlStatus = ControlStatus.PLANEJADO
    progress_percent: int = 0  # 0-100
    completion_date: Optional[str] = None
    notes: str = ""

    # Efetividade
    expected_reduction_percent: int = 0  # Redução esperada de severidade (%)
    actual_reduction_percent: Optional[int] = None
    verified: bool = False
    verified_by: Optional[str] = None
    verified_date: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def is_overdue(self) -> bool:
        """Verifica se está atrasado"""
        if self.status in [ControlStatus.CONCLUIDO, ControlStatus.CANCELADO]:
            return False

        from datetime import datetime as dt
        try:
            deadline = dt.strptime(self.deadline, '%Y-%m-%d').date()
            return deadline < dt.now().date()
        except:
            return False

    def get_priority(self) -> str:
        """Retorna prioridade baseada em data e status"""
        if self.status == ControlStatus.CONCLUIDO:
            return "Concluída"
        if self.is_overdue():
            return "🔴 Crítica (Atrasada)"

        from datetime import datetime as dt, timedelta
        try:
            deadline = dt.strptime(self.deadline, '%Y-%m-%d').date()
            days_remaining = (deadline - dt.now().date()).days

            if days_remaining < 0:
                return "🔴 Crítica"
            elif days_remaining <= 7:
                return "🟠 Alta"
            elif days_remaining <= 30:
                return "🟡 Média"
            else:
                return "🟢 Baixa"
        except:
            return "⚪ Não definida"

    def to_dict(self):
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'description': self.description,
            'control_type': self.control_type.value,
            'start_date': self.start_date,
            'deadline': self.deadline,
            'responsible': self.responsible,
            'alternative_responsible': self.alternative_responsible,
            'estimated_cost': self.estimated_cost,
            'actual_cost': self.actual_cost,
            'supplier': self.supplier,
            'status': self.status.value,
            'progress_percent': self.progress_percent,
            'completion_date': self.completion_date,
            'notes': self.notes,
            'expected_reduction_percent': self.expected_reduction_percent,
            'actual_reduction_percent': self.actual_reduction_percent,
            'verified': self.verified,
            'verified_by': self.verified_by,
            'verified_date': self.verified_date,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
