import string
data = """Jvcrd prizjdrtzcri, vxvi sl prqzpz fblprszczpfijrezq svezd xzqcz bfuldl bziuzezq uvdvbkzi. Sl ur jzqcviv wribcz jvbzcuv szi BVCZDV mviuzxzd qrdre, fecriz ur tfqvszcvtvxzezqz recrkzpfi. Yvi kvjkkv wribcz szi jrpz blccrertrxzq szcxzezq fcjle.

Efk: Jruvtv szi bvczdv mvivtvxzd, drbjzdld vccz brirbkviuve fcljrtrb"""

punc = string.punctuation
data_decrypt = ""
h = ""
count = 0
unsuz = "BCDFGHJKLMNPRSTVWXYZbcdfghjklmnprstvwxyz"
check = True
key = 1
data1 = data.lower()
while check:
    data_decrypt = ""
    for i, letter in enumerate(data1):
        if letter != ' ' and letter != '\n' and letter not in punc:
            if 97 <= ord(letter) <= 122:
                h = chr((ord(letter) + key) % 26 + 97)
                data_decrypt += h
            if h in unsuz:
                count += 1
            else:
                count = 0
            if count == 4:
                break
        else:
            data_decrypt += letter
            count = 0
        if i == len(data1) - 1:
            check = False
    key += 1

list_data = [i for i in data_decrypt]
for i, letter in enumerate(data):
    if 65 <= ord(letter) <= 90:
        list_data[i] = list_data[i].upper()
print("".join(list_data))
