import re

TOKEN_RE = re.compile(r'\+\+|--|\+=|-=|==|!=|<=|>=|[A-Za-z_]\w*|\d+|[<>=+\-*/;(),]')
tokenize = lambda s: TOKEN_RE.findall(s)

def parse_for(tokens):
    pos = [0]
    peek = lambda: tokens[pos[0]] if pos[0] < len(tokens) else None
    advance = lambda: pos.__setitem__(0, pos[0] + 1)
    def expect(tok):
        if peek() != tok: raise Exception(f"expected '{tok}' but found '{peek()}'")
        advance()
    def factor():
        t = peek()
        if t is None or not (t.isidentifier() or t.isdigit()):
            raise Exception(f"expected identifier or number, found '{t}'")
        advance()
    def term():
        factor()
        while peek() in ('*', '/'): advance(); factor()
    def expr():
        term()
        while peek() in ('+', '-'): advance(); term()
    def assignment():
        t = peek()
        if t is None or not t.isidentifier(): raise Exception(f"expected identifier, found '{t}'")
        advance()
        op = peek()
        if op == '=': advance(); expr()
        elif op in ('++', '--'): advance()
        elif op in ('+=', '-='): advance(); expr()
        else: raise Exception(f"expected assignment operator, found '{op}'")
    def condition():
        expr()
        op = peek()
        if op not in ('<', '>', '<=', '>=', '==', '!='): raise Exception(f"expected relational operator, found '{op}'")
        advance(); expr()
    def for_stmt():
        expect('for'); expect('(')
        assignment(); expect(';')
        condition(); expect(';')
        assignment(); expect(')')
        if pos[0] != len(tokens): raise Exception(f"unexpected token '{peek()}' after loop header")
    for_stmt()

if __name__ == "__main__":
    while True:
        try: s = input("Enter for-loop header: ")
        except EOFError: break
        if not s: continue
        try:
            parse_for(tokenize(s))
            print("Valid for loop")
        except Exception as e:
            print(f"Invalid for loop: {e}")