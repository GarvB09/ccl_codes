import re

keywords = {
    "int", "float", "char", "double", "void",
    "if", "else", "while", "for", "return"
}

token_patterns_ordered = [
    ("WHITESPACE",     r'[ \t\r\n]+'),
    ("NUMBER",         r'\d+\.\d+|\d+'),
    ("IDENTIFIER",     r'[A-Za-z_][A-Za-z0-9_]*'),
    ("OPERATOR",       r'==|!=|<=|>=|&&|\|\||[+\-*/%=<>]'),
    ("PUNCTUATION",    r'[(){}\[\];,]'),
]

compiled_patterns = []
for name, pattern in token_patterns_ordered:
    compiled_patterns.append((name, re.compile(pattern)))


def tokenize(code):
    tokens = []
    counts = {"Keywords": 0, "Identifiers": 0, "Operators": 0, "Numbers": 0}
    unknown_count = 0

    pos = 0
    n = len(code)

    if n == 0:
        print("Warning: Empty input received. No tokens to scan.")
        return tokens, counts

    while pos < n:
        match = None
        token_type = None

        for name, regex in compiled_patterns:
            m = regex.match(code, pos)
            if m:
                match = m
                token_type = name
                break

        if match is None:
            bad_char = code[pos]
            print(f"Warning: Unknown token '{bad_char}' at position {pos}")
            unknown_count += 1
            pos += 1
            continue

        text = match.group()

        if token_type == "WHITESPACE":
            pos = match.end()
            continue

        if token_type == "IDENTIFIER":
            if text in keywords:
                token_type = "KEYWORD"
                counts["Keywords"] += 1
            else:
                counts["Identifiers"] += 1

        elif token_type == "NUMBER":
            counts["Numbers"] += 1

        elif token_type in ("OPERATOR", "PUNCTUATION"):
            counts["Operators"] += 1

        tokens.append((token_type, text))
        pos = match.end()

    if unknown_count:
        print(f"Total unknown/invalid characters skipped: {unknown_count}")

    return tokens, counts


def display_results(tokens, counts):
    total = sum(counts.values())
    print("\nTokens Found:")
    for token_type, text in tokens:
        print(f"  {token_type:<12} -> {text}")

    print("\nLexical Analysis Results:")
    print(f"Keywords: {counts['Keywords']}")
    print(f"Identifiers: {counts['Identifiers']}")
    print(f"Operators: {counts['Operators']}")
    print(f"Numbers: {counts['Numbers']}")
    print(f"Total Tokens: {total}")


def main():
    choice = input("Enter 1 to read from file, 2 to type code manually: ")

    if choice == "1":
        filename = input("Enter C file name: ")
        try:
            with open(filename, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return
    else:
        print("Enter your C code. Type 'END' on a new line when done:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        code = "\n".join(lines)

    tokens, counts = tokenize(code)
    display_results(tokens, counts)


if __name__ == "__main__":
    main()