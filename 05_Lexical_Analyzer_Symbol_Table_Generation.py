sizes = {"int": 2, "float": 4, "char": 1, "double": 8}

symbol_table = {}   # name -> (type, line, address, bytes)
address = 0

filename = input("Enter C file name: ")
with open(filename) as file:
    for line_no, line in enumerate(file, start=1):
        line = line.strip().replace(";", "")
        words = line.split()

        # skip blank lines, function headers and non-declarations
        if "(" in line or not words or words[0] not in sizes:
            continue

        dtype = words[0]
        for part in line[len(dtype):].split(","):
            name = part.split("=")[0].replace("*", "").strip()
            if name and name not in symbol_table:
                symbol_table[name] = (dtype, line_no, address, sizes[dtype])
                address += sizes[dtype]

print("\nName\tType\tLine\tAddress\tBytes")
print("----------------------------------------")
for name, (dtype, line_no, addr, size) in symbol_table.items():
    print(name, "\t", dtype, "\t", line_no, "\t", addr, "\t", size)
