import ply.lex as lex
import ply.yacc as yacc

reserved = {'and': 'AND', 'or': 'OR', 'not': 'NOT', 'true': 'TRUE', 'false': 'FALSE'}
tokens = ['ID', 'NUMBER', 'RELOP', 'LPAREN', 'RPAREN'] + list(reserved.values())

t_RELOP = r'<=|>=|==|!=|<|>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

BASE = 100
lex_error = False
code = []
trace = []

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
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (('left', 'OR'), ('left', 'AND'), ('right', 'NOT'))

def nextquad():
    return BASE + len(code)

def emit(text):
    code.append(text)

def merge(a, b):
    return a + b

def backpatch(lst, target):
    if not lst:
        return
    trace.append(f"backpatch({{{', '.join(map(str, sorted(lst)))}}}, {target})")
    for q in lst:
        code[q - BASE] = code[q - BASE][:-1] + str(target)

def p_e_or(p):
    'e : e OR m e'
    backpatch(p[1][1], p[3])
    p[0] = (merge(p[1][0], p[4][0]), p[4][1])

def p_e_and(p):
    'e : e AND m e'
    backpatch(p[1][0], p[3])
    p[0] = (p[4][0], merge(p[1][1], p[4][1]))

def p_e_not(p):
    'e : NOT e'
    p[0] = (p[2][1], p[2][0])

def p_e_group(p):
    'e : LPAREN e RPAREN'
    p[0] = p[2]

def p_e_rel(p):
    'e : operand RELOP operand'
    t, f = nextquad(), nextquad() + 1
    emit(f"if {p[1]} {p[2]} {p[3]} goto _")
    emit("goto _")
    p[0] = ([t], [f])

def p_e_true(p):
    'e : TRUE'
    p[0] = ([nextquad()], [])
    emit("goto _")

def p_e_false(p):
    'e : FALSE'
    p[0] = ([], [nextquad()])
    emit("goto _")

def p_operand(p):
    '''operand : ID
               | NUMBER'''
    p[0] = p[1]

def p_m(p):
    'm :'
    p[0] = nextquad()

def p_error(p):
    if not lex_error:
        print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

parser = yacc.yacc()

while True:
    try:
        s = input("Enter boolean expression: ")
    except EOFError:
        break
    if not s.strip():
        continue
    lex_error = False
    code, trace = [], []
    lexer.lineno = 1
    result = parser.parse(s, lexer=lexer)
    if result is None or lex_error:
        continue
    tl, fl = result
    print(f"truelist = {sorted(tl)}  falselist = {sorted(fl)}")
    t = nextquad()
    emit("result = 1")
    emit(f"goto {t + 3}")
    f = nextquad()
    emit("result = 0")
    backpatch(tl, t)
    backpatch(fl, f)
    print("Backpatch trace:")
    for line in trace:
        print("  " + line)
    print("Code:")
    for i, line in enumerate(code):
        print(f"  {BASE + i}: {line}")