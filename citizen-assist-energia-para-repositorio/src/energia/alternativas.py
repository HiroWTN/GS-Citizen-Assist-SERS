"""Comparação de alternativas para a mesma necessidade: reduzir a conta de energia
do espaço comunitário mantendo iluminação adequada e equipamentos assistivos.

A: eficiência (LED e controle de standby)
B: energia solar fotovoltaica dimensionada para o consumo atual
C: eficiência primeiro e solar dimensionada para o consumo já reduzido

Todas usam o mesmo horizonte, a mesma tarifa e as mesmas premissas de reajuste.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import calculos as c


@dataclass
class Resultado:
    chave: str
    nome: str
    descricao: str
    investimento_rs: float
    economia_kwh_mes: float
    custo_antes_rs_mes: float
    custo_depois_rs_mes: float
    economia_rs_mes: float
    economia_rs_ano1: float
    payback_anos: Optional[float]
    saldo_horizonte_rs: float
    emissoes_evitadas_kg_ano: float
    potencia_fv_kwp: float = 0.0
    geracao_fv_kwh_mes: float = 0.0
    fluxo: list = field(default_factory=list)
    limitacoes: list = field(default_factory=list)
    detalhes: dict = field(default_factory=dict)


LIMITACOES_GERAIS = [
    "Os valores de potência, horas de uso, preços e tarifa são estimativas e não garantem a economia real.",
]

LIMITACOES_EFICIENCIA = [
    "A lâmpada LED deve ter fluxo luminoso equivalente ao da fluorescente. Para pessoas com baixa visão, confira a iluminância com um luxímetro (NBR ISO/CIE 8995-1) antes e depois da troca.",
    "Lâmpadas fluorescentes contêm mercúrio e devem ser descartadas em pontos de logística reversa.",
    "Tomadas inteligentes consomem energia própria e precisam de aplicativo compatível com leitor de tela.",
]

LIMITACOES_SOLAR = [
    "Exige telhado ou área adequada, sem sombreamento, e autorização do proprietário e da distribuidora.",
    "Pela Lei 14.300/2022, parte da tarifa (Fio B) continua sendo cobrada sobre a energia compensada. O desconto usado é uma estimativa e tende a mudar com os anos.",
    "A geração varia ao longo do ano. O cálculo usa a média anual de sol.",
    "O inversor costuma precisar de troca entre 10 e 15 anos, o que não entra no horizonte de 10 anos.",
    "O benefício climático é pequeno, porque a rede elétrica brasileira já é majoritariamente renovável. O ganho principal é financeiro.",
]


def consumo_base(equipamentos: list) -> dict:
    por_categoria: dict = {}
    por_equipamento = []
    uso_total = standby_total = 0.0
    for eq in equipamentos:
        uso = c.consumo_uso_mensal_kwh(eq)
        standby = c.consumo_standby_mensal_kwh(eq)
        uso_total += uso
        standby_total += standby
        por_categoria[eq.categoria] = por_categoria.get(eq.categoria, 0.0) + uso + standby
        por_equipamento.append((eq, uso, standby))
    return {
        "total_kwh_mes": uso_total + standby_total,
        "uso_kwh_mes": uso_total,
        "standby_kwh_mes": standby_total,
        "por_categoria": por_categoria,
        "por_equipamento": por_equipamento,
    }


def _parametros(premissas: dict) -> dict:
    return {
        "tarifa": premissas["tarifa"]["valor_rs_kwh"],
        "disp": premissas["rede"]["custo_disponibilidade_kwh"],
        "ef": premissas["eficiencia"],
        "fv": premissas["solar"],
        "anos": premissas["economia"]["horizonte_anos"],
        "reaj": premissas["economia"]["reajuste_tarifa_anual"],
        "f_rede": premissas["emissoes"]["fator_rede_kgco2_kwh"],
        "f_fv": premissas["emissoes"]["fator_ciclo_vida_fv_kgco2_kwh"],
    }


def _eficiencia(premissas: dict, equipamentos: list) -> dict:
    """Economia e investimento das medidas de eficiência (sem montar o Resultado)."""
    p = _parametros(premissas)
    ef = p["ef"]
    iluminacao = [e for e in equipamentos if e.categoria == "iluminacao"]
    n_lampadas = sum(e.quantidade for e in iluminacao)
    econ_iluminacao = sum(
        e.quantidade
        * max(e.potencia_w - ef["led_tubular_potencia_w"], 0)
        * e.horas_dia
        * e.dias_mes
        / 1000
        for e in iluminacao
    )
    standby_total = sum(c.consumo_standby_mensal_kwh(e) for e in equipamentos)
    autoconsumo = (
        ef["tomadas_inteligentes_quantidade"]
        * c.energia_kwh(ef["tomada_inteligente_autoconsumo_w"], c.HORAS_DIA)
        * c.DIAS_REF_MES
    )
    econ_standby = standby_total - autoconsumo
    investimento = (
        n_lampadas * (ef["led_custo_unitario_rs"] + ef["led_mao_de_obra_rs"])
        + ef["tomadas_inteligentes_quantidade"] * ef["tomada_inteligente_custo_rs"]
    )
    return {
        "n_lampadas": n_lampadas,
        "econ_iluminacao_kwh": econ_iluminacao,
        "standby_total_kwh": standby_total,
        "autoconsumo_tomadas_kwh": autoconsumo,
        "econ_standby_kwh": econ_standby,
        "econ_total_kwh": econ_iluminacao + econ_standby,
        "investimento_rs": investimento,
    }


def alternativa_a(premissas: dict, equipamentos: list) -> Resultado:
    p = _parametros(premissas)
    e_base = consumo_base(equipamentos)["total_kwh_mes"]
    ef = _eficiencia(premissas, equipamentos)
    custo_antes = c.custo_mensal(e_base, p["tarifa"], disponibilidade_kwh=p["disp"])
    custo_depois = c.custo_mensal(
        e_base - ef["econ_total_kwh"], p["tarifa"], disponibilidade_kwh=p["disp"]
    )
    economia_mes = custo_antes - custo_depois
    fluxo = c.fluxo_anual(economia_mes * 12, p["anos"], p["reaj"])
    return Resultado(
        chave="A",
        nome="A. Eficiência energética",
        descricao="Trocar as lâmpadas fluorescentes por LED e cortar o consumo em standby com tomadas inteligentes.",
        investimento_rs=ef["investimento_rs"],
        economia_kwh_mes=ef["econ_total_kwh"],
        custo_antes_rs_mes=custo_antes,
        custo_depois_rs_mes=custo_depois,
        economia_rs_mes=economia_mes,
        economia_rs_ano1=economia_mes * 12,
        payback_anos=c.payback_anos(ef["investimento_rs"], fluxo),
        saldo_horizonte_rs=c.saldo_acumulado(ef["investimento_rs"], fluxo),
        emissoes_evitadas_kg_ano=c.emissoes_kg(ef["econ_total_kwh"] * 12, p["f_rede"]),
        fluxo=fluxo,
        limitacoes=LIMITACOES_GERAIS + LIMITACOES_EFICIENCIA,
        detalhes=ef,
    )


def _solar(premissas: dict, consumo_kwh: float) -> dict:
    """Dimensionamento e economia de um sistema solar para um dado consumo mensal."""
    p = _parametros(premissas)
    fv = p["fv"]
    kwp = c.dimensionar_fv_kwp(consumo_kwh, p["disp"], fv["hsp_kwh_m2_dia"], fv["desempenho_pr"])
    geracao = c.geracao_mensal_kwh(kwp, fv["hsp_kwh_m2_dia"], fv["desempenho_pr"])
    compensado = c.kwh_compensado(consumo_kwh, geracao, p["disp"])
    custo_sem = c.custo_mensal(consumo_kwh, p["tarifa"], disponibilidade_kwh=p["disp"])
    custo_com = c.custo_mensal(
        consumo_kwh,
        p["tarifa"],
        geracao_kwh=geracao,
        disponibilidade_kwh=p["disp"],
        desconto_compensacao=fv["desconto_compensacao"],
    )
    investimento = kwp * 1000 * fv["custo_rs_por_wp"]
    emissoes = c.emissoes_kg(compensado * 12, p["f_rede"]) - c.emissoes_kg(
        geracao * 12, p["f_fv"]
    )
    return {
        "kwp": kwp,
        "geracao_kwh_mes": geracao,
        "compensado_kwh_mes": compensado,
        "custo_sem_rs_mes": custo_sem,
        "custo_com_rs_mes": custo_com,
        "economia_rs_mes": custo_sem - custo_com,
        "investimento_rs": investimento,
        "emissoes_liquidas_kg_ano": emissoes,
    }


def alternativa_b(premissas: dict, equipamentos: list) -> Resultado:
    p = _parametros(premissas)
    e_base = consumo_base(equipamentos)["total_kwh_mes"]
    s = _solar(premissas, e_base)
    fluxo = c.fluxo_anual(
        s["economia_rs_mes"] * 12,
        p["anos"],
        p["reaj"],
        degradacao=p["fv"]["degradacao_anual"],
        custo_anual=p["fv"]["manutencao_anual_rs"],
    )
    return Resultado(
        chave="B",
        nome="B. Energia solar fotovoltaica",
        descricao="Instalar sistema solar conectado à rede, dimensionado para o consumo atual.",
        investimento_rs=s["investimento_rs"],
        economia_kwh_mes=s["compensado_kwh_mes"],
        custo_antes_rs_mes=s["custo_sem_rs_mes"],
        custo_depois_rs_mes=s["custo_com_rs_mes"],
        economia_rs_mes=s["economia_rs_mes"],
        economia_rs_ano1=s["economia_rs_mes"] * 12,
        payback_anos=c.payback_anos(s["investimento_rs"], fluxo),
        saldo_horizonte_rs=c.saldo_acumulado(s["investimento_rs"], fluxo),
        emissoes_evitadas_kg_ano=s["emissoes_liquidas_kg_ano"],
        potencia_fv_kwp=s["kwp"],
        geracao_fv_kwh_mes=s["geracao_kwh_mes"],
        fluxo=fluxo,
        limitacoes=LIMITACOES_GERAIS + LIMITACOES_SOLAR,
        detalhes=s,
    )


def alternativa_c(premissas: dict, equipamentos: list) -> Resultado:
    p = _parametros(premissas)
    e_base = consumo_base(equipamentos)["total_kwh_mes"]
    ef = _eficiencia(premissas, equipamentos)
    e_pos_a = e_base - ef["econ_total_kwh"]
    s = _solar(premissas, e_pos_a)

    custo_antes = c.custo_mensal(e_base, p["tarifa"], disponibilidade_kwh=p["disp"])
    custo_depois = s["custo_com_rs_mes"]
    economia_mes = custo_antes - custo_depois

    custo_pos_a = c.custo_mensal(e_pos_a, p["tarifa"], disponibilidade_kwh=p["disp"])
    fluxo_a = c.fluxo_anual((custo_antes - custo_pos_a) * 12, p["anos"], p["reaj"])
    fluxo_fv = c.fluxo_anual(
        s["economia_rs_mes"] * 12,
        p["anos"],
        p["reaj"],
        degradacao=p["fv"]["degradacao_anual"],
        custo_anual=p["fv"]["manutencao_anual_rs"],
    )
    fluxo = c.somar_fluxos(fluxo_a, fluxo_fv)
    investimento = ef["investimento_rs"] + s["investimento_rs"]
    emissoes = (
        c.emissoes_kg(ef["econ_total_kwh"] * 12, p["f_rede"]) + s["emissoes_liquidas_kg_ano"]
    )
    return Resultado(
        chave="C",
        nome="C. Eficiência e solar combinadas",
        descricao="Aplicar primeiro a eficiência (A) e dimensionar o solar para o consumo já reduzido.",
        investimento_rs=investimento,
        economia_kwh_mes=ef["econ_total_kwh"] + s["compensado_kwh_mes"],
        custo_antes_rs_mes=custo_antes,
        custo_depois_rs_mes=custo_depois,
        economia_rs_mes=economia_mes,
        economia_rs_ano1=economia_mes * 12,
        payback_anos=c.payback_anos(investimento, fluxo),
        saldo_horizonte_rs=c.saldo_acumulado(investimento, fluxo),
        emissoes_evitadas_kg_ano=emissoes,
        potencia_fv_kwp=s["kwp"],
        geracao_fv_kwh_mes=s["geracao_kwh_mes"],
        fluxo=fluxo,
        limitacoes=LIMITACOES_GERAIS + LIMITACOES_EFICIENCIA + LIMITACOES_SOLAR,
        detalhes={"eficiencia": ef, "solar": s, "consumo_pos_a_kwh": e_pos_a},
    )


def comparar(premissas: dict, equipamentos: list) -> dict:
    """Roda as três alternativas com as mesmas premissas e retorna tudo junto."""
    base = consumo_base(equipamentos)
    p = _parametros(premissas)
    base["custo_rs_mes"] = c.custo_mensal(
        base["total_kwh_mes"], p["tarifa"], disponibilidade_kwh=p["disp"]
    )
    resultados = [
        alternativa_a(premissas, equipamentos),
        alternativa_b(premissas, equipamentos),
        alternativa_c(premissas, equipamentos),
    ]
    return {"base": base, "resultados": resultados, "horizonte_anos": p["anos"]}


def recomendada(resultados: list) -> Resultado:
    """Alternativa com maior saldo no horizonte entre as que se pagam."""
    pagam = [r for r in resultados if r.payback_anos is not None]
    return max(pagam or resultados, key=lambda r: r.saldo_horizonte_rs)
