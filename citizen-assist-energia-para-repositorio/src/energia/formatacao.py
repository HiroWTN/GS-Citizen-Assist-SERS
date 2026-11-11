"""Formatação de números no padrão brasileiro e adaptação de texto para leitores de tela."""
from __future__ import annotations

import re


def fmt_num(valor: float, casas: int = 1) -> str:
    """1234.5 -> '1.234,5'."""
    if round(valor, casas) == 0:
        valor = 0.0
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_rs(valor: float) -> str:
    """1234.5 -> 'R$ 1.234,50'."""
    return f"R$ {fmt_num(valor, 2)}"


def fmt_anos(valor) -> str:
    """Payback em anos e meses legíveis; None vira texto explicativo."""
    if valor is None:
        return "não se paga no horizonte analisado"
    meses = round(valor * 12)
    anos, resto = divmod(meses, 12)
    partes = []
    if anos:
        partes.append(f"{anos} ano" + ("s" if anos > 1 else ""))
    if resto or not anos:
        partes.append(f"{resto} " + ("mês" if resto == 1 else "meses"))
    return " e ".join(partes)


_REAIS = re.compile(r"R\$\s?(-?\d[\d.]*(?:,\d+)?)")

_SUBSTITUICOES = [
    ("kWh/mês", "quilowatts-hora por mês"),
    ("kWh/ano", "quilowatts-hora por ano"),
    ("kWp", "quilowatts-pico"),
    ("kWh", "quilowatts-hora"),
    ("kg CO2/ano", "quilogramas de dióxido de carbono por ano"),
    ("kg CO2", "quilogramas de dióxido de carbono"),
    ("CO2", "dióxido de carbono"),
    ("%", " por cento"),
]


def falar(texto: str) -> str:
    """Troca símbolos e siglas por palavras, para o leitor de tela ler sem ambiguidade."""
    texto = _REAIS.sub(r"\1 reais", texto)
    for origem, destino in _SUBSTITUICOES:
        texto = texto.replace(origem, destino)
    return texto
