# 🗺️ Roadmap - Ocupational Health & Safety App

Plano de desenvolvimento e próximas funcionalidades para o aplicativo de Gestão de Riscos e Segurança do Trabalho.

## ✅ Implementado (MVP)

- [x] Gerenciamento de Ambientes
- [x] Identificação de Perigos (10 categorias NR)
- [x] Atividades de Trabalho
- [x] Avaliação de Riscos (ISO 31010)
- [x] Persistência de Dados (JSON)
- [x] Geração PGR (DOCX)
- [x] Geração de Relatórios (PDF)

---

## 📋 Fase 2: Análise e Controle

### 🎯 Análise Postural (NR-17)
**Objetivo**: Avaliação ergonômica específica com metodologia RULA/RAPID

- Módulo específico para análise de postura
- Questões padronizadas RULA/RAPID
- Cálculo automático de score de risco ergonômico
- Recomendações de intervenção por score
- Relatório específico de ergonomia em PDF

**Estimativa**: ~40 horas
**Prioridade**: Alta

### 📝 Plano de Controles
**Objetivo**: Gerenciamento completo de ações corretivas

**Funcionalidades**:
- Criar planos de ação com:
  - Descrição da medida de controle
  - Tipo (eliminação, substituição, controle administrativo, EPI)
  - Prazo de implementação
  - Responsável designado
  - Orçamento estimado
- Status de progresso (Planejado, Em Execução, Concluído, Adiado)
- Rastreamento de cumprimento de prazos
- Matriz de responsabilidades
- Notificações de vencimento

**Estimativa**: ~50 horas
**Prioridade**: Alta

### 📊 Histórico e Auditoria
**Objetivo**: Rastreabilidade completa de alterações

- Log de todas as alterações (quem, quando, o quê)
- Histórico de versões de documentos
- Comparação de versões
- Relatório de auditoria

**Estimativa**: ~30 horas
**Prioridade**: Média

### 📈 Dashboards Interativos
**Objetivo**: Visualização de métricas em tempo real

- Dashboard executivo:
  - Distribuição de riscos (gráfico pizza)
  - Riscos por categoria (gráfico barra)
  - Atividades com risco intolerável
- Dashboard de controles:
  - Ações em dia vs atrasadas
  - Taxa de cumprimento de prazos
- Dashboard de ambientes:
  - Evolução do risco ao longo do tempo

**Tecnologia**: matplotlib/plotly
**Estimativa**: ~35 horas
**Prioridade**: Média

---

## 🔧 Fase 3: Gerenciamento de Recursos

### 🛠️ Ferramentas e EPIs
**Objetivo**: Cadastro e rastreamento de equipamentos de proteção

**Funcionalidades**:
- Cadastro de EPIs:
  - Nome, descrição, CA
  - Associação a perigos
  - Prazo de validade
  - Fornecedor
- Cadastro de Ferramentas:
  - Tipo, localização
  - Inspeção periódica
- Matriz EPI x Perigo:
  - Especificar qual EPI para cada risco
  - Recomendação em laudos

**Estimativa**: ~45 horas
**Prioridade**: Alta

### 📋 Matriz de Requisitos de Recursos
**Objetivo**: Relatório de necessidades por atividade

- Gerar requisição de EPIs para cada atividade
- Quantidades necessárias
- Custos estimados
- Relatório para compras

**Estimativa**: ~20 horas
**Prioridade**: Média

### 🎓 Registro de Treinamentos
**Objetivo**: Rastreamento de capacitação

- Cadastro de treinamentos:
  - Tema (NR-10, NR-12, Primeiros Socorros, etc.)
  - Data, instrutor
  - Participantes
  - Certificado
- Relatório de participação por trabalhador
- Alertas de treinamento vencido

**Estimativa**: ~35 horas
**Prioridade**: Média

### ✅ Check-lists
**Objetivo**: Criação de roteiros de inspeção

- Templates de check-lists para:
  - Inspeção de ambientes
  - Verificação de controles implementados
  - Análise de conformidade
