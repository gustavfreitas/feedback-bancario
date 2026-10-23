# Auditoria de Dados

> Dados fictícios/sintéticos. Fonte: `load/relatorio_completo_etl.xlsx`.

## Abas da planilha

| Aba | Conteúdo | Uso |
|---|---|---|
| `relatorio_manifestacoes (2)` | 45 linhas × 8 colunas, limpa | **Usada na análise** |
| `relatorio_manifestacoes` | Mesmo conteúdo como CSV em uma coluna, com encoding corrompido (`Ã§Ã£o`) e 9ª coluna `product_or_service_name` vazia | Apenas auditoria |
| `ListaErros` | 22 linhas com o literal `[List]` (artefato de exportação) | Descartada |

## Qualidade (aba usada)

| Verificação | Resultado |
|---|---|
| Registros | 45 |
| Nulos | 0% em todas as colunas |
| Duplicidades | 0 (`manifestation_id` único) |
| Categorias | Padronizadas, sem variações de grafia |
| Período | 05/01/2026 a 13/08/2026 |
| Escala de nota | 1 a 5 (NPS não calculável) |

**Classificação:** pronta para análise, com ressalvas.

## Lacunas

- `product_or_service_name` vazio em 45/45 linhas; `manifestation_products` nunca populada. Sem dimensão de produto oficial.
- Não existem status, tempo de resolução, região nem perfil de cliente.
- n = 45: grupos tipo × canal têm de 1 a 6 casos. Percentuais são indicativos.
- `docs/CONCLUSAO-ANALISE.md` cita o registro de ID 46 como perdido na exportação.

## Tratamento aplicado (não destrutivo)

Os dados originais não são alterados. `analysis/full_analysis.py` gera uma camada tratada (`dataset_tratado.csv`) com campos derivados: mês, sentimento negativo/positivo, reclamação, peso de urgência, CSAT e tópico derivado do texto por palavra-chave (estimativa, não dado oficial).

## Nota sobre scores de prioridade

Este repositório tem duas versões: `docs/CONCLUSAO-ANALISE.md` (Telefone 0,82, WhatsApp 0,81) e `RELATORIO.md` (0,742 e 0,733). As normalizações diferem; o ranking é o mesmo. A fórmula vigente é a do `RELATORIO.md`.
