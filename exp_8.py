import ply.lex as lex
import ply.yacc as yacc

tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')
t_PLUS, t_MINUS, t_TIMES, t_DIVIDE = r'\+', r'-', r'\*', r'/'
t_LPAREN, t_RPAREN = r'\(', r'\)'
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

precedence = (('left', 'PLUS', 'MINUS'), ('left', 'TIMES', 'DIVIDE'))

def p_expression_binop(p):
    '''expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_error(p):
    if lex_error:
        return
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

parser = yacc.yacc()

def print_tree(node, prefix="", last=True):
    c = "└── " if last else "├── "
    if isinstance(node, tuple):
        op, l, r = node
        print(prefix + c + op)
        p2 = prefix + ("    " if last else "│   ")
        print_tree(l, p2, False)
        print_tree(r, p2, True)
    else:
        print(prefix + c + str(node))

if __name__ == "__main__":
    while True:
        try:
            s = input("Enter expression: ")
        except EOFError:
            break
        if not s:
            continue
        lex_error = False
        lexer.lineno = 1
        tree = parser.parse(s, lexer=lexer)
        if tree is not None and not lex_error:
            print_tree(tree)