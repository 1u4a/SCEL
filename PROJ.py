
def calcular_projecao_anual(consumo_mensal_kwh, tarifa_kwh):
    gasto_mensal = consumo_mensal_kwh * tarifa_kwh
    meses_nomes = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    projecao_meses = []
    acumulado_kwh = 0
    acumulado_reais = 0

    for i, nome_mes in enumerate(meses_nomes, 1):
        acumulado_kwh += consumo_mensal_kwh
        acumulado_reais += gasto_mensal
        
        projecao_meses.append({
            'mes_num': i,
            'mes_nome': nome_mes,
            'consumo_mensal_kwh': consumo_mensal_kwh,
            'gasto_mensal_reais': gasto_mensal,
            'acumulado_kwh': acumulado_kwh,
            'acumulado_reais': acumulado_reais
        })

    return {
        'resumo_anual': {
            'consumo_total_ano_kwh': consumo_mensal_kwh * 12,
            'gasto_total_ano_reais': gasto_mensal * 12,
            'media_mensal_kwh': consumo_mensal_kwh,
            'media_mensal_reais': gasto_mensal
        },
        'meses': projecao_meses
    }