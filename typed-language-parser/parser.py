"""
parser.py

A Python implementation of a lexer and recursive-descent parser
for a custom domain-specific language (DSL) with typed variable
declarations, block scoping, arithmetic expressions, conditionals,
and loops.

Features:
- Tokenizer (Lexer) with support for integers, floats, operators, keywords, braces
- Recursive-descent Parser building a structured AST with Node classes
- Type checking and scope management using symbol tables
"""

from enum import Enum

# ------------------------------
# Token and TokenType Definitions
# ------------------------------

class Token:
    """
    Represents a single token produced by the lexer.
    """
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"{self.value}: {self.type}"


class TokenType(Enum):
    """
    Enum defining all possible token types in the DSL.
    """
    VARIABLE = 0
    NUMBER = 1
    FNUMBER = 2
    ARTHOP = 3
    CONDOP = 4
    ASSIGNOP = 5
    PARETHESES = 6
    SCOPE = 7
    KEYWORD = 8
    INVALID = 9
    EOF = 10


# ------------------------------
# Lexer Definition
# ------------------------------

class Lexer:
    """
    A simple lexer for tokenizing source code in the custom DSL.

    Supports:
    - Integers and floats
    - Arithmetic and conditional operators
    - Assignment
    - Keywords (if, then, else, while, do, int, float)
    - Parentheses and braces for scoping
    """
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.arthop = {'+', '-', '*', '/'}
        self.condop = {'==', '!=', '<', '>', '<=', '>='}
        self.parentheses = {'(', ')'}
        self.assignop = {'='}
        self.keywords = {'if', 'then', 'else', 'while', 'do', 'int', 'float'}
        self.braces = {'{', '}'}

    def curr_char(self):
        if self.position >= len(self.code):
            return "\0"
        return self.code[self.position]

    def move_forward(self):
        if self.position < len(self.code):
            self.position += 1

    def update_token(self, token):
        token += self.curr_char()
        self.move_forward()
        return token

    def get_token(self):
        token = ''

        while self.curr_char().isspace():
            self.move_forward()

        if self.curr_char() == "\0":
            return Token(TokenType.EOF, token)

        if self.curr_char().isnumeric():
            while self.curr_char().isnumeric():
                token = self.update_token(token)
            if self.curr_char() == '.':
                token = self.update_token(token)
                while self.curr_char().isnumeric():
                    token = self.update_token(token)
                return Token(TokenType.FNUMBER, token)
            return Token(TokenType.NUMBER, token)

        if self.curr_char().isalpha():
            token = self.update_token(token)
            while self.curr_char().isalnum():
                token = self.update_token(token)
            if token in self.keywords:
                return Token(TokenType.KEYWORD, token)
            return Token(TokenType.VARIABLE, token)

        while not self.curr_char().isalnum():
            if self.curr_char().isspace():
                break
            if self.curr_char() in self.parentheses:
                if not token:
                    token = self.update_token(token)
                break
            token = self.update_token(token)

        if token in self.arthop:
            return Token(TokenType.ARTHOP, token)
        elif token in self.condop:
            return Token(TokenType.CONDOP, token)
        elif token in self.parentheses:
            return Token(TokenType.PARETHESES, token)
        elif token in self.braces:
            return Token(TokenType.SCOPE, token)
        elif token in self.assignop:
            return Token(TokenType.ASSIGNOP, token)
        else:
            return Token(TokenType.INVALID, token)


# ------------------------------
# AST Node Definitions
# ------------------------------

class Node:
    """Base class for all AST nodes."""
    pass


class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements


class DeclarationNode(Node):
    def __init__(self, identifier, expression, myType):
        self.identifier = identifier
        self.expression = expression
        self.type = myType


class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression


class IfStatementNode(Node):
    def __init__(self, condition, if_block, else_block):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block


class WhileLoopNode(Node):
    def __init__(self, condition, loop_block):
        self.condition = condition
        self.loop_block = loop_block


class ConditionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class ArithmeticExpressionNode(Node):
    def __init__(self, operator, left, right, myType):
        self.operator = operator
        self.left = left
        self.right = right
        self.type = myType


class TermNode(Node):
    def __init__(self, operator, left, right, myType):
        self.operator = operator
        self.left = left
        self.right = right
        self.type = myType


class FactorNode(Node):
    def __init__(self, value, myType):
        self.value = value
        self.type = myType


# ------------------------------
# Parser Definition
# ------------------------------

