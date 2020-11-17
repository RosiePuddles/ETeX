import os
from secrets import token_urlsafe as key

__all__ = ['Document', 'Text', 'Footnote', 'Columns', 'Equation', 'List', 'Table', 'Group', 'line', 'Code', 'Chemical', 'ChemEquation']

list_types = {'numbered': 'enumerate', 'bullet': 'itemize'}
TT_B = 'bold'  # *
TT_I = 'italic'  # **
TT_H = 'highlight'  # ~
TT_U = 'underline'  # ~~
tokenStarts = {TT_B: '\\textbf{', TT_I: '\\textit{', TT_H: '\\hl{', TT_U: '\\underline{'}
headings = ['empty', 'plain', 'headings', 'myheadings', 'fancy']
DocSettingsOpt = ['size', 'fontSize', 'top', 'bottom', 'left', 'right', 'colors', 'portrait']
_key = key(20)


def sortPackages(e):
    return e.name


class _main:
    def __init__(self, Packages: list = None):
        self.packages = Packages if Packages else [None]

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__getattr__(item)

    def add_super(self, new_packages: list):
        for i in new_packages:
            self.packages.append(i) if i not in self.packages else None

    def transfer_packages(self):
        return self.packages

    def generate_TeX(self):
        raise Warning(f'{print(type(self).__name__)} does not have a generate_TeX method!')


class _handler(_main):
    def __init__(self, packages: list = None):
        super().__init__(packages) if packages else super().__init__()

    def add(self, item):
        if not isinstance(item, _main):
            item = Text(str(item))
        self.items.append(item)
        self.add_super(item.packages)


class out:
    def __init__(self):
        self.given = ''

    def __add__(self, other):
        if not isinstance(other[0], type(None)):
            self.given += f'{other[1]}{other[0]}{other[2]}'
        else:
            self.given = self.given
        return self

    def __sub__(self, other):
        self.given += f'{other}'

    def __repr__(self):
        return self.given


class DocumentSettings(_main):
    __preDocClass = ['size', 'portrait', 'fontSize']
    __sizeOpts = ['a4', 'a5', 'b5', 'executive', 'legal', 'letter']
    __colorLengths = [0, 1, 1, 3, 4]
    __colorTypes = ['gray', '', ('RGB', 'rgb'), 'cmyk']

    def __init__(self, **kwargs):
        packages = self.__checkSettings(kwargs)
        super().__init__(packages)

    def __getattr__(self, item):
        if item in self.__dict__:
            return item
        else:
            return _key

    def __checkSettings(self, toProcess) -> list:
        packages = []
        geometry = True
        for i in list(toProcess.items()):
            if i[0] in DocSettingsOpt:
                method = None
                if i[0] in ['top', 'bottom', 'left', 'right']:
                    if geometry:
                        method = self.check_geometry(list(toProcess.items()))
                        geometry = False
                else:
                    method = getattr(self, f'check_{i[0]}', self.noMethod)(i)
                packages.append(method) if method is not None else None

        return packages

    def noMethod(self, item):
        return None

    def check_size(self, item):
        if item[1] in self.__sizeOpts:
            self.__dict__.update({'size': f'{item[1]}paper'})
        elif item[1] == 'article':
            self.__dict__.update({'size': 'article'})
        return None

    def check_fontSize(self, item):
        item = (item[0], max(min(int(item[1]), 100), 1))
        if item[1] in [10, 11, 12]:
            self.__dict__.update({'fontSize': item[1]})
        else:
            return _package('scrextend', f'fontsize={item[1]}pt')
        return None

    def check_orientation(self, item):
        if isinstance(item[1], bool):
            self.__dict__.update({'landscape': ('landscape' if item[1] else 'portrait')})
        return None

    def check_colors(self, item):
        if isinstance(item[1], dict):
            self.__dict__.update({'colors': item[1]})
        else:
            raise Exception('"colors" must be a dict type!')

    def check_geometry(self, item):
        postPre = '\\geometry{\n'
        for i in item:
            if i[0] in ['top', 'bottom', 'left', 'right']:
                postPre += f'{i[0]}={i[1]}cm,\n'
        return _package('geometry', postPre=postPre + '}')

    def generate_TeX(self) -> str:
        give = '\\documentclass['
        for i in list(self.__dict__.items()):
            if i in self.__preDocClass:
                give += i[1] + ', '
        give += f']{{{self.size if self.size != _key else "article"}}}'

        # colour magic
        if self.colors != _key:
            temp = ''
            assert isinstance(self.colors, dict)
            for i in self.colors.items():
                length = self.__colorLengths[len(i[1])]
                colType = self.__colorTypes[length - 1]
                if length == 3:
                    colType = colType[0 if sum([1 if n > 1 else 0 for n in i[1]]) > 0 else 1]
                give += f'\\definecolor{{{i[0]}}}{{{colType}}}{{{", ".join([str(n) for n in i[1][:length]])}}}'

        return give


