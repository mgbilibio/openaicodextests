# 📋 Próximos Módulos a Implementar

Este documento detalha os 4 módulos principais solicitados para implementação, em ordem de prioridade.

---

## 1️⃣ **Análise Postural (NR-17)**

### 📌 Descrição
Módulo especializado para avaliação ergonômica de postura em atividades de trabalho, seguindo metodologia padronizada RULA (Rapid Upper Limb Assessment) ou RAPID (Rapid Assessment and Priority Setting of Work-related injuries).

### 🎯 Funcionalidades Principais

#### A) Nova Aba: "Análise Ergonômica"
```
- Seleção da atividade a avaliar
- Questionário estruturado:
  - Posição dos membros superiores
  - Posição do tronco
  - Rotação de pescoço
  - Carga/força aplicada
  - Frequência de movimentos
  - Duração do ciclo
- Cálculo automático do score RULA (1-7)
- Recomendação por nivel:
  - 1-2: Aceitável
  - 3-4: Investigação necessária
  - 5-6: Mudanças necessárias urgentemente
  - 7: Mudanças necessárias imediatamente
```

#### B) Modelos de Dados
```python
@dataclass
class PosturalAssessment:
    id: str
    activity_id: str
    assessment_date: datetime
    
    # Upper limb positions
    shoulder_elevation: str  # Neutral, Slightly raised, Raised
    elbow_flexion: int  # 0-180 degrees
    wrist_extension: int  # -30 to 60 degrees
    wrist_deviation: bool  # Radial/ulnar deviation
    
    # Trunk and neck
    trunk_flexion: int  # 0-60 degrees
    neck_flexion: int  # 0-90 degrees
    neck_rotation: bool
    
    # Force and repetition
    force_level: str  # Light, Moderate, Heavy
    repetitive: bool
    static_duration_min: int
    
    # Results
    rula_score: int  # 1-7
    risk_level: str  # Acceptable, Investigation, Urgent, Immediate
    recommendations: List[str]
    
    created_by: str
    reviewed_by: Optional[str] = None
```

#### C) Geração de Documento
- Relatório de Ergonomia em PDF/DOCX
- Fotos/ilustrações das posições analisadas
- Recomendações de intervenção
- Comparação com parâmetros NR-17

### 🔗 Integração
- Associar score de risco ergonômico à atividade
- Incrementar severidade do risco se necessário
- Linkar no plano de controles

### ⏱️ Estimativa: 40-50 horas

---

## 2️⃣ **Plano de Controles/Ações**

### 📌 Descrição
Módulo para planejamento, execução e acompanhamento de medidas de controle (ações corretivas) mapeadas na avaliação de riscos.

### 🎯 Funcionalidades Principais

#### A) Nova Aba: "Plano de Ações"
```
Interface tipo Kanban:
- Coluna: Planejado
  - Ações não iniciadas
  - Orçamento a alocar
  - Responsável a designar

- Coluna: Em Execução
  - Ações em desenvolvimento
  - % progresso
  - Próximas etapas

- Coluna: Concluído
  - Ações implementadas
  - Data conclusão
  - Verificação de efetividade
```

#### B) Modelos de Dados
```python
@dataclass
class ControlMeasure:
    id: str
    assessment_id: str  # Link to RiskAssessment
    
    # Descrição
    description: str
    type: str  # Eliminação, Substituição, Controle Administrativo, PPE, Monitoramento
    
    # Planejamento
    start_date: date
    deadline: date
    responsible: str  # Nome + função
    alternative_responsible: Optional[str]
    
    # Orçamento
    estimated_cost: float
    actual_cost: float
    supplier: Optional[str]
    
    # Execução
    status: str  # Planned, In Progress, Completed, Delayed, Cancelled
    completion_date: Optional[date]
    % progress: int  # 0-100
    notes: str
    
    # Efetividade
    expected_reduction_percent: int  # Redução esperada de severidade
    actual_reduction_percent: Optional[int]
    verified: bool
    verified_by: Optional[str]
    verified_date: Optional[date]
    
    # Documentação
    evidence_files: List[str]  # Fotos, recibos, certificados
    follow_up_date: Optional[date]

@dataclass
class ActionPlan:
    id: str
    company_id: str
    
    creation_date: datetime
    created_by: str
    
    measures: List[ControlMeasure]
    
    total_budget: float
    total_spent: float
    
    completion_rate: float  # Percentual de medidas concluídas
```

#### C) Recursos de Gerenciamento
- **Matriz de Responsabilidades**: Quem é responsável por qual ação
- **Timeline Visual**: Cronograma Gantt de ações
- **Alertas de Vencimento**: Notificações de prazos próximos
- **Relatório de Progresso**: Acompanhamento mensal/trimestral
- **Análise de Custos**: Orçado vs Realizado

#### D) Integração com Documentos
- Incluir plano de ações no PPRA gerado
- Cronograma de revisão automático (6/12 meses)
- Rastreabilidade de cumprimento regulatório

### ⏱️ Estimativa: 50-60 horas

---

## 3️⃣ **Ferramentas e EPIs**

### 📌 Descrição
Módulo para cadastro, rastreamento e associação de Equipamentos de Proteção Individual (EPIs) e ferramentas aos perigos identificados.

### 🎯 Funcionalidades Principais

