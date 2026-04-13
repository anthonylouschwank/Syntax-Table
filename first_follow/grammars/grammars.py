"""
grammars.py
Gramáticas de ejemplo para probar la implementación.
"""

# ── Gramática 1: Expresiones aritméticas
ARITHMETIC = """\
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
"""

# ── Gramática 2: Sentencias if-else (simplificada)
IF_ELSE = """\
S -> if E then S else S | if E then S | other
E -> bool
"""

# ── Gramática 3: Declaraciones de variables
DECLARATIONS = """\
D  -> T id D'
D' -> , id D' | ;
T  -> int | float | bool
"""


SAMPLE_GRAMMARS = {
    "Expresiones Aritméticas": ARITHMETIC,
    "Sentencias if-else (dangling else)": IF_ELSE,
    "Declaraciones de Variables": DECLARATIONS,
}
