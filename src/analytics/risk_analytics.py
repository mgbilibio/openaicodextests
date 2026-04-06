"""Módulo de análises e estatísticas para dashboards"""

from typing import Dict, List, Tuple
from collections import defaultdict
from src.database.storage import DataStorage
from src.models.risk import RiskSeverity, RiskProbability


class RiskAnalytics:
    """Análises e estatísticas de risco"""

    def __init__(self, storage: DataStorage):
        self.storage = storage

    # ===== Estatísticas Gerais =====

    def get_risk_distribution(self) -> Dict[str, int]:
        """Distribuição de riscos por nível"""
        distribution = defaultdict(int)
        for assess in self.storage.get_all_assessments():
            level = assess.get_risk_level()
            distribution[level] += 1

        return dict(distribution)

    def get_risks_by_severity(self) -> Dict[str, int]:
        """Contagem por severidade"""
        by_severity = defaultdict(int)
        for assess in self.storage.get_all_assessments():
            severity = assess.severity.value
            by_severity[severity] += 1

        return dict(by_severity)

    def get_risks_by_probability(self) -> Dict[str, int]:
        """Contagem por probabilidade"""
        by_probability = defaultdict(int)
        for assess in self.storage.get_all_assessments():
            prob = assess.probability.value
            by_probability[prob] += 1

        return dict(by_probability)

    def get_risks_by_hazard_category(self) -> Dict[str, int]:
        """Riscos agrupados por categoria de perigo"""
        by_category = defaultdict(int)
        for assess in self.storage.get_all_assessments():
            hazard = self.storage.get_hazard(assess.hazard_id)
            if hazard:
                category = hazard.category.value
                by_category[category] += 1

        return dict(sorted(by_category.items()))

    def get_risks_by_environment(self) -> Dict[str, int]:
        """Riscos por ambiente"""
        by_env = defaultdict(int)
        for assess in self.storage.get_all_assessments():
            hazard = self.storage.get_hazard(assess.hazard_id)
            if hazard:
                # Contar riscos de atividades naquele ambiente
                for activity in self.storage.get_all_activities():
                    if hazard.id in activity.hazards:
                        env = self.storage.get_environment(activity.environment_id)
                        if env:
                            by_env[env.name] += 1
                            break

        return dict(sorted(by_env.items()))

    # ===== Matriz de Riscos =====

    def get_risk_matrix(self) -> List[List[int]]:
        """Matriz 5x5 de severidade x probabilidade"""
        severities = [s.value for s in RiskSeverity]
        probabilities = [p.value for p in RiskProbability]

        matrix = [[0 for _ in range(len(probabilities))]
                  for _ in range(len(severities))]

        for assess in self.storage.get_all_assessments():
            sev_idx = severities.index(assess.severity.value)
            prob_idx = probabilities.index(assess.probability.value)
            matrix[sev_idx][prob_idx] += 1

        return matrix

    def get_matrix_labels(self) -> Tuple[List[str], List[str]]:
        """Labels para a matriz"""
        severities = [s.value for s in RiskSeverity]
        probabilities = [p.value for p in RiskProbability]
        return severities, probabilities

    # ===== Ações Corretivas =====

    def get_controls_by_status(self) -> Dict[str, int]:
        """Ações corretivas por status"""
        from src.models.risk import ControlStatus

        by_status = defaultdict(int)
        for control in self.storage.get_all_control_measures():
            status = control.status.value
            by_status[status] += 1

        return dict(by_status)

    def get_overdue_controls(self) -> List:
        """Ações atrasadas"""
        overdue = []
        for control in self.storage.get_all_control_measures():
            if control.is_overdue():
                hazard = self.storage.get_hazard(control.assessment_id)
                overdue.append({
                    'id': control.id,
                    'description': control.description,
                    'deadline': control.deadline,
                    'responsible': control.responsible,
                    'priority': control.get_priority()
                })

        return sorted(overdue, key=lambda x: x['deadline'])

    def get_control_budget_summary(self) -> Dict:
        """Resumo de orçamento de controles"""
        total_estimated = 0
        total_spent = 0
        controls_count = 0

        for control in self.storage.get_all_control_measures():
            total_estimated += control.estimated_cost
            total_spent += control.actual_cost
            controls_count += 1

        return {
            'estimated': total_estimated,
            'spent': total_spent,
            'remaining': total_estimated - total_spent,
            'variance_percent': ((total_spent / total_estimated * 100) if total_estimated > 0 else 0),
            'controls_count': controls_count
        }

    # ===== EPIs e Ferramentas =====

    def get_epis_summary(self) -> Dict:
        """Resumo de EPIs"""
        epis = self.storage.get_all_epis()
        expired_ca = sum(1 for e in epis if e.is_ca_expired())
        low_stock = sum(1 for e in epis if e.is_low_stock())

        return {
            'total': len(epis),
            'expired_ca': expired_ca,
            'low_stock': low_stock,
            'ok': len(epis) - expired_ca - low_stock
        }

    def get_tools_summary(self) -> Dict:
        """Resumo de ferramentas"""
        tools = self.storage.get_all_tools()
        overdue_inspection = sum(1 for t in tools if t.is_inspection_overdue())
        with_defect = sum(1 for t in tools if 'Defeito' in t.get_inspection_status_text())

        return {
            'total': len(tools),
            'overdue_inspection': overdue_inspection,
            'with_defect': with_defect,
            'ok': len(tools) - overdue_inspection - with_defect
        }

    # ===== Análises Ergonômicas =====

    def get_ergonomic_summary(self) -> Dict:
        """Resumo de análises ergonômicas"""
        assessments = self.storage.get_all_postural_assessments()

        risk_levels = defaultdict(int)
        for assess in assessments:
            level = assess.risk_level.value
            risk_levels[level] += 1

        return {
            'total': len(assessments),
            'by_risk_level': dict(risk_levels),
            'needs_followup': sum(1 for a in assessments if a.follow_up_needed)
        }

    # ===== Filtros Avançados =====

    def filter_assessments(self, filters: Dict) -> List:
        """Filtra avaliações por critérios"""
        assessments = self.storage.get_all_assessments()

        # Filtro por severidade
        if 'severities' in filters and filters['severities']:
            assessments = [a for a in assessments
                          if a.severity.value in filters['severities']]

        # Filtro por probabilidade
        if 'probabilities' in filters and filters['probabilities']:
            assessments = [a for a in assessments
                          if a.probability.value in filters['probabilities']]

        # Filtro por nível de risco
        if 'risk_levels' in filters and filters['risk_levels']:
            assessments = [a for a in assessments
                          if a.get_risk_level() in filters['risk_levels']]

        # Filtro por categoria de perigo
        if 'categories' in filters and filters['categories']:
            assessments = [a for a in assessments
                          if any(h.category.value in filters['categories']
                                for h in [self.storage.get_hazard(a.hazard_id)]
                                if h)]

        # Filtro por ambiente
        if 'environments' in filters and filters['environments']:
            env_ids = filters['environments']
            assessments = [a for a in assessments
                          if any(act.environment_id in env_ids
                                for act in self.storage.get_all_activities()
                                if a.hazard_id in act.hazards)]

        return assessments

    def filter_controls(self, filters: Dict) -> List:
        """Filtra ações corretivas por critérios"""
        controls = self.storage.get_all_control_measures()

        # Filtro por status
        if 'statuses' in filters and filters['statuses']:
            controls = [c for c in controls
                       if c.status.value in filters['statuses']]

        # Filtro por tipo
        if 'types' in filters and filters['types']:
            controls = [c for c in controls
                       if c.control_type.value in filters['types']]

        # Filtro por responsável
        if 'responsible' in filters and filters['responsible']:
            controls = [c for c in controls
                       if c.responsible and filters['responsible'].lower() in c.responsible.lower()]

        # Filtro por prioridade (apenas atrasados)
        if 'overdue_only' in filters and filters['overdue_only']:
            controls = [c for c in controls if c.is_overdue()]

        return controls

    # ===== Sumários Executivos =====

    def get_executive_summary(self) -> Dict:
        """Sumário executivo do sistema"""
        return {
            'environments': len(self.storage.get_all_environments()),
            'hazards': len(self.storage.get_all_hazards()),
            'activities': len(self.storage.get_all_activities()),
            'assessments': len(self.storage.get_all_assessments()),
            'controls': len(self.storage.get_all_control_measures()),
            'epis': len(self.storage.get_all_epis()),
            'tools': len(self.storage.get_all_tools()),
            'risk_distribution': self.get_risk_distribution(),
            'controls_status': self.get_controls_by_status(),
            'epis_summary': self.get_epis_summary(),
            'tools_summary': self.get_tools_summary(),
            'control_budget': self.get_control_budget_summary(),
            'ergonomic_summary': self.get_ergonomic_summary()
        }
