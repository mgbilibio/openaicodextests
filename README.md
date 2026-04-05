# App de Gestão de Riscos e Segurança do Trabalho

Sistema desktop para análise, avaliação e documentação de riscos ocupacionais baseado na ISO 31010 e Normas Regulamentadoras (NRs) brasileiras.

## 🎯 Funcionalidades

### 1. **Gerenciamento de Ambientes**
- Cadastro de ambientes/setores de trabalho
- Classificação por tipo (Escritório, Produção, Obra, Comercial, etc.)
- Registro de número de trabalhadores
- Descrição e localização

### 2. **Identificação de Perigos**
- Cadastro de perigos conforme categorias NR
  - Físicos, Químicos, Biológicos
  - Ergonômicos, Psicossociais, Mecânicos
  - Elétricos, Térmicos, Radiação, Pressão
- Registro de pessoas expostas
- Localização específica do perigo

### 3. **Gerenciamento de Atividades**
- Cadastro de atividades/tarefas executadas
- Associação a ambientes específicos
- Frequência de execução (Contínua, Intermitente, Ocasional)
- Vinculação automática a perigos identificados
- Número de trabalhadores por atividade

### 4. **Avaliação de Riscos (ISO 31010)**
- Matriz de severidade x probabilidade
- 5 níveis de severidade: Insignificante, Menor, Moderado, Maior, Catastrófico
- 5 níveis de probabilidade: Raro, Improvável, Possível, Provável, Muito Provável
- Cálculo automático do nível de risco
- Avaliação de risco residual
- Atribuição de responsáveis e prazos

### 5. **Geração de Documentos**
- **PGR (Programa de Gestão de Riscos)** em DOCX
  - Informações da empresa
  - Escopo da avaliação
  - Ambientes e perigos
  - Matriz de riscos completa
  - Recomendações
  
- **Relatório de Análise** em PDF
  - Resumo executivo
  - Estatísticas de riscos
  - Distribuição por nível de risco
  - Formatação profissional

### 6. **Persistência de Dados**
- Armazenamento em JSON no diretório do usuário
- Salvamento automático
- Recuperação de dados entre sessões

## 📋 Requisitos

- Python 3.8+
- PySide6 6.7.0
- python-docx 0.8.11
- reportlab 4.0.9
- Pillow 10.2.0

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd openaicodextests
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 🏃 Execução

```bash
python main.py
```

A aplicação abrirá uma janela com interface gráfica.

## 📖 Guia de Uso

### 1. **Cadastrar Ambientes**
- Abra a aba "Ambientes"
- Clique em "Adicionar Ambiente"
- Preencha:
  - Nome do ambiente
  - Tipo (escolha na lista)
  - Localização
  - Número de trabalhadores
  - Descrição (opcional)
- Clique em "Salvar"

### 2. **Identificar Perigos**
- Abra a aba "Perigos"
- Clique em "Adicionar Perigo"
- Preencha:
  - Categoria (conforme NR)
  - Descrição detalhada do perigo
  - Localização no ambiente
  - Descrição de quem está exposto
- Clique em "Salvar"

### 3. **Gerenciar Atividades**
- Abra a aba "Atividades"
- Clique em "Adicionar Atividade"
- Preencha:
  - Nome da atividade
  - Descrição detalhada
  - Ambiente onde é executada
  - Frequência (Contínua, Intermitente, Ocasional)
  - Número de trabalhadores envolvidos
  - Selecione perigos associados (checklist)
- Clique em "Salvar"

### 4. **Avaliar Riscos**
- Abra a aba "Avaliação de Riscos"
- Clique em "Adicionar Avaliação"
- Selecione o perigo a avaliar
- Defina:
  - **Severidade**: Impacto potencial do risco
  - **Probabilidade**: Chance de ocorrência
- O sistema calcula automaticamente o **Nível de Risco**
- Descreva **Medidas de Controle** propostas
- (Opcional) Registre severidade e probabilidade residuais
- Atribua responsável e prazo
- Clique em "Salvar"

### 5. **Gerar Documentos**
- Abra a aba "Gerar Documentos"
- Preencha informações da empresa:
  - Razão Social
  - CNPJ
  - Endereço
  - Responsável (gerente, técnico em segurança, etc.)
- Descreva o escopo da avaliação
- Escolha o formato:
  - **Gerar PGR (DOCX)**: Programa de Gestão de Riscos completo
  - **Gerar Relatório (PDF)**: Análise de riscos formatada

## 📐 Metodologia ISO 31010

A avaliação de riscos segue a norma **ISO 31010:2019 - Risk Management - Risk Assessment Techniques**, que estabelece:

