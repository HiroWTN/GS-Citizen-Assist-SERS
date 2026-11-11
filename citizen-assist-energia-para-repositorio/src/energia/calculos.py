"""Cálculos de energia, custo, geração solar, retorno financeiro e emissões.

As funções são puras (sem efeitos colaterais) para facilitar os testes.
Unidades: potência em W (ou kWp para sistemas solares), energia em kWh,
dinheiro em R$ e emissões em kg de CO2.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

RAIZ = Path(__file__).resolve().parents[2]
PASTA_DADOS = RAIZ / "dados"
HORAS_DIA = 24
DIAS_REF_MES = 30


@dataclass(frozen=True)
class Equipamento:
    id: str
    nome: str
    categoria: str
    quantidade: int
    potencia_w: float
    horas_dia: float
    dias_mes: int
    standby_w: float
    palavras_chave: tuple
    origem: str
    estimado: bool


def validar_equipamento(eq: Equipamento) -> None:
    """Levanta ValueError se algum dado do equipamento for impossível."""
    if eq.quantidade < 0:
        raise ValueError(f"{eq.id}: quantidade negativa")
    if eq.potencia_w < 0 or eq.standby_w < 0:
        raise ValueError(f"{eq.id}: potência negativa")
    if not 0 <= eq.horas_dia <= HORAS_DIA:
        raise ValueError(f"{eq.id}: horas por dia deve estar entre 0 e 24")
    if not 0 <= eq.dias_mes <= 31:
        raise ValueError(f"{eq.id}: dias por mês deve estar entre 0 e 31")


def validar_premissas(p: dict) -> None:
    """Confere se as premissas têm valores coerentes."""
    if p["tarifa"]["valor_rs_kwh"] <= 0:
        raise ValueError("tarifa deve ser maior que zero")
    if p["solar"]["hsp_kwh_m2_dia"] <= 0:
        raise ValueError("HSP deve ser maior que zero")
    if not 0 < p["solar"]["desempenho_pr"] <= 1:
        raise ValueError("desempenho (PR) deve estar entre 0 e 1")
    if p["solar"]["custo_rs_por_wp"] <= 0:
        raise ValueError("custo por Wp deve ser maior que zero")
    if not 0 <= p["solar"]["desconto_compensacao"] <= 1:
        raise ValueError("desconto de compensação deve estar entre 0 e 1")
    if p["economia"]["horizonte_anos"] < 1:
        raise ValueError("horizonte deve ser de pelo menos 1 ano")
    if p["rede"]["custo_disponibilidade_kwh"] < 0:
        raise ValueError("custo de disponibilidade não pode ser negativo")


def carregar_premissas(caminho: Optional[Path] = None) -> dict:
    caminho = Path(caminho) if caminho else PASTA_DADOS / "premissas.json"
    with open(caminho, encoding="utf-8") as arquivo:
        premissas = json.load(arquivo)
    validar_premissas(premissas)
    return premissas


def carregar_equipamentos(caminho: Optional[Path] = None) -> list:
    caminho = Path(caminho) if caminho else PASTA_DADOS / "equipamentos.csv"
    equipamentos = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        for numero, linha in enumerate(csv.DictReader(arquivo), start=2):
            try:
                eq = Equipamento(
                    id=linha["id"].strip(),
                    nome=linha["nome"].strip(),
                    categoria=linha["categoria"].strip(),
                    quantidade=int(linha["quantidade"]),
                    potencia_w=float(linha["potencia_w"]),
                    horas_dia=float(linha["horas_dia"]),
                    dias_mes=int(linha["dias_mes"]),
                    standby_w=float(linha["standby_w"]),
                    palavras_chave=tuple(
                        p.strip() for p in linha["palavras_chave"].split(";") if p.strip()
                    ),
                    origem=linha["origem"].strip(),
                    estimado=linha["estimado"].strip().lower() == "sim",
                )
                validar_equipamento(eq)
            except (KeyError, ValueError) as erro:
                raise ValueError(f"Linha {numero} de {caminho.name}: {erro}") from erro
            equipamentos.append(eq)
    return equipamentos


# ---------------------------------------------------------------- energia

def energia_kwh(potencia_w: float, horas: float) -> float:
    """Energia (kWh) = potência (W) x tempo (h) / 1000."""
    if potencia_w < 0 or horas < 0:
        raise ValueError("potência e horas não podem ser negativas")
    return potencia_w * horas / 1000


def consumo_uso_mensal_kwh(eq: Equipamento) -> float:
    return eq.quantidade * energia_kwh(eq.potencia_w, eq.horas_dia) * eq.dias_mes


def consumo_standby_mensal_kwh(eq: Equipamento) -> float:
    """Energia gasta com o aparelho ligado na tomada, mas sem uso (30 dias de referência)."""
    horas_standby = max(HORAS_DIA * DIAS_REF_MES - eq.horas_dia * eq.dias_mes, 0)
    return eq.quantidade * energia_kwh(eq.standby_w, horas_standby)


def consumo_mensal_kwh(eq: Equipamento) -> float:
    return consumo_uso_mensal_kwh(eq) + consumo_standby_mensal_kwh(eq)


# ------------------------------------------------------------------ custo

def custo_mensal(
    consumo_kwh: float,
    tarifa: float,
    geracao_kwh: float = 0.0,
    disponibilidade_kwh: float = 0.0,
    desconto_compensacao: float = 0.0,
) -> float:
    """Custo mensal da fatura (R$).

    Regras simplificadas:
    - a geração própria compensa o consumo acima do custo de disponibilidade;
    - sempre se paga, no mínimo, o custo de disponibilidade;
    - cada kWh compensado ainda paga a fração `desconto_compensacao` da tarifa
      (representação simplificada do Fio B, Lei 14.300/2022).
    """
    if consumo_kwh < 0 or geracao_kwh < 0 or tarifa < 0:
        raise ValueError("consumo, geração e tarifa não podem ser negativos")
    compensado = kwh_compensado(consumo_kwh, geracao_kwh, disponibilidade_kwh)
    faturado = max(consumo_kwh - compensado, disponibilidade_kwh)
    return faturado * tarifa + compensado * tarifa * desconto_compensacao


def kwh_compensado(consumo_kwh: float, geracao_kwh: float, disponibilidade_kwh: float) -> float:
    return min(geracao_kwh, max(consumo_kwh - disponibilidade_kwh, 0.0))


# ------------------------------------------------------------------ solar

def geracao_mensal_kwh(kwp: float, hsp: float, pr: float, dias: int = DIAS_REF_MES) -> float:
    """Geração estimada (kWh/mês) = kWp x HSP x PR x dias."""
    if kwp < 0 or hsp <= 0 or not 0 < pr <= 1:
        raise ValueError("parâmetros solares inválidos")
    return kwp * hsp * pr * dias


def dimensionar_fv_kwp(
    consumo_kwh: float,
    disponibilidade_kwh: float,
    hsp: float,
    pr: float,
    dias: int = DIAS_REF_MES,
) -> float:
    """Potência (kWp) para cobrir o consumo acima do custo de disponibilidade,
    arredondada para cima em passos de 0,1 kWp."""
    if hsp <= 0 or not 0 < pr <= 1:
        raise ValueError("parâmetros solares inválidos")
    alvo = max(consumo_kwh - disponibilidade_kwh, 0.0)
    kwp = alvo / (hsp * pr * dias)
    return math.ceil(round(kwp * 10, 6)) / 10


# ------------------------------------------------------------- economia

def fluxo_anual(
    economia_ano1: float,
    anos: int,
    reajuste_tarifa: float = 0.0,
    degradacao: float = 0.0,
    custo_anual: float = 0.0,
) -> list:
    """Economia líquida de cada ano (R$), com reajuste da tarifa e degradação."""
    if anos < 1:
        raise ValueError("anos deve ser pelo menos 1")
    return [
        economia_ano1 * ((1 + reajuste_tarifa) ** ano) * ((1 - degradacao) ** ano) - custo_anual
        for ano in range(anos)
    ]


def somar_fluxos(a: list, b: list) -> list:
    if len(a) != len(b):
        raise ValueError("fluxos com tamanhos diferentes")
    return [x + y for x, y in zip(a, b)]


def payback_anos(investimento: float, fluxos: list) -> Optional[float]:
    """Anos para recuperar o investimento (interpolado). None se não recupera no horizonte."""
    if investimento <= 0:
        return 0.0
    acumulado = 0.0
    for indice, fluxo in enumerate(fluxos):
        if acumulado + fluxo >= investimento:
            return indice + (investimento - acumulado) / fluxo
        acumulado += fluxo
    return None


def saldo_acumulado(investimento: float, fluxos: list) -> float:
    """Economia acumulada no horizonte menos o investimento (R$)."""
    return sum(fluxos) - investimento


# --------------------------------------------------------------- emissões

def emissoes_kg(kwh: float, fator_kg_por_kwh: float) -> float:
    return kwh * fator_kg_por_kwh
