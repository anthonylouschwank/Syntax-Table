"""
main.py
Punto de entrada principal del programa.

Modos de uso:
  python main.py                → analiza las gramáticas de ejemplo
  python main.py --interactive  → permite ingresar una gramática manualmente
"""

import sys
import os

# Asegurar que el paquete raíz esté en el path al ejecutar directamente
sys.path.insert(0, os.path.dirname(__file__))

from grammar import parse_grammar
from analysis import compute_first, compute_follow, build_parsing_table
from display import print_full_analysis
from grammars.grammars import SAMPLE_GRAMMARS


def analyze_grammar_text(text: str, title: str):
    """Pipeline completo: texto → gramática → FIRST → FOLLOW → tabla → reporte."""
    grammar = parse_grammar(text)
    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, first_sets)
    table = build_parsing_table(grammar, first_sets, follow_sets)
    print_full_analysis(grammar, first_sets, follow_sets, table, title)


def run_sample_grammars():
    """Analiza todas las gramáticas de ejemplo definidas en grammars/grammars.py."""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║   Calculadora FIRST, FOLLOW y Tabla LL(1)               ║")
    print("╚══════════════════════════════════════════════════════════╝")

    for title, text in SAMPLE_GRAMMARS.items():
        analyze_grammar_text(text, title)


def run_interactive():
    """Modo interactivo: el usuario ingresa una gramática en consola."""
    print("\n── Modo interactivo ──────────────────────────────────────────")
    print("Ingrese la gramática (línea vacía para terminar):")
    print("Formato: A -> B C | ε\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)

    if not lines:
        print("No se ingresó ninguna gramática.")
        return

    title = input("Nombre de la gramática (Enter para omitir): ").strip() or "Gramática ingresada"
    analyze_grammar_text("\n".join(lines), title)


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive()
    else:
        run_sample_grammars()
