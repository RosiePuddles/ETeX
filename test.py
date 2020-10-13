class test:
    def __init__(self):
        self.inc = []

    def add(self, string):
        self.inc.append(string)

    def __repr__(self):
        return f'{self.inc}\n'


a = test()
b = test()

b.add("Test string")
a.add("AAAAA")

print(f'{a}\n{b}')
