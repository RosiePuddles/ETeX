def test_func(a: int or list):
    if type(a) is int:
        return "int"
    if type(a) is list:
        return "list"


print(test_func([1,2]))
