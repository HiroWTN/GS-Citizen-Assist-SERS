"""Interface de texto para testar o assistente de energia.

Uso (a partir da raiz do repositório):
    python -m src.energia.cli                      # conversa interativa
    python -m src.energia.cli -p "vale a pena instalar solar?"
    python -m src.energia.cli --abreviado          # mantém siglas (kWh, R$) em vez de palavras
"""
from __future__ import annotations

import argparse

from .assistente import contexto, responder_energia


def main() -> None:
    parser = argparse.ArgumentParser(description="Assistente de energia do Citizen Assist AI")
    parser.add_argument("-p", "--pergunta", help="faz uma pergunta e encerra")
    parser.add_argument(
        "--abreviado",
        action="store_true",
        help="mantém siglas e símbolos (por padrão o texto é adaptado para leitor de tela)",
    )
    args = parser.parse_args()
    acessivel = not args.abreviado

    if args.pergunta:
        print(responder_energia(args.pergunta, acessivel=acessivel))
        return

    ctx = contexto()  # carrega e valida os dados uma vez, para falhar cedo se houver erro
    print("Assistente de energia. Digite sua pergunta, ou 'ajuda', ou 'sair'.")
    while True:
        try:
            pergunta = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if pergunta.lower() in {"sair", "fim", "exit", "quit"}:
            break
        print()
        print(
            responder_energia(
                pergunta,
                acessivel=acessivel,
                premissas=ctx["premissas"],
                equipamentos=ctx["equipamentos"],
            )
        )


if __name__ == "__main__":
    main()
