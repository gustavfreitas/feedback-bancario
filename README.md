# feedback-bancario - Análise de Feedbacks Bancários (Dados Fictícios)

> Projeto de Análise de Feedbacks de clientes de um banco fictício, criado exclusivamente com dados sintéticos/simulados, sem qualquer vínculo com instituições financeiras reais ou dados pessoais reais.

## 1. Definição do Problema
 
### Que feedback será analisado?
>   Qual é a origem e a natureza dos feedbacks? Exemplos de perguntas-guia:
> - Vêm de qual canal? (app, SAC, redes sociais, pesquisa NPS, e-mail, chat)
> - São textos livres, notas (1-5, 0-10), ou ambos?
> - Sobre qual produto/serviço? (conta corrente, cartão de crédito, empréstimo, atendimento, app mobile)
> - Qual o período e volume simulado? (ex: 500 feedbacks fictícios gerados entre jan-jun/2026)
 
**Resposta:**
```
Feedbacks fictícios de clientes de um banco digital, cobrindo os principais pontos de
contato e produtos: aplicativo, Pix, cartões, transferências, pagamentos, empréstimos,
atendimento (humano e chatbot), abertura de conta, autenticação/segurança e tarifas.
 
Os feedbacks combinam texto livre (relato do cliente) com dados estruturados de apoio:
nota de satisfação, sentimento, urgência, status e tempo de resolução, canal, categoria/
subcategoria, região e tipo de cliente — todos sintéticos, sem qualquer dado pessoal real.
 
Período e volume simulado, ex. "1000 feedbacks fictícios entre jan-jun/2026"]
```
 
### Quem utilizará o resultado?
>   Qual é o público-alvo da análise?
> - Time de produto? Atendimento ao cliente? Diretoria? Compliance?
> - Terão conhecimento técnico para interpretar métricas/gráficos, ou precisam de um resumo executivo?
 
**Resposta:**
```
Áreas hipotéticas do banco fictício que consumiriam essa análise:
- Customer Experience (CX) — visão geral da satisfação e dos pontos de atrito
- Produto — priorização de melhorias por funcionalidade/canal
- Atendimento — gargalos de resolução e canais mais sobrecarregados
- Operações — problemas técnicos recorrentes
- Dados — insumo para dashboards e monitoramento contínuo
 
O público combina perfis técnicos (Dados/Produto, que interpretam KPIs e tabelas
detalhadas) e não técnicos (CX/Atendimento/Operações, que precisam do Resumo
Executivo e das Recomendações em linguagem direta e acionável).
```
 
### Qual decisão o resultado deve apoiar?
>   O que será feito com base na análise?
> - Priorizar melhorias no app?
> - Identificar causas de insatisfação recorrentes?
> - Medir impacto de uma mudança recente (ex: nova política de tarifas)?
> - Alimentar um dashboard de acompanhamento contínuo?
 
**Resposta:**
```
Priorização de ações de melhoria na experiência do cliente, respondendo diretamente à
pergunta central do prompt mestre: "Quais são os principais problemas enfrentados pelos
clientes, qual o impacto desses problemas e quais ações deveriam ser priorizadas?"
 
Na prática, o resultado deve apoiar:
- Priorização de problemas por produto/canal usando uma metodologia objetiva de
  pontuação (volume + impacto + urgência + recorrência + satisfação + tempo de
  resolução), evitando priorizar só por volume;
- Direcionamento de recomendações acionáveis para áreas responsáveis específicas
  (CX, Produto, Atendimento, Operações), com KPI de acompanhamento definido;
- Diferenciação entre problemas críticos e urgentes de baixo esforço de correção;
- Base para decisões futuras de monitoramento contínuo (dashboard) — não é o
  objetivo final deste projeto, mas é um desdobramento natural.
 
Não é objetivo apoiar decisões de negócio reais (ex: aprovação de crédito, análise de
risco individual) — o escopo é estritamente experiência do cliente com dados fictícios.
```
 
---
 
## 2. Objetivo do Projeto
 
