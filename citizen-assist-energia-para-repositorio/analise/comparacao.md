# Comparação das alternativas

> Arquivo gerado por `python -m src.energia.relatorio`. 
> **Todos os dados são estimados** 

## Necessidade analisada

Reduzir o custo de energia de um espaço comunitário que atende pessoas com deficiência visual, em São Paulo, **sem reduzir a iluminação adequada e sem prejudicar os equipamentos assistivos**. As três alternativas respondem à mesma necessidade, com a mesma tarifa (R$ 0,95 por kWh) e o mesmo horizonte de 10 anos.

## 1. Consumo atual (cenário-base)

Período de referência: 1 mês (30 dias). Energia = potência (W) x horas / 1000. O standby é a energia gasta pelo aparelho ligado na tomada fora do horário de uso.

| Equipamento | Qtd. | Potência (W) | Horas/dia | Dias/mês | Uso (kWh) | Standby (kWh) | Total (kWh) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lâmpada fluorescente tubular com reator | 24 | 40 | 10 | 26 | 249,6 | 0,0 | 249,6 |
| Computador com leitor de tela (CPU e monitor) | 8 | 100 | 6 | 26 | 124,8 | 13,5 | 138,3 |
| Lupa eletrônica de mesa (vídeo-ampliador) | 4 | 35 | 4 | 26 | 14,6 | 4,9 | 19,5 |
| Impressora braille | 1 | 80 | 2 | 26 | 4,2 | 2,0 | 6,2 |
| Carregadores (celulares e linhas braille) | 10 | 10 | 3 | 26 | 7,8 | 3,2 | 11,0 |
| Ventilador | 6 | 60 | 6 | 26 | 56,2 | 0,0 | 56,2 |
| Geladeira e bebedouro (potência média) | 1 | 70 | 24 | 30 | 50,4 | 0,0 | 50,4 |
| **Total** |  |  |  |  | 507,5 | 23,7 | **531,2** |

Consumo total: **531,2 kWh por mês**, custo estimado de **R$ 504,60 por mês**.

| Categoria | kWh/mês | Parcela |
| --- | --- | --- |
| Iluminação | 249,6 | 47% |
| Computadores | 138,3 | 26% |
| Ventilação | 56,2 | 11% |
| Geladeira e bebedouro | 50,4 | 9% |
| Equipamentos assistivos | 36,7 | 7% |

## 2. Resultados das alternativas

- **A. Eficiência:** Trocar as lâmpadas fluorescentes por LED e cortar o consumo em standby com tomadas inteligentes.
- **B. Solar:** Instalar sistema solar conectado à rede, dimensionado para o consumo atual. Sistema de 4,1 kWp, geração estimada de 441 kWh por mês.
- **C. Combinada:** Aplicar primeiro a eficiência (A) e dimensionar o solar para o consumo já reduzido. Sistema de 2,7 kWp, geração estimada de 291 kWh por mês.

| Alternativa | Investimento | Economia (kWh/mês) | Economia (R$/mês, ano 1) | Retorno (payback) | Saldo em 10 anos | Emissões evitadas (kg CO2/ano) |
| --- | --- | --- | --- | --- | --- | --- |
| A. Eficiência energética | R$ 1.380,00 | 144 | R$ 136,95 | 10 meses | R$ 19.290,52 | 67 |
| B. Energia solar fotovoltaica | R$ 18.450,00 | 431 | R$ 348,16 | 4 anos e 5 meses | R$ 29.829,49 | -18 |
| C. Eficiência e solar combinadas | R$ 13.530,00 | 431 | R$ 368,70 | 3 anos e 1 mês | R$ 38.274,68 | 56 |

Saldo = economia acumulada em 10 anos (com reajuste da tarifa) menos o investimento. A economia em kWh da alternativa B e da C é parecida porque ambas levam a conta ao mínimo cobrado (custo de disponibilidade); a diferença está no tamanho e no custo do sistema solar.

### Detalhe da alternativa A

- Iluminação: 124,8 kWh por mês (24 lâmpadas).
- Standby evitado: 23,7 kWh por mês, menos 4,3 kWh gastos pelas próprias tomadas inteligentes, resultando em 19,4 kWh.
- Investimento: R$ 1.380,00 (LED com mão de obra mais tomadas inteligentes).

## 3. Custos, viabilidade e impactos ambientais

| Critério | A. Eficiência | B. Solar | C. Combinada |
| --- | --- | --- | --- |
| Custo inicial | R$ 1.380,00 | R$ 18.450,00 | R$ 13.530,00 |
| Viabilidade | Alta: troca simples, sem obra civil | Média: precisa de telhado, autorização e instalador | Média: igual à B, com sistema menor |
| Impacto ambiental | Menos energia consumida. Descarte correto de lâmpadas fluorescentes (mercúrio) | Geração renovável local. Efeito climático líquido próximo de zero na rede brasileira atual | Soma dos benefícios de A com um sistema menor |
| Principal limitação | Garantir iluminância adequada para baixa visão | Valor depende do Fio B, do telhado e de orçamentos reais | Exige as duas etapas |

## 4. Análise de sensibilidade (retorno do investimento)

| Cenário | Retorno de A | Retorno de B | Retorno de C |
| --- | --- | --- | --- |
| Tarifa 20% menor | 1 ano e 1 mês | 5 anos e 5 meses | 3 anos e 11 meses |
| Cenário-base | 10 meses | 4 anos e 5 meses | 3 anos e 1 mês |
| Tarifa 20% maior | 8 meses | 3 anos e 8 meses | 2 anos e 7 meses |
| Solar 20% mais caro | 10 meses | 5 anos e 2 meses | 3 anos e 7 meses |
| Solar 20% mais barato | 10 meses | 3 anos e 7 meses | 2 anos e 7 meses |
| Sol 15% menor | 10 meses | 5 anos e 1 mês | 3 anos e 7 meses |
| Sem reajuste da tarifa | 10 meses | 4 anos e 10 meses | 3 anos e 4 meses |

## 5. Conclusão da análise

A alternativa com maior saldo em 10 anos neste cenário é **C. Eficiência e solar combinadas**. A recomendação prática é começar pela eficiência (A), que tem o menor investimento e o retorno mais rápido, e depois dimensionar o solar para o consumo já reduzido (C). A conclusão depende dos valores estimados e deve ser refeita com a fatura real e orçamentos reais do espaço.

**Sobre o clima:** com o fator de emissão médio da rede de 38,5 g CO2/kWh e emissões do ciclo de vida do solar de 41 g CO2/kWh, o solar sozinho evita praticamente nenhuma emissão líquida (resultado de B: -18 kg CO2/ano). Isso acontece porque a rede brasileira já é majoritariamente renovável. O fator médio é o dado oficial, mas o efeito marginal real de gerar ou economizar energia pode ser diferente. O benefício do solar aqui é principalmente financeiro e de previsibilidade de custo.
