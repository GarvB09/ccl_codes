import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'ID',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
