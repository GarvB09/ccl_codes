import sys
def remove_comments(code):
    lines_out = []
    numbers_out = []
    in_comment = False

    for n, line in enumerate(code.splitlines(), start=1):
        if in_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1]
                in_comment = False
            else:
                continue

        if "/*" in line:
            before, after = line.split("/*", 1)
            if "*/" in after:
                after = after.split("*/", 1)[1]
                line = before + after
            else:
                line = before
                in_comment = True

        line = line.split("//")[0]

        if line.strip():
            lines_out.append(line)
            numbers_out.append(n)

    return "\n".join(lines_out), numbers_out


if __name__ == "__main__":
    print("Enter the C code with comments.")
    print("When done, press Ctrl+Z then Enter (Windows) or Ctrl+D (Linux/Mac):")
    code = sys.stdin.read()  # reads everything until EOF, not just one line
    output_code, line_numbers = remove_comments(code)
    print("\n---- Output C program (comments removed) ----")
    print(output_code)