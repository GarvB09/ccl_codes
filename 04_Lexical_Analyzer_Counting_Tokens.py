import re

keywords = {"int", "float", "char", "double", "void",
            "if", "else", "while", "for", "return"}

# order matters: first matching pattern wins
patterns = [
    ("WHITESPACE",  r'[ \t\r\n]+'),
    ("NUMBER",      r'\d+\.\d+|\d+'),
    ("IDENTIFIER",  r'[A-Za-z_][A-Za-z0-9_]*'),
    ("OPERATOR",    r'==|!=|<=|>=|&&|\|\||[+\-*/%=<>]'),
    ("PUNCTUATION", r'[(){}\[\];,]'),
]
master = re.compile("|".join(f"(?P<{name}>{rx})" for name, rx in patterns))

# which counter each token type adds to
group = {"KEYWORD": "Keywords", "IDENTIFIER": "Identifiers", "NUMBER": "Numbers",
         "OPERATOR": "Operators", "PUNCTUATION": "Operators"}


def tokenize(code):
    tokens = []
    counts = {"Keywords": 0, "Identifiers": 0, "Operators": 0, "Numbers": 0}
    unknown = 0

    if not code:
        print("Warning: Empty input received. No tokens to scan.")
        return tokens, counts

    pos = 0
    while pos < len(code):
        m = master.match(code, pos)
        if m is None:
            print(f"Warning: Unknown token '{code[pos]}' at position {pos}")
            unknown += 1
            pos += 1
            continue
        pos = m.end()
        kind, text = m.lastgroup, m.group()
        if kind == "WHITESPACE":
            continue
        if kind == "IDENTIFIER" and text in keywords:
            kind = "KEYWORD"
        counts[group[kind]] += 1
        tokens.append((kind, text))

    if unknown:
        print(f"Total unknown/invalid characters skipped: {unknown}")
    return tokens, counts


def display_results(tokens, counts):
    print("\nTokens Found:")
    for kind, text in tokens:
        print(f"  {kind:<12} -> {text}")

    print("\nLexical Analysis Results:")
    for name, n in counts.items():
        print(f"{name}: {n}")
    print(f"Total Tokens: {sum(counts.values())}")


def main():
    choice = input("Enter 1 to read from file, 2 to type code manually: ")

    if choice == "1":
        filename = input("Enter C file name: ")
        try:
            with open(filename) as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return
    else:
        print("Enter your C code. Type 'END' on a new line when done:")
        lines = []
        while (line := input()).strip() != "END":
            lines.append(line)
        code = "\n".join(lines)

    display_results(*tokenize(code))


if __name__ == "__main__":
    main()
