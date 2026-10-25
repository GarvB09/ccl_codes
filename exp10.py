import ply.lex as lex
import ply.yacc as yacc

tokens = ('NUMBER', 'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'LPAREN', 'RPAREN')

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

lex_error = False
temp_count = 0
tac_code = []

def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    global lex_error
    lex_error = True
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (('left', 'PLUS', 'MINUS'), ('left', 'TIMES', 'DIVIDE'))

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def p_statement(p):
    'statement : ID ASSIGN expression'
    tac_code.append(f"{p[1]} = {p[3]}")
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression'''
    t = new_temp()
    tac_code.append(f"{t} = {p[1]} {p[2]} {p[3]}")
    p[0] = t

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_atom(p):
    '''expression : ID
                   | NUMBER'''
    p[0] = str(p[1])

def p_error(p):
    if lex_error:
        return
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

parser = yacc.yacc()

class Feed:
    def __init__(self, toks):
        self.it = iter(toks)
    def token(self):
        return next(self.it, None)

if __name__ == "__main__":
    while True:
        try:
            s = input("Enter statement: ")
        except EOFError:
            break
        if not s:
            continue
        lex_error = False
        temp_count = 0
        tac_code = []
        lexer.lineno = 1
        lexer.input(s)
        toks = list(iter(lexer.token, None))
        if lex_error:
            continue
        print("Tokens:", " ".join(f"<{t.type},{t.value}>" for t in toks))
        if parser.parse(lexer=Feed(toks)) is not None:
            print("Three-Address Code:")
            print("\n".join(tac_code))