from lexer import lexer

filename = input("Enter filename: ")

with open(filename) as f:
    lexer.input(f.read())

for tok in lexer:
    print(tok)