#### A) Nova Aba: "Ferramentas e EPIs"
```
Seções:
- Cadastro de EPIs
  - Nome, descrição
  - Certificação (CA número)
  - Validade do certificado
  - Foto/catálogo
  - Fornecedor + contato

- Cadastro de Ferramentas
  - Tipo, descrição
  - Localização/ambiente
  - Última inspeção
  - Próxima inspeção
  - Responsável

- Matriz de Associação
  - Qual EPI para cada perigo?
  - Alternativas aceitas
  - Quantidade necessária
  - Reposição periódica
```

#### B) Modelos de Dados
```python
@dataclass
class EPI:
    id: str
    name: str  # Ex: "Protetor Auricular 3M X5A"
    category: str  # Cabeça, Olhos, Auditivo, Respiratório, Tronco, Membros, Pés
    description: str
    
    # Certificação
    ca_number: str  # Número do Certificado de Aprovação
    ca_validity_date: date
    manufacturer: str
    
    # Efetividade
    attenuation_db: Optional[int]  # Para protetor auricular
    protection_level: str  # Alto, Médio, Baixo
    
    # Gestão
    cost_unit: float
    quantity_in_stock: int
    reorder_quantity: int
    supplier: str
    supplier_contact: str
    
    image_path: Optional[str]
    notes: str
    
    active: bool = True
    created_date: datetime = field(default_factory=datetime.now)

@dataclass
class Tool:
    id: str
    name: str
    category: str  # Corte, Impacto, Mecânica, Elétrica, Etc.
    description: str
    
    location: str  # Ambiente onde está
    responsible: str  # Quem usa/cuida
    
    last_inspection_date: date
    next_inspection_date: date
    inspection_status: str  # OK, Com Defeito, Precisa Reparo
    
    maintenance_notes: str
    image_path: Optional[str]

@dataclass
class EPIAssignment:
    id: str
    hazard_id: str  # Qual perigo
    epi_id: str     # Qual EPI
    
    required: bool  # Obrigatório ou opcional
    quantity_per_worker: int
    replacement_frequency_days: int  # A cada quantos dias substituir
    observations: str
```

#### C) Relatórios e Listas
- **Lista de EPIs Necessários por Atividade**: Gerar requisição para compras
- **Planilha de Distribuição**: Quem recebeu qual EPI
- **Matriz EPI x Perigo**: Tabela de referência
- **Relatório de Estoque**: EPIs com vencimento próximo
- **Adequação Regulatória**: Verificar se EPIs estão em conformidade

### ⏱️ Estimativa: 45-55 horas

---

## 4️⃣ **Plano de Ações Integrado (Controles Avançados)**

### 📌 Descrição
Integração avançada entre avaliação de riscos, plano de controles, EPIs e acompanhamento de efetividade.

### 🎯 Funcionalidades Principais

#### A) Dashboard de Controles
```
Visualização em tempo real:
- Ações planejadas vs Ações concluídas (%)
- Orçamento utilizado vs Planejado
- Riscos reduzidos vs Riscos residuais
- Atrasos em ações (alerta)
- Próximos vencimentos de prazos
```

#### B) Fluxo de Aprovação
```
Hierarquia de validação:
1. Técnico em SST: Propõe medida
2. Gerente da Área: Aprova e aloca orçamento
3. Responsável Execução: Implementa
4. Auditor: Verifica cumprimento
5. Diretor: Aprova conclusão
```

#### C) Rastreabilidade Completa
- Histórico de todas as alterações
- Quem fez, quando, o quê
- Evidências anexadas (fotos, certificados)
- Comparação antes/depois (para fotos)

#### D) Relatórios Executivos
- **Relatório de Cumprimento de Prazos**: Taxa de adimplência
- **Relatório de Efetividade**: Redução de risco alcançada
- **Relatório de Custos**: Investimento vs Impacto
- **Relatório de Compliance**: Conformidade regulatória

### ⏱️ Estimativa: 35-45 horas

---

## 📊 Sequência Recomendada de Implementação

```
Semana 1-2:  Plano de Controles (core)
Semana 3-4:  Ferramentas e EPIs
Semana 5-6:  Análise Postural
Semana 7-8:  Integração Avançada (Dashboards + Aprovações)
```

---

## 🔗 Interdependências

```
Análise Postural
    └─ Conecta a: Atividades → RiskAssessment

Plano de Controles
    ├─ Lê de: RiskAssessment (riscos a controlar)
    ├─ Usa: EPIs (especificar no plano)
    └─ Gera: Documentos (PPRA, Cronograma)

Ferramentas e EPIs
    ├─ Usado por: Plano de Controles
    └─ Vincula a: Perigos (qual EPI para qual risco)

Integração Avançada
    └─ Combina: Tudo acima + Dashboards + Aprovações
```

---

## 💾 Estrutura de Dados Geral

```
database/
├── environments.json (existente)
├── hazards.json (existente)
├── assessments.json (existente)
├── activities.json (existente)
├── postural_assessments.json (novo)
├── control_measures.json (novo)
├── action_plans.json (novo)
├── epis.json (novo)
├── tools.json (novo)
└── epi_assignments.json (novo)
```

---

## 🎓 Referências Normativas

- **NR-17** (Ergonomia): Requisitos para análise postural
- **NR-6** (EPI): Classificação e requisitos de EPIs
- **NR-12** (Máquinas): Ferramentas e segurança
- **ISO 31010**: Integração no plano de ações
- **ABNT NBR 14277**: Terminologia de risco

---

**Última atualização**: 2026-04-05
**Pronto para desenvolvimento**
