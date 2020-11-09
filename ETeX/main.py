import os

__all__ = ['Document', 'Text', 'Footnote', 'Columns', 'Equation', 'List', 'Table', 'Group', 'line', 'plot', 'coordinates', 'axis', 'Code', 'Chemical', 'ChemEquation']

list_types = {'numbered': 'enumerate', 'bullet': 'itemize'}
TT_B = 'bold'  # *
TT_I = 'italic'  # **
TT_H = 'highlight'  # ~
TT_U = 'underline'  # ~~
tokenStarts = {TT_B: '\\textbf{', TT_I: '\\textit{', TT_H: '\\hl{', TT_U: '\\underline{'}
headings = ['empty', 'plain', 'headings', 'myheadings', 'fancy']


class _main:
    def __init__(self, Packages: list = None):
        self.packages = Packages if Packages else []

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__getattr__(item)

    def add_super(self, new_packages: list):
        for i in new_packages:
            self.packages.append(i) if i not in self.packages else None

    def transfer_packages(self):
        return self.packages

    def generate_TeX(self):
        raise Exception(f'{print(type(self).__name__)} does not have a generate_TeX method!')


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


class _docSettings:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # def get


class _section:
    def __init__(self, title: str, _type: int = 0):
        self.title = title
        self.items = []
        self.packages = []
        self.type = _type

    def generate_TeX(self):
        if self.type >= 0:
            name = "sub" * self.type
            given = f'\n\\{name}section[{self.title}]{{{self.title}}}\n'
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
        given += f'{{{self.name}}}'
        return given + '\n'


class Document:
    def __init__(self, top: int = None, bottom: int = None, left: int = None, right: int = None, **kwargs):
        self.__dict__.update(kwargs)
        self.top = f'{top}cm' if top else None
        self.bottom = f'{bottom}cm' if bottom else None
        self.left = f'{left}cm' if left else None
        self.right = f'{right}cm' if right else None
        self.contains = []
        self.__preamble = [_package('fontenc', 'T1'), _package('inputenc', 'utf8'), _package('lmodern'), _package('textcomp'), _package('hyperref', postPre='\\hypersetup{colorlinks,\ncitecolor = blue,\nfilecolor = blue,\nlinkcolor = blue,\nurlcolor = blue\n}\n'), _package('geometry')]

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
                self.__preamble.append(n) if n.name not in [m.name for m in self.__preamble] else None

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
        temp = temp.replace('.', '_')

        katex = open(f'{temp}.tex', "w+")
        katex.truncate()
        katex = katex.write(give.__repr__())

        if _compile:
            command = f'latex -jobname=\"{temp}\" \"{temp}.tex\"'
            silent = True
            if 'debug' in kwargs:
                if kwargs['debug'] is True:
                    silent = False
            command += ' >/dev/null' if silent else ''
            os.system(command)
            os.system(f'pdf{command}')
        temp = temp.replace(" ", "\ ")
        os.system(f'open ./{temp}.pdf')

    def add(self, item: _main):
        self.contains.append(item)
        try:
            self.__postPre.append(item._postPre)
        except AttributeError:
            pass

    def new_section(self, title: str, _type: int = 0):
        self.contains.append(_section(title, _type))


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
        super().__init__(packages)

    def _LexerLike(self) -> None:
        given = []
        temp = ''
        n = len(self.text)
        textList = [m for m in self.text]
        i = 0
        while i < n:
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


class Columns(_main):
    def __init__(self, columns: int, items: list = None, unbalanced: bool = False):
        super().__init__([_package('multicol')])
        self.columns = max(columns, 1)
        self.items = items if items else []
        self.unbalanced = unbalanced

    def add(self, item: _main):
        self.items.append(item)
        self.add_super(item.packages)

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


