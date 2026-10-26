import ply.lex as lex
import ply.yacc as yacc

tokens = ('FLOAT', 'NUMBER', 'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
          'ASSIGN', 'LPAREN', 'RPAREN', 'SEMI')

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_ignore = ' \t'

lex_error = False
had_error = False
temp_count = 0
tac_code = []

def t_COMMENT(t):
    r'\#.*'
    pass

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    return t

def t_error(t):
    global lex_error
    lex_error = True
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def p_program(p):
    '''program : program statement
               | statement'''

def p_statement(p):
    'statement : ID ASSIGN expression SEMI'
    tac_code.append(f"{p[1]} = {p[3]}")

def p_expression_binop(p):
    '''expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression'''
    t = new_temp()
    tac_code.append(f"{t} = {p[1]} {p[2]} {p[3]}")
    p[0] = t

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    t = new_temp()
    tac_code.append(f"{t} = -{p[2]}")
    p[0] = t

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_atom(p):
    '''expression : ID
                   | NUMBER
                   | FLOAT'''
    p[0] = str(p[1])

def p_error(p):
    global had_error
    first = not had_error
    had_error = True
    if lex_error or not first:
        return
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        print("Enter program (blank line to run):")
        lines = []
        try:
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
        except EOFError:
            if not lines:
                break
        lex_error = had_error = False
        temp_count = 0
        tac_code = []
        lexer.lineno = 1
        parser.parse("\n".join(lines), lexer=lexer)
        if not had_error and not lex_error:
            print("Three-Address Code:")
            print("\n".join(tac_code))