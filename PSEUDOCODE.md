# Compiler Construction Lab - Pseudocode

Exam-revision pseudocode for experiments 2-14 (experiment 1 is a theory assignment on LEX/YACC).
`PLY` = Python Lex-Yacc: the `t_` rules are the LEX part, the `p_` rules are the YACC part.

---

## 2. Lexical Analyzer - Arithmetic Operators and Identifiers

```
TOKENS: NUMBER, PLUS, MINUS, ID
RULES:
    PLUS   : '+'
    MINUS  : '-'
    ID     : letter or '_' followed by letters, digits, '_'
    NUMBER : one or more digits  -> convert to integer
    NEWLINE: increase line counter
    IGNORE : space, tab
    ERROR  : print "Illegal character", skip it

read input (hard-coded string / file / typed program)
give input to lexer
REPEAT
    tok = next token
    IF no token: STOP
    print tok
```

---

## 3. Comment and Whitespace Removal

```
FUNCTION remove_comments(code)
    out = empty list
    in_comment = false
    FOR each line in code
        IF in_comment
            IF line has "*/"
                line = text after "*/"
                in_comment = false
            ELSE
                skip this line
        IF line has "/*"
            before, after = split at "/*"
            IF after has "*/"
                line = before + text after "*/"
            ELSE
                line = before
                in_comment = true
        line = text before "//"
        IF line is not blank
            add line to out
    RETURN out joined by newlines

read all input until EOF
print remove_comments(input)
```

---

## 4. Counting Tokens

```
keywords = {int, float, char, double, void, if, else, while, for, return}
patterns (in this order): WHITESPACE, NUMBER, IDENTIFIER, OPERATOR, PUNCTUATION
counts = {Keywords, Identifiers, Operators, Numbers} all 0

FUNCTION tokenize(code)
    pos = 0
    WHILE pos < length(code)
        match the patterns at pos, first one that matches wins
        IF nothing matches
            warn "unknown token", unknown++, pos++, continue
        pos = end of match
        IF WHITESPACE: continue
        IF IDENTIFIER and text in keywords: type = KEYWORD
        counts[group of type]++      (punctuation counts as Operators)
        add (type, text) to tokens
    RETURN tokens, counts

main:
    ask: read from file, or type code ending with END
    tokens, counts = tokenize(code)
    print every token, each count, and total = sum of counts
```

---

## 5. Symbol Table Generation

```
sizes = {int:2, float:4, char:1, double:8}
symbol_table = empty ordered map, address = 0

FOR each line (line_no starting at 1) of the C file
    remove ';' and surrounding spaces
    IF line has '(' or is empty or first word not in sizes
        skip line                        (functions, statements, blanks)
    dtype = first word
    FOR each part of rest-of-line split by ','
        name = part before '=', with '*' removed, trimmed
        IF name is not empty AND not already in symbol_table
            symbol_table[name] = (dtype, line_no, address, sizes[dtype])
            address = address + sizes[dtype]

print table: Name, Type, Line, Address, Bytes
```

---

## 6. Syntax Analyzer - Arithmetic Expressions (infix, evaluates)

```
TOKENS: NUMBER, + - * /
PRECEDENCE: (+ -) lower than (* /), all left-associative

GRAMMAR
    expression -> expression OP expression     { value = apply OP to the two values }
    expression -> NUMBER                       { value = number }
ON SYNTAX ERROR: print "Syntax error at <token>" or "... at EOF"

LOOP: read line -> reset lexer -> parse
      IF no lexical error and no syntax error: print result
```

---

## 7. Evaluation of Postfix Expressions

```
Same lexer as experiment 6.

GRAMMAR (postfix: operator comes after both operands)
    expression -> expression expression OP     { value = apply OP to value1, value2 }
    expression -> NUMBER                       { value = number }

e.g.  2 3 4 * +   ->   3 4 * = 12,  2 12 + = 14
```

---

## 8. Syntax Tree Generator

```
TOKENS: NUMBER, + - * /, ( )
GRAMMAR
    expression -> expression OP expression     { node = (OP, left, right) }
    expression -> ( expression )               { node = inner node }
    expression -> NUMBER                       { node = number }

PROCEDURE print_tree(node, prefix, is_last)
    print prefix + branch symbol
    IF node is an operator node (op, left, right)
        print op
        print_tree(left,  new prefix, not last)
        print_tree(right, new prefix, last)
    ELSE
        print the number
```

---

## 9. Recursive Descent Parser - for loop

Grammar (one function per rule):

```
for_stmt   -> 'for' '(' assignment ';' condition ';' assignment ')'
assignment -> id '=' expr | id '++' | id '--' | id '+=' expr | id '-=' expr
condition  -> expr relop expr          relop in { < > <= >= == != }
expr       -> term  { ('+' | '-') term }
term       -> factor { ('*' | '/') factor }
factor     -> id | number
```

```
tokens = split input with a regex
FUNCTION expect(t): IF next token != t: error ELSE advance
FUNCTION factor(): IF next is id or number: advance ELSE error
FUNCTION term():   factor(); WHILE next in (*, /): advance; factor()
FUNCTION expr():   term();   WHILE next in (+, -): advance; term()
FUNCTION assignment():
    must see id, then one of  =  ++  --  +=  -=   (with expr after = += -=)
FUNCTION condition(): expr(); need relop; advance; expr()
FUNCTION for_stmt():
    expect 'for', '('; assignment(); expect ';'
    condition(); expect ';'; assignment(); expect ')'
    IF tokens are left over: error
print "Valid for loop"   OR   "Invalid for loop: <reason>"
```

