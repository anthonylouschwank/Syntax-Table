"""
table.py
Construcción de la tabla de análisis sintáctico predictivo LL(1).

Para cada producción A → α:
  - Para cada terminal a ∈ FIRST(α): agregar A → α a M[A, a]
  - Si ε ∈ FIRST(α): para cada b ∈ FOLLOW(A), agregar A → α a M[A, b]
"""

from grammar import Grammar, Production, EPSILON, END_OF_INPUT
from .first import first_of_sequence


# Tipo: tabla[no-terminal][terminal] = lista de producciones (lista vacía = error)
ParsingTable = dict[str, dict[str, list[Production]]]


def build_parsing_table(
    grammar: Grammar,
    first_sets: dict[str, set[str]],
    follow_sets: dict[str, set[str]],
) -> ParsingTable:
    """
    Construye la tabla de análisis sintáctico predictivo M[A, a].
    Si una celda contiene más de una producción → conflicto → no es LL(1).
    """
    # Inicializar tabla vacía para todos los no-terminales y terminales + $
    all_terminals = grammar.terminals + [END_OF_INPUT]
    table: ParsingTable = {
        nt: {t: [] for t in all_terminals}
        for nt in grammar.non_terminals
    }

    for production in grammar.productions:
        head = production.head
        body = production.body

        first_alpha = first_of_sequence(body, first_sets, grammar)

        # Regla: Para cada terminal a ∈ FIRST(α), M[A, a] += A → α
        for terminal in first_alpha - {EPSILON}:
            if terminal in table[head]:
                table[head][terminal].append(production)

        # Regla: Si ε ∈ FIRST(α), para cada b ∈ FOLLOW(A), M[A, b] += A → α
        if EPSILON in first_alpha:
            for terminal in follow_sets[head]:
                if terminal in table[head]:
                    table[head][terminal].append(production)

    return table


def is_ll1(table: ParsingTable) -> tuple[bool, list[tuple[str, str]]]:
    """
    Verifica si la gramática es LL(1) revisando conflictos en la tabla.
    Retorna (True, []) si es LL(1), o (False, lista_de_conflictos) si no lo es.
    """
    conflicts: list[tuple[str, str]] = []
    for non_terminal, row in table.items():
        for terminal, productions in row.items():
            if len(productions) > 1:
                conflicts.append((non_terminal, terminal))
    return (len(conflicts) == 0, conflicts)