- Geração de check-lists para campo
- Preenchimento mobile
- Relatório de não-conformidades

**Estimativa**: ~40 horas
**Prioridade**: Média

---

## 📄 Fase 4: Conformidade Regulatória

### 📘 Gerador de PPRA
**Objetivo**: Documento integrado com todos os dados

- Incluir dados de:
  - Ambientes avaliados
  - Perigos identificados
  - Riscos por ambiente
  - Plano de ação
  - Cronograma de revisão
- Formato oficial PPRA
- Assinatura digital
- Versioning automático

**Estimativa**: ~40 horas
**Prioridade**: Alta

### 🔴 Comparação com Legislação
**Objetivo**: Validação automática contra NRs

- Base de dados de limites legais:
  - Nível de ruído (NR-15)
  - Temperatura (NR-15)
  - Radiação (NR-15)
  - Jornada (NR-17)
- Alertas automáticos de não-conformidade
- Relatório de conformidade

**Estimativa**: ~50 horas
**Prioridade**: Média

### 📊 Exportação Excel
**Objetivo**: Análise dinâmica de dados

- Tabelas dinâmicas para:
  - Riscos por ambiente
  - Riscos por categoria
  - Atividades de maior risco
  - Controles por tipo
- Gráficos interativos
- Fórmulas para análises customizadas

**Estimativa**: ~25 horas
**Prioridade**: Baixa

### 📋 Relatório CEREST
**Objetivo**: Exportação para órgãos reguladores

- Formato compatível com CEREST
- Dados de comunicação de acidente
- Notificação automática

**Estimativa**: ~30 horas
**Prioridade**: Média

---

## 📱 Fase 5: Integração e Mobilidade

### 📱 Aplicativo Mobile
**Objetivo**: Coleta de dados em tempo real no campo

- App Android/iOS (React Native ou Flutter)
- Sincronização com desktop
- Offline-first
- Câmera para documentação
- GPS para localização

**Estimativa**: ~80 horas
**Prioridade**: Baixa

### ☁️ Cloud Sync
**Objetivo**: Backup e acesso remoto

- Sincronização com nuvem:
  - AWS S3 / Google Drive / OneDrive
- Backup automático
- Acesso remoto via web
- Controle de acesso e permissões

**Estimativa**: ~60 horas
**Prioridade**: Média

### 🗄️ Banco de Dados
**Objetivo**: Escalabilidade para múltiplos usuários

- Migração para PostgreSQL/MySQL
- Servidor central
- Multi-usuário com permissões
- Sincronização de dados

**Estimativa**: ~70 horas
**Prioridade**: Média

### 🔌 API REST
**Objetivo**: Integração com sistemas externos

- API para:
  - CRUD de ambientes, perigos, riscos
  - Geração de documentos
  - Consulta de relatórios
- Documentação OpenAPI/Swagger
- Autenticação JWT

**Estimativa**: ~50 horas
**Prioridade**: Média

---

## 📊 Métricas de Sucesso

- [ ] 95% de conformidade com ISO 31010
- [ ] Documentação gerada em < 30 segundos
- [ ] Interface intuitiva (SUS score > 70)
- [ ] < 5 segundos de resposta em todas as operações
- [ ] Zero perda de dados (backup automático)

---

## 🎯 Priorização

### Alta (Próximos 3 meses)
1. Plano de Controles
2. Análise Postural
3. Ferramentas e EPIs
4. Gerador de PPRA

### Média (3-6 meses)
5. Dashboards
6. Cloud Sync
7. Banco de Dados
8. Comparação com Legislação

### Baixa (6+ meses)
9. App Mobile
10. Exportação Excel
11. Check-lists

---

## 🤝 Contribuindo

Para sugerir novas funcionalidades ou reportar bugs:
- Abra uma issue no GitHub
- Descreva claramente a funcionalidade desejada
- Indique a prioridade

---

**Última atualização**: 2026-04-05
**Versão**: 0.1.0
