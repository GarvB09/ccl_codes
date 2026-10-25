data_types = ["int", "float", "char", "double"]
sizes = {"int": 2, "float": 4, "char": 1, "double": 8}

symbol_table = []
address = 0

filename = input("Enter C file name: ")
file = open(filename, "r")

line_no = 0
for line in file:
    line_no = line_no + 1
    line = line.strip()
    line = line.replace(";", "")

    if "(" in line:
        continue

    words = line.split()
    if len(words) == 0:
        continue

    if words[0] in data_types:
        dtype = words[0]
        rest = line[len(dtype):]
        parts = rest.split(",")

        for part in parts:
            part = part.strip()
            part = part.split("=")[0]
            part = part.replace("*", "")
            part = part.strip()

            if part == "":
                continue

            already_added = False
            for row in symbol_table:
                if row[0] == part:
                    already_added = True

            if already_added == False:
                symbol_table.append([part, dtype, line_no, address, sizes[dtype]])
                address = address + sizes[dtype]

file.close()

print("\nName\tType\tLine\tAddress\tBytes")
print("----------------------------------------")
for row in symbol_table:
    print(row[0], "\t", row[1], "\t", row[2], "\t", row[3], "\t", row[4])