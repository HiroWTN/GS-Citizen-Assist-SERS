# Citizen Assist AI: orientações de energia para um espaço comunitário

Global Solution 2026 · FIAP · Ciência da Computação (1CCPI)  
Disciplina: **Soluções em Energias Renováveis e Sustentáveis**

## Integrantes

| Nome completo | RM |
| --- | --- |
| Nathan Hiroshi Watanabe | 572806 |
| Mateus de Oliveira Fernandes Neve | 572431 |

## Público e problema

**Público:** pessoas com deficiência visual (cegueira e baixa visão) que frequentam um **espaço comunitário** de apoio em São Paulo, e a equipe que administra o espaço.

**Necessidade energética:** reduzir o custo da conta de luz do espaço **sem reduzir a iluminação adequada** (essencial para quem tem baixa visão) **e sem prejudicar os equipamentos assistivos** (computadores com leitor de tela, lupas eletrônicas, impressora braille). Além disso, a informação sobre energia precisa ser acessível: texto simples, sem depender de gráficos ou tabelas, compatível com leitor de tela.

**Como as orientações contribuem:** o assistente responde perguntas como "quanto o espaço gasta?", "vale trocar para LED?" e "vale instalar energia solar?", sempre com a conta explicada, as premissas, as limitações e as fontes.

> O espaço é um **cenário hipotético** com dados **estimados**. Os resultados são simulações e não garantem economia em um local real.

## Funcionalidades de energia

1. **Consumo:** quanto o espaço e cada equipamento consomem por mês, em kWh e em reais.
2. **Eficiência:** quanto se economiza trocando lâmpadas fluorescentes por LED e controlando o standby.
3. **Energia solar:** tamanho do sistema, custo, economia e retorno estimado.
4. **Comparação:** três alternativas para a mesma necessidade e o mesmo período, com recomendação.
5. **Conta de luz:** explica kWh, tarifa, bandeira e custo de disponibilidade.
6. **Fontes:** lista as referências usadas.

As respostas do módulo seguem o formato **Resposta, Como calculei, Limitações, Fontes**. Por padrão, o texto troca símbolos por palavras (por exemplo, "quilowatts-hora" e "reais") para facilitar o uso com leitor de tela.

## Alternativas comparadas

| Alternativa | O que é |
| --- | --- |
| **A. Eficiência** | LED no lugar das fluorescentes e controle do standby |
| **B. Solar** (fonte renovável) | Sistema fotovoltaico conectado à rede, dimensionado para o consumo atual |
| **C. Combinada** | Eficiência primeiro e solar dimensionado para o consumo já reduzido |

Resumo do cenário-base (detalhes em `citizen-assist-energia-para-repositorio/analise/comparacao.md`):

| Alternativa | Investimento | Retorno estimado | Saldo em 10 anos |
| --- | ---: | ---: | ---: |
| A | R$ 1.380 | 10 meses | R$ 19.291 |
| B | R$ 18.450 | 4 anos e 5 meses | R$ 29.829 |
| C | R$ 13.530 | 3 anos e 1 mês | R$ 38.275 |

Achado do cenário estudado: com as premissas adotadas, a eficiência tem benefício ambiental mais direto. O efeito climático líquido do solar foi estimado como próximo de zero usando o fator médio histórico da rede e as emissões de ciclo de vida adotadas. Consulte as premissas antes de reutilizar essa conclusão.

## Como executar

Requisitos: Python 3.9 ou superior. O módulo usa apenas a biblioteca padrão do Python.

**Importante:** os comandos abaixo devem ser executados a partir da pasta do módulo de energia. Se você estiver na raiz do repositório recém-clonado, entre nela primeiro:

```bash
cd citizen-assist-energia-para-repositorio
```

Depois, execute:

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

Perguntas para testar: "quanto o espaço consome?", "quanto gasta a lupa?", "vale trocar para LED?", "tomada inteligente compensa?", "vale a pena energia solar?", "qual alternativa é a melhor?", "como entender minha conta de luz?" e "quais são as fontes?".

## Integração com o Citizen Assist AI

O módulo disponibiliza uma função de texto para texto:

```python
from src.energia.assistente import responder_energia

texto = responder_energia("vale a pena instalar energia solar?")
```

Essa função pode ser chamada pelo assistente principal do grupo ou registrada como ferramenta de um agente de IA. Exemplo ilustrativo para projetos que utilizem Pydantic AI (a integração exige adaptar e registrar a ferramenta na aplicação principal):

```python
from pydantic_ai import Agent
from src.energia.assistente import responder_energia

agent = Agent("openai:gpt-4o")  # substituir pelo modelo usado no projeto

@agent.tool_plain
def consultar_energia(pergunta: str) -> str:
    """Responde perguntas sobre consumo, eficiência e energia solar do espaço comunitário."""
    return responder_energia(pergunta)
```

**Status da integração:** este repositório contém o módulo de energia e seu ponto de entrada. Para demonstrar a integração exigida no desafio, a aplicação principal do Citizen Assist AI precisa chamar essa função e apresentar as respostas ao usuário. O exemplo acima, isoladamente, não comprova que essa integração já foi realizada.

O texto produzido pela ferramenta deve ser apresentado sem alterar números, premissas ou limitações.

## Testes com usuários

O roteiro e os modelos de registro estão em `citizen-assist-energia-para-repositorio/testes_usuarios/`.

**Situação atual:** os arquivos dessa pasta são modelos para documentar a validação. Eles devem ser preenchidos pela equipe depois de realizar testes reais com pessoas do público escolhido. Não há resultados de testes com usuários registrados neste repositório neste momento.

Registrem as tarefas realizadas, a compreensão das respostas, os comentários recebidos e os ajustes efetivamente feitos. Não incluam nomes, contatos ou outros dados pessoais desnecessários.

## Estrutura do repositório

```text
GS-Citizen-Assist-SERS/
├── README.md
└── citizen-assist-energia-para-repositorio/
    ├── analise/
    │   ├── comparacao.md
    │   └── justificativas.md
    ├── dados/
    │   ├── equipamentos.csv
    │   ├── premissas.json
    │   └── FONTES_E_PREMISSAS.md
    ├── referencias.md
    ├── src/energia/
    │   ├── calculos.py
    │   ├── alternativas.py
    │   ├── assistente.py
    │   ├── formatacao.py
    │   ├── relatorio.py
    │   └── cli.py
    ├── tests/test_energia.py
    └── testes_usuarios/
        ├── roteiro_teste.md
        ├── registros.md
        └── ajustes.md
```

## Limitações

- O espaço comunitário é hipotético e os dados de consumo são estimados.
- A tarifa de R$ 0,95/kWh é provisória: substitua pelo valor efetivo da fatura do local analisado.
- Os parâmetros de geração solar, Fio B, custos e manutenção são estimativas e precisam ser validados com localização, enquadramento regulatório e orçamentos reais.
- O assistente funciona por regras de palavras-chave e não entende qualquer pergunta livre. Perguntas fora do escopo recebem uma lista de assuntos que ele sabe responder.
- A análise não substitui orçamento, vistoria ou projeto de profissional habilitado.
