"""
main.py — Ponto de entrada do Streamify

Como executar:
    python main.py

Raiz de composição (Composition Root):
    Este é o único lugar onde classes concretas são instanciadas e
    as dependências são montadas. Todos os outros módulos recebem
    abstrações via injeção de dependência (DIP).
"""

from ui.terminal_ui import TerminalUI


def main() -> None:
    app = TerminalUI()
    app.run()


if __name__ == "__main__":
    main()
