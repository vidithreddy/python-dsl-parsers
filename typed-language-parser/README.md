# typed-language-parser

# Typed DSL Parser in Python

This project implements a complete lexer and recursive-descent parser for a custom-designed, **typed** domain-specific language (DSL). The language supports variable declarations with types, block scoping with braces, arithmetic expressions, conditional branching (`if/then/else`), and nested loops (`while/do`).

The parser enforces type checking (e.g., int vs. float) and scope rules to prevent invalid redeclarations and use-before-declare errors. It builds a structured abstract syntax tree (AST) with custom Node classes.

---

## Features

- Tokenization with a custom **Lexer**:
  - Supports integers, floats
  - Operators (+, -, *, /, comparison)
  - Keywords (if, then, else, while, do, int, float)
  - Block scoping with braces

- Recursive-descent **Parser** producing a typed AST:
  - Variable declarations with type enforcement
  - Assignments
  - Conditional expressions with comparison
  - Nested `if`/`else` and `while` blocks with proper scoping
  - Type checking between variables and expressions

- **Symbol Table**:
  - Enforces block scoping
  - Tracks declared variables and their types
  - Prevents redeclaration in same scope

- **Error Reporting**:
  - Detailed messages for:
    - Type mismatches
    - Use-before-declare
    - Redeclaration errors

- Well-defined **grammar specification** (see [grammar.txt](./grammar.txt))

- **Unit tests** validating parser correctness and rule enforcement

---

## Purpose

This project demonstrates:

- Building a custom typed programming language's grammar
- Implementing a robust Lexer and recursive-descent Parser in Python
- Enforcing static type checking and block scoping rules
- Designing and using an Abstract Syntax Tree (AST)
- Writing clear, maintainable, modular code with professional standards

It serves as a practical example of compiler front-end design, type systems, and language parsing.

---

## Grammar Specification

See [`grammar.txt`](./grammar.txt) for the full formal grammar.  

Example excerpt:
declaration -> type variable '=' arithmetic_expression
if_statement -> 'if' condition 'then' '{' statement* '}' ('else' '{' statement* '}')?

---

## Project Structure
typed-language-parser<br />
├── parser.py # Lexer and Parser implementation with AST and type checking<br />
├── test_parser.py # Unit tests validating parser rules<br />
└── grammar.txt # Formal grammar definition<br />