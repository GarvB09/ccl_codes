from lexer import lexer

print("Enter the program (Press Enter twice to finish):")

lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

program = "\n".join(lines)

lexer.input(program)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
