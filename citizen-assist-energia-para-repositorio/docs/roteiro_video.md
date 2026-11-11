# Roteiro do vídeo técnico (máximo de 3 minutos)

Vídeo **não listado** no YouTube. Narração em ritmo calmo, cerca de 130 palavras por minuto, para caber em 3 minutos. Conferir os números com o relatório gerado antes de gravar. Se os dados em `dados/` mudarem, os números abaixo mudam.

## Cena 1 · Público e necessidade (0:00 a 0:30)

**Na tela:** título do projeto e a pasta `src/energia/` no repositório.

**Narração:** "Este é o Citizen Assist AI, com a contribuição de energias renováveis. Nosso público são pessoas com deficiência visual que frequentam um espaço comunitário em São Paulo. A necessidade é reduzir a conta de luz do espaço sem tirar a iluminação adequada, que é essencial para quem tem baixa visão, e sem prejudicar computadores com leitor de tela, lupas e impressora braille."

## Cena 2 · Análise de consumo (0:30 a 1:05)

**Na tela:** tabela de consumo de `analise/comparacao.md` e o gráfico ou lista por categoria.

**Narração:** "Montamos um cenário estimado do espaço. Energia é potência vezes tempo. Somando todos os aparelhos, o espaço consome cerca de 531 quilowatts-hora por mês, perto de 505 reais. A iluminação responde por 47% do consumo. Todos os dados são estimados e estão marcados no repositório com a origem de cada um."

## Cena 3 · Comparação das alternativas (1:05 a 1:50)

**Na tela:** tabela de resultados das alternativas A, B e C.

**Narração:** "Comparamos três alternativas para a mesma necessidade, em 10 anos. A, eficiência: LED e controle de standby. Custa cerca de 1.380 reais e se paga em 10 meses. B, energia solar, a fonte renovável: um sistema de 4,1 quilowatts-pico custa cerca de 18 mil reais e se paga em 4 anos e 5 meses. C, as duas juntas: com a eficiência primeiro, o solar necessário cai para 2,7 quilowatts-pico, o investimento cai e o retorno melhora para 3 anos e 1 mês. Um achado honesto: como a rede elétrica brasileira já é majoritariamente renovável, o solar sozinho evita quase nenhuma emissão líquida. O ganho dele é financeiro."

## Cena 4 · Demonstração no assistente (1:50 a 2:35)

**Na tela:** terminal ou interface do assistente.

**Perguntas a demonstrar, nesta ordem:**
1. "Quanto o espaço consome?"
2. "Vale a pena instalar energia solar?"
3. Mostrar o formato da resposta: Resposta, Como calculei, Limitações, Fontes.
4. Mostrar o modo acessível, sem símbolos, lido por um leitor de tela (se possível, com o áudio).

**Narração:** "No assistente, a pessoa pergunta com as próprias palavras. A resposta vem da mesma análise e sempre mostra como foi calculada, as limitações e as fontes. O texto troca símbolos por palavras, para o leitor de tela ler sem confusão."

## Cena 5 · Recomendações e limitações (2:35 a 3:00)

**Na tela:** lista curta das recomendações e dos avisos.

**Narração:** "Nossa recomendação: começar pela eficiência, conferindo a iluminação com um luxímetro, e depois dimensionar o solar para o consumo reduzido. Os valores são estimativas, a tarifa precisa vir da fatura real, e o solar depende de telhado, autorização e orçamentos. Nada aqui é economia garantida."

## Checklist antes de gravar

- [ ] Duração final de 3 minutos ou menos
- [ ] Números conferidos com `analise/comparacao.md`
- [ ] Demonstração mostra o assistente respondendo, não só slides
- [ ] Limitações citadas em voz alta
- [ ] Vídeo configurado como **não listado** e link testado em janela anônima
- [ ] Se citar testes com usuários, citar apenas o que de fato foi feito