### Matriz de Risco
```
Probabilidade vs Severidade

Score = Severidade × Probabilidade

Classificação Final:
- 1-3: Insignificante
- 4-6: Aceitável
- 7-12: Moderado
- 13-16: Substancial
- 17-25: Intolerável
```

### Processo
1. **Identificação**: Listar todos os perigos
2. **Análise**: Avaliar severidade e probabilidade
3. **Avaliação**: Determinar nível de risco
4. **Controle**: Propor medidas mitigadoras
5. **Acompanhamento**: Monitorar risco residual

## 🇧🇷 Conformidade com NRs Brasileiras

Categorias de risco conforme **NR-12, NR-15, NR-16**:

| Categoria | Exemplos | NR |
|-----------|----------|-----|
| Físico | Ruído, Vibração, Temperatura | NR-15 |
| Químico | Gases, Vapores, Poeiras | NR-15 |
| Biológico | Vírus, Bactérias, Fungos | NR-15 |
| Ergonômico | Postura, Esforço Repetitivo | NR-17 |
| Psicossocial | Estresse, Assédio | NR-17 |
| Mecânico | Máquinas, Ferramentas | NR-12 |
| Elétrico | Descarga, Fiação | NR-10 |
| Térmico | Queimaduras, Congelamento | - |
| Radiação | Ionizante, UV | NR-15 |
| Pressão | Ar comprimido, Mergulho | NR-15 |

## 💾 Estrutura de Dados

Os arquivos são salvos em `~/.occupational_health_app/`:

```
environments.json     # Ambientes cadastrados
hazards.json         # Perigos identificados
assessments.json     # Avaliações de risco
activities.json      # Atividades de trabalho
```

Cada arquivo contém dados estruturados em JSON para facilitar integração futura.

## 🔄 Fluxo de Trabalho Recomendado

1. **Fase 1 - Planejamento**
   - Definir escopo da avaliação
   - Listar ambientes a serem avaliados

2. **Fase 2 - Identificação**
   - Cadastrar ambientes
   - Identificar todos os perigos por ambiente

3. **Fase 3 - Avaliação**
   - Avaliar cada perigo (severidade + probabilidade)
   - Documentar medidas de controle existentes

4. **Fase 4 - Documentação**
   - Gerar PGR inicial
   - Gerar relatório para stakeholders

5. **Fase 5 - Acompanhamento**
   - Registrar responsáveis e prazos
   - Atualizar riscos residuais conforme controles são implementados

## 📞 Suporte

Para dúvidas sobre:
- **ISO 31010**: Consulte a norma oficial ou especialistas em gestão de riscos
- **NRs Brasileiras**: Acesse www.gov.br/trabalho ou contate a CEREST regional
- **App**: Abra uma issue no repositório

## 📝 Licença

Este projeto é fornecido como ferramenta de suporte para Profissionais de Segurança do Trabalho (PPRA/PGR).

## 🚧 Roadmap - Próximas Funcionalidades

### Fase 2 - Análise Avançada
- [ ] **Análise Postural (NR-17)**: Avaliação ergonômica específica com RULA/RAPID
- [ ] **Plano de Controles**: Módulo dedicado para planejamento e acompanhamento de ações
- [ ] **Histórico de Auditoria**: Rastreamento de alterações e responsáveis
- [ ] **Dashboards**: Visualização de métricas e tendências de riscos

### Fase 3 - Gerenciamento de Recursos
- [ ] **Ferramentas e EPIs**: Cadastro de equipamentos e associação a riscos
- [ ] **Matriz de Recursos**: Requisitos de EPIs por atividade
- [ ] **Registro de Treinamentos**: Rastreamento de capacitação de trabalhadores
- [ ] **Check-lists**: Criação de roteiros de inspeção e verificação

### Fase 4 - Conformidade e Relatórios
- [ ] **Gerador de PPRA**: Documento integrado com dados de risco
- [ ] **Relatório CEREST**: Exportação para formato de notificação
- [ ] **Comparação com Legislação**: Validação automática contra NRs
- [ ] **Exportação Excel**: Tabelas dinâmicas para análise

### Fase 5 - Integração e Mobilidade
- [ ] **Aplicativo Mobile**: Coleta de dados em campo
- [ ] **Sincronização Cloud**: Backup e acesso remoto
- [ ] **Integração com Banco de Dados**: PostgreSQL/MySQL
- [ ] **API REST**: Para integração com outros sistemas

---

**Desenvolvido com foco em conformidade regulatória e usabilidade para profissionais de SST.**
