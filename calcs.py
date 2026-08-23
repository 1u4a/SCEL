from tabela_Eletros import BancoDeDados

TARIFAMT = 0.899

def calcular_potencia_total(aparelhos, banco_dados):
    potencia_total = 0
    detalhes = {}
    for nome, quantidade in aparelhos.items():
        if nome in banco_dados:
            potencia = banco_dados[nome]['potencia_w'] * quantidade
            potencia_total += potencia
            detalhes[nome] = potencia
    return potencia_total, detalhes

def calcular_consumo(potencia_total, horas_por_dia=5, dias=30):
    return (potencia_total * horas_por_dia * dias) / 1000


def calcular_valor(consumo_kwh):
    return consumo_kwh * TARIFAMT


def calcular_tudo(aparelhos, banco_dados, horas_por_dia=5, dias=30):
    potencia_total, detalhes_potencia = calcular_potencia_total(aparelhos, banco_dados)
    
    consumo_kwh = calcular_consumo(potencia_total, horas_por_dia, dias)
    
    valor_reais = calcular_valor(consumo_kwh)
    
    consumo_individual = {}
    for nome, potencia in detalhes_potencia.items():
        consumo_individual[nome] = (potencia * horas_por_dia * dias) / 1000
    
    return {
        'potencia_total_w': potencia_total,
        'consumo_kwh': consumo_kwh,
        'valor_reais': valor_reais,
        'detalhes_potencia': detalhes_potencia,
        'detalhes_consumo': consumo_individual
    }

def identificarOsCaros(consumo_individual, top_n=3):
    return sorted(consumo_individual.items(), key=lambda x: x[1], reverse=True)[:top_n]


def calcular_percentuais(consumo_individual, consumo_total):
    percentuais = {}
    for nome, consumo in consumo_individual.items():
        percentuais[nome] = (consumo / consumo_total) * 100
    return percentuais