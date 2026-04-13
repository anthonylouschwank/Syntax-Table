"""
follow.py
Cálculo del conjunto FOLLOW para gramáticas libres de contexto.

FOLLOW(A) = conjunto de terminales que pueden aparecer inmediatamente
despues de A en alguna forma sentencial.
"""

from grammar import Grammar, EPSILON, END_OF_INPUT
from .first import first_of_sequence


def compute_follow(
    grammar: Grammar,
    first_sets: dict[str, set[str]],
) -> dict[str, set[str]]:
    """
    Calcula FOLLOW(A) para cada no-terminal A.
    """
    follow: dict[str, set[str]] = {nt: set() for nt in grammar.non_terminals}

    # Regla 1: símbolo inicial siempre tiene $ en su FOLLOW
    if grammar.start_symbol:
        follow[grammar.start_symbol].add(END_OF_INPUT)

    changed = True
    while changed:
        changed = False
        for production in grammar.productions:
            head = production.head
            body = production.body

            for i, symbol in enumerate(body):
                if not grammar.is_non_terminal(symbol):
                    continue

                beta = body[i + 1:]  # resto de la producción tras el símbolo

                # Regla 2: agregar FIRST(B) \ {ε} a FOLLOW(symbol)
                if beta:
                    first_beta = first_of_sequence(beta, first_sets, grammar)
                    additions = first_beta - {EPSILON}
                else:
                    first_beta = {EPSILON}
                    additions = set()

                before = len(follow[symbol])
                follow[symbol] |= additions

                # Regla 3: si B puede derivar ε (o B está vacío), FOLLOW(head) ⊆ FOLLOW(symbol)
                if EPSILON in first_beta:
                    follow[symbol] |= follow[head]

                if len(follow[symbol]) > before:
                    changed = True

    return follow
