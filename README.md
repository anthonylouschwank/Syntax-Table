# FIRST, FOLLOW y Tabla LL(1)

Implementación modular en Python para calcular conjuntos FIRST, FOLLOW y construir la tabla de análisis sintáctico predictivo LL(1) para cualquier gramática libre de contexto.

---

## Estructura del proyecto

```
first_follow/
├── main.py                  ← Punto de entrada
├── grammar/
│   ├── grammar.py           ← Clases Grammar y Production
│   └── parser.py            ← Convierte texto a objeto Grammar
├── analysis/
│   ├── first.py             ← Algoritmo FIRST
│   ├── follow.py            ← Algoritmo FOLLOW
│   └── table.py             ← Construcción de tabla LL(1) y detección de conflictos
├── display/
│   └── display.py           ← Impresión de resultados en consola
└── grammars/
    └── grammars.py          ← Gramáticas de ejemplo
```

---

## Requisitos

- Python 3.10+
- Sin dependencias externas

---

## Cómo correrlo

**Modo automático** (corre las tres gramáticas de ejemplo):
```bash
python main.py
```

**Modo interactivo** (ingresa su propia gramática):
```bash
python main.py --interactive
python main.py -i
```

### Formato de entrada

Una producción por línea, alternativas separadas con `|`, símbolos separados por espacios:

```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
```

---

## Gramáticas probadas

### 1. Expresiones Aritméticas

```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
```

> **¿Es LL(1)? Sí**
> La recursión izquierda fue eliminada con E' y T', lo que garantiza conjuntos FIRST disjuntos en todas las alternativas.

---

### 2. Sentencias if-else *(dangling else)*

```
S -> if E then S else S | if E then S | other
E -> bool
```

> **¿Es LL(1)? No**
> Conflicto en `M[S, if]`: las dos producciones de S que empiezan con `if` tienen el mismo FIRST. Es el problema clásico del *dangling else*, irresoluble con LL(1) puro sin modificar la gramática.
> Se eligió esta gramática para ilustrar explícitamente qué es un conflicto LL(1).

---

### 3. Declaraciones de Variables

```
D  -> T id D'
D' -> , id D' | ;
T  -> int | float | bool
```

> **¿Es LL(1)? Sí**
> Modela declaraciones estilo C/Java (`int x, y;`). Cada alternativa de `T` tiene FIRST disjunto (`int`, `float`, `bool`) y las de `D'` también (`,` vs `;`).
> Se eligió porque representa un patrón real de lenguajes de programación.

---

## Resultado del análisis LL(1)

| Gramática | ¿LL(1)? | Motivo |
|---|---|---|
| Expresiones Aritméticas | Sí | FIRST disjuntos en todas las alternativas |
| if-else (dangling else) | No | Conflicto en `M[S, if]` |
| Declaraciones de Variables | Sí | FIRST disjuntos, sin ambigüedad |

---

## Video

https://youtu.be/dU9mGbPWfMU
