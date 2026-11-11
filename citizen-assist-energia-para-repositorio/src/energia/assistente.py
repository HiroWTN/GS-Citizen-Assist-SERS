"""Funcionalidades de energia do Citizen Assist AI.

Ponto de integração: `responder_energia(pergunta)`.
Todas as respostas vêm dos mesmos cálculos de `alternativas.py`, então o que o
assistente diz é sempre coerente com a análise do repositório.

Formato de toda resposta (pensado para leitor de tela, sem tabelas nem emojis):
    Resposta / Como calculei / Limitações / Fontes
"""
from __future__ import annotations

import re
import unicodedata
from typing import Optional

from . import alternativas as alt
from . import calculos as c
from .formatacao import falar, fmt_anos, fmt_num, fmt_rs

FONTES = (
    "ANEEL (tarifas, bandeiras e custo de disponibilidade); CRESESB (irradiação solar); "
    "Programa Procel e Inmetro (consumo de aparelhos); MCTI (fator de emissão do sistema elétrico); "
    "Lei 14.300/2022 (geração distribuída). Lista completa no arquivo referencias.md."
)

AVISO_ESTIMATIVA = (
    "Os dados do espaço são estimados e os resultados não são garantia de economia. "
    "Para valores reais, use a sua fatura e orçamentos de profissionais."
)


def _normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFD", texto.lower())
    return "".join(ch for ch in sem_acento if unicodedata.category(ch) != "Mn")


def _tem(texto: str, palavras: list) -> bool:
    return any(p in texto for p in palavras)


def _montar(resposta: str, como: str, limites: str, acessivel: bool) -> str:
    texto = (
        f"Resposta: {resposta}\n\n"
        f"Como calculei: {como}\n\n"
        f"Limitações: {limites} {AVISO_ESTIMATIVA}\n\n"
        f"Fontes: {FONTES}"
    )
    return falar(texto) if acessivel else texto


# ------------------------------------------------------------- respostas

def _consumo_total(ctx: dict, acessivel: bool) -> str:
    base = ctx["base"]
    ordem = sorted(base["por_categoria"].items(), key=lambda kv: kv[1], reverse=True)
    nomes = {
        "iluminacao": "iluminação",
        "informatica": "computadores",
        "assistivo": "equipamentos assistivos",
        "climatizacao": "ventilação",
        "copa": "geladeira e bebedouro",
    }
    maiores = ", ".join(
        f"{nomes.get(cat, cat)} ({fmt_num(kwh, 0)} kWh)" for cat, kwh in ordem[:3]
    )
    return _montar(
        f"O espaço consome cerca de {fmt_num(base['total_kwh_mes'], 0)} kWh por mês, "
        f"o que custa aproximadamente {fmt_rs(base['custo_rs_mes'])}. "
        f"Os maiores consumos são: {maiores}.",
        "Energia em kWh é a potência do aparelho em watts, vezes as horas de uso, dividido por mil. "
        "Somei todos os aparelhos do inventário e o consumo parado na tomada (standby).",
        "O inventário é um cenário estimado de um espaço comunitário.",
        acessivel,
    )


def _consumo_equipamento(ctx: dict, eq_id: str, acessivel: bool) -> Optional[str]:
    for eq, uso, standby in ctx["base"]["por_equipamento"]:
        if eq.id == eq_id:
            tarifa = ctx["tarifa"]
            total = uso + standby
            return _montar(
                f"{eq.nome}: cerca de {fmt_num(total, 1)} kWh por mês, ou {fmt_rs(total * tarifa)} "
                f"({eq.quantidade} " + ("unidade" if eq.quantidade == 1 else "unidades") + " no espaço).",
                f"{eq.quantidade} x {fmt_num(eq.potencia_w, 0)} watts x {fmt_num(eq.horas_dia, 0)} horas por dia "
                f"x {eq.dias_mes} dias, dividido por mil, mais {fmt_num(standby, 1)} kWh parados na tomada.",
                f"Potência e horas de uso são estimativas. Origem: {eq.origem}.",
                acessivel,
            )
    return None


