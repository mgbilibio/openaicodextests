"""Modelos para Análise Ergonômica e Postural (NR-17)"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime


class ForceLevel(Enum):
    """Nível de força/carga"""
    LEVE = "Leve"
    MODERADO = "Moderado"
    PESADO = "Pesado"


class RULAScore(Enum):
    """Nível de risco RULA (Rapid Upper Limb Assessment)"""
    RULA_1_2 = "1-2"  # Aceitável
    RULA_3_4 = "3-4"  # Investigação necessária
    RULA_5_6 = "5-6"  # Mudanças necessárias urgentemente
    RULA_7 = "7"  # Mudanças necessárias imediatamente


class RiskLevel(Enum):
    """Nível de risco ergonômico"""
    ACEITAVEL = "Aceitável"
    INVESTIGACAO = "Investigação Necessária"
    URGENTE = "Mudanças Urgentes"
    CRITICA = "Crítica - Mudanças Imediatas"


@dataclass
class PosturalAssessment:
    """Avaliação Postural seguindo metodologia RULA"""
    id: str
    activity_id: str

    # Informações gerais
    assessment_date: str  # YYYY-MM-DD
    assessor: str
    reviewed_by: Optional[str] = None
    reviewed_date: Optional[str] = None

    # ===== Membros Superiores (Arm) =====
    # Ombro
    shoulder_elevation: str = "Neutro"  # Neutro, Ligeiramente Elevado, Elevado
    shoulder_abduction: bool = False  # Abdução presente

    # Cotovelo
    elbow_flexion: int = 90  # 0-180 graus
    elbow_away_from_body: bool = False  # Afastado do corpo

    # Pulso
    wrist_extension: int = 0  # -30 a 60 graus
    wrist_deviation: str = "Nenhuma"  # Nenhuma, Radial, Ulnar

    # Rotação do pulso
    wrist_rotation: bool = False  # Rotação presente

    # ===== Pescoço e Tronco =====
    # Pescoço
    neck_flexion: int = 0  # 0-90 graus
    neck_rotation: bool = False  # Rotação presente
    neck_side_flexion: bool = False  # Flexão lateral

    # Tronco
    trunk_flexion: int = 0  # 0-60 graus (considerando cadeira)
    trunk_rotation: bool = False  # Rotação presente
    trunk_side_flexion: bool = False  # Flexão lateral

    # Pernas
    seated_properly: bool = True  # Posição correta sentado
    feet_flat_or_footrest: bool = True  # Pés apoiados

    # ===== Força e Repetição =====
    # Carga
    force_level: ForceLevel = ForceLevel.LEVE
    force_duration: str = "Ocasional"  # Ocasional, Frequente (>2/min), Repetitivo

    # Repetição
    repetitive_movements: bool = False
    static_posture_min: int = 0  # Duração da postura estática em minutos

    # Frequência
    activity_frequency: str = "Ocasional"  # Ocasional, Frequente, Contínuo

    # ===== Fatores Adicionais =====
    # Estresse
    high_stress: bool = False
    poor_visibility: bool = False
    inadequate_support: bool = False

    # ===== Resultados RULA =====
    rula_arm_score: int = 1  # Score do braço (A)
    rula_neck_trunk_score: int = 1  # Score pescoço/tronco (B)
    rula_muscle_activity: int = 0  # Atividade muscular (0-1)
    rula_force_load: int = 0  # Força/Carga (0-3)
    rula_final_score: int = 1  # Score final (1-7)

    risk_level: RiskLevel = RiskLevel.ACEITAVEL

    # ===== Recomendações =====
    recommendations: List[str] = field(default_factory=list)
    interventions_priority: str = "Nenhuma"  # Nenhuma, Baixa, Média, Alta, Crítica
    suggested_breaks: Optional[str] = None
    suggested_positions: List[str] = field(default_factory=list)
    required_equipment: List[str] = field(default_factory=list)

    # ===== Acompanhamento =====
    follow_up_needed: bool = False
    follow_up_date: Optional[str] = None
    implemented_changes: str = ""
    effectiveness_notes: str = ""

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def calculate_rula_score(self) -> int:
        """Calcula score RULA automático baseado nos dados"""
        # Score do braço (A)
        arm_score = 1

        # Upper arm (ombro/cotovelo)
        if self.elbow_flexion < 80 or self.elbow_flexion > 100:
            arm_score += 1
        if self.shoulder_elevation or self.elbow_away_from_body:
            arm_score += 1

        # Wrist
        if self.wrist_extension < -15 or self.wrist_extension > 20:
            arm_score += 1
        if self.wrist_deviation != "Nenhuma":
            arm_score += 1

        self.rula_arm_score = min(arm_score, 9)

        # Score pescoço/tronco (B)
        neck_trunk_score = 1

        # Neck
        if self.neck_flexion > 20:
            neck_trunk_score += 1
        if self.neck_rotation or self.neck_side_flexion:
            neck_trunk_score += 1

        # Trunk
        if self.trunk_flexion > 20:
            neck_trunk_score += 1
        if self.trunk_rotation or self.trunk_side_flexion:
            neck_trunk_score += 1

        if not self.seated_properly or not self.feet_flat_or_footrest:
            neck_trunk_score += 1

        self.rula_neck_trunk_score = min(neck_trunk_score, 6)

        # Força/Carga
        force_score = 0
        if self.force_level == ForceLevel.MODERADO:
            force_score = 1
        elif self.force_level == ForceLevel.PESADO:
            force_score = 2
        if self.static_posture_min > 30:
            force_score += 1

        self.rula_force_load = min(force_score, 3)

        # Atividade muscular
        muscle_score = 0
        if self.repetitive_movements or self.activity_frequency in ["Frequente", "Contínuo"]:
            muscle_score = 1

        self.rula_muscle_activity = muscle_score

        # Matriz final de risco RULA
        # Simplificado para fins práticos
        combined_score = self.rula_arm_score + self.rula_neck_trunk_score

        if combined_score <= 5:
            final_score = 1
        elif combined_score <= 7:
            final_score = 2 if muscle_score == 0 else 3
        elif combined_score <= 10:
            final_score = 3 if muscle_score == 0 else 4
        else:
            final_score = 5

        # Ajuste pela força/carga
        if self.rula_force_load >= 2:
            final_score = min(final_score + 1, 7)

        self.rula_final_score = final_score

        # Definir nível de risco
        if final_score <= 2:
            self.risk_level = RiskLevel.ACEITAVEL
        elif final_score == 3:
            self.risk_level = RiskLevel.INVESTIGACAO
        elif final_score in [4, 5]:
            self.risk_level = RiskLevel.URGENTE
        else:
            self.risk_level = RiskLevel.CRITICA

        return final_score

    def generate_recommendations(self):
        """Gera recomendações baseadas na avaliação"""
        self.recommendations = []

        if self.rula_final_score <= 2:
            self.recommendations.append("Postura aceitável. Manutenção das condições atuais.")
            self.interventions_priority = "Nenhuma"

        elif self.rula_final_score <= 4:
            self.recommendations.append("Investigar fatores de risco e considerar mudanças.")
            self.recommendations.append("Revisar altura da bancada e disposição do trabalho.")
            self.recommended_breaks = "Pausas a cada 60 minutos"
            self.interventions_priority = "Média"

        else:  # Score 5-7
            self.recommendations.append("URGENTE: Implementar mudanças ergonômicas imediatamente.")
            self.recommendations.append("Revisar completamente o layout do ambiente.")
            self.recommendations.append("Reduzir tempo em postura de risco.")
            self.recommended_breaks = "Pausas a cada 30 minutos"
            self.interventions_priority = "Crítica"

        # Posições sugeridas
        if self.elbow_flexion < 80 or self.elbow_flexion > 100:
            self.suggested_positions.append("Manter cotovelo entre 80-100 graus")
        if self.neck_flexion > 20:
            self.suggested_positions.append("Manter pescoço neutro (flexão < 20 graus)")
        if not self.seated_properly:
            self.suggested_positions.append("Ajustar altura da cadeira para posição correta")

        # Equipamentos necessários
        if not self.seated_properly:
            self.required_equipment.append("Cadeira ergonômica ajustável")
        if not self.feet_flat_or_footrest:
            self.required_equipment.append("Apoio para pés (footrest)")
        if self.poor_visibility:
            self.required_equipment.append("Suporte de documento ou monitor")
        if self.trunk_flexion > 20:
            self.required_equipment.append("Encosto lombar ou almofada de apoio")

    def to_dict(self):
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'assessment_date': self.assessment_date,
            'assessor': self.assessor,
            'reviewed_by': self.reviewed_by,
            'reviewed_date': self.reviewed_date,
            'shoulder_elevation': self.shoulder_elevation,
            'shoulder_abduction': self.shoulder_abduction,
            'elbow_flexion': self.elbow_flexion,
            'elbow_away_from_body': self.elbow_away_from_body,
            'wrist_extension': self.wrist_extension,
            'wrist_deviation': self.wrist_deviation,
            'wrist_rotation': self.wrist_rotation,
            'neck_flexion': self.neck_flexion,
            'neck_rotation': self.neck_rotation,
            'neck_side_flexion': self.neck_side_flexion,
            'trunk_flexion': self.trunk_flexion,
            'trunk_rotation': self.trunk_rotation,
            'trunk_side_flexion': self.trunk_side_flexion,
            'seated_properly': self.seated_properly,
            'feet_flat_or_footrest': self.feet_flat_or_footrest,
            'force_level': self.force_level.value,
            'force_duration': self.force_duration,
            'repetitive_movements': self.repetitive_movements,
            'static_posture_min': self.static_posture_min,
            'activity_frequency': self.activity_frequency,
            'high_stress': self.high_stress,
            'poor_visibility': self.poor_visibility,
            'inadequate_support': self.inadequate_support,
            'rula_arm_score': self.rula_arm_score,
            'rula_neck_trunk_score': self.rula_neck_trunk_score,
            'rula_muscle_activity': self.rula_muscle_activity,
            'rula_force_load': self.rula_force_load,
            'rula_final_score': self.rula_final_score,
            'risk_level': self.risk_level.value,
            'recommendations': self.recommendations,
            'interventions_priority': self.interventions_priority,
            'suggested_breaks': self.suggested_breaks,
            'suggested_positions': self.suggested_positions,
            'required_equipment': self.required_equipment,
            'follow_up_needed': self.follow_up_needed,
            'follow_up_date': self.follow_up_date,
            'implemented_changes': self.implemented_changes,
            'effectiveness_notes': self.effectiveness_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
