import os

list_types = {'numbered': 'enumerate', 'bullet': 'itemize'}
Tokens = {'*': 'B', '**': 'I', '~': 'H', '~~': 'U'}
toks = {'B': True, 'I': True, 'H': True, 'U': True}
beginToks = {'B': '\\textbf{', 'I': '\\textit{', 'H': '\\hl{', 'U': '\\underline{'}
headings = ['empty', 'plain', 'headings', 'myheadings', 'fancy']


class __main:
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
        print('__add__ method called')
        temp = self.given
        if not isinstance(other[0], type(None)):
            self.given += f'{other[1]}{other[0]}{other[2]}'
        else:
            self.given = self.given
        print(f'Added something : {self.given != temp}\n')
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
        return f'\\{"sub" * self.type}section{{{self.title}}}\n'


class Document:
    def __init__(self, top: int = None, bottom: int = None, left: int = None, right: int = None, **kwargs):
        self.__dict__.update(kwargs)
        self.top = f'{top}mm' if top else None
        self.bottom = f'{bottom}mm' if bottom else None
        self.left = f'{left}mm' if left else None
        self.right = f'{right}mm' if right else None
        self.contains = []
        self.__preamble = [('fontenc', 'T1'), ('inputenc', 'utf8'), 'lmodern', 'textcomp', 'geometry']

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
                self.__preamble.append(n) if n not in self.__preamble else None

        for i in self.__preamble:
            give - self.__add_package(i)

        if 'pgfplots' in self.__preamble:
            give - '\\pgfplotsset{compat=newest}\n'
        if 'hyperref' in self.__preamble:
            give - '\\hypersetup{colorlinks=true}\n'

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
        if temp: give - f'\n\\title{{{temp}}}\n\\date{{}}'
        give += (self.author,'\n\\author{',  '}')
        give += (self.contents_title,'\\renewcommand*\\contentsname{',  '}')
        give - f'\n\n\\begin{{document}}\n'
        give - '\\maketitle\n'
        if self.contents: give - '\\tableofcontents\n'

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
            command = f'pdflatex -jobname=\"{temp}\" \"{temp}.tex\"'
            silent = True
            if 'debug' in kwargs:
                if kwargs['debug'] is True:
                    silent = False
            command += ' >/dev/null' if silent else ''
            os.system(command)
        temp = temp.replace(" ", "\ ")
        os.system(f'open ./{temp}.pdf')

    def add(self, item):
        self.contains.append(item)

    def new_section(self, title: str, _type: int = 0):
        _type = _type % 3
        self.contains.append(_section(title, _type))

    def __add_package(self, package: str or tuple):
        out = '\\usepackage'
        if type(package) is tuple:
            out += f'[{package[1]}]{{{package[0]}}}'
        else:
            out += f'{{{package}}}'
        return out + '\n'


class headFoot(__main):
    def __init__(self, style: int = 1, **kwargs):
        self.style = headings[style % (len(headings) - 1)]
        super().__init__(['fancyhdr']) if self.style == 'fancy' else super().__init__()
        if self.style == 'myheadings':
            self.kargs = kwargs

    def generate_TeX(self):
        pass


class _string:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'<_string: \'{self.text}\'>'


class _tok:
    def __init__(self, type_):
        self.type_ = Tokens[type_]  # Type can be either 'B', 'I', 'H', or 'U'

    def __repr__(self):
        return f'<_tok: {self.type_}>'


class Text(__main):
    def __init__(self, *args, align: str = None):
        self.text = []
        for arg in args:
            given = self.LexerLike(str(arg).replace('->', '$\\rightarrow$').replace('\n', '\\\\'))
            self.text += given
        self.align = align
        packages = []
        packages += ['ragged2e'] if self.align is not None else []
        for i in self.text:
            if isinstance(i, _tok):
                if i.type_ == 'H':
                    packages += ['hyperref', 'soul']
                    break
        super().__init__(packages)

    def LexerLike(self, text):
        out = []
        temp = ''
        textList = [i for i in text]
        if '*' not in textList and '~' not in textList:
            return [_string(text)]
        end = len(textList)
        n = 0
        while n < end:
            if textList[n] == '\\':
                try:
                    temp += textList[n + 1]
                except IndexError:
                    pass
                n += 1
            elif textList[n] in ['*', '~']:
                out.append(_string(temp)) if temp != '' else None
                try:
                    if textList[n + 1] == textList[n]:
                        out.append(_tok(textList[n] * 2))
                        n += 1
                    else:
                        out.append(_tok(textList[n]))
                except IndexError:
                    out.append(_tok(textList[n]))
                temp = ''
            else:
                temp += textList[n]
            n += 1
        types = {'B': 0, 'I': 0, 'H': 0, 'U': 0}
        for i in out:
            if isinstance(i, _tok):
                types[i.type_] += 1
        for i in types.values():
            if i % 2 != 0:
                raise Exception('An incorrect number of formatting characters were passed into the class.')
        return out

    def generate_TeX(self):
        out = ''
        if self.align:
            out += f'\\begin{{flush{self.align}}}\n'
            out += f'{self.generateSyntaxed(self.text)}\n'
            out += f'\\end{{flush{self.align}}}\\\\\n'
        else:
            out += f'{self.generateSyntaxed(self.text)}\\\\\n'
        return out

    def generateSyntaxed(self, text):
        out = ''
        for i in text:
            if isinstance(i, _string):
                out += i.text
            else:
                out += beginToks[i.type_] if toks[i.type_] else '}'
                toks[i.type_] = False if toks[i.type_] else True
        return str(out)


