from ETeX import DocumentSettings

test = DocumentSettings(type='letter', leftEqn=True, colors={'a': (1, 2, 3), 'b': (5, 5, 5, 9)})
print(test)
print(test.docType())
