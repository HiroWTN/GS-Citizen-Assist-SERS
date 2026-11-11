# Roteiro de teste com usuários

Objetivo: verificar se as orientações de energia do assistente são **compreensíveis** e **úteis** para pessoas com deficiência visual e para a equipe do espaço comunitário.

## Cuidados éticos

- **Participação voluntária.** Explicar o objetivo e que a pessoa pode parar a qualquer momento.
- **Consentimento verbal ou escrito** antes de começar. Se for por escrito, oferecer o texto em formato acessível ou lê-lo em voz alta.
- **Sem dados pessoais.** Não registrar nome, contato, endereço, RM de terceiros ou informações de saúde. Identificar participantes como P1, P2, P3.
- **Não pressupor.** Cada pessoa tem uma experiência e uma forma de usar tecnologia. Perguntar como prefere usar, em vez de supor.
- **Quem testa é o assistente, não a pessoa.** Dificuldades são falhas do assistente.
- **Instituições.** Para recrutar participantes, procurar associações ou centros de apoio e pedir autorização à coordenação antes de qualquer teste.

## Preparação

1. Deixar o assistente rodando (`python -m src.energia.cli`) ou integrado à interface do grupo.
2. Combinar o formato: leitura por leitor de tela (NVDA no Windows, TalkBack no Android, VoiceOver no iPhone) ou leitura em voz alta pelo aplicador.
3. Ter à mão o modo abreviado (`--abreviado`) apenas para comparação com o modo acessível, se desejado.

## Tarefas (cenários)

| Nº | Cenário | Pergunta sugerida |
| --- | --- | --- |
| 1 | Entender o consumo do espaço | "Quanto o espaço gasta de energia?" |
| 2 | Decidir sobre a iluminação | "Vale a pena trocar as lâmpadas por LED?" |
| 3 | Considerar energia renovável | "Vale a pena instalar energia solar?" |
| 4 | Escolher entre opções | "Qual alternativa é a melhor?" |
| 5 | Entender a fatura | "Como entender minha conta de luz?" |

Pedir que a pessoa pergunte com as próprias palavras. Registrar também as perguntas que o assistente **não** soube responder.

## Perguntas após cada tarefa

1. Você entendeu a resposta? (sim, em parte, não)
2. O que ficou confuso ou longo demais?
3. Alguma palavra ou número foi difícil de acompanhar por voz?
4. A resposta ajuda a decidir alguma coisa? O quê?
5. Faltou alguma informação?

