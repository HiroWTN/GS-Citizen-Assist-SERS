"""Gera `analise/comparacao.md` direto dos cálculos, para que os números do
relatório sejam sempre os mesmos usados pelo assistente.

Uso: python -m src.energia.relatorio
"""
from __future__ import annotations

import copy

from . import alternativas as alt
from . import calculos as c
from .formatacao import fmt_anos, fmt_num, fmt_rs

NOMES_CATEGORIA = {
    "iluminacao": "Iluminação",
    "informatica": "Computadores",
    "assistivo": "Equipamentos assistivos",
    "climatizacao": "Ventilação",
    "copa": "Geladeira e bebedouro",
}


def _tabela(cabecalho: list, linhas: list) -> str:
    saida = ["| " + " | ".join(cabecalho) + " |", "| " + " | ".join("---" for _ in cabecalho) + " |"]
    saida += ["| " + " | ".join(str(x) for x in linha) + " |" for linha in linhas]
    return "\n".join(saida)


def _sensibilidade(premissas: dict, equipamentos: list) -> str:
    cenarios = []
    for rotulo, ajuste in [
        ("Tarifa 20% menor", lambda p: p["tarifa"].update(valor_rs_kwh=p["tarifa"]["valor_rs_kwh"] * 0.8)),
        ("Cenário-base", lambda p: None),
        ("Tarifa 20% maior", lambda p: p["tarifa"].update(valor_rs_kwh=p["tarifa"]["valor_rs_kwh"] * 1.2)),
        ("Solar 20% mais caro", lambda p: p["solar"].update(custo_rs_por_wp=p["solar"]["custo_rs_por_wp"] * 1.2)),
        ("Solar 20% mais barato", lambda p: p["solar"].update(custo_rs_por_wp=p["solar"]["custo_rs_por_wp"] * 0.8)),
        ("Sol 15% menor", lambda p: p["solar"].update(hsp_kwh_m2_dia=p["solar"]["hsp_kwh_m2_dia"] * 0.85)),
        ("Sem reajuste da tarifa", lambda p: p["economia"].update(reajuste_tarifa_anual=0.0)),
    ]:
        p = copy.deepcopy(premissas)
        ajuste(p)
        r = alt.comparar(p, equipamentos)["resultados"]
        cenarios.append([rotulo] + [fmt_anos(x.payback_anos) for x in r])
    return _tabela(["Cenário", "Retorno de A", "Retorno de B", "Retorno de C"], cenarios)


