# Justificativas das recomendações

Os números abaixo são os do cenário-base gerado por `python -m src.energia.relatorio` (ver `comparacao.md`). 

## Recomendação 1: começar pela eficiência (alternativa A)

**Por quê.** Quase metade do consumo (47%) vem da iluminação. Trocar 24 lâmpadas fluorescentes por LED economiza cerca de 125 kWh por mês, o que é o maior ganho individual do estudo.

- **Custo:** o investimento total da alternativa A é de cerca de R$ 1.380, e o retorno estimado é de aproximadamente 10 meses.
- **Viabilidade:** alta. É uma troca simples, sem obra civil e sem autorização de terceiros.
- **Impacto ambiental:** reduz o consumo na origem, o que é o impacto mais certo. As lâmpadas fluorescentes contêm mercúrio e precisam ir para a logística reversa.
- **Cuidado com o público:** economizar energia não pode reduzir a iluminação. Pessoas com baixa visão dependem de luz adequada e bem distribuída. Por isso o LED escolhido deve ter fluxo luminoso equivalente, e a iluminância deve ser medida antes e depois com luxímetro (NBR ISO/CIE 8995-1).

## Recomendação 2: tomadas inteligentes só em grupo, e com expectativa baixa

**Por quê.** O consumo parado na tomada (standby) soma só cerca de 24 kWh por mês. Cada tomada inteligente gasta cerca de 1 W o tempo todo (cerca de 0,7 kWh por mês). Por isso a recomendação é usar uma tomada ou régua inteligente por **grupo** de aparelhos, e não uma por aparelho.

- **Ganho líquido estimado:** cerca de 19 kWh por mês, pequeno em comparação com a iluminação.
- **Benefício de acessibilidade:** quem não enxerga os indicadores luminosos dos aparelhos pode desligar tudo por horário ou por comando de voz. Esse benefício existe mesmo quando o ganho de energia é pequeno, mas o aplicativo precisa ser compatível com leitor de tela.

## Recomendação 3: dimensionar o solar depois da eficiência (alternativa C)

**Por quê.** O sistema solar é dimensionado pelo consumo. Se a eficiência vem antes, o consumo cai e o sistema necessário diminui de cerca de 4,1 kWp (alternativa B) para cerca de 2,7 kWp (alternativa C).

- **Custo:** a alternativa C custa cerca de R$ 13.530, contra R$ 18.450 da B, e tem retorno estimado de cerca de 3 anos e 1 mês, contra 4 anos e 5 meses.
- **Saldo em 10 anos:** é o maior entre as três alternativas neste cenário.
- **Viabilidade:** média. Exige telhado ou área sem sombra, autorização do proprietário e da distribuidora, e um instalador habilitado. Se o espaço for alugado ou cedido, a autorização é o primeiro passo. Outra possibilidade a pesquisar é a energia por assinatura, que não exige telhado.
- **Sensibilidade:** nos cenários testados (tarifa de 20% a menos até 20% a mais, solar 20% mais caro ou mais barato, sol 15% menor, sem reajuste da tarifa), o retorno da alternativa C ficou entre cerca de 2 anos e 7 meses e 3 anos e 11 meses. A ordem entre as alternativas não mudou.

## O que o estudo não prova

1. **O benefício climático do solar é pequeno.** Com o fator médio da rede brasileira de 2023 (38,5 g CO2/kWh) e as emissões de ciclo de vida do solar (41 g CO2/kWh), o solar sozinho evita praticamente nenhuma emissão líquida. A rede brasileira já é majoritariamente renovável. O ganho do solar aqui é financeiro e de previsibilidade de custo. Dizer o contrário seria exagero.
2. **O fator médio não é o efeito marginal.** Economizar ou gerar energia em horários de maior uso de usinas térmicas pode evitar mais emissões do que a média indica. Este estudo usa o dado oficial médio e não mede esse efeito.
3. **Os dados são estimados.** Tarifa, potências, horas de uso, preços e HSP precisam ser trocados por dados reais antes de qualquer decisão de compra.
4. **Fio B e reajuste da tarifa mudam com o tempo,** e podem piorar o retorno do solar nos próximos anos.
5. **Itens fora do horizonte:** troca do inversor (10 a 15 anos), descarte dos módulos e impostos específicos não foram incluídos.

## Como o assistente usa estas justificativas

Cada resposta do assistente (`src/energia/assistente.py`) é montada a partir dos mesmos cálculos e termina com as limitações e as fontes. O teste `test_resposta_coerente_com_a_analise` verifica que o investimento e a potência do solar citados pelo assistente são iguais aos do relatório.
