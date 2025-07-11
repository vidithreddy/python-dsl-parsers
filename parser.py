from enum import Enum

class TokenType(Enum):
    """
    Defines possible token types returned by the Lexer.
    """
    VARIABLE = 0
    NUMBER = 1
    ARITHOP = 2
    CONDOP = 3
    ASSIGNOP = 4
    PARENTHESES = 5
    KEYWORD = 6
    EOP = 7
    INVALID = 8


class Lexer:
    """
    A simple lexer for tokenizing a custom expression language.

    Supports variables, numbers, arithmetic operators, conditional operators,
    assignment, parentheses, and keywords like if/then/else/while/do.
    """
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.arthop = {'+', '-', '*', '/'}
        self.condop = {'==', '!=', '<', '>', '<=', '>='}
        self.parentheses = {'(', ')'}
        self.assignop = {'='}
        self.keywords = {'if', 'then', 'else', 'while', 'do'}

    def curr_char(self):
        """
        Returns the current character or end-of-program marker.
        """
        if self.position >= len(self.code):
            return "\0"
        return self.code[self.position]

    def move_forward(self):
        """
        Advances the position by one character.
        """
        if self.position < len(self.code):
            self.position += 1

    def update_token(self, token):
        """
        Appends the current character to the token and advances.
        """
        token += self.curr_char()
        self.move_forward()
        return token

    def get_token(self):
        """
        Returns the next token and its type.
        """
        token = ''

        # Skip whitespace
        while self.curr_char().isspace():
            self.move_forward()

        if self.curr_char() == "\0":
            return token, TokenType.EOP

        # Numbers
        if self.curr_char().isnumeric():
            while self.curr_char().isnumeric():
                token = self.update_token(token)
            return token, TokenType.NUMBER

        # Variables / Keywords
        if self.curr_char().isalpha():
            token = self.update_token(token)
            while self.curr_char().isalnum():
                token = self.update_token(token)
            if token in self.keywords:
                return token, TokenType.KEYWORD
            return token, TokenType.VARIABLE

        # Operators and parentheses
        while not self.curr_char().isalnum() and not self.curr_char().isspace():
            if self.curr_char() in self.parentheses:
                if not token:
                    token = self.update_token(token)
                break
            token = self.update_token(token)

        if token in self.arthop:
            return token, TokenType.ARITHOP
        elif token in self.condop:
            return token, TokenType.CONDOP
        elif token in self.parentheses:
            return token, TokenType.PARENTHESES
        elif token in self.assignop:
            return token, TokenType.ASSIGNOP
        else:
            return token, TokenType.INVALID


class Parser:
    """
    A simple recursive-descent parser that builds an AST
    for a custom expression language supporting assignments,
    arithmetic expressions, if/else, and while loops.
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.current_token_type = None

    def parse(self):
        """
        Entry point for parsing the entire program.
        Returns an AST representation as a string.
        """
        return self.program()

    def advance(self):
        """
        Advances to the next token from the lexer.
        """
        self.current_token, self.current_token_type = self.lexer.get_token()

    def program(self):
        """
        Parses a sequence of statements.
        """
        ast = ""
        self.advance()
        while self.current_token:
            ast += self.statement()
        return ast

    def statement(self):
        """
        Parses a single statement (if, while, or assignment).
        """
        if self.current_token == 'if':
            return self.if_statement()
        elif self.current_token == 'while':
            return self.while_loop()
        else:
            return self.assignment()

    def assignment(self):
        """
        Parses an assignment statement of the form: variable = expression.
        """
        if self.current_token_type != TokenType.VARIABLE:
            return "INVALID ASSIGNMENT STATEMENT"
        ast = f"'{self.current_token}'"
        self.advance()
        if self.current_token != '=':
            return "INVALID ASSIGNMENT STATEMENT"
        self.advance()
        ast += ', ' + self.arithmetic_expression()
        return f"('=', {ast})"

    def arithmetic_expression(self):
        """
        Parses an arithmetic expression with + or - operators.
        """
        t1 = self.term()
        while self.current_token in ('+', '-'):
            op = self.current_token
            self.advance()
            t2 = self.term()
            t1 = f"('{op}', {t1}, {t2})"
        return t1

    def term(self):
        """
        Parses a term with * or / operators.
        """
        f1 = self.factor()
        while self.current_token in ('*', '/'):
            op = self.current_token
            self.advance()
            f1 = f"('{op}', {f1}, {self.factor()})"
        return f1

    def factor(self):
        """
        Parses a factor: number, variable, or parenthesized expression.
        """
        token = self.current_token
        token_type = self.current_token_type
        self.advance()
        if token_type == TokenType.NUMBER:
            return token
        elif token_type == TokenType.VARIABLE:
            return f"'{token}'"
        elif token == '(':
            token = self.arithmetic_expression()
            if self.current_token != ')':
                return "ERROR: EXPECTED PARENTHESIS ')'"
            self.advance()
        return token

    def if_statement(self):
        """
        Parses an if-then[-else] statement with condition.
        """
        if self.current_token != "if":
            return "INVALID if statement"
        self.advance()
        cond = self.condition()
        if self.current_token != "then":
            return "INVALID if statement"
        self.advance()
        ifstmt = self.statement()
        result = f"('if', {cond}, {ifstmt}"
        if self.current_token == "else":
            self.advance()
            elsestmt = self.statement()
            result += f", {elsestmt}"
        result += ")"
        return result

    def while_loop(self):
        """
        Parses a while-do loop with condition.
        """
        if self.current_token != "while":
            return "INVALID while statement"
        self.advance()
        cond = self.condition()
        if self.current_token != "do":
            return "INVALID while statement"
        self.advance()
        stmt = self.statement()
        return f"('while', {cond}, [{stmt}])"

    def condition(self):
        """
        Parses a condition: arithmetic_expression conditional_operator arithmetic_expression.
        """
        op1 = self.arithmetic_expression()
        if self.current_token_type != TokenType.CONDOP:
            return "INVALID CONDITION"
        optr = self.current_token
        self.advance()
        op2 = self.arithmetic_expression()
        return f"('{optr}', {op1}, {op2})"