class Footnote(__main):
    def __init__(self, *args, number: int = None):
        super().__init__(['hyperref'])
        self.text = ''
        for arg in args:
            self.text += str(arg)
        self.number = number

    def generate_TeX(self):
        out = '\\footnote'
        out += f'[{self.number}]' if self.number else ''
        out += f'{{{self.text}}}'

        return out


class Columns(__main):
    def __init__(self, columns: int, items: str or list = None, unbalanced: bool = False):
        super().__init__()
        self.columns = max(columns, 1)
        self.items = items if type(items) == list else [items]
        self.unbalanced = unbalanced

    def add(self, item):
        self.items.append(item)

    def generate_TeX(self):
        out = '\\begin{multicols'
        out += f'*}}{{{self.columns}}}' if self.unbalanced else f'}}{{{self.columns}}}'
        for i in self.items:
            out += i.generate_TeX()
        out += '\\end{multicols'
        out += '*}' if self.unbalanced else '}'


class Equation(__main):
    def __init__(self, equation: str = '', numbered: bool = True):
        super().__init__(['amsmath']) if ('\\text' in equation or numbered is False) else super().__init__()
        self.equation = equation
        self.numbered = '' if numbered else '*'

    def generate_TeX(self):
        out = f'\\begin{{equation{self.numbered}}}\n'
        out += self.equation + '\n'
        out += f'\\end{{equation{self.numbered}}}\n'

        return out


class List(__main):
    def __init__(self, list_type: str = 'numbered', items: list = None):
        super().__init__()
        self.list_type = list_types.get(list_type)
        self.items = items
        self.__clear_list() if items is not [] else None

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


class group(__main):
    def __init__(self, items: list = None):
        super().__init__()
        self.items = items

    def add(self, item):
        self.items.append(item)
        self.add_super(item.packages)

    def generate_TeX(self):
        out = ''
        for i in self.items:
            out += i.generate_TeX()
        return out


class line(__main):
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


class plot(__main):
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


class coordinates(__main):
    def __init__(self, coords: list, color: list = None, name: str = None):
        super().__init__()
        self.coords = coords
        self.name = name
        self.color = color
        self.color = f'{{rgb:red,{color[0]};green,{color[1]};blue,{color[2]}}}' if self.color is not None else None

        self.generate_TeX()

    def generate_TeX(self):
        out = f'\\addplot['
        out += f'color={self.color}' if self.color else ''
        out += ']\ncoordinates {'
        for i in self.coords:
            out += f'{i}\n'
        out += '};\n'
        out += f'\\addlegendentry{{{self.name}}}\n' if self.name else ''

        return out


class axis(__main):
    def __init__(self, title: str = None, samples: int = 100, labels: list = [None] * 2, showTickMarks: bool = True, clip: bool = False, **kwargs):
        super().__init__(['tikz', 'pgfplots'])
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

    def generate_TeX(self):
        out = '\\begin{center}\n\\begin{tikzpicture}\n\\begin{axis}[\naxis lines=left,'
        out += f'\nclip={str(self.clip).lower()},'
        out += f'\nsamples={self.samples},' if self.samples else ''
        out += f'\nxlabel={self.xlab},' if self.xlab else ''
        out += f'\nylabel={self.ylab},' if self.ylab else ''
        out += f'\nxmin={self.xmin},' if self.xmin is not None else ''
        out += f'\nxmax={self.xmax},' if self.xmax is not None else ''
        out += f'\nymin={self.ymin},' if self.ymin is not None else ''
        out += f'\nymax={self.ymax},' if self.ymax is not None else ''
        out += '\nticks=none,' if not self.showTickMarks else ''
        out += f'\nwidth={self.width},' if self.width else ''
        out += f'\nheight={self.height},' if self.height else ''
        out += f'\ntitle={self.title}' if self.title else ''
        out += ']\n'

        # axis lines=middle tag inside the [] section option #

        for i in self.plots:
            out += i.generate_TeX()

        out += '\\end{axis}\n\\end{tikzpicture}\n\\end{center}\n'

        return out

    def add_plot(self, new_plot: plot or line):
        self.plots.append(new_plot)

    def __repr__(self):
        return f'x-label: {self.xlab}\ny-label: {self.ylab}\nPlot(s):\n{self.plots}'


class Code(__main):
    def __init__(self, code: str, language: str = None):
        super().__init__(['listings'])
        self.code = code
        self.language = language

    def generate_TeX(self):
        out = f'\\lstset{{language={self.language}}}\n\\begin{{lstlisting}}\n'
        out += self.code
        out += '\\end{lstlisting}\n'

        return out


class Chemical(__main):
    def __init__(self, chemical,):
        super().__init__(['mhchem'])
        self.chemical = chemical

    def generate_TeX(self):
        return f'\\ce{{{self.chemical}}}'

    def __repr__(self):
        return f'{self.chemical}'


class ChemEquation(__main):
    def __init__(self, reactants: str or list, products: str or list, catalysts: str or list = None, conditions: str or list = None):
        super().__init__(['mhchem'])
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
