# Relatório Final — Customer Experience Analytics (Banco Digital Fictício)

> Dados sintéticos. Este relatório simula uma operação de Customer Experience de uma
> instituição financeira; as métricas seguem práticas reais de análise de dados e CX, mas
> os resultados **não representam** uma instituição financeira real.

Fonte: [`gustavfreitas/feedback-bancario`](https://github.com/gustavfreitas/feedback-bancario/tree/Principal/load)
→ `load/relatorio_completo_etl.xlsx`

---

## 1. Dataset

| Item | Valor |
|---|---|
| Registros | 45 |
| Campos (planilha tratada) | 8: `manifestation_id`, `feedback_text`, `satisfaction_score`, `sentiment`, `urgency`, `created_at`, `channel_name`, `type_name` |
| Período | 05/jan/2026 a 13/ago/2026 (8 meses) |
| Qualidade | **Pronta para análise** — 0% nulos, 0 duplicidades, `manifestation_id` único em 100% das linhas, categorias padronizadas (sem variações de grafia) |

**Achados da auditoria (planilha tem 3 abas):**

1. **`relatorio_manifestacoes (2)`** — dataset limpo, 45 linhas × 8 colunas, usado nesta análise.
2. **`relatorio_manifestacoes`** — mesmo conteúdo colado como CSV bruto em uma única coluna, com encoding corrompido (`Ã§Ã£o` no lugar de `ção`). O cabeçalho traz uma 9ª coluna, `product_or_service_name`, que está **vazia em 100% das 45 linhas** — confirma que o campo de produto existe no schema do projeto mas nunca foi populado (consistente com a limitação já documentada em `docs/CONCLUSAO-ANALISE.md` do repositório original).
3. **`ListaErros`** — 22 linhas contendo apenas o literal `"[List]"`. Não é dado real; é um artefato de exportação (provável referência de tabela dinâmica do Excel não resolvida). Não impacta a análise, mas é uma inconsistência que vale corrigir na próxima exportação.

**Consequência prática:** não é possível segmentar por produto (Pix, cartão, empréstimo etc.) com dado oficial. Nesta análise, um **tópico derivado do texto livre** (heurística por palavra-chave) foi criado como proxy — tratado explicitamente como estimativa, não como dado estruturado.

---

## 2. KPIs

| KPI | Resultado | Interpretação |
|---|---:|---|
| Total de feedbacks | 45 | Amostra pequena — leia todos os percentuais abaixo como indicativos, não conclusivos (1 registro ≈ 2,2% do total) |
| Nota média | 3,00 / 5 | Ponto médio da escala, mas mascara uma distribuição **bimodal** (polarização entre satisfeitos e insatisfeitos), não uma experiência "neutra" |
| CSAT (nota ≥ 4, top-2-box) | 37,8% | Menos de 4 em cada 10 clientes avaliam a experiência como boa/ótima |
| % Negativo (sentimento) | 42,2% | Quase metade das manifestações expressa insatisfação |
| % Positivo (sentimento) | 37,8% | Base de elogios relevante — útil para identificar boas práticas a replicar |
| Taxa de reclamação | 26,7% | 12 das 45 manifestações são reclamações formais (maior categoria isolada) |
| % Urgência alta/crítica | 42,2% | O problema não é só volume — quase metade dos casos exige resposta rápida |
| NPS | **Não calculável** | Escala de satisfação é 1–5; a metodologia NPS exige escala 0–10. Calcular NPS aqui seria metodologicamente incorreto. |

---

## 3. Top 5 Insights

**Insight 01 — Reclamações por Telefone e WhatsApp são o único risco recorrente**
- **Evidência:** os dois grupos têm os maiores scores de prioridade (0,74 e 0,73) entre 12 combinações Tipo×Canal — 3 casos cada, nota média 1,33, urgência média acima de 2,3 (escala 0–3), e recorrência em 2–3 meses distintos.
- **Impacto:** juntos representam metade dos casos de prioridade Alta/Crítica identificados.
- **Recomendação:** Atendimento deve auditar scripts e fluxo de escalonamento desses dois canais nos últimos 3 meses antes de qualquer ação genérica de "melhorar atendimento".

**Insight 02 — Agosto/2026 é o ponto mais crítico da série temporal**
- **Evidência:** nota média de 1,5 e 100% dos 4 feedbacks do mês são negativos — o pior resultado dos 8 meses da série (média geral do período: 34,7% negativo/mês).
- **Impacto:** se a tendência persistir, o % negativo mensal pode superar o patamar histórico em mais de 30 p.p.
- **Recomendação:** CX deve revisar individualmente os 4 casos de agosto para descartar causa técnica pontual antes de tratar como tendência (amostra de 4 casos ainda não confirma mudança estrutural).

**Insight 03 — A ausência de dado de produto é a maior lacuna analítica do projeto**
- **Evidência:** o campo `product_or_service_name` existe no schema mas está vazio em 45/45 linhas, tanto na planilha tratada quanto na bruta.
- **Impacto:** qualquer priorização por produto hoje depende de heurística por palavra-chave no texto livre, sujeita a erro de classificação e amostras de 3 a 9 casos por tópico — insuficiente para decisão.
- **Recomendação:** Tecnologia/Dados deve popular a tabela associativa de produto antes da próxima rodada de priorização.

**Insight 04 — Nenhum canal isolado concentra o problema (achado negativo relevante)**
- **Evidência:** Aplicativo, Telefone e WhatsApp empatam com 50% de negativos cada; os 19 feedbacks negativos se distribuem de 10,5% a 21,1% entre os 6 canais — sem concentração 80/20 clássica.
- **Impacto:** uma correção pontual em um único canal não resolveria a maior parte do problema; a causa provável é transversal (ex.: processo de atendimento, não uma falha de canal específico).
- **Recomendação:** tratar a melhoria como iniciativa cross-canal, não como projeto de um canal isolado.

**Insight 05 — A distribuição de notas é bimodal, não normal**
- **Evidência:** pico em nota 2 (12 casos) e um segundo agrupamento em notas 4–5 (17 casos); nota 3 (neutro genuíno) é a menos comum entre os extremos (9 casos).
- **Impacto:** a nota média de 3,0 esconde uma polarização real — a experiência do cliente tende a ser claramente boa ou claramente ruim, raramente "mediana".
- **Recomendação:** CX deve monitorar o % em notas 1–2 separadamente do % em notas 4–5, em vez de acompanhar apenas a média geral, que oculta essa polarização.

---

## 4. Top 5 Problemas (ranking por score de prioridade)

Metodologia: `Prioridade = Volume_norm×0,30 + Impacto_norm×0,30 + Urgência_norm×0,25 + Recorrência_norm×0,15`, normalizado dentro do conjunto de 12 combinações Tipo×Canal com Reclamação/Problema Técnico. Impacto = (5 − nota média) / 4.

| # | Problema | Canal | Volume | Nota média | Urgência (0–3) | Meses | Score | Classe |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Reclamação | Telefone | 3 | 1,33 | 2,67 | 2 | 0,742 | 🔴 Crítico |
| 2 | Reclamação | WhatsApp | 3 | 1,33 | 2,33 | 3 | 0,733 | 🔴 Crítico |
| 3 | Problema Técnico | Agência | 1 | 1,00 | 3,00 | 1 | 0,550 | 🟠 Alto |
| 3 | Reclamação | Agência | 1 | 1,00 | 3,00 | 1 | 0,550 | 🟠 Alto |
| 5 | Reclamação | Aplicativo | 2 | 1,50 | 2,50 | 2 | 0,500 | 🟠 Alto |

---

## 5. Recomendações por área

### Produto
- Investigar hipótese de atrito em Pix (66,7% negativo, n=3 — amostra pequena) somente após dado estruturado de produto estar disponível.
- Revisar a jornada de Aplicativo — maior volume entre canais com 50% de negativos.

### Tecnologia
- Popular a tabela/campo de produto (`product_or_service_name`) na próxima carga de dados.
- Investigar causa técnica dos 4 casos negativos de agosto/2026.
- Adicionar campo de tempo de resolução ao schema para viabilizar métricas de SLA.

### Atendimento
- Auditar scripts e fluxo de escalonamento de Telefone e WhatsApp (últimos 3 meses).
- Mapear causa raiz dos 3 casos de Reclamação/Telefone com urgência crítica.

### Operações
- Avaliar horário/capacidade de atendimento na Agência (menções a fila e horário aparecem no texto livre dos feedbacks).

### CX
- Acompanhar CSAT e % negativo mensal como indicador contínuo.
- Monitorar % em notas 1–2 separadamente da média geral (distribuição bimodal).
- Ampliar a amostra fictícia (hoje 45 registros) para reduzir a margem de incerteza dos percentuais.

---

## 6. Limitações

- **Amostra pequena (n=45):** cada registro equivale a ~2,2% do total — todos os percentuais devem ser lidos como indicativos, não como estimativas populacionais confiáveis.
- **Dado de produto ausente:** a análise por produto usa uma classificação heurística por palavra-chave no texto livre, não um dado estruturado oficial — sujeita a erro de classificação.
- **NPS não calculável:** a escala de satisfação disponível (1–5) é incompatível com a metodologia NPS (0–10).
- **Ausência de tempo de resolução:** não é possível calcular SLA nem cruzar urgência × tempo de resolução, como um projeto de CX maduro normalmente faria.
- **Ausência de causalidade:** todas as associações reportadas (ex.: canal × sentimento, tipo × urgência) são correlacionais. Nenhuma relação de causa foi testada nem deve ser assumida.
- **Viés potencial de classificação de tópico:** a categorização derivada do texto (Pix, Cartão, Aplicativo etc.) é uma heurística por palavra-chave simples e pode classificar incorretamente casos ambíguos ou que mencionam mais de um tema.
- **Natureza sintética dos dados:** todos os feedbacks foram gerados artificialmente para fins de portfólio/estudo. Os resultados não devem ser usados para decisões de negócio reais.

---

## Anexos entregues

- `dashboard.html` — painel interativo (4 páginas: Visão Executiva, Customer Experience, Análise de Problemas, Recomendações)
- `dataset_tratado.csv` — camada de dados limpa e enriquecida com campos derivados (`month`, `is_negative`, `is_csat_positive`, `urgency_weight`, `topic_derived` etc.)
- `full_analysis.py` — script Python reprodutível (auditoria → limpeza → KPIs → priorização → Pareto → temporal)
- `dashboard_data.json` — dados agregados usados pelo dashboard
