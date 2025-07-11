# python-dsl-parser

# Python DSL Parsers

This repository showcases two custom-designed **domain-specific language (DSL) parsers** implemented in Python. Each project demonstrates progressively advanced parsing techniques, from a simple untyped DSL to a typed language with static type checking and block scoping.

These projects highlight my ability to design grammars, implement lexers and recursive-descent parsers, enforce scoping rules, and build abstract syntax trees (ASTs) in Python.

---

## Projects Included

### 1. custom-language-parser

A basic untyped DSL parser that supports:

- Variable assignments
- Arithmetic expressions (+, -, *, /)
- Conditional expressions with comparison operators
- `if/then/else` branching
- `while/do` loops (including nesting)

Features:

- Custom **Lexer** for tokenization
- Recursive-descent **Parser** producing canonical ASTs
- Clean, modular design
- Test suite validating AST output

**Folder:** [custom-language-parser/](./custom-language-parser/)

---

### 2. typed-language-parser

A more advanced DSL parser with:

- **Typed variable declarations** (int, float)
- Block scoping using braces `{ }`
- Type checking (e.g., preventing int/float mismatches)
- Symbol tables enforcing declaration-before-use
- Nested `if/then/else` and `while/do` constructs with proper scoping

Features:

- Custom **Lexer** supporting numbers, floats, operators, braces
- Recursive-descent **Parser** building a typed AST
- Enforces static type checking and scoping rules
- Detailed error reporting
- Comprehensive test suite

**Folder:** [typed-language-parser/](./typed-language-parser/)

---

## Skills Demonstrated

- Formal grammar design and specification  
- Lexer and recursive-descent parser implementation in Python  
- AST construction with custom Node classes  
- Static type checking and error reporting  
- Block scoping with symbol table management  
- Clean, modular, professional code design  
- Test-driven development practices  

---

## Folder Structure

python-dsl-parsers/<br />
├── custom-language-parser/<br />
│ ├── parser.py<br />
│ ├── test_parser.py<br />
│ ├── grammar.txt<br />
│ └── README.md<br />
└── typed-language-parser/<br />
  ├── parser.py<br />
  ├── test_parser.py<br />
  ├── grammar.txt<br />
  └── README.md<br />


## Purpose
This repository showcases two custom-designed **domain-specific language (DSL) parsers** implemented in Python. Each project demonstrates progressively advanced parsing techniques, from a simple untyped DSL to a typed language with static type checking and block scoping.

These projects highlight my ability to design grammars, implement lexers and recursive-descent parsers, enforce scoping rules, and build abstract syntax trees (ASTs) in Python.