---

## 10. Mini Tokenizer for Pseudo Language (statement to three-address code)

```
TOKENS: NUMBER, ID, + - * /, =, ( )
temp_count = 0, tac = empty list

PROCEDURE new_temp(): temp_count++; RETURN "t" + temp_count

GRAMMAR
    statement  -> ID '=' expression    { add "ID = expr_place" to tac }
    expression -> expression OP expression
                  { t = new_temp(); add "t = left OP right"; place = t }
    expression -> ( expression )       { place = inner place }
    expression -> ID | NUMBER          { place = the name or number }

LOOP: read statement -> run lexer -> print tokens as <TYPE,value>
      -> parse -> print the three-address code
```

Example: `x = a + b * (c - 2)` gives

```
t1 = c - 2
t2 = b * t1
t3 = a + t2
x = t3
```

---

## 11. Intermediate Code Generator - Arithmetic Expressions

```
Like experiment 10, with these extras:
    program   -> a list of statements, each ending with ';'
    comments  -> '#' to end of line, ignored
    FLOAT token (digits '.' digits) as well as NUMBER
    unary minus (highest precedence):  expression -> '-' expression
                  { t = new_temp(); add "t = -operand"; place = t }
    error handling: report only the first syntax error, with its line number

read lines until blank line -> parse the whole program
IF no errors: print the three-address code
```

---

## 12. Intermediate Code Generator - Control Statements

```
TOKENS: keywords if/else/while, ID, NUMBER, + - * /, = , relational ops, ( ) { } ;
temp_count = 0, label_count = 0, code = empty list

GRAMMAR with ACTIONS (empty "marker" rules run the action at the right moment)

assign : ID '=' expression ';'
    emit "ID = place"

cond : expression RELOP expression
    t = new_temp();  emit "t = e1 RELOP e2";  place = t

if_stmt : 'if' '(' cond ')' if_mark block else_part
    if_mark  (after cond):  Lfalse = new_label();  emit "ifFalse cond goto Lfalse"
    no else  :  emit "Lfalse:"
    with else:  else_mark:  Lend = new_label();  emit "goto Lend";  emit "Lfalse:"
                after else block:  emit "Lend:"

while_stmt : 'while' while_start '(' cond ')' while_mark block
    while_start :  Lstart = new_label();  emit "Lstart:"
    while_mark  :  Lexit  = new_label();  emit "ifFalse cond goto Lexit"
    after block :  emit "goto Lstart";  emit "Lexit:"
```

Example: `while (a < 10) { a = a + 1; }` gives

```
L1:
t1 = a < 10
ifFalse t1 goto L2
t2 = a + 1
a = t2
goto L1
L2:
```

---

## 13. Regex-Based Spam Filter

```
SPAM_WORDS = free, win, winner, prize, lottery, cash, urgent, offer,
             click, claim, bonus, guaranteed, congratulations   (ignore case)

LEXER (the order of rules matters)
    URL      : http://, https:// or www. followed by non-space characters
    EMAIL    : name @ domain . tld
    MONEY    : $ or Rs-symbol followed by digits (commas, decimals allowed)
    WORD     : letters
               -> type SPAMWORD  if it is in SPAM_WORDS
               -> type CAPS      if length >= 3 and all upper case
    NUMBER, EXCL ('!' run), PUNCT

SCORING (points added per token)
    SPAMWORD +2,  URL +2,  MONEY +2,  CAPS +1,  EXCL +1,  others 0

GRAMMAR:  message -> message item | item
    each item rule calls mark(text, label, points):
        score = score + points
        add text annotated as  text[LABEL +points]   to notes

LOOP: read message -> parse -> print annotated notes and score
      verdict = SPAM if score >= 5, SUSPICIOUS if score >= 3, else HAM
```

---

## 14. Backpatching for Boolean Expressions

```
Each boolean expression E has two lists of incomplete jumps:
    E.true   - quads that must jump when E is true
    E.false  - quads that must jump when E is false
nextquad = 100 + number of quads generated so far
M (marker) -> empty,  M.quad = nextquad

backpatch(list, target): fill the jump target of every quad in list with target
merge(a, b): a + b

GRAMMAR with ACTIONS
E -> E1 OR M E2:   backpatch(E1.false, M.quad)
                   E.true  = merge(E1.true, E2.true);   E.false = E2.false
E -> E1 AND M E2:  backpatch(E1.true, M.quad)
                   E.true  = E2.true;   E.false = merge(E1.false, E2.false)
E -> NOT E1:       E.true = E1.false;   E.false = E1.true
E -> ( E1 ):       E.true = E1.true;    E.false = E1.false
E -> id RELOP id:  E.true  = [nextquad];  E.false = [nextquad + 1]
                   emit "if a RELOP b goto _"
                   emit "goto _"
E -> true:         E.true  = [nextquad];  emit "goto _"
E -> false:        E.false = [nextquad];  emit "goto _"

after parsing the whole expression
    t = nextquad;   emit "result = 1";  emit "goto (t+3)"
    f = nextquad;   emit "result = 0"
    backpatch(E.true, t);  backpatch(E.false, f)
    print lists, backpatch trace and code with quad numbers
```

Example: `a < b and c > d`

```
100: if a < b goto 102
101: goto 106
102: if c > d goto 104
103: goto 106
104: result = 1
105: goto 107
106: result = 0
```
