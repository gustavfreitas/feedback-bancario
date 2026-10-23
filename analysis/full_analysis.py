from pathlib import Path
import pandas as pd
import numpy as np
import json, re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "output"; OUT.mkdir(exist_ok=True)
xl = pd.ExcelFile(ROOT / "load" / "relatorio_completo_etl.xlsx")
df = xl.parse('relatorio_manifestacoes (2)').copy()

# ---------------------------------------------------------------------------
# LIMPEZA (camada tratada - nao altera o arquivo original)
# ---------------------------------------------------------------------------
df['feedback_text'] = df['feedback_text'].str.strip()
df['channel_name'] = df['channel_name'].str.strip()
df['type_name'] = df['type_name'].str.strip()
df['sentiment'] = df['sentiment'].str.strip().str.lower()
df['urgency'] = df['urgency'].str.strip().str.lower()
df['created_at'] = pd.to_datetime(df['created_at'])
df['month'] = df['created_at'].dt.to_period('M').astype(str)

# categorias derivadas
df['is_negative'] = df['sentiment'].eq('negativo')
df['is_positive'] = df['sentiment'].eq('positivo')
df['is_complaint'] = df['type_name'].eq('Reclamação')
urgency_weight = {'baixa': 0, 'media': 1, 'alta': 2, 'critica': 3}
df['urgency_weight'] = df['urgency'].map(urgency_weight)

# CSAT: escala 1-5 -> positivo definido como nota >= 4 (padrao de mercado
# para escalas Likert 1-5: top-2-box)
df['is_csat_positive'] = df['satisfaction_score'] >= 4

# dimensao de produto/topico DERIVADA do texto livre (heuristica por
# palavras-chave). Documentada como estimativa, nao como dado oficial,
# ja que o campo estruturado 'product_or_service_name' existe no schema
# mas nunca foi populado (ver auditoria).
KEYWORDS = [
    ('Pix', r'\bpix\b'),
    ('Cartão', r'cart[aã]o'),
    ('Aplicativo/App', r'\baplicativo\b|\bapp\b'),
    ('Empréstimo', r'empr[eé]stimo|renegoci|d[ií]vida'),
    ('Transferência', r'transfer[eê]ncia'),
    ('Tarifas/Conta', r'tarifa|conta corrente|cadastral|extrato|boleto'),
    ('Atendimento/Processo', r'atendimento|fila|caixa|hor[aá]rio|menu de op'),
]
def classify_topic(text):
    t = text.lower()
    hits = [name for name, pat in KEYWORDS if re.search(pat, t)]
    return hits[0] if hits else 'Outros/Não classificado'
df['topic_derived'] = df['feedback_text'].apply(classify_topic)

# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
n = len(df)
kpi = {}
kpi['total_feedbacks'] = n
kpi['nota_media'] = round(df['satisfaction_score'].mean(), 2)
kpi['nota_mediana'] = float(df['satisfaction_score'].median())
kpi['csat_pct'] = round(df['is_csat_positive'].mean() * 100, 1)
kpi['pct_negativo'] = round(df['is_negative'].mean() * 100, 1)
kpi['pct_positivo'] = round(df['is_positive'].mean() * 100, 1)
kpi['pct_neutro'] = round((100 - kpi['pct_negativo'] - kpi['pct_positivo']), 1)
kpi['taxa_reclamacao'] = round(df['is_complaint'].mean() * 100, 1)
kpi['pct_urgencia_alta_critica'] = round(df['urgency'].isin(['alta','critica']).mean()*100, 1)
kpi['nps_calculavel'] = False
kpi['nps_motivo'] = "Escala de satisfacao vai de 1 a 5, incompativel com a metodologia NPS (0-10). NPS nao calculavel com os dados disponiveis."

# nota media por sentimento (validacao de consistencia interna)
nota_por_sentimento = df.groupby('sentiment')['satisfaction_score'].mean().round(2).to_dict()

# ---------------------------------------------------------------------------
# ANALISE POR CANAL
# ---------------------------------------------------------------------------
canal = df.groupby('channel_name').agg(
    volume=('manifestation_id','count'),
    nota_media=('satisfaction_score','mean'),
    pct_negativo=('is_negative','mean'),
    pct_positivo=('is_positive','mean'),
    urgencia_media=('urgency_weight','mean'),
).reset_index()
canal['pct_negativo'] = (canal['pct_negativo']*100).round(1)
canal['pct_positivo'] = (canal['pct_positivo']*100).round(1)
canal['nota_media'] = canal['nota_media'].round(2)
canal['urgencia_media'] = canal['urgencia_media'].round(2)
canal = canal.sort_values('pct_negativo', ascending=False)

# ---------------------------------------------------------------------------
# ANALISE POR TIPO (categoria da manifestacao)
# ---------------------------------------------------------------------------
tipo = df.groupby('type_name').agg(
    volume=('manifestation_id','count'),
    nota_media=('satisfaction_score','mean'),
    pct_negativo=('is_negative','mean'),
    urgencia_media=('urgency_weight','mean'),
).reset_index()
tipo['pct_negativo'] = (tipo['pct_negativo']*100).round(1)
tipo['nota_media'] = tipo['nota_media'].round(2)
tipo['urgencia_media'] = tipo['urgencia_media'].round(2)
tipo = tipo.sort_values('volume', ascending=False)

