"""
test_parser.py

Unit tests for the typed-language-parser project.

These tests verify:
1. Type consistency in expressions (no mixing int and float).
2. Enforcement of variable declaration before use.
3. Scoping rules that prevent redeclaring variables in the same scope.
"""

import parser as p

def test_parser(code, expected_messages):
    """
    Runs the parser on the provided code string and compares
    its error messages to the expected messages.
    """
    lexer = p.Lexer(code)
    parser = p.Parser(lexer)
    parse_tree = parser.parse_program()

    return 0 if parser.messages == expected_messages else 1


def test1():
    """
    Test Case 1: Type mismatch in declaration assignment.
    """
    code = '''
    int a = 10
    int b = 10.2
    '''
    expected = ['Type Mismatch between int and float']
    return 1 if test_parser(code, expected) == 0 else 0


def test2():
    """
    Test Case 2: Redeclaring variable in same scope inside if block.
    """
    code = '''
    int a = 10
    float b = 10.2
    if a > 10 then {
      int a = a * a
      int b = 10
      int a = a * b
    }
    '''
    expected = ['Variable a has already been declared in the current scope']
    return 1 if test_parser(code, expected) == 0 else 0


def test3():
    """
    Test Case 3: Mixed type assignments and undeclared variable usage.
    """
    code = '''
    int a = 10
    float b = 10.2
    if a > 10 then {
      float a = 10.2
      int b = 10
    } else {
      a = 10
      b = a * 10.56778
    }
    '''
    expected = ['Type Mismatch between int and float', 'Type Mismatch between float and None']
    return 1 if test_parser(code, expected) == 0 else 0


def test4():
    """
    Test Case 4: Use of undeclared variables in while loop.
    """
    code = '''
    while x > 0 do {
      int x = 10
      int y = x
    }
    int c = y
    '''
    expected = [
        'Variable x has not been declared in the current or any enclosing scopes',
        'Variable y has not been declared in the current or any enclosing scopes',
        'Type Mismatch between int and None'
    ]
    return 1 if test_parser(code, expected) == 0 else 0


def test5():
    """
    Test Case 5: Complex nested if/while with type mismatch.
    """
    code = '''
    float x = 0.234
    int y = 0
    int z = 0
    if x > y then {
      float sum = 10.50
      int cnt = 20
      if cnt > 0 then {
        int x = 1
        sum = 2.0 * sum
        x = x + 1
      }
      x = 10
      while x > 1.9 do {
        z = z + y
        x = x - 1.0
        sum = x + sum
      }
    }
    '''
    expected = ['Type Mismatch between float and int']
    return 1 if test_parser(code, expected) == 0 else 0


def test6():
    """
    Test Case 6: Multiple scoping and type errors.
    """
    code = '''
    int a = 10
    float b = 10.2
    if a > 10 then {
      int a = c
      int c = a
      int a = c * b
    } else {
      while a > 10 do {
        a = a - 12.456
        b = b + 1.0
      }
    }
    '''
    expected = [
        'Variable c has not been declared in the current or any enclosing scopes',
        'Type Mismatch between int and None',
        'Variable a has already been declared in the current scope',
        'Type Mismatch between int and float',
        'Type Mismatch between int and None',
        'Type Mismatch between int and float',
        'Type Mismatch between int and None'
    ]
    return 1 if test_parser(code, expected) == 0 else 0


def test7():
    """
    Test Case 7: Valid program with correct scoping and typing.
    """
    code = '''
    int a = 10
    int b = 12
    float z = 10.2

    if a + b > 10 then {
        int zoo = 10
        if a > 10 then {
            int zoo = 12
            float a = 10.2
            zoo = 10
        }
        zoo = a
    }
    else {
        float c = 20.3
        c = 10.2
    }
    while a > 10 do {
        int y = 100
        y = y + y
    }
    '''
    expected = []
    return 1 if test_parser(code, expected) == 0 else 0


# ------------------------------
# Main test runner
# ------------------------------

if __name__ == "__main__":
    passed = 0
    passed += test1()
    passed += test2()
    passed += test3()
    passed += test4()
    passed += test5()
    passed += test6()
    passed += test7()
    print('Tests passed:', passed)
