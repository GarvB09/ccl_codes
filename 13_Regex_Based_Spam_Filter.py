import re
import ply.lex as lex
import ply.yacc as yacc

SPAM_RE = re.compile(r'free|win|winner|prize|lottery|cash|urgent|offer|click|claim|bonus|guaranteed|congratulations', re.I)

tokens = ('URL', 'EMAIL', 'MONEY', 'SPAMWORD', 'CAPS', 'WORD', 'NUMBER', 'EXCL', 'PUNCT')

t_ignore = ' \t'

lex_error = False
notes = []
score = 0

def t_URL(t):
    r'(https?://|www\.)[^\s]+'
    return t

def t_EMAIL(t):
    r'[\w.]+@[\w.]+\.\w+'
    return t

def t_MONEY(t):
    r'[$\u20b9]\d+(,\d{3})*(\.\d+)?'
    return t

def t_WORD(t):
    r'[A-Za-z]+'
    if SPAM_RE.fullmatch(t.value):
        t.type = 'SPAMWORD'
    elif len(t.value) >= 3 and t.value.isupper():
        t.type = 'CAPS'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_EXCL(t):
    r'!+'
    return t

def t_PUNCT(t):
    r'[.,?:;\'"()\-]'
    return t

def t_error(t):
    global lex_error
    lex_error = True
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

def mark(text, label, pts):
    global score
    score += pts
    notes.append(f"{text}[{label} +{pts}]" if pts else text)

def p_message(p):
    '''message : message item
               | item'''
    p[0] = True

def p_item_spam(p):
    'item : SPAMWORD'
    mark(p[1], 'SPAMWORD', 2)

def p_item_url(p):
    'item : URL'
    mark(p[1], 'URL', 2)

def p_item_money(p):
    'item : MONEY'
    mark(p[1], 'MONEY', 2)

def p_item_caps(p):
    'item : CAPS'
    mark(p[1], 'CAPS', 1)

def p_item_excl(p):
    'item : EXCL'
    mark(p[1], 'EXCL', 1)

def p_item_plain(p):
    '''item : EMAIL
            | WORD
            | NUMBER
            | PUNCT'''
    mark(p[1], '', 0)

def p_error(p):
    if not lex_error:
        print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

parser = yacc.yacc()

while True:
    try:
        s = input("Enter message: ")
    except EOFError:
        break
    if not s.strip():
        continue
    lex_error = False
    notes = []
    score = 0
    lexer.lineno = 1
    if parser.parse(s, lexer=lexer) is None or lex_error:
        continue
    print("Annotated:", " ".join(notes))
    verdict = "SPAM" if score >= 5 else "SUSPICIOUS" if score >= 3 else "HAM"
    print(f"Score: {score}  Verdict: {verdict}")