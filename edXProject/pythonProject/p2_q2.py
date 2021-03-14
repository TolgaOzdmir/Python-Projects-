num = int(input())
pow_list = []
for i in range(num):
    if 3**i <= num:
        pow_list.append(3**i)
    else:
        break
sum = pow_list[len(pow_list)-1]
for i in range(len(pow_list)-1):
    if sum + pow_list[i] > num:
        break
    sum += pow_list[i]
print(sum)