def _led(ctx: dict, acessivel: bool) -> str:
    r = ctx["resultados"][0]
    d = r.detalhes
    ef = ctx["premissas"]["eficiencia"]
    fluor = next(e for e in ctx["equipamentos"] if e.categoria == "iluminacao")
    return _montar(
        f"Trocar as {d['n_lampadas']} lâmpadas fluorescentes por LED economiza cerca de "
        f"{fmt_num(d['econ_iluminacao_kwh'], 0)} kWh por mês, sem reduzir a iluminação se o LED tiver "
        f"fluxo luminoso equivalente. Isso é importante para quem tem baixa visão.",
        f"Cada fluorescente usa cerca de {fmt_num(fluor.potencia_w, 0)} watts e o LED escolhido cerca de {fmt_num(ef['led_tubular_potencia_w'], 0)} watts. "
        f"A diferença, vezes as horas de uso, dá a economia. O custo estimado da troca, com mão de obra, "
        f"é {fmt_rs(d['n_lampadas'] * (ef['led_custo_unitario_rs'] + ef['led_mao_de_obra_rs']))}.",
        "Confira a iluminância com um luxímetro antes e depois. Descarte as fluorescentes em ponto de logística reversa, pois contêm mercúrio.",
        acessivel,
    )


def _standby(ctx: dict, acessivel: bool) -> str:
    d = ctx["resultados"][0].detalhes
    saldo = d["econ_standby_kwh"]
    veredito = (
        f"Cortar o standby economiza cerca de {fmt_num(saldo, 0)} kWh por mês, um ganho pequeno."
        if saldo > 0
        else "Neste cenário as tomadas inteligentes gastam mais energia do que economizam."
    )
    return _montar(
        f"{veredito} A dica mais útil é usar uma tomada ou régua inteligente por grupo de aparelhos, "
        f"com desligamento por horário ou comando de voz, em vez de uma tomada para cada aparelho.",
        f"Os aparelhos parados na tomada gastam {fmt_num(d['standby_total_kwh'], 0)} kWh por mês. "
        f"As tomadas inteligentes gastam {fmt_num(d['autoconsumo_tomadas_kwh'], 1)} kWh por mês, "
        f"e esse consumo foi descontado.",
        "O ganho é pequeno e depende do aplicativo ser compatível com leitor de tela.",
        acessivel,
    )


def _solar(ctx: dict, acessivel: bool) -> str:
    b = ctx["resultados"][1]
    c_res = ctx["resultados"][2]
    return _montar(
        f"Um sistema solar de cerca de {fmt_num(b.potencia_fv_kwp, 1)} kWp, dimensionado para o consumo atual, "
        f"custaria perto de {fmt_rs(b.investimento_rs)} e reduziria a conta em cerca de {fmt_rs(b.economia_rs_mes)} "
        f"por mês. O retorno estimado é de {fmt_anos(b.payback_anos)}. Se você fizer antes a eficiência (LED e standby), "
        f"o sistema necessário cai para cerca de {fmt_num(c_res.potencia_fv_kwp, 1)} kWp e o retorno estimado "
        f"melhora para {fmt_anos(c_res.payback_anos)}.",
        "Geração por mês = potência do sistema em kWp x horas de sol pleno por dia x desempenho do sistema x 30 dias. "
        "O retorno é o investimento dividido pela economia, considerando reajuste da tarifa de "
        f"{fmt_num(ctx['premissas']['economia']['reajuste_tarifa_anual'] * 100, 0)}% ao ano e perda de geração de 0,5% ao ano.",
        " ".join(b.limitacoes[1:]),
        acessivel,
    )


def _comparacao(ctx: dict, acessivel: bool) -> str:
    a, b, c_res = ctx["resultados"]
    melhor = alt.recomendada(ctx["resultados"])
    anos = ctx["horizonte_anos"]
    return _montar(
        f"Para reduzir a conta do espaço, a alternativa com maior saldo em {anos} anos é a {melhor.nome}. "
        f"Resumo: A, eficiência, custa {fmt_rs(a.investimento_rs)} e se paga em {fmt_anos(a.payback_anos)}. "
        f"B, solar sozinho, custa {fmt_rs(b.investimento_rs)} e se paga em {fmt_anos(b.payback_anos)}. "
        f"C, eficiência e depois solar, custa {fmt_rs(c_res.investimento_rs)} e se paga em {fmt_anos(c_res.payback_anos)}. "
        f"A ordem recomendada é começar pela eficiência, que é mais barata, e depois dimensionar o solar "
        f"para o consumo já reduzido. Sobre o ambiente: a eficiência evita cerca de "
        f"{fmt_num(a.emissoes_evitadas_kg_ano, 0)} kg CO2 por ano e o solar tem efeito climático líquido próximo de zero "
        f"na rede brasileira, que já é majoritariamente renovável. O ganho do solar é principalmente financeiro.",
        f"As três alternativas atendem à mesma necessidade, no mesmo período de {anos} anos, com a mesma tarifa. "
        f"Saldo = economia acumulada menos investimento.",
        "Preços, tarifa e sol são estimativas. A recomendação muda se a tarifa real, os orçamentos ou o local de instalação forem diferentes. "
        "Solar exige telhado adequado e autorização do proprietário.",
        acessivel,
    )


