import sys

path = sys.argv[1]

file = open(path)
program = file.readlines()
program_file = program
program = []
for line in program_file:
    if line[0] == '#' or line[0] == '\n':
        pass
    else:
        program.append(line[:8])

for line in program:
    print(line)