# ---------------------------------------------------------------------------
# ANALISE POR TOPICO DERIVADO (proxy de produto)
# ---------------------------------------------------------------------------
topico = df.groupby('topic_derived').agg(
    volume=('manifestation_id','count'),
    nota_media=('satisfaction_score','mean'),
    pct_negativo=('is_negative','mean'),
).reset_index()
topico['pct_negativo'] = (topico['pct_negativo']*100).round(1)
topico['nota_media'] = topico['nota_media'].round(2)
topico = topico.sort_values('volume', ascending=False)

# ---------------------------------------------------------------------------
# MATRIZ DE PRIORIZACAO (Tipo x Canal, apenas grupos com reclamacao/problema)
# Prioridade = Volume_norm*0.30 + Impacto_norm*0.30 + Urgencia_norm*0.25 + Recorrencia_norm*0.15
# ---------------------------------------------------------------------------
problem_types = ['Reclamação', 'Problema Técnico']
prob = df[df['type_name'].isin(problem_types)].copy()
grp = prob.groupby(['type_name','channel_name']).agg(
    volume=('manifestation_id','count'),
    nota_media=('satisfaction_score','mean'),
    urgencia_media=('urgency_weight','mean'),
    meses_distintos=('month','nunique'),
).reset_index()

def norm(s):
    if s.max() == s.min():
        return s.apply(lambda x: 1.0)
    return (s - s.min()) / (s.max() - s.min())

grp['volume_norm'] = norm(grp['volume'])
grp['impacto_norm'] = norm(5 - grp['nota_media'])
grp['urgencia_norm'] = norm(grp['urgencia_media'])
grp['recorrencia_norm'] = norm(grp['meses_distintos'])
grp['prioridade_score'] = (
    grp['volume_norm']*0.30 + grp['impacto_norm']*0.30 +
    grp['urgencia_norm']*0.25 + grp['recorrencia_norm']*0.15
).round(3)

def classifica(score):
    if score >= 0.70: return '🔴 Crítico'
    if score >= 0.50: return '🟠 Alto'
    if score >= 0.30: return '🟡 Médio'
    return '🟢 Baixo'
grp['classe'] = grp['prioridade_score'].apply(classifica)
grp = grp.sort_values('prioridade_score', ascending=False)

# ---------------------------------------------------------------------------
# PARETO dos motivos de insatisfacao (type_name entre feedbacks negativos)
# ---------------------------------------------------------------------------
neg = df[df['is_negative']]
pareto = neg['type_name'].value_counts().reset_index()
pareto.columns = ['motivo','qtd']
pareto['pct'] = (pareto['qtd'] / pareto['qtd'].sum() * 100).round(1)
pareto['pct_acum'] = pareto['pct'].cumsum().round(1)

# ---------------------------------------------------------------------------
# TEMPORAL
# ---------------------------------------------------------------------------
temporal = df.groupby('month').agg(
    volume=('manifestation_id','count'),
    nota_media=('satisfaction_score','mean'),
    pct_negativo=('is_negative','mean'),
).reset_index()
temporal['pct_negativo'] = (temporal['pct_negativo']*100).round(1)
temporal['nota_media'] = temporal['nota_media'].round(2)

# ---------------------------------------------------------------------------
# SAIDA
# ---------------------------------------------------------------------------
print("KPIs:", json.dumps(kpi, indent=2, ensure_ascii=False))
print("\nNota media por sentimento:", nota_por_sentimento)
print("\n=== CANAL ===\n", canal.to_string(index=False))
print("\n=== TIPO ===\n", tipo.to_string(index=False))
print("\n=== TOPICO DERIVADO ===\n", topico.to_string(index=False))
print("\n=== PRIORIZACAO (top 12) ===\n", grp[['type_name','channel_name','volume','nota_media','urgencia_media','meses_distintos','prioridade_score','classe']].to_string(index=False))
print("\n=== PARETO ===\n", pareto.to_string(index=False))
print("\n=== TEMPORAL ===\n", temporal.to_string(index=False))

# salvar dataset tratado
df.to_csv(OUT / 'dataset_tratado.csv', index=False)

# salvar tudo em JSON para o dashboard
out = {
    'kpi': kpi,
    'nota_por_sentimento': nota_por_sentimento,
    'canal': canal.to_dict('records'),
    'tipo': tipo.to_dict('records'),
    'topico': topico.to_dict('records'),
    'priorizacao': grp[['type_name','channel_name','volume','nota_media','urgencia_media','meses_distintos','prioridade_score','classe']].to_dict('records'),
    'pareto': pareto.to_dict('records'),
    'temporal': temporal.to_dict('records'),
}
with open(OUT / 'dashboard_data.json','w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\nOK - JSON salvo")
