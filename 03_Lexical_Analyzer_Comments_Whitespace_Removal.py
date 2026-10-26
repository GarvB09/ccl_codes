import sys

def remove_comments(code):
    out = []
    in_comment = False

    for line in code.splitlines():
        if in_comment:
            if "*/" not in line:
                continue
            line = line.split("*/", 1)[1]
            in_comment = False

        if "/*" in line:
            before, after = line.split("/*", 1)
            if "*/" in after:
                line = before + after.split("*/", 1)[1]
            else:
                line = before
                in_comment = True

        line = line.split("//")[0]

        if line.strip():
            out.append(line)

    return "\n".join(out)


if __name__ == "__main__":
    print("Enter the C code with comments.")
    print("When done, press Ctrl+Z then Enter (Windows) or Ctrl+D (Linux/Mac):")
    print("\n---- Output C program (comments removed) ----")
    print(remove_comments(sys.stdin.read()))