class _section:
    def __init__(self, title: str, label: str, _type: int):
        self.title = title
        self.label = label
        self.items = []
        self.packages = []
        self.type = _type

    def generate_TeX(self):
        if self.type >= 0:
            name = "sub" * self.type
            given = f'\n\\{name}section{{{self.title}}}\\label{{{name}sec:{self.label}}}\n'
            # out += f'\\label{{{name}sec:{self.title.lower().replace(" ", "_")}}}\n\n'
        else:
            given = f'\\part{{{self.title}}}'
        return given


class _package:
    def __init__(self, name: str, additional: str = None, postPre: str = None):
        self.name = name
        self.additional = additional
        self.postPre = postPre

    def __repr__(self):
        given = '\\usepackage'
        if self.additional: given += f'[{self.additional}]'
        given += f'{{{self.name}}}\n'
        return given


class Document:
    def __init__(self, top: int = None, bottom: int = None, left: int = None, right: int = None, **kwargs):
        self.__dict__.update(kwargs)
        self.top = f'{top}cm' if top else None
        self.bottom = f'{bottom}cm' if bottom else None
        self.left = f'{left}cm' if left else None
        self.right = f'{right}cm' if right else None
        self.contains = []
        self.__preamble = [_package('fontenc', 'T1'), _package('inputenc', 'utf8'), _package('lmodern'), _package('textcomp'), _package('hyperref', postPre='\\hypersetup{colorlinks,\ncitecolor = blue,\nfilecolor = blue,\nlinkcolor = blue,\nurlcolor = blue\n}\n'), _package('geometry')]
        self.headings = [[], [], [], []]

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__getattr__(item)

    def generate_TeX(self, _compile: bool = True, **kwargs):
        if self.contains is []:
            raise Exception("Nothing to generate in the file!")
        give = out()
        give - '\\documentclass{article}\n'

        for i in self.contains:
            for n in i.packages:
                if not isinstance(n, type(None)):
                    self.__preamble.append(n)

        tempHolding = []
        self.__preamble.sort(key=sortPackages)
        for i in range(len(self.__preamble) - 1):
            if self.__preamble[i].name == self.__preamble[i + 1].name:
                self.__preamble[i + 1].additional += f'\n{self.__preamble[i].additional}'
                self.__preamble[i + 1].postPre += f'\n{self.__preamble[i].postPre}'
            else:
                tempHolding.append(self.__preamble[i])
        tempHolding.append(self.__preamble[-1])

        for i in self.__preamble:
            give - i.__repr__()

        for i in self.__preamble:
            if i.postPre: give - i.postPre

        give - '\\geometry{'
        give += (self.top, '\ntop=', ',')
        give += (self.bottom, '\nbottom=', ',')
        give += (self.left, '\nleft=', ',')
        give += (self.right, '\nright=', ',')
        give - '}\n\n'

        temp = None
        if self.title:
            temp = self.title
            temp += f'\\\\\\large {self.subtitle}' if self.subtitle else ''
        if temp: give - f'\n\\title{{{temp}}}'
        give - '\n\\date{'
        give += (self.date, '', '')
        give - '}'
        give += (self.author, '\n\\author{', '}')
        give += (self.contents_title, '\\renewcommand*\\contentsname{', '}')
        give - f'\n\n\\begin{{document}}\n'
        give - '\\maketitle\n'
        if self.contents: give - '\\tableofcontents\n\\newpage\n'

        for i in self.contains:
            give - i.generate_TeX()

        give - '\\end{document}'

        temp = self.title
        for i in ["$", "%", "/", "\\"]:
            temp = temp.replace(i, "")
        temp = temp.replace(' ', '_').replace('.', '_')

        katex = open(f'{temp}.tex', "w+")
        katex.truncate()
        katex = katex.write(give.__repr__())

        if _compile:
            command = f'latex -shell-escape -jobname=\"{temp}\" \"{temp}.tex\"'
            silent = True
            if 'debug' in kwargs:
                if kwargs['debug'] is True:
                    silent = False
            command += ' >/dev/null' if silent else ''
            os.system(command)
            os.system(f'pdf{command}')
        temp = temp.replace(" ", "\ ")
        os.system(f'open ./{temp}.pdf')

    def add(self, item):
        if not isinstance(item, _main):
            item = Text(str(item))
        self.contains.append(item)
        try:
            self.__postPre.append(item._postPre)
        except AttributeError:
            pass

    def new_section(self, title: str, _type: int = 0):
        self._labelMaker(name=title, _type=_type)

    def _labelMaker(self, name, _type):
        name_ = name.replace('%', '\\%').replace('$', '\\$')
        label_ = name.replace(' ', '_').lower().replace('\\', '')
        index = _type + 1
        if label_ in self.headings[index]:
            i = 1
            while True:
                if f'{label_}{i:03}' not in self.headings[index]:
                    label_ = f'{label_}{i:03}'
                    break
                else:
                    i += 1
        self.headings[index].append(label_)
        self.contains.append(_section(name_, label_, _type))


