from lexer import lexer

lexer.input("25+30-abc")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
