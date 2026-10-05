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

def calcular_tudo(lista_aparelhos, banco_dados=BancoDeDados, bandeira='verde', possui_solar=False, geracao_solar_kwh=0, consumo_anterior_kwh=0):
    """
    lista_aparelhos: aceita aparelhos cadastrados ou customizados informando 'potencia_w' e 'nome_custom':
    [
        {'chave': 'ar_condicionado', 'qtd': 1, 'horas': 8, 'dias': 30},
        {'chave': 'novo_customizado', 'nome_custom': 'Adega Climatizada', 'potencia_w': 350, 'qtd': 1, 'horas': 24, 'dias': 30}
    ]
    """
    potencia_total_instalada = 0
    consumo_total_kwh = 0
    detalhes_consumo = []

    for item in lista_aparelhos:
        chave = item.get('chave')
        qtd = item.get('qtd', 1)
        horas = item.get('horas', 0)
        dias = item.get('dias', 0)

        # Determina a potência unitária (caso seja customizado ou vindo do banco)
        if chave in banco_dados:
            pot_unit = banco_dados[chave]['potencia_w']
            nome_exibicao = chave
        else:
            pot_unit = item.get('potencia_w', 0)
            nome_exibicao = item.get('nome_custom', 'Aparelho Customizado')

        if pot_unit > 0 and qtd > 0 and horas > 0 and dias > 0:
            pot_total_item = pot_unit * qtd
            potencia_total_instalada += pot_total_item
            
            consumo_item = calcular_consumo_item(pot_unit, qtd, horas, dias)
            consumo_total_kwh += consumo_item
            
            detalhes_consumo.append({
                'nome': nome_exibicao,
                'potencia_w': pot_total_item,
                'consumo_kwh': consumo_item
            })

    tarifa_aplicada = obter_tarifa_final(bandeira)
    
    # Cálculo de Energia Solar
    if possui_solar:
        consumo_faturado_kwh = max(30.0, consumo_total_kwh - geracao_solar_kwh)
        economia_kwh = max(0.0, consumo_total_kwh - consumo_faturado_kwh)
        economia_reais = economia_kwh * tarifa_aplicada
    else:
        consumo_faturado_kwh = consumo_total_kwh
        economia_kwh = consumo_total_kwh * 0.90
        economia_reais = economia_kwh * tarifa_aplicada

    valor_faturado_reais = consumo_faturado_kwh * tarifa_aplicada
    valor_sem_solar_reais = consumo_total_kwh * tarifa_aplicada

    # Comparativo com mês anterior
    diferenca_historico_kwh = consumo_total_kwh - consumo_anterior_kwh if consumo_anterior_kwh > 0 else 0
    percentual_historico = ((diferenca_historico_kwh / consumo_anterior_kwh) * 100) if consumo_anterior_kwh > 0 else 0

    return {
        'potencia_total_w': potencia_total_instalada,
        'consumo_bruto_kwh': consumo_total_kwh,
        'consumo_faturado_kwh': consumo_faturado_kwh,
        'valor_reais': valor_faturado_reais,
        'valor_sem_solar_reais': valor_sem_solar_reais,
        'economia_solar_kwh': economia_kwh,
        'economia_solar_reais': economia_reais,
        'diferenca_historico_kwh': diferenca_historico_kwh,
        'percentual_historico': percentual_historico,
        'tarifa_usada': tarifa_aplicada,
        'detalhes_consumo': detalhes_consumo
    }