def _conta(ctx: dict, acessivel: bool) -> str:
    disp = ctx["premissas"]["rede"]["custo_disponibilidade_kwh"]
    watts = ctx["premissas"]["eficiencia"]["led_tubular_potencia_w"]
    exemplo = c.energia_kwh(watts, 10)
    return _montar(
        "Na conta de luz, o consumo aparece em kWh. Um kWh é a energia de um aparelho de 1000 watts ligado por uma hora. "
        f"Exemplo: uma lâmpada LED de {fmt_num(watts, 0)} watts ligada por 10 horas gasta {fmt_num(exemplo, 1)} kWh. "
        "A conta soma o consumo vezes a tarifa, os impostos e a bandeira tarifária, que sobe quando a geração fica mais cara. "
        f"Existe também um valor mínimo cobrado mesmo sem consumo, chamado custo de disponibilidade: "
        f"30 kWh no monofásico, 50 no bifásico e 100 no trifásico. Neste cenário usei {disp} kWh.",
        "kWh = watts x horas / 1000. Custo = kWh x tarifa.",
        "Confira a tarifa e o tipo de ligação na sua própria fatura ou no site da distribuidora.",
        acessivel,
    )


def _fontes(acessivel: bool) -> str:
    return _montar(
        "As referências usadas nesta análise estão listadas abaixo e também no arquivo referencias.md.",
        "Cada dado do repositório tem origem e marcação de estimativa nos arquivos da pasta dados.",
        "Fontes oficiais mudam com o tempo. Confira sempre a versão mais recente.",
        acessivel,
    )


def _ajuda(acessivel: bool) -> str:
    texto = (
        "Posso ajudar com orientações de energia para o espaço comunitário. Você pode perguntar, por exemplo: "
        "quanto o espaço consome por mês; quanto gasta o computador, a lupa ou a geladeira; "
        "se vale trocar para LED; se vale usar tomada inteligente; se vale instalar energia solar; "
        "qual alternativa é a melhor; como entender a conta de luz; ou quais são as fontes.\n\n"
        f"Aviso: {AVISO_ESTIMATIVA}"
    )
    return falar(texto) if acessivel else texto


# ---------------------------------------------------------- roteamento

def contexto(premissas: Optional[dict] = None, equipamentos: Optional[list] = None) -> dict:
    premissas = premissas or c.carregar_premissas()
    equipamentos = equipamentos or c.carregar_equipamentos()
    ctx = alt.comparar(premissas, equipamentos)
    ctx["premissas"] = premissas
    ctx["equipamentos"] = equipamentos
    ctx["tarifa"] = premissas["tarifa"]["valor_rs_kwh"]
    return ctx


def responder_energia(
    pergunta: str,
    acessivel: bool = True,
    premissas: Optional[dict] = None,
    equipamentos: Optional[list] = None,
) -> str:
    """Responde uma pergunta de energia. Nunca levanta exceção por texto inesperado."""
    if not isinstance(pergunta, str) or not pergunta.strip():
        return _ajuda(acessivel)
    ctx = contexto(premissas, equipamentos)
    texto = _normalizar(pergunta)

    if _tem(texto, ["fonte", "referencia", "de onde"]):
        return _fontes(acessivel)
    if _tem(texto, ["conta", "fatura", "bandeira", "tarifa", "kwh significa", "o que e kwh"]):
        return _conta(ctx, acessivel)
    if _tem(texto, ["standby", "tomada", "esquecid", "deixar ligad"]):
        return _standby(ctx, acessivel)
    if _tem(texto, ["solar", "fotovolt", "placa", "renovavel"]):
        return _solar(ctx, acessivel)
    if re.search(r"\bled\b", texto):
        return _led(ctx, acessivel)
    if _tem(texto, ["compar", "vale a pena", "melhor", "recomend", "alternativa"]):
        return _comparacao(ctx, acessivel)

    # Equipamento específico, pelas palavras-chave do inventário.
    for eq in ctx["equipamentos"]:
        if any(_normalizar(p) in texto for p in eq.palavras_chave):
            if eq.categoria == "iluminacao" and _tem(texto, ["trocar", "troca", "economi"]):
                return _led(ctx, acessivel)
            resposta = _consumo_equipamento(ctx, eq.id, acessivel)
            if resposta:
                return resposta

    if _tem(texto, ["consumo", "consome", "gasta", "gasto", "quanto"]):
        return _consumo_total(ctx, acessivel)
    return _ajuda(acessivel)