def gerar(premissas: dict, equipamentos: list) -> str:
    ctx = alt.comparar(premissas, equipamentos)
    base, resultados, anos = ctx["base"], ctx["resultados"], ctx["horizonte_anos"]
    tarifa = premissas["tarifa"]["valor_rs_kwh"]
    melhor = alt.recomendada(resultados)

    linhas_eq = [
        [
            eq.nome,
            eq.quantidade,
            fmt_num(eq.potencia_w, 0),
            fmt_num(eq.horas_dia, 0),
            eq.dias_mes,
            fmt_num(uso, 1),
            fmt_num(standby, 1),
            fmt_num(uso + standby, 1),
        ]
        for eq, uso, standby in base["por_equipamento"]
    ]
    linhas_eq.append(
        ["**Total**", "", "", "", "", fmt_num(base["uso_kwh_mes"], 1), fmt_num(base["standby_kwh_mes"], 1), f"**{fmt_num(base['total_kwh_mes'], 1)}**"]
    )

    linhas_cat = [
        [NOMES_CATEGORIA.get(cat, cat), fmt_num(kwh, 1), f"{fmt_num(100 * kwh / base['total_kwh_mes'], 0)}%"]
        for cat, kwh in sorted(base["por_categoria"].items(), key=lambda kv: kv[1], reverse=True)
    ]

    linhas_res = [
        [
            r.nome,
            fmt_rs(r.investimento_rs),
            fmt_num(r.economia_kwh_mes, 0),
            fmt_rs(r.economia_rs_mes),
            fmt_anos(r.payback_anos),
            fmt_rs(r.saldo_horizonte_rs),
            fmt_num(r.emissoes_evitadas_kg_ano, 0),
        ]
        for r in resultados
    ]

    a, b, cc = resultados
    texto = f"""# Comparação das alternativas

> Arquivo gerado por `python -m src.energia.relatorio`. Não edite à mão: altere os arquivos da pasta `dados/` e gere de novo.
> **Todos os dados são estimados** (ver `dados/FONTES_E_PREMISSAS.md`). Os resultados não são garantia de economia.

## Necessidade analisada

Reduzir o custo de energia de um espaço comunitário que atende pessoas com deficiência visual, em São Paulo, **sem reduzir a iluminação adequada e sem prejudicar os equipamentos assistivos**. As três alternativas respondem à mesma necessidade, com a mesma tarifa (R$ {fmt_num(tarifa, 2)} por kWh) e o mesmo horizonte de {anos} anos.

## 1. Consumo atual (cenário-base)

Período de referência: 1 mês (30 dias). Energia = potência (W) x horas / 1000. O standby é a energia gasta pelo aparelho ligado na tomada fora do horário de uso.

{_tabela(["Equipamento", "Qtd.", "Potência (W)", "Horas/dia", "Dias/mês", "Uso (kWh)", "Standby (kWh)", "Total (kWh)"], linhas_eq)}

Consumo total: **{fmt_num(base['total_kwh_mes'], 1)} kWh por mês**, custo estimado de **{fmt_rs(base['custo_rs_mes'])} por mês**.

{_tabela(["Categoria", "kWh/mês", "Parcela"], linhas_cat)}

## 2. Resultados das alternativas

- **A. Eficiência:** {a.descricao}
- **B. Solar:** {b.descricao} Sistema de {fmt_num(b.potencia_fv_kwp, 1)} kWp, geração estimada de {fmt_num(b.geracao_fv_kwh_mes, 0)} kWh por mês.
- **C. Combinada:** {cc.descricao} Sistema de {fmt_num(cc.potencia_fv_kwp, 1)} kWp, geração estimada de {fmt_num(cc.geracao_fv_kwh_mes, 0)} kWh por mês.

{_tabela(["Alternativa", "Investimento", "Economia (kWh/mês)", "Economia (R$/mês, ano 1)", "Retorno (payback)", f"Saldo em {anos} anos", "Emissões evitadas (kg CO2/ano)"], linhas_res)}

Saldo = economia acumulada em {anos} anos (com reajuste da tarifa) menos o investimento. A economia em kWh da alternativa B e da C é parecida porque ambas levam a conta ao mínimo cobrado (custo de disponibilidade); a diferença está no tamanho e no custo do sistema solar.

### Detalhe da alternativa A

- Iluminação: {fmt_num(a.detalhes['econ_iluminacao_kwh'], 1)} kWh por mês ({a.detalhes['n_lampadas']} lâmpadas).
- Standby evitado: {fmt_num(a.detalhes['standby_total_kwh'], 1)} kWh por mês, menos {fmt_num(a.detalhes['autoconsumo_tomadas_kwh'], 1)} kWh gastos pelas próprias tomadas inteligentes, resultando em {fmt_num(a.detalhes['econ_standby_kwh'], 1)} kWh.
- Investimento: {fmt_rs(a.investimento_rs)} (LED com mão de obra mais tomadas inteligentes).

## 3. Custos, viabilidade e impactos ambientais

| Critério | A. Eficiência | B. Solar | C. Combinada |
| --- | --- | --- | --- |
| Custo inicial | {fmt_rs(a.investimento_rs)} | {fmt_rs(b.investimento_rs)} | {fmt_rs(cc.investimento_rs)} |
| Viabilidade | Alta: troca simples, sem obra civil | Média: precisa de telhado, autorização e instalador | Média: igual à B, com sistema menor |
| Impacto ambiental | Menos energia consumida. Descarte correto de lâmpadas fluorescentes (mercúrio) | Geração renovável local. Efeito climático líquido próximo de zero na rede brasileira atual | Soma dos benefícios de A com um sistema menor |
| Principal limitação | Garantir iluminância adequada para baixa visão | Valor depende do Fio B, do telhado e de orçamentos reais | Exige as duas etapas |

## 4. Análise de sensibilidade (retorno do investimento)

{_sensibilidade(premissas, equipamentos)}

## 5. Conclusão da análise

A alternativa com maior saldo em {anos} anos neste cenário é **{melhor.nome}**. A recomendação prática é começar pela eficiência (A), que tem o menor investimento e o retorno mais rápido, e depois dimensionar o solar para o consumo já reduzido (C). A conclusão depende dos valores estimados e deve ser refeita com a fatura real e orçamentos reais do espaço.

**Sobre o clima:** com o fator de emissão médio da rede de {fmt_num(premissas['emissoes']['fator_rede_kgco2_kwh'] * 1000, 1)} g CO2/kWh e emissões do ciclo de vida do solar de {fmt_num(premissas['emissoes']['fator_ciclo_vida_fv_kgco2_kwh'] * 1000, 0)} g CO2/kWh, o solar sozinho evita praticamente nenhuma emissão líquida (resultado de B: {fmt_num(b.emissoes_evitadas_kg_ano, 0)} kg CO2/ano). Isso acontece porque a rede brasileira já é majoritariamente renovável. O fator médio é o dado oficial, mas o efeito marginal real de gerar ou economizar energia pode ser diferente. O benefício do solar aqui é principalmente financeiro e de previsibilidade de custo.
"""
    return texto


def main() -> None:
    premissas = c.carregar_premissas()
    equipamentos = c.carregar_equipamentos()
    destino = c.RAIZ / "analise" / "comparacao.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(gerar(premissas, equipamentos), encoding="utf-8")
    print(f"Relatório gerado em {destino}")


if __name__ == "__main__":
    main()
