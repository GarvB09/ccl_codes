from lexer import lexer

lexer.input("25+30-abc")

for tok in lexer:
    print(tok)
