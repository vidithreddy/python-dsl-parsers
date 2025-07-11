# custom-language-parser

# Custom DSL Parser in Python

This project implements a complete lexer and recursive-descent parser for a custom-designed domain-specific language (DSL). The language supports variable assignments, arithmetic expressions, conditional branching (`if/then/else`), and nested loops (`while/do`).

The parser converts source code written in this DSL into a canonical abstract syntax tree (AST) representation, demonstrating language design, parsing techniques, and test-driven development in Python.

---

## Features

- Tokenization with a custom **Lexer**
- Recursive-descent **Parser** producing canonical ASTs
- Supports:
  - Variable assignments
  - Arithmetic expressions (+, -, *, /)
  - Conditional expressions with comparison operators
  - `if/then/else` branching
  - `while/do` loops (including nesting)
- Well-defined **grammar specification**
- Includes **unit tests** validating AST output

---

## Grammar Specification

See [`grammar.txt`](./grammar.txt) for the complete formal grammar definition.  

Example excerpt:
statement -> expression | if_statement | while_loop
expression -> variable '=' arithmetic_expression
arithmetic_expression -> term (('+' | '-') term)*

## Project File Structure

custom-language-parser<br />
    ├── parser.py<br />
    ├── grammar.txt<br />
    ├── example.txt<br />
    └── tests<br />
        └── test_parser.py<br />

---

## Purpose

This project was built to practice language design, formal grammar specification, and implementing a complete parsing pipeline in Python.

It demonstrates how to:
- Define a custom domain-specific language (DSL) with a formal grammar.
- Implement a **Lexer** to tokenize source code.
- Use recursive-descent parsing to produce a canonical AST.
- Support real programming constructs like assignments, arithmetic expressions, conditionals, and loops.
- Write clean, testable, and modular Python code following professional standards.

---
