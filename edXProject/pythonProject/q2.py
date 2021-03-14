dict_prime = {}
size = int(input())
if size != 0:
    inp = input().split(" ")
    inp = [int(i) for i in inp]
    for nmr in inp:
        if nmr == 1:
            dict_prime.update({1: 1})
        else:
            for i in range(2, nmr + 1):
                if nmr % i == 0:
                    dict_prime.update({nmr: i})
                    break
    dict_prime = sorted(dict_prime.items(), key=lambda item: (item[1], item[0]))
    for i in dict_prime:
        print(i[0], end=" ")
