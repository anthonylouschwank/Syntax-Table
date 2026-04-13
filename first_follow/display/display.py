"""
display.py
Funciones de presentación: imprime gramáticas, conjuntos FIRST/FOLLOW
y la tabla de análisis sintáctico de forma legible en consola.
"""

from grammar import Grammar, EPSILON, END_OF_INPUT
from analysis.table import ParsingTable, is_ll1


def print_grammar(grammar: Grammar, title: str = "Gramática"):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    print(f"  Símbolo inicial: {grammar.start_symbol}")
    print(f"  No-terminales:   {', '.join(grammar.non_terminals)}")
    print(f"  Terminales:      {', '.join(grammar.terminals)}")
    print("\n  Producciones:")
    for p in grammar.productions:
        print(f"    {p}")


def print_first_follow(
    grammar: Grammar,
    first_sets: dict[str, set[str]],
    follow_sets: dict[str, set[str]],
):
    print("\n  Conjuntos FIRST y FOLLOW:")
    print(f"  {'No-terminal':<14} {'FIRST':<35} {'FOLLOW'}")
    print(f"  {'-' * 70}")
    for nt in grammar.non_terminals:
        first_str = '{ ' + ', '.join(sorted(first_sets[nt])) + ' }'
        follow_str = '{ ' + ', '.join(sorted(follow_sets[nt])) + ' }'
        print(f"  {nt:<14} {first_str:<35} {follow_str}")


def print_parsing_table(grammar: Grammar, table: ParsingTable):
    """Imprime la tabla de análisis sintáctico en formato de rejilla."""
    all_terminals = grammar.terminals + [END_OF_INPUT]
    col_width = 22
    nt_width = 14

    print("\n  Tabla de Análisis Sintáctico Predictivo:")

    # Cabecera
    header = f"  {'': <{nt_width}}" + "".join(f"{t: ^{col_width}}" for t in all_terminals)
    print(header)
    print(f"  {'-' * (nt_width + col_width * len(all_terminals))}")

    for nt in grammar.non_terminals:
        row = f"  {nt: <{nt_width}}"
        for t in all_terminals:
            productions = table[nt][t]
            if not productions:
                cell = ""
            elif len(productions) == 1:
                cell = str(productions[0])
            else:
                # Conflicto: mostrar todas las producciones separadas por " / "
                cell = " / ".join(str(p) for p in productions)
            row += f"{cell: ^{col_width}}"
        print(row)


def print_ll1_result(table: ParsingTable):
    ll1, conflicts = is_ll1(table)
    print()
    if ll1:
        print(" La gramática ES LL(1): no hay conflictos en la tabla.")
    else:
        print(" La gramática NO es LL(1). Conflictos encontrados:")
        for nt, t in conflicts:
            prods = table[nt][t]
            print(f"    M[{nt}, {t}] = " + " | ".join(str(p) for p in prods))


def print_full_analysis(
    grammar: Grammar,
    first_sets: dict[str, set[str]],
    follow_sets: dict[str, set[str]],
    table: ParsingTable,
    title: str = "Gramática",
):
    """Wrapper que imprime todo el análisis de una gramática."""
    print_grammar(grammar, title)
    print_first_follow(grammar, first_sets, follow_sets)
    print_parsing_table(grammar, table)
    print_ll1_result(table)
    print()
