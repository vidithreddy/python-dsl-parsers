"""
Test suite for verifying the output of a custom DSL parser.

Runs multiple parsing scenarios to ensure the parser produces
the expected abstract syntax tree (AST) representations.

Each test compares the parser output to an expected canonical
AST string, covering assignments, arithmetic expressions,
if/else conditionals, and while loops.
"""

import project1_parser

def test_parser(code, expected_ast_str):
    """
    Runs the parser on given code and checks if the output
    matches the expected AST string.
    """
    lexer = project1_parser.Lexer(code)
    parser = project1_parser.Parser(lexer)
    ast = parser.parse()
    ast_str = ''.join(map(str, ast))

    if ast_str == expected_ast_str:
        print(f"[PASS] AST: {ast}")
        return 0
    else:
        print(f"[FAIL] Expected: {expected_ast_str}")
        print(f"       Got:      {ast_str}")
        return 1


def test_simple_statements():
    """
    Tests basic assignment and arithmetic expression parsing.
    """
    passed = 0

    code_1 = "x = 5 + 3"
    expected_1 = "('=', 'x', ('+', 5, 3))"
    if test_parser(code_1, expected_1) == 1:
        return passed
    passed += 1

    code_2 = "y = y + z"
    expected_2 = "('=', 'y', ('+', 'y', 'z'))"
    if test_parser(code_2, expected_2) == 1:
        return passed
    passed += 1

    code_3 = """
    x = 1
    y = 2
    z = 3
    a = x + y + z
    """
    expected_3 = "('=', 'x', 1)('=', 'y', 2)('=', 'z', 3)('=', 'a', ('+', ('+', 'x', 'y'), 'z'))"
    if test_parser(code_3, expected_3) == 1:
        return passed
    passed += 1

    code_4 = "x = 1  y = 2  b = (x + 1) * y"
    expected_4 = "('=', 'x', 1)('=', 'y', 2)('=', 'b', ('*', ('+', 'x', 1), 'y'))"
    if test_parser(code_4, expected_4) == 1:
        return passed
    passed += 1

    return passed


def test_if_statements():
    """
    Tests parsing of if-then[-else] statements.
    """
    code = """
    x = 5 + 3
    y = 0
    if x > y then
        y = x
    """
    expected = "('=', 'x', ('+', 5, 3))('=', 'y', 0)('if', ('>', 'x', 'y'), ('=', 'y', 'x'))"
    if test_parser(code, expected) == 1:
        return 0
    return 1


def test_while_statements():
    """
    Tests parsing of while loops, including nested while statements.
    """
    passed = 0

    code_1 = """
    x = 1
    x99 = 1234
    c99 = (x99 * x)
    cnt = 0
    while c99 > x99 do
        cnt = cnt + 1
    """
    expected_1 = "('=', 'x', 1)('=', 'x99', 1234)('=', 'c99', ('*', 'x99', 'x'))('=', 'cnt', 0)('while', ('>', 'c99', 'x99'), [('=', 'cnt', ('+', 'cnt', 1))])"
    if test_parser(code_1, expected_1) == 1:
        return passed
    passed += 1

    code_2 = """
    x = 5 + 3 + 10
    y = x + 3
    if y > 8 then z = y - x else z = y + x
    x = x / y
    x = y + x * x
    while x > 0 do
        while y > 0 do
            x = x - 1
    """
    expected_2 = "('=', 'x', ('+', ('+', 5, 3), 10))('=', 'y', ('+', 'x', 3))('if', ('>', 'y', 8), ('=', 'z', ('-', 'y', 'x')), ('=', 'z', ('+', 'y', 'x')))('=', 'x', ('/', 'x', 'y'))('=', 'x', ('+', 'y', ('*', 'x', 'x')))('while', ('>', 'x', 0), [('while', ('>', 'y', 0), [('=', 'x', ('-', 'x', 1))])])"
    if test_parser(code_2, expected_2) == 1:
        return passed
    passed += 1

    return passed


def main():
    """
    Runs all test suites and reports total passing tests.
    """
    total_passed = 0
    total_passed += test_simple_statements()
    total_passed += test_if_statements()
    total_passed += test_while_statements()
    print(f"Test cases passed: {total_passed}")


if __name__ == "__main__":
    main()