class headFoot(_main):
    def __init__(self, style: int = 1, **kwargs):
        self.style = headings[style % (len(headings) - 1)]
        super().__init__([_package('fancyhdr')]) if self.style == 'fancy' else super().__init__()
        if self.style == 'myheadings':
            self.kargs = kwargs

    def generate_TeX(self):
        pass


class _str:
    def __init__(self, text: str):
        self.value = text

    def __repr__(self):
        return f'_str: {self.value}'


class _tok:
    def __init__(self, tokType: str):
        self.value = tokType

    def __repr__(self):
        return f'_tok: {self.value}'


class Text(_main):
    def __init__(self, text: str, align: str = None) -> None:
        self.text = text
        self._LexerLike()
        self.align = align
        packages = [_package('ragged2e')] if self.align else []
        for i in self.text:
            if isinstance(i, _tok):
                if i.value == TT_H:
                    packages += [_package('color, soul')]
                    break
        # if '\\text{' in self.text: packages += [_package('asmath')]
        super().__init__(packages)

    def _LexerLike(self):
        given = []
        temp = ''
        n = len(self.text)
        textList = [m for m in self.text]
        i = 0
        while i < n:
            try:
                if textList[i] == '\\' and textList[i + 1] == '/':
                    i += 1
                    temp += '\\\\\n'
            except IndexError:
                pass
            if textList[i] == '/':
                try:
                    temp += textList[i + 1]
                    i += 1
                except IndexError:
                    pass
            elif textList[i] == '*':
                given.append(_str(temp))
                temp = ''
                token = TT_B
                try:
                    if textList[i + 1] == '*':
                        token = TT_I
                        i += 1
                except IndexError:
                    pass
                given.append(_tok(token))
            elif textList[i] == '~':
                given.append(_str(temp))
                temp = ''
                token = TT_H
                try:
                    if textList[i + 1] == '~':
                        token = TT_U
                        i += 1
                except IndexError:
                    pass
                given.append(_tok(token))
            else:
                temp += textList[i]
            i += 1
        given.append(_str(temp))
        self.text = given

    def generate_TeX(self) -> str:
        given = ''
        openTokens = {TT_B: False, TT_I: False, TT_H: False, TT_U: False}
        for i in self.text:
            if isinstance(i, _str):
                given += i.value
            else:
                assert isinstance(i, _tok)
                if openTokens[i.value]:
                    given += '}'
                else:
                    given += tokenStarts[i.value]
                openTokens[i.value] = bool((openTokens[i.value] + 1) % 2)
        for i in openTokens.values():
            if i:
                raise Exception('Not enough formatting characters were inputted into the input string.')

        if self.align:
            given = f'\\begin{{flush{self.align}}}\n{given}\n\\end{{flush{self.align}}}\n'

        return given


class Footnote(_main):
    def __init__(self, *args, number: int = None):
        super().__init__()
        self.text = ''
        for arg in args:
            self.text += str(arg)
        self.number = number

    def generate_TeX(self):
        out = '\\footnote'
        out += f'[{self.number}]' if self.number else ''
        out += f'{{{self.text}}}'

        return out


class Columns(_handler):
    def __init__(self, columns: int, items: list = None, unbalanced: bool = False):
        super().__init__([_package('multicol')])
        self.columns = max(columns, 1)
        self.items = items if items else []
        self.unbalanced = unbalanced

    def generate_TeX(self):
        given = '\\begin{multicols'
        given += f'*}}{{{self.columns}}}' if self.unbalanced else f'}}{{{self.columns}}}'
        for i in self.items:
            given += i.generate_TeX()
        given += '\\end{multicols'
        given += '*}' if self.unbalanced else '}'
        return given


class Equation(_main):
    def __init__(self, equation: str = '', numbered: bool = True):
        super().__init__([_package('amsmath')]) if ('\\text' in equation or numbered is False) else super().__init__()
        self.equation = equation
        self.numbered = '' if numbered else '*'

    def generate_TeX(self):
        out = f'\\begin{{equation{self.numbered}}}\n'
        out += self.equation + '\n'
        out += f'\\end{{equation{self.numbered}}}\n'

        return out


