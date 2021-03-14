class Person:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name + " ismim."

a = Person("tolga")
print(a)
# while(True):
#     if inp == 'q':
#         break
#     toplam += int(inp)
#     inp =input()
# print(toplam)
