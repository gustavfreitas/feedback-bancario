# Conclusão da Análise — Feedbacks Bancários (Dados Fictícios)

> Documento gerado seguindo o processo analítico definido em [`PROMPT-METODOLOGIA.md`](./PROMPT-METODOLOGIA.md), com base nos 45 registros exportados em [`staged/relatorio_manifestacoes.csv`](../staged/relatorio_manifestacoes.csv).

---

## Resumo Executivo

1. **42% dos feedbacks (19 de 45) são negativos**, concentrados em Reclamação (12) e Problema Técnico (7) — juntos, 42% do volume total.
2. **Telefone e WhatsApp são os canais mais críticos**: cada um concentra 3 reclamações com urgência média "alta/crítica" (peso médio 2,3–2,7 em escala 0–3), o maior nível entre todos os canais.
3. **Nota de satisfação está fortemente ligada ao sentimento** (correlação direta e esperada): negativo ≈ 1,6, neutro = 3,0, positivo ≈ 4,5 — validando a consistência dos dados e o uso da nota como proxy de sentimento.
4. **Agência e Chat têm o melhor desempenho relativo**, com apenas 28,6% de feedbacks negativos, contra 50% em Aplicativo, Telefone e WhatsApp.
5. **A base não permite associar reclamações a produtos específicos** (Pix, cartão, etc.) — a tabela de junção `manifestation_products` existe no schema mas nunca foi populada, o que é a maior lacuna de dados do projeto.

---

## Qualidade dos Dados

| Problema | Quantidade | Impacto | Tratamento recomendado |
|---|---|---|---|
| `manifestation_products` sem registros | 45/45 linhas (100%) | Alto — impossibilita responder "qual produto gera mais atrito?", que é uma pergunta central do prompt mestre | Popular a tabela associativa antes da próxima rodada de análise; sem isso, qualquer segmentação por produto seria inventada |
| Amostra pequena (n=45) | — | Médio — qualquer percentual está sujeito a grande variação (1 registro ≈ 2,2% do total) | Tratar todos os percentuais como indicativos, não conclusivos; ampliar a base fictícia para pelo menos 200–300 registros antes de decisões |
| Ausência de campo de tempo de resolução | 45/45 linhas | Médio — o prompt mestre pede "urgência × tempo de resolução", que não pode ser calculado | Adicionar `status_resolucao` e `tempo_resolucao` ao schema em uma próxima iteração |
| Ausência de campo de região/tipo de cliente | 45/45 linhas | Baixo para este escopo — mencionado no prompt mestre mas não crítico para o objetivo de CX | Registrar como escopo não coberto, não como erro |
| 1 registro perdido na exportação (ID 46 do INSERT original não chegou ao banco) | 1 linha | Baixo — não altera conclusões | Conferir se o `INSERT` foi cortado (linha final sem `;`, problema já identificado e corrigido anteriormente no projeto) |
| Duplicidades | 0 | — | Nenhuma ação necessária — todos os 45 `manifestation_id` são únicos |
| Nulos | 0 em nenhuma coluna analisada | — | Nenhuma ação necessária |

---

## Principais Indicadores

| KPI | Valor | Interpretação | Relevância |
|---|---|---|---|
| Volume total de feedbacks | 45 | Base pequena, típica de piloto/protótipo | Define o quanto os percentuais abaixo devem ser lidos com cautela |
| % Sentimento negativo | 42,2% (19/45) | Quase metade dos feedbacks expressa insatisfação | Sinaliza atenção geral em CX, não só em pontos isolados |
| % Sentimento positivo | 37,8% (17/45) | Base de elogios relevante, útil para identificar o que funciona bem | Pode orientar boas práticas a replicar entre canais |
| Nota média geral | 3,0 (escala 1–5) | Exatamente no meio da escala | Neutro no agregado, mas mascara a polarização (negativos ~1,6 vs. positivos ~4,5) |
| % Urgência alta/crítica | 42,2% (19/45) | Quase metade dos casos exige atenção rápida | Reforça que o problema não é só volume, mas também criticidade |
| Canal com maior % de negativos | Aplicativo, Telefone e WhatsApp (50% cada) | Empate entre 3 canais | Nenhum canal isolado domina — o problema é transversal, não de um canal só |
| Canal com menor % de negativos | Agência e Chat (28,6% cada) | Menor insatisfação relativa | Podem servir de referência para investigar boas práticas de atendimento |
| Tipo mais frequente | Reclamação (12, 26,7%) | Maior categoria isolada | Confirma foco correto do projeto em tratar reclamações |

