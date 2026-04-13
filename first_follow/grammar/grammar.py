"""
grammar.py
Representación y parsing de gramáticas libres de contexto.
"""

EPSILON = 'ε'
END_OF_INPUT = '$'


class Production:
    """Representa una producción A → α"""

    def __init__(self, head: str, body: list[str]):
        self.head = head
        self.body = body  # lista de símbolos; [EPSILON] para producciones vacías

    def is_epsilon(self) -> bool:
        return self.body == [EPSILON]

    def __repr__(self):
        return f"{self.head} → {' '.join(self.body)}"


class Grammar:
    """
    Almacena una gramática libre de contexto con sus producciones,
    terminales y no-terminales.
    """

    def __init__(self):
        self.productions: list[Production] = []
        self.non_terminals: list[str] = []
        self.terminals: list[str] = []
        self.start_symbol: str | None = None

    def add_production(self, head: str, body: list[str]):
        self.productions.append(Production(head, body))
        if head not in self.non_terminals:
            self.non_terminals.append(head)
        if self.start_symbol is None:
            self.start_symbol = head

    def get_productions_for(self, non_terminal: str) -> list[Production]:
        return [p for p in self.productions if p.head == non_terminal]

    def is_non_terminal(self, symbol: str) -> bool:
        return symbol in self.non_terminals

    def is_terminal(self, symbol: str) -> bool:
        return symbol not in self.non_terminals and symbol not in (EPSILON, END_OF_INPUT)

    def derive_terminals(self):
        """Infiere el conjunto de terminales a partir de las producciones."""
        seen = set()
        for p in self.productions:
            for sym in p.body:
                if sym not in self.non_terminals and sym not in (EPSILON, END_OF_INPUT):
                    seen.add(sym)
        # Preservar orden de aparición
        ordered = []
        for p in self.productions:
            for sym in p.body:
                if sym in seen and sym not in ordered:
                    ordered.append(sym)
        self.terminals = ordered
