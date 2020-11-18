from ETeX import DocumentSettings

test = DocumentSettings(colors={'test': (2, 2, 1, 4, 9, 6)})
print(test.generate_TeX())
