class holder:
    def __init__(self, name: str, extra1: str = '', extra2: str = ''):
        self.name = name
        self.extra1 = extra1
        self.extra2 = extra2

    def __repr__(self):
        out = self.name
        if self.extra1: out += f'\n{self.extra1}'
        if self.extra2: out += f'\n{self.extra2}'
        return out + '\n'


def sortMe(e):
    return e.name


if __name__ == '__main__':
    temp = [holder('avocado', 'food', 'find string'), holder('carpet'), holder('avocado', 'aaaaa'), holder('antidisestablishmentarianism', extra2='why')]
    temp.sort(key=sortMe)
    print(temp)
    holdingList = []
    for i in range(len(temp) - 1):
        if temp[i].name == temp[i + 1].name:
            temp[i + 1].extra1 += temp[i].extra1
            temp[i + 1].extra2 += temp[i].extra2
        else:
            holdingList.append(temp[i])
    holdingList.append(temp[-1])
    print(holdingList)
