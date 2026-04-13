"""
parser.py
Convierte texto con formato BNF simplificado a un objeto Grammar.
"""

from .grammar import Grammar, EPSILON


def parse_grammar(text: str) -> Grammar:
    """
    Parsea una gramática en formato de texto.
    """
    grammar = Grammar()
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]

    for line in lines:
        if '->' not in line:
            raise ValueError(f"Línea sin '->': {line!r}")

        head, _, rest = line.partition('->')
        head = head.strip()

        alternatives = rest.split('|')
        for alt in alternatives:
            symbols = alt.split()
            if not symbols or symbols == ['']:
                body = [EPSILON]
            elif len(symbols) == 1 and symbols[0] in ('ε', 'epsilon', "''", '""'):
                body = [EPSILON]
            else:
                body = symbols
            grammar.add_production(head, body)

    grammar.derive_terminals()
    return grammar