Analisar feedbacks fictícios de clientes de um banco digital — cobrindo app, Pix, cartões,
empréstimos, atendimento e outros pontos de contato — para transformar relatos individuais
em padrões mensuráveis. O resultado se destina às áreas de CX, Produto, Atendimento,
Operações e Dados, e deve apoiar a priorização objetiva de problemas e a definição de
ações concretas de melhoria na experiência do cliente, com evidências quantitativas e
recomendações claramente separadas de hipóteses.
 
---

## 3. Dados Utilizados (Fictícios)
 
- **Fonte:** dados gerados sinteticamente para fins de estudo/portfólio.
- **Aviso:** nenhum dado real de clientes, contas, CPF ou informações sensíveis é utilizado.
- **Estrutura esperada** (ajuste conforme seu dataset):

| Campo | Descrição |
|---|---|
| `id_feedback` | Identificador único (fictício) |
| `canal` | Origem do feedback (app, chat, e-mail...) |
| `data` | Data do feedback |
| `produto` | Produto/serviço relacionado |
| `nota` | Nota numérica (se aplicável) |
| `texto` | Texto livre do feedback |
| `sentimento` | Classificação (positivo/neutro/negativo) — se calculado |
 
---

## 4. Metodologia
 
A análise segue um processo estruturado em 8 etapas, definido no prompt mestre do projeto (ver [`docs/PROMPT-METODOLOGIA.md`](docs/PROMPT-METODOLOGIA.md)):
 
1. **Qualidade dos dados** — identificação de nulos, duplicidades, inconsistências e outliers, sem correção silenciosa.
2. **Análise descritiva** — volumes, distribuição de notas, sentimento, canal, produto, taxa e tempo de resolução.
3. **Segmentação** — comparação entre produto, canal, período, categoria, sentimento e urgência.
4. **Análise de problemas** — identificação de problemas recorrentes, críticos e em crescimento.
5. **Análise de relacionamento** — cruzamentos entre variáveis, sem confundir correlação com causalidade.
6. **Priorização** — metodologia objetiva combinando volume, impacto, urgência, recorrência e satisfação.
7. **Insights** — cada um estruturado como fato → evidência → interpretação → hipótese → impacto.
8. **Recomendações** — ação, responsável, prioridade, impacto esperado e KPI de acompanhamento para cada problema identificado.
**Papel assumido na análise:** Data Analyst Sênior, Customer Experience Analyst, Business Intelligence Analyst e consultor de tomada de decisão orientada por dados — atuando de forma integrada para transformar feedbacks individuais em padrões mensuráveis e decisões acionáveis.
 
**Regras críticas seguidas:** uso exclusivo dos dados fornecidos (sem inventar números ou causas), separação explícita entre fato/interpretação/hipótese/recomendação, e nenhuma exposição de dados pessoais — reforçando o caráter fictício e sintético de todo o dataset.
 
📄 Prompt completo: [`docs/PROMPT-METODOLOGIA.md`](docs/PROMPT-METODOLOGIA.md)
 
---

## 5. Resultados Esperados
 
O relatório final de análise segue o formato definido no prompt mestre, contendo:
 
- **Resumo Executivo** (máx. 5 pontos)
- **Qualidade dos Dados** (tabela de problemas identificados e tratamento recomendado)
- **Principais Indicadores** (KPIs com interpretação e relevância)
- **Principais Problemas** (por produto, volume, impacto, urgência e prioridade)
- **Principais Insights** (fato → evidência → interpretação → hipótese → impacto)
- **Recomendações** (ação, responsável, prioridade e KPI de acompanhamento)
- **Limitações** (o que não pode ser sustentado pelos dados disponíveis)
- **Próximas Análises** sugeridas

## 6. Limitações
 
- Dados fictícios podem não capturar toda a complexidade de feedbacks reais.
- Resultados servem para fins de estudo/demonstração, não para decisões reais de negócio.

---
 
## 👤 Autor

**Gustavo Freitas**
GitHub: [@gustavfreitas](https://github.com/gustavfreitas)