class Parser:
    """
    A recursive-descent parser for the custom DSL.

    Builds a typed AST while maintaining symbol tables for variable
    declarations and enforcing scope and type checking.
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
        self.messages = []
        self.scopes = {0: {}}
        self.current_scope = 0

    def advance(self):
        self.current_token = self.lexer.get_token()

    def error(self, message):
        self.messages.append(message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_token()
        else:
            self.error(f'Expected token of type {token_type}, but found {self.current_token.type}')

    def enter_scope(self):
        self.current_scope += 1
        self.scopes[self.current_scope] = {}

    def leave_scope(self):
        del self.scopes[self.current_scope]
        self.current_scope -= 1

    def declareVar(self, identifier, dataType):
        cs = self.current_scope
        self.scopes[cs][identifier] = dataType

    def checkVarDeclared(self, identifier):
        cs = self.current_scope
        if identifier in self.scopes[cs]:
            self.error(f'Variable {identifier} has already been declared in the current scope')

    def checkVarUse(self, identifier):
        cs = self.current_scope
        for i in reversed(range(0, cs + 1)):
            if identifier in self.scopes[i]:
                return None
        self.error(f'Variable {identifier} has not been declared in the current or any enclosing scopes')

    def getMyType(self, identifier):
        cs = self.current_scope
        for i in reversed(range(0, cs + 1)):
            if identifier in self.scopes[i]:
                return self.scopes[i][identifier]
        return None

    def toStr(self, type):
        if type == TokenType.NUMBER:
            return 'int'
        elif type == TokenType.FNUMBER:
            return 'float'
        return None

    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self):
        if self.current_token.value == 'if':
            return self.parse_if_statement()
        elif self.current_token.value == 'while':
            return self.parse_while_loop()
        elif self.current_token.value in ('int', 'float'):
            return self.parse_declaration()
        else:
            return self.parse_assignment()

    def parse_declaration(self):
        token_value = self.current_token.value
        token_type = TokenType.NUMBER if token_value == 'int' else TokenType.FNUMBER
        self.advance()
        if self.current_token.type != TokenType.VARIABLE:
            raise Exception("INVALID ASSIGNMENT STATEMENT")
        variable_name = self.current_token.value
        self.checkVarDeclared(variable_name)
        self.declareVar(variable_name, token_type)
        self.advance()
        if self.current_token.value != '=':
            raise Exception("INVALID ASSIGNMENT STATEMENT")
        self.advance()
        expr = self.parse_arithmetic_expression()
        if expr.type != token_type:
            self.error(f"Type Mismatch between {self.toStr(token_type)} and {self.toStr(expr.type)}")
        return DeclarationNode(variable_name, expr, token_type)

    def parse_assignment(self):
        if self.current_token.type != TokenType.VARIABLE:
            raise Exception('INVALID ASSIGNMENT STATEMENT')
        variable_name = self.current_token.value
        self.checkVarUse(variable_name)
        self.advance()
        if self.current_token.value != '=':
            raise Exception('INVALID ASSIGNMENT STATEMENT')
        self.advance()
        expr = self.parse_arithmetic_expression()
        variable_type = self.getMyType(variable_name)
        if expr.type != variable_type:
            self.error(f"Type Mismatch between {self.toStr(variable_type)} and {self.toStr(expr.type)}")
        return AssignmentNode(variable_name, expr)

    def parse_if_statement(self):
        if self.current_token.value != "if":
            raise Exception("INVALID if statement")
        self.advance()
        cond = self.parse_condition()
        if self.current_token.value != "then":
            raise Exception("INVALID if statement")
        self.advance()
        if self.current_token.value != '{':
            raise Exception("INVALID if statement")
        self.advance()
        self.enter_scope()
        ifstmt = []
        while self.current_token.value != '}':
            ifstmt.append(self.parse_statement())
        self.leave_scope()
        self.advance()
        elsestmt = None
        if self.current_token.value == "else":
            self.advance()
            if self.current_token.value != '{':
                raise Exception("INVALID if statement")
            self.advance()
            self.enter_scope()
            elsestmt = []
            while self.current_token.value != '}':
                elsestmt.append(self.parse_statement())
            self.leave_scope()
            self.advance()
        return IfStatementNode(cond, ifstmt, elsestmt)

    def parse_while_loop(self):
        if self.current_token.value != "while":
            raise Exception("INVALID while statement")
        self.advance()
        cond = self.parse_condition()
        if self.current_token.value != "do":
            raise Exception("INVALID while statement")
        self.advance()
        if self.current_token.value != '{':
            raise Exception("INVALID while statement")
        self.advance()
        self.enter_scope()
        stmt = []
        while self.current_token.value != '}':
            stmt.append(self.parse_statement())
        self.leave_scope()
        self.advance()
        return WhileLoopNode(cond, stmt)

    def parse_condition(self):
        op1 = self.parse_arithmetic_expression()
        if self.current_token.type != TokenType.CONDOP:
            return "INVALID CONDITION"
        optr = self.current_token.value
        self.advance()
        op2 = self.parse_arithmetic_expression()
        return ConditionNode(op1, optr, op2)

    def parse_arithmetic_expression(self):
        lterm = self.parse_term()
        while self.current_token.value in ('+', '-'):
            op = self.current_token.value
            self.advance()
            rterm = self.parse_term()
            if lterm.type != rterm.type:
                self.error(f"Type Mismatch between {self.toStr(lterm.type)} and {self.toStr(rterm.type)}")
                rterm.type = None
            lterm = ArithmeticExpressionNode(op, lterm, rterm, rterm.type)
        return lterm

    def parse_term(self):
        f1 = self.parse_factor()
        while self.current_token.value in ('*', '/'):
            op = self.current_token.value
            self.advance()
            f2 = self.parse_factor()
            if f1.type != f2.type:
                self.error(f"Type Mismatch between {self.toStr(f1.type)} and {self.toStr(f2.type)}")
                f1.type = None
            f1 = TermNode(op, f1, f2, f1.type)
        return f1

    def parse_factor(self):
        token = self.current_token
        self.advance()
        if token.type in (TokenType.NUMBER, TokenType.FNUMBER):
            return FactorNode(token.value, token.type)
        elif token.type == TokenType.VARIABLE:
            self.checkVarUse(token.value)
            return FactorNode(token.value, self.getMyType(token.value))
        if token.value == '(':
            expr = self.parse_arithmetic_expression()
            if self.current_token.value != ')':
                raise Exception("ERROR: EXPECTED PARENTHESIS ')'")
            self.advance()
            return FactorNode(expr, expr.type)
        raise Exception("INVALID factor")
