# Dados utilizados: origem, unidades e premissas

**Regra do projeto:** nenhum dado é apresentado como medido. Tudo o que está nesta pasta é **estimado**

- Período de referência dos cálculos: **1 mês de 30 dias** para consumo e **10 anos** para retorno financeiro.
- Unidades: potência em watts (W), energia em quilowatts-hora (kWh), sistema solar em quilowatts-pico (kWp), dinheiro em reais (R$), emissões em kg de CO2.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `equipamentos.csv` | Inventário estimado do espaço comunitário (quantidade, potência, horas de uso, standby) |
| `premissas.json` | Tarifa, custo de disponibilidade, parâmetros de eficiência, solar, economia e emissões |

## Premissas e como validar cada uma

| Premissa | Valor usado | Situação | Como validar ou substituir |
| --- | --- | --- | --- |
| Funcionamento do espaço | 10 h por dia, 26 dias por mês | Estimado | Perguntar ao espaço o horário real |
| Potência e horas de cada equipamento | Ver `equipamentos.csv` | Estimado | Ler a etiqueta ou o manual; medir com wattímetro; consultar tabelas do Procel/Inmetro |
| Tarifa de energia | R$ 0,95 por kWh | **Provisório** | Usar o valor da fatura (tarifa com impostos). A ANEEL aprovou reajuste médio de 10,18% para a Enel SP em julho de 2026, então valores antigos estão defasados |
| Custo de disponibilidade | 100 kWh (trifásico) | Estimado | Conferir o tipo de ligação na fatura (30, 50 ou 100 kWh) |
| LED tubular | 20 W, R$ 30 por unidade, R$ 10 de instalação | Estimado | Pedir orçamento. Conferir se o fluxo luminoso (lúmens) é equivalente |
| Tomada inteligente | R$ 70, consumo próprio de 1 W, 6 unidades | Estimado | Conferir ficha técnica e compatibilidade do aplicativo com leitor de tela |
| Horas de sol pleno (HSP) | 4,6 kWh/m²/dia | Estimado | Consultar o CRESESB (SunData) com a coordenada do local |
| Desempenho do sistema (PR) | 0,78 | Estimado | Valor típico de 0,75 a 0,80. Pedir ao instalador |
| Custo do solar | R$ 4,50 por Wp | Estimado | Pedir pelo menos 3 orçamentos |
| Manutenção do solar | R$ 300 por ano | Estimado | Pedir ao instalador |
| Degradação dos módulos | 0,5% ao ano | Valor típico | Conferir garantia do fabricante |
| Desconto de compensação (Fio B) | 15% sobre a energia compensada | Estimado | Depende da distribuidora e do ano de protocolo (Lei 14.300/2022). Conferir com o instalador |
| Reajuste anual da tarifa | 5% ao ano | Hipótese do grupo | Testado na análise de sensibilidade, inclusive com 0% |
| Fator de emissão da rede | 0,0385 kg CO2/kWh | Dado oficial de 2023 | MCTI (SIRENE). O valor muda a cada ano e a metodologia mudou em 2025 |
| Emissões do solar (ciclo de vida) | 0,041 kg CO2/kWh | Mediana da literatura | IPCC AR5 (2014) |

## Limitações dos dados

- O espaço comunitário é um **cenário hipotético** criado pelo grupo. Os resultados valem para esse cenário e não para um local específico.
- O reajuste da tarifa e o Fio B mudam com o tempo e podem alterar o retorno do solar.
- O fator de emissão médio da rede não captura o efeito marginal de economizar ou gerar energia em cada hora do dia.
