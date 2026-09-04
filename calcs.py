from tabela_Eletros import BancoDeDados

TARIFA_BASE_MT = 0.899

BANDEIRAS_TARIFARIAS = {
    'verde': 0.0,
    'amarela': 0.01885,
    'vermelha_1': 0.04463,
    'vermelha_2': 0.07877,
    'escassez_hidrica': 0.14200
}

def calcular_consumo_item(potencia_w, quantidade, horas_dia, dias_mes):
    potencia_kw = (potencia_w * quantidade) / 1000.0
    consumo_kwh = potencia_kw * horas_dia * dias_mes
    return consumo_kwh

def obter_tarifa_final(bandeira='verde'):
    adicional = BANDEIRAS_TARIFARIAS.get(bandeira, 0.0)
    return TARIFA_BASE_MT + adicional

def calcular_tudo(aparelhos_uso, banco_dados=BancoDeDados, bandeira='verde'):
    potencia_total_instalada = 0
    consumo_total_kwh = 0
    detalhes_consumo = {}
    detalhes_potencia = {}

    for chave, dados in aparelhos_uso.items():
        if chave in banco_dados:
            qtd = dados.get('qtd', 0)
            horas = dados.get('horas', 0)
            dias = dados.get('dias', 0)

            if qtd > 0:
                pot_w = banco_dados[chave]['potencia_w'] * qtd
                potencia_total_instalada += pot_w
                
                consumo_item = calcular_consumo_item(banco_dados[chave]['potencia_w'], qtd, horas, dias)
                consumo_total_kwh += consumo_item
                
                detalhes_potencia[chave] = pot_w
                detalhes_consumo[chave] = consumo_item

    tarifa_aplicada = obter_tarifa_final(bandeira)
    valor_total_reais = consumo_total_kwh * tarifa_aplicada

    return {
        'potencia_total_w': potencia_total_instalada,
        'consumo_kwh': consumo_total_kwh,
        'valor_reais': valor_total_reais,
        'tarifa_usada': tarifa_aplicada,
        'detalhes_potencia': detalhes_potencia,
        'detalhes_consumo': detalhes_consumo
    }

def identificarOsCaros(consumo_individual, top_n=3):
    return sorted(consumo_individual.items(), key=lambda x: x[1], reverse=True)[:top_n]

def calcular_percentuais(consumo_individual, consumo_total):
    if consumo_total == 0:
        return {}
    return {nome: (consumo / consumo_total) * 100 for nome, consumo in consumo_individual.items()}