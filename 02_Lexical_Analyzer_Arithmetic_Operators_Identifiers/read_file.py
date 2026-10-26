from lexer import lexer

filename = input("Enter filename: ")

with open(filename, "r") as f:
    source = f.read()

lexer.input(source)
