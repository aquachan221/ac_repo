import re
import sys

# === Tokenizer ===
TOKEN_SPEC = [
    ('RETURN',   r'return'),
    ('IF',       r'if'),
    ('ELSE',     r'else'),
    ('FOR',      r'for'),
    ('WHILE',    r'while'),
    ('FUNC',     r'func'),
    ('IMPORT',   r'import'),
    ('TRUE',     r'true'),
    ('FALSE',    r'false'),
    ('NULL',     r'null'),
    ('NUMBER',   r'\d+'),
    ('STRING',   r'"[^"]*"'),
    ('NAME',     r'[A-Za-z_][A-Za-z0-9_]*'),
    ('DOTS',     r'\.\.'),
    ('DOT',      r'\.'),
    ('ASSIGN',   r'='),
    ('COLON',    r':'),
    ('COMMA',    r','),
    ('OP',       r'[\+\-\*/<>!]=?|=='),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACK',   r'\['),
    ('RBRACK',   r'\]'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('NEWLINE',  r'\n'),
    ('INDENT',   r' {2,}'),
    ('SKIP',     r'[ \t]+'),
    ('COMMENT',  r'\#.*'),
    
    ('UNKNOWN',  r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
get_token = re.compile(tok_regex).match

def tokenize(code):
    pos, tokens = 0, []
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f"Unexpected character: {code[pos]}")
        kind = match.lastgroup
        value = match.group()
        if kind not in ('SKIP', 'NEWLINE', 'COMMENT'):
            tokens.append((kind, value))
        pos = match.end()
    return tokens

# === Context & Exceptions ===
class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Context:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        raise NameError(f"Undefined variable '{name}'")

    def set(self, name, value):
        self.vars[name] = value

# === Parser ===
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected=None):
        if self.pos >= len(self.tokens):
            return None
        kind, value = self.tokens[self.pos]
        if expected and kind != expected:
            raise SyntaxError(f"Expected {expected}, got {kind}")
        self.pos += 1
        return value

    def peek(self):
        return self.tokens[self.pos][0] if self.pos < len(self.tokens) else None

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() == 'OP':
            op = self.consume('OP')
            right = self.parse_term()
            left = ('binop', op, left, right)
        return left

    def parse_term(self):
        kind, val = self.tokens[self.pos]

        if kind == 'NAME':
            self.consume('NAME')
            if self.peek() == 'LPAREN':
                self.consume('LPAREN')
                args = []
                if self.peek() != 'RPAREN':
                    while True:
                        args.append(self.parse_expr())
                        if self.peek() == 'COMMA':
                            self.consume('COMMA')
                        else:
                            break
                self.consume('RPAREN')
                node = ('call', val, args)
            else:
                node = ('var', val)

            while self.peek() in ('DOT', 'LBRACK'):
                if self.peek() == 'DOT':
                    self.consume('DOT')
                    attr = self.consume('NAME')
                    node = ('getprop', node, attr)
                elif self.peek() == 'LBRACK':
                    self.consume('LBRACK')
                    index = self.parse_expr()
                    self.consume('RBRACK')
                    node = ('index', node, index)
            return node

        elif kind == 'NUMBER':
            self.consume('NUMBER')
            return ('number', int(val))

        elif kind == 'STRING':
            self.consume('STRING')
            return ('string', val.strip('"'))

        elif kind == 'TRUE':
            self.consume('TRUE')
            return ('bool', True)

        elif kind == 'FALSE':
            self.consume('FALSE')
            return ('bool', False)

        elif kind == 'NULL':
            self.consume('NULL')
            return ('null', None)

        elif kind == 'LBRACK':
            self.consume('LBRACK')
            elements = []
            if self.peek() != 'RBRACK':
                while True:
                    elements.append(self.parse_expr())
                    if self.peek() == 'COMMA':
                        self.consume('COMMA')
                    else:
                        break
            self.consume('RBRACK')
            return ('list', elements)

        elif kind == 'LBRACE':
            self.consume('LBRACE')
            pairs = []
            if self.peek() != 'RBRACE':
                while True:
                    key = self.consume('NAME')
                    self.consume('COLON')
                    value = self.parse_expr()
                    pairs.append((key, value))
                    if self.peek() == 'COMMA':
                        self.consume('COMMA')
                    else:
                        break
            self.consume('RBRACE')
            return ('object', pairs)

        else:
            raise SyntaxError(f"Unexpected token: {kind}")

    def parse_statement(self):
        if self.pos >= len(self.tokens):
            return None
        kind, val = self.tokens[self.pos]

        if kind == 'FUNC':
            return self.parse_func()
        elif kind == 'IF':
            return self.parse_if()
        elif kind == 'WHILE':
            return self.parse_while()
        elif kind == 'FOR':
            return self.parse_for()
        elif kind == 'RETURN':
            return self.parse_return()
        elif kind == 'IMPORT':
            self.consume('IMPORT')
            filename = self.consume('STRING').strip('"')
            return ('import', filename)
        elif kind == 'NAME' and val == 'prompt':
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'COLON':
                self.consume('NAME')   # prompt
                self.consume('COLON')  # :
                expr = self.parse_expr()
                return ('prompt', expr)
            else:
                return self.parse_expr()
        elif kind == 'NAME':
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'ASSIGN':
                return self.parse_assignment()
            else:
                return self.parse_expr()
        else:
            return self.parse_expr()

    def parse_assignment(self):
        name = self.consume('NAME')
        self.consume('ASSIGN')
        expr = self.parse_expr()
        return ('assign', name, expr)

    def parse_func(self):
        self.consume('FUNC')
        name = self.consume('NAME')
        self.consume('LPAREN')
        params = []
        if self.peek() != 'RPAREN':
            while True:
                params.append(self.consume('NAME'))
                if self.peek() == 'COMMA':
                    self.consume('COMMA')
                else:
                    break
        self.consume('RPAREN')
        self.consume('COLON')
        body = self.parse_block()
        return ('func', name, params, body)

    def parse_if(self):
        self.consume('IF')
        cond = self.parse_expr()
        self.consume('COLON')
        then_body = self.parse_block()
        else_body = []
        if self.peek() == 'ELSE':
            self.consume('ELSE')
            self.consume('COLON')
            else_body = self.parse_block()
        return ('if', cond, then_body, else_body)

    def parse_while(self):
        self.consume('WHILE')
        cond = self.parse_expr()
        self.consume('COLON')
        body = self.parse_block()
        return ('while', cond, body)

    def parse_for(self):
        self.consume('FOR')
        var = self.consume('NAME')
        self.consume('ASSIGN')
        start = self.parse_expr()
        self.consume('DOTS')
        end = self.parse_expr()
        self.consume('COLON')
        body = self.parse_block()
        return ('for', var, start, end, body)

    def parse_return(self):
        self.consume('RETURN')
        return ('return', self.parse_expr())

    def parse_block(self):
        stmts = []
        while self.peek() == 'INDENT':
            self.consume('INDENT')
            stmts.append(self.parse_statement())
        return stmts

    def parse_all(self):
        ast = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                ast.append(stmt)
        return ast

# === Evaluator ===
def evaluate(node, ctx):
    tag = node[0]

    if tag == 'assign':
        _, name, expr = node
        value = evaluate(expr, ctx)
        ctx.set(name, value)
        return value

    elif tag == 'number':
        return node[1]

    elif tag == 'string':
        return node[1]

    elif tag == 'bool':
        return node[1]

    elif tag == 'null':
        return None

    elif tag == 'var':
        return ctx.get(node[1])

    elif tag == 'binop':
        _, op, l, r = node
        a, b = evaluate(l, ctx), evaluate(r, ctx)
        return eval(f"{repr(a)} {op} {repr(b)}")

    elif tag == 'list':
        return [evaluate(e, ctx) for e in node[1]]

    elif tag == 'object':
        return {k: evaluate(v, ctx) for k, v in node[1]}

    elif tag == 'index':
        _, collection, key = node
        return evaluate(collection, ctx)[evaluate(key, ctx)]

    elif tag == 'getprop':
        _, obj, attr = node
        return evaluate(obj, ctx).get(attr)

    elif tag == 'func':
        _, name, params, body = node
        ctx.funcs[name] = (params, body)
        return f"<function {name}>"

    elif tag == 'call':
        _, name, args = node
        if name == 'print':
            vals = [evaluate(a, ctx) for a in args]
            print(*vals)
            return None
        if name == 'str':
            return str(evaluate(args[0], ctx))
        if name == 'int':
            return int(evaluate(args[0], ctx))
        if name == 'len':
            return len(evaluate(args[0], ctx))
        if name not in ctx.funcs:
            raise NameError(f"Undefined function '{name}'")
        params, body = ctx.funcs[name]
        if len(args) != len(params):
            raise TypeError(f"{name} expects {len(params)} args, got {len(args)}")
        local = Context()
        local.funcs = ctx.funcs
        for i in range(len(params)):
            local.set(params[i], evaluate(args[i], ctx))
        try:
            for stmt in body:
                evaluate(stmt, local)
        except ReturnSignal as r:
            return r.value
        return None

    elif tag == 'if':
        _, cond, then_body, else_body = node
        if evaluate(cond, ctx):
            for stmt in then_body:
                evaluate(stmt, ctx)
        else:
            for stmt in else_body:
                evaluate(stmt, ctx)

    elif tag == 'while':
        _, cond, body = node
        while evaluate(cond, ctx):
            for stmt in body:
                evaluate(stmt, ctx)

    elif tag == 'for':
        _, var, start, end, body = node
        for i in range(evaluate(start, ctx), evaluate(end, ctx)):
            ctx.set(var, i)
            for stmt in body:
                evaluate(stmt, ctx)

    elif tag == 'return':
        _, expr = node
        raise ReturnSignal(evaluate(expr, ctx))

    elif tag == 'import':
        filename = node[1]
        try:
            with open(filename, 'r') as f:
                code = f.read()
            tokens = tokenize(code)
            parser = Parser(tokens)
            imported_ast = parser.parse_all()
            for stmt in imported_ast:
                evaluate(stmt, ctx)
            print(f"(✔ imported {filename})")
        except FileNotFoundError:
            print(f"⚠ Warning: file '{filename}' not found.")
            return None
    
    elif tag == 'prompt':
        obj = evaluate(node[1], ctx)
        text = obj.get("text", "")
        buttons = obj.get("buttons", [])
        
        # Fallback for non-GUI: simulate the first button
        print(f"[PROMPT] {text}")
        print("Options:", ", ".join(buttons))
        return buttons[0] if buttons else None

    else:
        raise Exception(f"Unknown node type {tag}")
    

if __name__ == "__main__":
    ctx = Context()

    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse_all()
        for stmt in ast:
            evaluate(stmt, ctx)

        print("\nVariables:")
        for k, v in ctx.vars.items():
            if not k.startswith('_'):
                print(f"  {k} = {v}")

    print("\nWelcome to Caramel REPL (Ctrl+C or Ctrl+D to exit)")
    while True:
        try:
            line = input(">>> ").strip()
            if not line:
                continue
            tokens = tokenize(line)
            parser = Parser(tokens)
            expr = parser.parse_expr()
            result = evaluate(expr, ctx)
            if result is not None:
                print(result)
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        except Exception as e:
            print("Error:", e)