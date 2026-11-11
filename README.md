# Citizen Assist AI: orientações de energia para um espaço comunitário

Global Solution 2026 · FIAP · Ciência da Computação (1CCPI)
Disciplina: **Soluções em Energias Renováveis e Sustentáveis**



## Integrantes

| Nome completo | RM |
| --- | --- |
| *Nathan Hiroshi Watanabe* | *572806* |
| *Mateus de Oliveira Fernandes Neve* | *572431* |

## Público e problema

**Público:** pessoas com deficiência visual (cegueira e baixa visão) que frequentam um **espaço comunitário** de apoio em São Paulo, e a equipe que administra o espaço.

**Necessidade energética:** reduzir o custo da conta de luz do espaço **sem reduzir a iluminação adequada** (essencial para quem tem baixa visão) **e sem prejudicar os equipamentos assistivos** (computadores com leitor de tela, lupas eletrônicas, impressora braille). Além disso, a informação sobre energia precisa ser acessível: texto simples, sem depender de gráficos ou tabelas, compatível com leitor de tela.

**Como as orientações contribuem:** o assistente responde perguntas como "quanto o espaço gasta?", "vale trocar para LED?" e "vale instalar energia solar?", sempre com a conta explicada, as premissas, as limitações e as fontes.

> O espaço é um **cenário hipotético** com dados **estimados**.

## Funcionalidades de energia

1. **Consumo:** quanto o espaço e cada equipamento consomem por mês, em kWh e em reais.
2. **Eficiência:** quanto se economiza trocando lâmpadas fluorescentes por LED e controlando o standby.
3. **Energia solar:** tamanho do sistema, custo, economia e retorno estimado.
4. **Comparação:** três alternativas para a mesma necessidade e o mesmo período, com recomendação.
5. **Conta de luz:** explica kWh, tarifa, bandeira e custo de disponibilidade.
6. **Fontes:** lista as referências usadas.

Toda resposta segue o formato **Resposta, Como calculei, Limitações, Fontes**. Por padrão, o texto troca símbolos por palavras ("quilowatts-hora", "reais") para o leitor de tela.

## Alternativas comparadas

| Alternativa | O que é |
| --- | --- |
| **A. Eficiência** | LED no lugar das fluorescentes e controle do standby |
| **B. Solar** (fonte renovável) | Sistema fotovoltaico conectado à rede, dimensionado para o consumo atual |
| **C. Combinada** | Eficiência primeiro e solar dimensionado para o consumo já reduzido |

Resumo do cenário-base (detalhes em `analise/comparacao.md`):

| | Investimento | Retorno estimado | Saldo em 10 anos |
| --- | --- | --- | --- |
| A | R$ 1.380 | 10 meses | R$ 19.291 |
| B | R$ 18.450 | 4 anos e 5 meses | R$ 29.829 |
| C | R$ 13.530 | 3 anos e 1 mês | R$ 38.275 |

Achado importante: como a rede elétrica brasileira já é majoritariamente renovável, o solar sozinho evita quase nenhuma emissão líquida. O ganho dele é financeiro. A eficiência tem o benefício ambiental mais certo.

## Como executar

Requisitos: Python 3.9 ou superior. **Não há dependências externas.**

```bash
# conversar com o assistente
python -m src.energia.cli

# fazer uma pergunta e sair
python -m src.energia.cli -p "vale a pena instalar energia solar?"

# manter siglas e símbolos (kWh, R$) em vez de palavras
python -m src.energia.cli --abreviado

# regenerar o relatório de comparação
python -m src.energia.relatorio

# rodar os testes automáticos
python -m unittest discover -s tests -t .
```

Perguntas para testar: "quanto o espaço consome?", "quanto gasta a lupa?", "vale trocar para LED?", "tomada inteligente compensa?", "vale a pena energia solar?", "qual alternativa é a melhor?", "como entender minha conta de luz?", "quais são as fontes?".

## Como integrar ao assistente do grupo

O ponto de entrada é uma função de texto para texto:

```python
from src.energia.assistente import responder_energia

texto = responder_energia("vale a pena instalar energia solar?")  # str pronta para exibir ou ler em voz alta
```

Exemplo de uso como ferramenta de um agente de LLM (adaptar ao framework do grupo):

```python
from pydantic_ai import Agent
from src.energia.assistente import responder_energia

agent = Agent("openai:gpt-4o")  # trocar pelo modelo usado no projeto

@agent.tool_plain
def consultar_energia(pergunta: str) -> str:
    """Responde perguntas sobre consumo, eficiência e energia solar do espaço comunitário."""
    return responder_energia(pergunta)
```

O modelo de linguagem deve **repassar** o texto da ferramenta sem alterar números, premissas ou limitações.

## Estrutura do repositório

```
README.md
referencias.md
src/energia/        calculos.py, alternativas.py, assistente.py, formatacao.py, relatorio.py, cli.py
dados/              equipamentos.csv, premissas.json, FONTES_E_PREMISSAS.md
analise/            comparacao.md (gerado), justificativas.md
testes_usuarios/    roteiro_teste.md, registros.md, ajustes.md
docs/               roteiro_video.md
tests/              test_energia.py
ENTREGA.txt         modelo do arquivo a enviar no portal
```



## Limitações

- Dados estimados.
- Tarifa provisória: substituir pelo valor da fatura.
- O assistente funciona por regras (palavras-chave) e não entende qualquer pergunta livre. Perguntas fora do escopo recebem a lista do que ele sabe responder.
- Não substitui orçamento e projeto de um profissional habilitado.

