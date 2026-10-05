def calcular_projecao_anual(consumo_mensal_kwh, tarifa_kwh, possui_solar=False, geracao_solar_kwh=0):
    if possui_solar:
        consumo_faturado_kwh = max(30.0, consumo_mensal_kwh - geracao_solar_kwh)
        economia_mensal_kwh = max(0.0, consumo_mensal_kwh - consumo_faturado_kwh)
    else:
        consumo_faturado_kwh = consumo_mensal_kwh
        economia_mensal_kwh = consumo_mensal_kwh * 0.90  # Estimativa de potencial solar

    gasto_mensal = consumo_faturado_kwh * tarifa_kwh
    economia_mensal_reais = economia_mensal_kwh * tarifa_kwh

    meses_nomes = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    projecao_meses = []
    acumulado_kwh = 0
    acumulado_reais = 0
    acumulado_economia_reais = 0

    for i, nome_mes in enumerate(meses_nomes, 1):
        acumulado_kwh += consumo_faturado_kwh
        acumulado_reais += gasto_mensal
        acumulado_economia_reais += economia_mensal_reais
        
        projecao_meses.append({
            'mes_num': i,
            'mes_nome': nome_mes,
            'consumo_mensal_kwh': consumo_faturado_kwh,
            'gasto_mensal_reais': gasto_mensal,
            'economia_mensal_reais': economia_mensal_reais,
            'acumulado_kwh': acumulado_kwh,
            'acumulado_reais': acumulado_reais,
            'acumulado_economia_reais': acumulado_economia_reais
        })

    return {
        'resumo_anual': {
            'consumo_total_ano_kwh': consumo_faturado_kwh * 12,
            'gasto_total_ano_reais': gasto_mensal * 12,
            'economia_total_ano_reais': economia_mensal_reais * 12,
            'media_mensal_kwh': consumo_faturado_kwh,
            'media_mensal_reais': gasto_mensal
        },
        'meses': projecao_meses
    }