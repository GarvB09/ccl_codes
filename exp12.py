import ply.lex as lex
import ply.yacc as yacc

reserved = {'if': 'IF', 'else': 'ELSE', 'while': 'WHILE'}
tokens = ['NUMBER', 'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'RELOP',
          'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI'] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_RELOP = r'<=|>=|==|!=|<|>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_ignore = ' \t'

lex_error = False
had_error = False
temp_count = 0
label_count = 0
code = []

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_error(t):
    global lex_error
    lex_error = True
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (('left', 'PLUS', 'MINUS'), ('left', 'TIMES', 'DIVIDE'))

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def new_label():
    global label_count
    label_count += 1
    return f"L{label_count}"

def emit(line):
    code.append(line)

def p_program(p):
    '''program : program statement
               | statement'''

def p_statement(p):
    '''statement : assign
                 | if_stmt
                 | while_stmt'''

def p_assign(p):
    'assign : ID ASSIGN expression SEMI'
    emit(f"{p[1]} = {p[3]}")

def p_block(p):
    'block : LBRACE program RBRACE'

def p_if_stmt(p):
    'if_stmt : IF LPAREN cond RPAREN if_mark block else_part'
    emit(f"{p[5] if p[7] is None else p[7]}:")

def p_if_mark(p):
    'if_mark :'
    p[0] = new_label()
    emit(f"ifFalse {p[-2]} goto {p[0]}")

def p_else_part(p):
    '''else_part : ELSE else_mark block
                 | empty'''
    if len(p) == 4:
        p[0] = p[2]

def p_else_mark(p):
    'else_mark :'
    p[0] = new_label()
    emit(f"goto {p[0]}")
    emit(f"{p[-3]}:")

def p_empty(p):
    'empty :'

def p_while_stmt(p):
    'while_stmt : WHILE while_start LPAREN cond RPAREN while_mark block'
    emit(f"goto {p[2]}")
    emit(f"{p[6]}:")

def p_while_start(p):
    'while_start :'
    p[0] = new_label()
    emit(f"{p[0]}:")

def p_while_mark(p):
    'while_mark :'
    p[0] = new_label()
    emit(f"ifFalse {p[-2]} goto {p[0]}")

def p_cond(p):
    'cond : expression RELOP expression'
    p[0] = new_temp()
    emit(f"{p[0]} = {p[1]} {p[2]} {p[3]}")

def p_expression_binop(p):
    '''expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression'''
    p[0] = new_temp()
    emit(f"{p[0]} = {p[1]} {p[2]} {p[3]}")

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_atom(p):
    '''expression : ID
                   | NUMBER'''
    p[0] = p[1]

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
        temp_count = label_count = 0
        code = []
        lexer.lineno = 1
        parser.parse("\n".join(lines), lexer=lexer)
        if not had_error and not lex_error:
            print("Intermediate Code:")
            print("\n".join(code))