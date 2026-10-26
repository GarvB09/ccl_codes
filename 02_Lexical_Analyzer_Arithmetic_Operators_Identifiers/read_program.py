from lexer import lexer

print("Enter the program (Press Enter twice to finish):")

lines = []
while (line := input()) != "":
    lines.append(line)

lexer.input("\n".join(lines))

for tok in lexer:
    print(tok)