class List(_main):
    def __init__(self, list_type: str = 'numbered', items: list = None):
        super().__init__()
        self.list_type = list_types.get(list_type)
        self.items = items
        if self.items is None: self.__clear_list()

    def __clear_list(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        self.add_super(item.packages)

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

    def __repr__(self):
        out = 'List > [\n'
        for i in self.items:
            out += f'{i}\n'
        out += ']'
        return out


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
            given += '| c ' * (len(self.values[0]) - 1)
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


class Group(_main):
    def __init__(self, items: list = None):
        super().__init__()
        self.items = items if items else []

    def add(self, item):
        self.items.append(item)
        self.add_super(item.packages)

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


class plot(_main):
    def __init__(self, function: str, domain: tuple = None, color=None, name: str = None):
        super().__init__()
        self.function = function
        self.name = name
        self.color = color
        self.domain = domain

        self.generate_TeX()

    def generate_TeX(self):
        out = f'\\addplot['
        out += f'domain={self.domain[0]}:{self.domain[1]}, ' if self.domain else ''
        out += f'color={self.color}, ' if self.color else ''
        out += f']\n{{{self.function}}};\n'
        out += f'\\addlegendentry{{{self.name}}}\n' if self.name else ''

        return out


class coordinates(_main):
    def __init__(self, coords: list, color: list = None, name: str = None, order: bool = False, **kwargs):
        super().__init__()
        self.coords = coords
        self.name = name
        self.color = color
        self.color = f'{{rgb:red,{color[0]};green,{color[1]};blue,{color[2]}}}' if self.color is not None else None
        self.__dict__.update(kwargs)

        if order: self.coords.sort(key=self.__order)

    def generate_TeX(self):
        out = f'\\addplot['
        out += f'\ncolor={self.color},' if self.color else ''
        if self.points: out += f'\nmark={self.points},'
        out = out[:-1] + ']\ncoordinates {'
        for i in self.coords:
            out += f'({i[0]}, {i[1]})\n'
        out += '};\n'
        out += f'\\addlegendentry{{{self.name}}}\n' if self.name else ''

        return out

    def __order(self, e):
        return e[0]


class axis(_main):
    def __init__(self, title: str = None, samples: int = 100, labels: list = [None] * 2, showTickMarks: bool = True, clip: bool = False, **kwargs):
        super().__init__([_package('tikz'), _package('pgfplots', postPre='\\pgfplotsset{compat=newest}\n')])
        self.title = title
        self.width = f'{kwargs["width"]}cm' if 'width' in kwargs else None
        self.height = f'{kwargs["height"]}cm' if 'height' in kwargs else None
        self.ymax = kwargs['ymax'] if 'ymax' in kwargs else None
        self.ymin = kwargs['ymin'] if 'ymin' in kwargs else None
        self.xmax = kwargs['xmax'] if 'xmax' in kwargs else None
        self.xmin = kwargs['xmin'] if 'xmin' in kwargs else None
        self.ylab = labels[1]
        self.xlab = labels[0]
        self.samples = samples
        self.showTickMarks = showTickMarks
        self.clip = clip
        self.plots = []
        self.__dict__.update(kwargs)

    def generate_TeX(self):
        given = '\\begin{center}\n\\begin{tikzpicture}\n\\begin{axis}[\naxis lines=left,'
        given += f'\nclip={str(self.clip).lower()},'
        given += f'\nsamples={self.samples},' if self.samples else ''
        given += f'\nxlabel={{{self.xlab}}},' if self.xlab else ''
        given += f'\nylabel={{{self.ylab}}},' if self.ylab else ''
        given += f'\nxmin={self.xmin},' if self.xmin is not None else ''
        given += f'\nxmax={self.xmax},' if self.xmax is not None else ''
        given += f'\nymin={self.ymin},' if self.ymin is not None else ''
        given += f'\nymax={self.ymax},' if self.ymax is not None else ''
        given += '\nticks=none,' if not self.showTickMarks else ''
        given += f'\nwidth={self.width}cm,' if self.width else ''
        given += f'\nheight={self.height}cm,' if self.height else ''
        given += f'\ntitle={{{self.title}}},' if self.title else ''
        if self.xTick: given += f'\nxtick={self.xTick},'
        if self.xMinorTick: given += f'\nminor xtick={self.xMinorTick},'
        given = given[:-1] + '\n]\n'

        # axis lines=middle tag inside the [] section option #

        for i in self.plots:
            given += i.generate_TeX()

        given += '\\end{axis}\n\\end{tikzpicture}\n\\end{center}\n'

        return given

    def add_plot(self, new_plot: plot or line or coordinates):
        self.plots.append(new_plot)

    def __repr__(self):
        return f'x-label: {self.xlab}\ny-label: {self.ylab}\nPlot(s):\n{self.plots}'


class Code(_main):
    def __init__(self, code: str, language: str = None):
        super().__init__([_package('xcolor', postPre='\\definecolor{codegreen}{rgb}{0,0.6,0}\n\\definecolor{codefunc}{rgb}{0.9.1,0.471,0.2}\n'),
                          _package('listings', postPre='\\lstdefinestyle{mystyle}{\ncommentstyle=\\color{codegreen},\nkeywordstyle=\\color{codefunc},\nstringstyle=\\color{codegreen},'
                                                       '\nbasicstyle=\\ttfamily\\footnotesize\n}\\lstset{style=mystyle}\n')])
        self.code = code
        self.language = language

    def generate_TeX(self):
        given = f'\\lstset{{language={self.language}}}\n' if self.language else ''
        given += '\\begin{lstlisting}\n'
        given += self.code
        given += '\n\\end{lstlisting}\n'

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