---

## Principais Problemas

| Problema | Canal | Volume | Impacto (nota média) | Urgência (peso médio 0–3) | Prioridade |
|---|---|---|---|---|---|
| Reclamações | Telefone | 3 | 1,33 | 2,67 | **1º (0,82)** |
| Reclamações | WhatsApp | 3 | 1,33 | 2,33 | **2º (0,81)** |
| Reclamações | Aplicativo | 2 | 1,50 | 2,50 | 3º (0,61) |
| Problema Técnico | Agência | 1 | 1,00 | 3,00 | 4º (0,55) |
| Reclamações | Agência | 1 | 1,00 | 3,00 | 4º (0,55) |
| Reclamações | E-mail | 2 | 2,00 | 2,00 | 6º (0,45) |
| Problema Técnico | Aplicativo | 2 | 2,00 | 2,00 | 6º (0,45) |

*Fórmula de prioridade explicada na seção seguinte. Tabela completa (12 combinações) disponível nos dados brutos do projeto.*

---

## Metodologia de Priorização

Como pedido no prompt mestre, a prioridade **não é definida apenas por volume**. Foi usada a fórmula:

```
Prioridade = (Volume_norm × 0,30) + (Impacto_norm × 0,30) + (Urgência_norm × 0,25) + (Recorrência_norm × 0,15)
```

- **Volume_norm**: quantidade de casos no grupo (Tipo × Canal), normalizada de 0 a 1 dentro do conjunto de problemas.
- **Impacto_norm**: `(5 − nota_média) / 4` — quanto menor a nota, maior o impacto.
- **Urgência_norm**: peso médio de urgência (baixa=0, média=1, alta=2, crítica=3), normalizado.
- **Recorrência_norm**: número de meses distintos em que o problema apareceu, normalizado.

Pesos maiores em volume e impacto (0,30 cada) porque o prompt mestre pede que gravidade pese tanto quanto frequência; urgência com peso intermediário (0,25); recorrência com peso menor (0,15) pela base temporal curta (8 meses) e amostra pequena, que limita a confiança nesse sinal.

**Nota de transparência:** a fórmula não inclui "tempo de resolução" porque esse dado não existe na base atual (ver Qualidade dos Dados).

---

## Principais Insights

**Insight 1 — Telefone e WhatsApp concentram a maior gravidade combinada**
- **Fato:** Telefone e WhatsApp têm as duas maiores pontuações de prioridade (0,82 e 0,81).
- **Evidência:** cada canal soma 3 reclamações com nota média 1,33 e peso de urgência acima de 2,3.
- **Interpretação:** não é o canal com mais volume (Aplicativo também tem 8 registros no total), mas sim onde as reclamações são simultaneamente frequentes, graves e urgentes.
- **Hipótese:** esses dois canais podem estar lidando com problemas que exigem escalonamento humano imediato (ex.: bloqueios, falhas de transação) e não estão resolvendo no primeiro contato — mas a base não tem `tempo_resolucao` para confirmar isso.
- **Impacto potencial:** se a hipótese se confirmar, é o ponto de maior risco de churn entre os canais avaliados.
- **Nível de confiança:** baixo — amostra de apenas 3 casos por canal.

**Insight 2 — Agência e Chat têm o melhor desempenho relativo, mas por razões diferentes**
- **Fato:** ambos têm 28,6% de feedbacks negativos, o menor índice entre os canais.
- **Evidência:** Agência tem 4 elogios em 7 registros; Chat tem 3 feedbacks neutros (dúvidas/solicitações) em 7 registros.
- **Interpretação:** a Agência parece ter bom desempenho em atendimento humano direto; o Chat parece atrair mais dúvidas do que reclamações, não necessariamente indicando melhor resolução de problemas.
- **Hipótese:** o perfil de uso de cada canal pode ser diferente (Chat para tirar dúvidas simples, Agência para resolver casos que já escalaram) — isso é uma hipótese sobre o *tipo* de demanda, não sobre qualidade de atendimento.
- **Impacto potencial:** replicar práticas da Agência sem entender essa diferença de perfil pode não gerar o efeito esperado em outros canais.
- **Nível de confiança:** baixo — 7 registros por canal é insuficiente para separar causa de correlação.

