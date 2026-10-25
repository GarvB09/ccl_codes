import ply.lex as lex
import ply.yacc as yacc

# ---- Lexer ----
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE')

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ignore = ' \t'

lex_error = False

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

# ---- Parser ----
# Postfix grammar: two operands followed by an operator reduce to one operand.
def p_expression_binop(p):
    '''expression : expression expression PLUS
                   | expression expression MINUS
                   | expression expression TIMES
                   | expression expression DIVIDE'''
    a, b, op = p[1], p[2], p[3]
    if op == '+':
        p[0] = a + b
    elif op == '-':
        p[0] = a - b
    elif op == '*':
        p[0] = a * b
    elif op == '/':
        p[0] = a / b

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_error(p):
    if lex_error:
        return
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# ---- Driver ----
if __name__ == "__main__":
    while True:
        try:
            s = input("Enter postfix expression: ")
        except EOFError:
            break
        if not s:
            continue

        lex_error = False
        lexer.lineno = 1
        result = parser.parse(s, lexer=lexer)

        if result is not None and not lex_error:
            print(result)