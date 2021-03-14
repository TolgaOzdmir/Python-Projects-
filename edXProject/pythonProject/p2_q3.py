length = int(input())
line = input().split(" ")
line = [int(i) for i in line]

if sum(line) % 2 == 1:
    print("YES")
else:
    for i in range(length):
        val = line[i]
        for j in range(length):
            if line[j] == val:
                continue
            old_val = line[j]
            line[j] = val
            print(line)
            if sum(line) % 2 == 1:
                print("YES")
                exit(0)
            line[j] = old_val
    print("NO")