**Insight 3 — A nota de satisfação é internamente consistente com o sentimento**
- **Fato:** nota média por sentimento segue ordem esperada e sem sobreposição (negativo 1,63 / neutro 3,00 / positivo 4,53).
- **Evidência:** desvio-padrão dentro de cada grupo é baixo (negativo varia só entre 1–2, positivo só entre 4–5).
- **Interpretação:** os dados fictícios foram gerados de forma coerente — não há sinal de erro de rotulagem entre nota e sentimento.
- **Hipótese:** não aplicável — este é um insight de validação de qualidade, não uma hipótese de negócio.
- **Impacto potencial:** aumenta a confiança nos demais insights, já que a variável de sentimento não parece ruidosa.
- **Nível de confiança:** alto, para o propósito de validar a qualidade da base.

---

## Recomendações

| Problema | Ação | Responsável | Prioridade | KPI de acompanhamento |
|---|---|---|---|---|
| Reclamações concentradas em Telefone e WhatsApp com alta urgência | Revisar fluxo de escalonamento nesses dois canais; medir tempo até resolução (hoje ausente na base) | Atendimento | Alta | % de reclamações resolvidas no 1º contato, por canal |
| `manifestation_products` não populada | Popular a tabela de junção com o produto citado em cada feedback | Dados/Engenharia | Alta | % de feedbacks com produto associado (meta: 100%) |
| Ausência de campo de tempo de resolução | Adicionar `status_resolucao` e `tempo_resolucao` ao schema | Dados/Engenharia | Média | Tempo médio de resolução por canal |
| Amostra pequena limita confiança nos insights por canal | Ampliar geração de dados fictícios para 200+ registros antes da próxima rodada de decisão | Dados | Média | Tamanho da amostra por segmento (mínimo sugerido: 30 por canal) |
| Sentimento neutro concentrado em Dúvida/Solicitação no Chat | Avaliar se o Chat deveria ter uma base de autoatendimento (FAQ) para reduzir volume de dúvidas simples | Produto | Baixa | % de dúvidas resolvidas sem intervenção humana |

---

## Limitações

- **Não é possível** afirmar qual produto (Pix, cartão, empréstimo etc.) concentra mais reclamações — a tabela de associação existe no schema mas está vazia.
- **Não é possível** calcular tempo médio de resolução nem taxa de resolução — esses campos não existem na base atual.
- **Não é possível** afirmar causalidade em nenhum dos insights (ex.: "WhatsApp é pior porque...") — apenas correlações observadas em uma amostra pequena.
- **Não é possível** generalizar os percentuais com confiança estatística — com 45 registros, cada caso individual representa ~2,2% do total, tornando os percentuais sensíveis a poucos exemplos.
- **Não é possível** avaliar tendência real ao longo do tempo — a série de 8 meses tem poucos pontos por mês (4–6) para identificar sazonalidade ou tendência com confiança.
- Todos os dados são **sintéticos/fictícios**; nenhuma conclusão aqui deve ser tratada como refletindo um banco real.

---

## Próximas Análises

1. Popular `manifestation_products` e refazer a segmentação por produto — é a lacuna de maior valor para o objetivo do projeto.
2. Adicionar `tempo_resolucao` e `status_resolucao` para permitir a análise de relação "urgência × tempo de resolução" pedida no prompt mestre mas hoje inviável.
3. Ampliar a base fictícia (200–300+ registros) para reduzir a sensibilidade estatística a casos isolados.
4. Construir um dashboard (Power BI ou Excel dinâmico) consumindo o schema PostgreSQL diretamente, para tornar esta análise contínua em vez de um snapshot único.
5. Repetir esta mesma metodologia comparando dois períodos (ex.: primeiro semestre vs. segundo) para testar se os canais críticos (Telefone, WhatsApp) se mantêm estáveis ao longo do tempo.
