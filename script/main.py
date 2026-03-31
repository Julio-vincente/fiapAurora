import random

# --- 1.1 Simulacao da telemetria ---
telemetria = {
    "temp_interna_C":        round(random.uniform(15, 28), 1),
    "temp_externa_C":        round(random.uniform(-60, 60), 1),
    "integridade_estrutural": random.choice([0, 1, 1, 1, 1]),
    "nivel_energia_pct":     round(random.uniform(60, 100), 1),
    "pressao_tanques_bar":   round(random.uniform(100, 400), 1),
    "modulo_navegacao":      random.choice([0, 1, 1, 1]),
    "modulo_comunicacao":    random.choice([0, 1, 1, 1]),
    "modulo_suporte_vital":  random.choice([0, 1, 1, 1]),
}

print("=== DADOS DE TELEMETRIA ===")
for chave, valor in telemetria.items():
    print(f"  {chave}: {valor}")

# --- 1.3 Verificacao de pre-lancamento ---
FAIXAS = {
    "temp_interna_C":      (18, 25),
    "temp_externa_C":      (-50, 50),
    "pressao_tanques_bar": (150, 350),
}
ENERGIA_MIN = 80
MODULOS = ["modulo_navegacao", "modulo_comunicacao", "modulo_suporte_vital"]


def verificar_lancamento(dados):
    falhas = []

    for chave, (minimo, maximo) in FAIXAS.items():
        if dados[chave] < minimo or dados[chave] > maximo:
            falhas.append(f"{chave}: {dados[chave]} (faixa: {minimo} a {maximo})")

    if dados["integridade_estrutural"] != 1:
        falhas.append("Integridade estrutural comprometida")

    if dados["nivel_energia_pct"] < ENERGIA_MIN:
        falhas.append(f"Energia insuficiente: {dados['nivel_energia_pct']}%")

    for mod in MODULOS:
        if dados[mod] != 1:
            falhas.append(f"{mod} inoperante")

    return falhas


falhas = verificar_lancamento(telemetria)

print()
if falhas:
    print("RESULTADO: DECOLAGEM ABORTADA")
    print("Falhas detectadas:")
    for f in falhas:
        print(f"  - {f}")
else:
    print("RESULTADO: PRONTO PARA DECOLAR")

# --- 1.4 Analise energetica ---
CAPACIDADE_TOTAL = 5000
CONSUMO_DECOLAGEM = 1200
PERDA_PCT = 5
CONSUMO_CRUZEIRO = 150

carga = telemetria["nivel_energia_pct"]
energia_disponivel = CAPACIDADE_TOTAL * (carga / 100)
perda = energia_disponivel * (PERDA_PCT / 100)
energia_util = energia_disponivel - perda
energia_pos_decolagem = energia_util - CONSUMO_DECOLAGEM
autonomia = max(energia_pos_decolagem / CONSUMO_CRUZEIRO, 0)

print("\n=== ANALISE ENERGETICA ===")
print(f"  Capacidade total:      {CAPACIDADE_TOTAL} kWh")
print(f"  Carga atual:           {carga}% = {energia_disponivel:.1f} kWh")
print(f"  Perdas ({PERDA_PCT}%):          -{perda:.1f} kWh")
print(f"  Energia util:          {energia_util:.1f} kWh")
print(f"  Consumo decolagem:     -{CONSUMO_DECOLAGEM} kWh")
print(f"  Energia pos-decolagem: {energia_pos_decolagem:.1f} kWh")
print(f"  Autonomia estimada:    {autonomia:.1f} horas")

# --- 1.5 Classificacao e risco ---
CLASSIFICACAO = {
    "Ambientais":            ["temp_interna_C", "temp_externa_C"],
    "Estruturais/Mecanicos": ["integridade_estrutural", "pressao_tanques_bar"],
    "Sistemicos":            ["nivel_energia_pct"] + MODULOS,
}

print("\n=== CLASSIFICACAO DOS DADOS ===")
for categoria, chaves in CLASSIFICACAO.items():
    print(f"\n  [{categoria}]")
    for c in chaves:
        print(f"    {c}: {telemetria[c]}")

risco = "BAIXO"
if telemetria["integridade_estrutural"] != 1 or sum(telemetria[m] for m in MODULOS) < 2:
    risco = "ALTO"
elif telemetria["nivel_energia_pct"] < 80 or not (150 <= telemetria["pressao_tanques_bar"] <= 350):
    risco = "MEDIO"

print(f"\nNIVEL DE RISCO: {risco}")
