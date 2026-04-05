"""Módulo de persistência de dados com JSON"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from src.models.risk import (
    WorkEnvironment, Hazard, RiskAssessment, WorkActivity,
    RiskCategory, RiskSeverity, RiskProbability,
    ControlMeasure, ControlType, ControlStatus
)


class DataStorage:
    """Gerencia persistência de dados em JSON"""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.environments_file = self.data_dir / "environments.json"
        self.hazards_file = self.data_dir / "hazards.json"
        self.assessments_file = self.data_dir / "assessments.json"
        self.activities_file = self.data_dir / "activities.json"
        self.controls_file = self.data_dir / "control_measures.json"

        self.environments = self._load_environments()
        self.hazards = self._load_hazards()
        self.assessments = self._load_assessments()
        self.activities = self._load_activities()
        self.control_measures = self._load_control_measures()

    # ===== Environments =====

    def _load_environments(self) -> dict:
        """Carrega ambientes do arquivo"""
        if self.environments_file.exists():
            try:
                with open(self.environments_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: self._dict_to_environment(v)
                        for k, v in data.items()
                    }
            except:
                return {}
        return {}

    def _dict_to_environment(self, data: dict) -> WorkEnvironment:
        """Converte dicionário para WorkEnvironment"""
        return WorkEnvironment(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            location=data['location'],
            type=data['type'],
            workers_count=data['workers_count'],
            activities=data.get('activities', []),
            hazards=data.get('hazards', []),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )

    def save_environment(self, env: WorkEnvironment):
        """Salva ambiente"""
        self.environments[env.id] = env
        self._save_environments()

    def get_environment(self, env_id: str) -> Optional[WorkEnvironment]:
        """Obtém ambiente por ID"""
        return self.environments.get(env_id)

    def get_all_environments(self) -> List[WorkEnvironment]:
        """Retorna todos os ambientes"""
        return list(self.environments.values())

    def delete_environment(self, env_id: str):
        """Deleta ambiente"""
        if env_id in self.environments:
            del self.environments[env_id]
            self._save_environments()

    def _save_environments(self):
        """Salva ambientes no arquivo"""
        data = {}
        for env_id, env in self.environments.items():
            data[env_id] = {
                'id': env.id,
                'name': env.name,
                'description': env.description,
                'location': env.location,
                'type': env.type,
                'workers_count': env.workers_count,
                'activities': env.activities,
                'hazards': env.hazards,
                'created_at': env.created_at.isoformat(),
                'updated_at': env.updated_at.isoformat()
            }
        with open(self.environments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ===== Hazards =====

    def _load_hazards(self) -> dict:
        """Carrega perigos do arquivo"""
        if self.hazards_file.exists():
            try:
                with open(self.hazards_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: self._dict_to_hazard(v)
                        for k, v in data.items()
                    }
            except:
                return {}
        return {}

    def _dict_to_hazard(self, data: dict) -> Hazard:
        """Converte dicionário para Hazard"""
        return Hazard(
            id=data['id'],
            category=RiskCategory(data['category']),
            description=data['description'],
            location=data['location'],
            exposed_people=data['exposed_people'],
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )

    def save_hazard(self, hazard: Hazard):
        """Salva perigo"""
        self.hazards[hazard.id] = hazard
        self._save_hazards()

    def get_hazard(self, hazard_id: str) -> Optional[Hazard]:
        """Obtém perigo por ID"""
        return self.hazards.get(hazard_id)

    def get_all_hazards(self) -> List[Hazard]:
        """Retorna todos os perigos"""
        return list(self.hazards.values())

    def delete_hazard(self, hazard_id: str):
        """Deleta perigo"""
        if hazard_id in self.hazards:
            del self.hazards[hazard_id]
            self._save_hazards()

    def _save_hazards(self):
        """Salva perigos no arquivo"""
        data = {}
        for hazard_id, hazard in self.hazards.items():
            data[hazard_id] = {
                'id': hazard.id,
                'category': hazard.category.value,
                'description': hazard.description,
                'location': hazard.location,
                'exposed_people': hazard.exposed_people,
                'created_at': hazard.created_at.isoformat()
            }
        with open(self.hazards_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ===== Risk Assessments =====

    def _load_assessments(self) -> dict:
        """Carrega avaliações do arquivo"""
        if self.assessments_file.exists():
            try:
                with open(self.assessments_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: self._dict_to_assessment(v)
                        for k, v in data.items()
                    }
            except:
                return {}
        return {}

    def _dict_to_assessment(self, data: dict) -> RiskAssessment:
        """Converte dicionário para RiskAssessment"""
        residual_sev = None
        if data.get('residual_severity'):
            residual_sev = RiskSeverity(data['residual_severity'])

        residual_prob = None
        if data.get('residual_probability'):
            residual_prob = RiskProbability(data['residual_probability'])

        return RiskAssessment(
            id=data['id'],
            hazard_id=data['hazard_id'],
            severity=RiskSeverity(data['severity']),
            probability=RiskProbability(data['probability']),
            control_measures=data['control_measures'],
            residual_severity=residual_sev,
            residual_probability=residual_prob,
            responsible=data.get('responsible'),
            deadline=data.get('deadline'),
            status=data.get('status', 'Aberto'),
            notes=data.get('notes', ''),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )

    def save_assessment(self, assessment: RiskAssessment):
        """Salva avaliação de risco"""
        self.assessments[assessment.id] = assessment
        self._save_assessments()

    def get_assessment(self, assessment_id: str) -> Optional[RiskAssessment]:
        """Obtém avaliação por ID"""
        return self.assessments.get(assessment_id)

    def get_all_assessments(self) -> List[RiskAssessment]:
        """Retorna todas as avaliações"""
        return list(self.assessments.values())

    def delete_assessment(self, assessment_id: str):
        """Deleta avaliação"""
        if assessment_id in self.assessments:
            del self.assessments[assessment_id]
            self._save_assessments()

    def _save_assessments(self):
        """Salva avaliações no arquivo"""
        data = {}
        for assess_id, assess in self.assessments.items():
            data[assess_id] = {
                'id': assess.id,
                'hazard_id': assess.hazard_id,
                'severity': assess.severity.value,
                'probability': assess.probability.value,
                'control_measures': assess.control_measures,
                'residual_severity': assess.residual_severity.value if assess.residual_severity else None,
                'residual_probability': assess.residual_probability.value if assess.residual_probability else None,
                'responsible': assess.responsible,
                'deadline': assess.deadline,
                'status': assess.status,
                'notes': assess.notes,
                'created_at': assess.created_at.isoformat(),
                'updated_at': assess.updated_at.isoformat()
            }
        with open(self.assessments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ===== Activities =====

    def _load_activities(self) -> dict:
        """Carrega atividades do arquivo"""
        if self.activities_file.exists():
            try:
                with open(self.activities_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: self._dict_to_activity(v)
                        for k, v in data.items()
                    }
            except:
                return {}
        return {}

    def _dict_to_activity(self, data: dict) -> WorkActivity:
        """Converte dicionário para WorkActivity"""
        return WorkActivity(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            environment_id=data['environment_id'],
            workers=data['workers'],
            frequency=data['frequency'],
            hazards=data.get('hazards', []),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )

    def save_activity(self, activity: WorkActivity):
        """Salva atividade"""
        self.activities[activity.id] = activity
        self._save_activities()

    def get_activity(self, activity_id: str) -> Optional[WorkActivity]:
        """Obtém atividade por ID"""
        return self.activities.get(activity_id)

    def get_all_activities(self) -> List[WorkActivity]:
        """Retorna todas as atividades"""
        return list(self.activities.values())

    def delete_activity(self, activity_id: str):
        """Deleta atividade"""
        if activity_id in self.activities:
            del self.activities[activity_id]
            self._save_activities()

    def _save_activities(self):
        """Salva atividades no arquivo"""
        data = {}
        for activity_id, activity in self.activities.items():
            data[activity_id] = {
                'id': activity.id,
                'name': activity.name,
                'description': activity.description,
                'environment_id': activity.environment_id,
                'workers': activity.workers,
                'frequency': activity.frequency,
                'hazards': activity.hazards,
                'created_at': activity.created_at.isoformat()
            }
        with open(self.activities_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ===== Control Measures =====

    def _load_control_measures(self) -> dict:
        """Carrega medidas de controle do arquivo"""
        if self.controls_file.exists():
            try:
                with open(self.controls_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: self._dict_to_control(v)
                        for k, v in data.items()
                    }
            except:
                return {}
        return {}

    def _dict_to_control(self, data: dict) -> ControlMeasure:
        """Converte dicionário para ControlMeasure"""
        return ControlMeasure(
            id=data['id'],
            assessment_id=data['assessment_id'],
            description=data['description'],
            control_type=ControlType(data['control_type']),
            start_date=data['start_date'],
            deadline=data['deadline'],
            responsible=data['responsible'],
            alternative_responsible=data.get('alternative_responsible'),
            estimated_cost=data.get('estimated_cost', 0.0),
            actual_cost=data.get('actual_cost', 0.0),
            supplier=data.get('supplier'),
            status=ControlStatus(data.get('status', 'Planejado')),
            progress_percent=data.get('progress_percent', 0),
            completion_date=data.get('completion_date'),
            notes=data.get('notes', ''),
            expected_reduction_percent=data.get('expected_reduction_percent', 0),
            actual_reduction_percent=data.get('actual_reduction_percent'),
            verified=data.get('verified', False),
            verified_by=data.get('verified_by'),
            verified_date=data.get('verified_date'),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )

    def save_control_measure(self, control: ControlMeasure):
        """Salva medida de controle"""
        control.updated_at = datetime.now()
        self.control_measures[control.id] = control
        self._save_control_measures()

    def get_control_measure(self, control_id: str) -> Optional[ControlMeasure]:
        """Obtém medida de controle por ID"""
        return self.control_measures.get(control_id)

    def get_controls_by_assessment(self, assessment_id: str) -> List[ControlMeasure]:
        """Retorna todas as medidas de controle de uma avaliação"""
        return [c for c in self.control_measures.values() if c.assessment_id == assessment_id]

    def get_all_control_measures(self) -> List[ControlMeasure]:
        """Retorna todas as medidas de controle"""
        return list(self.control_measures.values())

    def delete_control_measure(self, control_id: str):
        """Deleta medida de controle"""
        if control_id in self.control_measures:
            del self.control_measures[control_id]
            self._save_control_measures()

    def _save_control_measures(self):
        """Salva medidas de controle no arquivo"""
        data = {}
        for control_id, control in self.control_measures.items():
            data[control_id] = control.to_dict()

        with open(self.controls_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ===== General =====

    def save_all(self):
        """Salva todos os dados"""
        self._save_environments()
        self._save_hazards()
        self._save_assessments()
        self._save_activities()
        self._save_control_measures()

    def get_statistics(self) -> dict:
        """Retorna estatísticas dos dados"""
        assessments = self.get_all_assessments()
        risks_by_level = {}

        for assess in assessments:
            level = assess.get_risk_level()
            risks_by_level[level] = risks_by_level.get(level, 0) + 1

        return {
            'total_environments': len(self.environments),
            'total_hazards': len(self.hazards),
            'total_assessments': len(assessments),
            'risks_by_level': risks_by_level
        }
