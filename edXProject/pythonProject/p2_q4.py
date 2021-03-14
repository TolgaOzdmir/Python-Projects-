line = input().split(" ")
row, column, mod = [int(i) for i in line]

matrix = []
starting_point = [0, 0]
for i in range(row):
    matrix.append(input().lower().split(" "))
    if 'g' in matrix[i]:
        starting_point[1] = matrix[i].index("g")
        starting_point[0] = i
instructions = input().lower()
instructions = instructions.replace(" ", "")
if row == 0 or column == 0:
    print(0)
    exit(0)

sumo = 0
matrix_info = ""
matrix[starting_point[0]][starting_point[1]] = 1
for inst in instructions:
    if inst == 'u' and starting_point[0] > 0:
        starting_point[0] -= 1
    elif inst == 'r' and starting_point[1] < row - 1:
        starting_point[1] += 1
    elif inst == 'l' and starting_point[1] > 0:
        starting_point[1] -= 1
    elif inst == 'd' and starting_point[0] < column - 1:
        starting_point[0] += 1
    elif inst == 'p':
        print(sumo)
    elif inst == 'x':
        print(sumo)
        exit(0)
    matrix_info = matrix[starting_point[0]][starting_point[1]]
    if matrix_info == 'p':
        print(sumo)
    elif matrix_info == 'x':
        print(sumo)
        exit(0)
    elif matrix_info != 1 and matrix_info != 'g' and 97 <= ord(matrix_info) <= 122:
        sumo += (ord(matrix_info) - 96) % mod
    if matrix[starting_point[0]][starting_point[1]] != 'p':
        matrix[starting_point[0]][starting_point[1]] = 1