class List(_handler):
    def __init__(self, list_type: str = 'numbered', items: list = None):
        super().__init__()
        self.list_type = list_types.get(list_type)
        self.items = items
        if self.items is None: self.__clear_list()
        self.items = [n if isinstance(n, _main) else Text(str(n)) for n in self.items]

    def __clear_list(self):
        self.items = []

    def generate_TeX(self):
        out = f'\\begin{{{self.list_type}}}\n'
        for item in self.items:
            out += '\\item '
            if type(item) is list:
                out += Text(str(item))
            else:
                out += f'{item.generate_TeX()}\n'
        out += f'\\end{{{self.list_type}}}\n'
        return out

    def add(self, item):
        if item != self:
            super().add(item=item)
        else:
            raise Warning('Cannot add list to itself. Please don\'t try to make an infinity.')


class Table(_main):
    def __init__(self, values: list, **kwargs):
        super().__init__()
        self.values = values
        self.__dict__.update(kwargs)

    def generate_TeX(self):
        given = '\n\\begin{center}\n\\begin{tabular}{'
        if self.format:
            for i in self.format:
                given += f'| {i} '
            given += '|}\n\\hline\n'
        else:
            given += '| c ' * (len(self.values[0]))
            given += '|}\n\\hline\n'

        for n in self.values[0]:
            assert isinstance(n, _main)
            given += f'{n.generate_TeX()} & '
        given = given[:-2]
        given += '\\\\ \\hline\n'

        for i in self.values[1:]:
            for n in i:
                assert isinstance(n, _main)
                given += f'{n.generate_TeX()} & '
            given = given[:-2]
            given += '\\\\\n'

        given += '\\hline\n\\end{tabular}\n\\end{center}\n'

        return given


class Group(_handler):
    def __init__(self, items: list = None):
        super().__init__()
        self.items = [n if isinstance(n, _main) else Text(str(n)) for n in items] if items else []

    def generate_TeX(self):
        out = ''
        for i in self.items:
            out += i.generate_TeX()
        return out


class line(_main):
    def __init__(self, coordinates: list, color: str = None, mark: str = None, style: str = None, label_offset: int or float = -0.2):
        super().__init__()
        self.label_offset = label_offset
        self.coordinates = coordinates
        self.color = color
        self.mark = mark
        self.style = style

    def generate_TeX(self):
        out = '\\addplot['
        out += f'\ncolor={self.color}, ' if self.color else ''
        out += f'\nmark={self.mark}, ' if self.mark else ''
        out += f'\nstyle={self.style}, ' if self.style else ''
        out += ']\ncoordinates {'
        for i in self.coordinates:
            out += f'{i} '

        out = out[:-1]

        Axis = (self.coordinates[0][0], 'x') if self.coordinates[0][0] == self.coordinates[1][0] else (self.coordinates[0][1], 'y')

        out += f'}};\n\\node at (axis cs:'
        out += f'{Axis[0]}, {self.label_offset})' if Axis[1] == 'x' else f'{self.label_offset}, {Axis[0]})'
        out += f'{{{Axis[1]}={Axis[0]}}};\n'

        return out


class Code(_main):
    def __init__(self, code: str, language: str = 'text'):
        super().__init__([_package('minted')])
        self.code = code
        self.language = language

    def generate_TeX(self):
        given = f'\\begin{{minted}}[breaklines=true]{{{self.language}}}\n'
        given += self.code
        given += '\n\\end{minted}\n'

        return given


class Chemical(_main):
    def __init__(self, chemical, ):
        super().__init__([_package('mhchem')])
        self.chemical = chemical

    def generate_TeX(self):
        return f'\\ce{{{self.chemical}}}'

    def __repr__(self):
        return f'{self.chemical}'


class ChemEquation(_main):
    def __init__(self, reactants: str or list, products: str or list, catalysts: str or list = None, conditions: str or list = None):
        super().__init__([_package('mhchem')])
        self.reactants = self.__StringOrList(reactants)
        self.products = self.__StringOrList(products)
        self.catalysts = self.__StringOrList(catalysts)
        self.conditions = self.__StringOrList(conditions)

    def __StringOrList(self, option):
        if option is None:
            return None
        else:
            out = []
            if type(option) == list:
                for i in option:
                    out.append(Chemical(i))
            else:
                out = [Chemical(option)]
            return out

    def generate_TeX(self):
        out = '\\ce{'
        for i in self.reactants[:-1]:
            out += f'{i.chemical} + '
        out += self.reactants[-1].chemical + ' ->'
        if self.catalysts is not None:
            out += '[{'
            for i in self.catalysts[:-1]:
                out += f'{i.chemical}, '
            out += self.catalysts[-1].chemical
            out += '}]'
        if self.conditions is not None:
            out += '[{'
            for i in self.conditions[:-1]:
                out += f'{i.chemical}, '
            out += self.conditions[-1].chemical
            out += '}]'
        out += ' '
        for i in self.products[:-1]:
            out += f'{i.chemical} + '
        out += self.products[-1].chemical
        out += '}'
        return out
