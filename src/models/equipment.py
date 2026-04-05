"""Modelos para Ferramentas e Equipamentos de Proteção"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List
from datetime import datetime, date


class EPICategory(Enum):
    """Categorias de EPIs conforme NR-6"""
    CABECA = "Proteção da Cabeça"
    OLHOS = "Proteção dos Olhos"
    AUDITIVO = "Proteção Auditiva"
    RESPIRATORIO = "Proteção Respiratória"
    TRONCO = "Proteção do Tronco"
    MEMBROS_SUPERIORES = "Proteção de Membros Superiores"
    MEMBROS_INFERIORES = "Proteção de Membros Inferiores"
    PES = "Proteção dos Pés"
    MULTIPLA = "Proteção Múltipla"


class ToolCategory(Enum):
    """Categorias de ferramentas"""
    CORTE = "Corte"
    IMPACTO = "Impacto"
    MECANICA = "Mecânica"
    ELETRICA = "Elétrica"
    PNEUMATICA = "Pneumática"
    SOLDAGEM = "Soldagem"
    MEDICAO = "Medição"
    ELEVACAO = "Elevação"
    OUTRO = "Outro"


class InspectionStatus(Enum):
    """Status da inspeção de ferramentas"""
    OK = "OK"
    COM_DEFEITO = "Com Defeito"
    PRECISA_REPARO = "Precisa Reparo"
    DESCARTADO = "Descartado"


@dataclass
class EPI:
    """Equipamento de Proteção Individual"""
    id: str
    name: str  # Ex: "Protetor Auricular 3M X5A"
    category: EPICategory
    description: str

    # Certificação NR-6
    ca_number: str  # Certificado de Aprovação
    ca_validity_date: str  # YYYY-MM-DD
    manufacturer: str

    # Especificações técnicas
    attenuation_db: Optional[int] = None  # Para protetor auricular (dB)
    protection_level: str = "Médio"  # Alto, Médio, Baixo
    color: Optional[str] = None
    size_range: Optional[str] = None  # Ex: "P, M, G, GG"

    # Gestão
    cost_unit: float = 0.0
    quantity_in_stock: int = 0
    reorder_point: int = 10  # Quantidade mínima
    supplier: str = ""
    supplier_contact: Optional[str] = None

    # Documentação
    image_path: Optional[str] = None
    notes: str = ""

    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def is_low_stock(self) -> bool:
        """Verifica se estoque está baixo"""
        return self.quantity_in_stock <= self.reorder_point

    def is_ca_expired(self) -> bool:
        """Verifica se certificação está vencida"""
        try:
            validity = datetime.strptime(self.ca_validity_date, '%Y-%m-%d').date()
            return validity < datetime.now().date()
        except:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'ca_number': self.ca_number,
            'ca_validity_date': self.ca_validity_date,
            'manufacturer': self.manufacturer,
            'attenuation_db': self.attenuation_db,
            'protection_level': self.protection_level,
            'color': self.color,
            'size_range': self.size_range,
            'cost_unit': self.cost_unit,
            'quantity_in_stock': self.quantity_in_stock,
            'reorder_point': self.reorder_point,
            'supplier': self.supplier,
            'supplier_contact': self.supplier_contact,
            'image_path': self.image_path,
            'notes': self.notes,
            'active': self.active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


@dataclass
class Tool:
    """Ferramenta ou equipamento de trabalho"""
    id: str
    name: str
    category: ToolCategory
    description: str

    # Localização e responsabilidade
    location: str  # Ambiente/setor onde está
    responsible: str  # Quem usa/cuida

    # Inspeção
    last_inspection_date: str  # YYYY-MM-DD
    next_inspection_date: str  # YYYY-MM-DD
    inspection_status: InspectionStatus = InspectionStatus.OK
    inspector: Optional[str] = None

    # Manutenção
    maintenance_interval_days: int = 365
    maintenance_notes: str = ""

    # Documentação
    serial_number: Optional[str] = None
    image_path: Optional[str] = None
    notes: str = ""

    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def is_inspection_overdue(self) -> bool:
        """Verifica se inspeção está atrasada"""
        try:
            next_inspection = datetime.strptime(self.next_inspection_date, '%Y-%m-%d').date()
            return next_inspection < datetime.now().date()
        except:
            return False

    def get_inspection_status_text(self) -> str:
        """Retorna status formatado"""
        if self.is_inspection_overdue():
            return "🔴 Inspeção Vencida"
        elif self.inspection_status == InspectionStatus.COM_DEFEITO:
            return "🟠 Com Defeito"
        elif self.inspection_status == InspectionStatus.PRECISA_REPARO:
            return "🟡 Precisa Reparo"
        elif self.inspection_status == InspectionStatus.OK:
            return "🟢 OK"
        else:
            return "⚪ Descartado"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'location': self.location,
            'responsible': self.responsible,
            'last_inspection_date': self.last_inspection_date,
            'next_inspection_date': self.next_inspection_date,
            'inspection_status': self.inspection_status.value,
            'inspector': self.inspector,
            'maintenance_interval_days': self.maintenance_interval_days,
            'maintenance_notes': self.maintenance_notes,
            'serial_number': self.serial_number,
            'image_path': self.image_path,
            'notes': self.notes,
            'active': self.active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


@dataclass
class EPIAssignment:
    """Associação entre Perigo e EPI"""
    id: str
    hazard_id: str
    epi_id: str

    required: bool = True  # Obrigatório ou opcional
    quantity_per_worker: int = 1
    replacement_frequency_days: int = 180  # Substituir a cada X dias
    observations: str = ""

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'hazard_id': self.hazard_id,
            'epi_id': self.epi_id,
            'required': self.required,
            'quantity_per_worker': self.quantity_per_worker,
            'replacement_frequency_days': self.replacement_frequency_days,
            'observations': self.observations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
