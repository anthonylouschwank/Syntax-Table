"""
first.py
Cálculo del conjunto FIRST para gramáticas libres de contexto.
"""

from grammar import Grammar, EPSILON


def compute_first(grammar: Grammar) -> dict[str, set[str]]:
    """
    Calcula FIRST(A) para cada no-terminal A de la gramática.
    """
    first: dict[str, set[str]] = {nt: set() for nt in grammar.non_terminals}

    changed = True
    while changed:
        changed = False
        for production in grammar.productions:
            head = production.head
            additions = first_of_sequence(production.body, first, grammar)
            before = len(first[head])
            first[head] |= additions
            if len(first[head]) > before:
                changed = True

    return first


def first_of_sequence(
    symbols: list[str],
    first_sets: dict[str, set[str]],
    grammar: Grammar,
) -> set[str]:
    """
    Calcula FIRST de una secuencia de símbolos a = X1 X2 ... Xn.
    """
    result: set[str] = set()

    for symbol in symbols:
        if symbol == EPSILON:
            result.add(EPSILON)
            break

        if grammar.is_terminal(symbol):
            result.add(symbol)
            break  # los terminales no derivan ε

        # Símbolo no-terminal: tomar su FIRST actual (puede estar incompleto)
        symbol_first = first_sets.get(symbol, set())
        result |= symbol_first - {EPSILON}

        if EPSILON not in symbol_first:
            break  # este símbolo no puede derivar ε → se detiene la propagación
    else:
        # Todos los símbolos pueden derivar ε
        result.add(EPSILON)

    return result
