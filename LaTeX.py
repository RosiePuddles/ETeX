import os

list_types = {'numbered': 'enumerate', 'bullet': 'itemize'}


class __main:
    def __init__(self, Packages: list = None):
        self.packages = Packages if Packages else []

    def add_super(self, new_packages: list):
        for i in new_packages:
            self.packages.append(i) if i not in self.packages else None

    def transfer_packages(self):
        return self.packages

    def generate_Tex(self):
        pass


class _section:
    def __init__(self, title: str):
        self.title = title
        self.items = []
        self.preamble = []

    def add(self, item):
        self.items.append(item)
        for i in item.packages:
            self.preamble.append(i)

    def generate_TeX(self):
        out = f'\\section{{{self.title}}}'
        for i in self.items:
            out += i.generate_TeX()

        return out


class Document:
    def __init__(self, title: str = None, author: str = None, first_section: str = 'Introduction', top: str = None, bottom: str = None, left: str = None, right: str = None):
        self.title = title
        self.author = author
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.contains = []
        self.__currentSection = _section(first_section)
        self.__preamble = [('fontenc', 'T1'), ('inputenc', 'utf8'), 'lmodern', 'textcomp']

    def generate_TeX(self):
        if self.contains is []:
            if self.__currentSection.items is []:
                print("Nothing to generate in the file!")
            else:
                self.contains = self.__currentSection.items
        out = '\\documentclass{article}\n'

        for i in self.contains:
            for n in i.preamble:
                self.__preamble.append(n) if n not in self.__preamble else None

        for i in self.__preamble:
            out += self.__add_package(i)

        if 'pfgplots' in self.__preamble:
            out += '\\pgfplotsset{compat=newest}'

        out += self.__add_package('geometry')
        out += '\\geometry{'
        out += f'\ntop={self.top},' if self.top else ''
        out += f'\nbottom={self.bottom},' if self.bottom else ''
        out += f'\nleft={self.left},' if self.left else ''
        out += f'\nright={self.right},' if self.right else ''
        out += '}\n'

        out += '\n'
        out += f'\n\\title{{{self.title}}}\n\\date{{}}' if self.title else ''
        out += f'\n\\author{{{self.author}}}' if self.author else ''
        out += f'\n\n\\begin{{document}}\n'
        out += '\\maketitle\n' if self.title else ''

        for i in self.contains:
            out += i.generate_TeX()

        out += '\\end{document}'

        katex = open(f'{self.title}.tex', "w+")
        katex.truncate()
        katex = katex.write(out)

        os.system(f'pdflatex -jobname=\"{self.title}\" \"{self.title}.tex\" >/dev/null')

    def add(self, item):
        self.__currentSection.add(item)

    def new_section(self, title: str):
        self.contains.append(self.__currentSection)
        self.__currentSection = _section(title)

    def __add_package(self, package: str or tuple):
        out = '\\usepackage'
        if type(package) is tuple:
            out += f'[{package[1]}]{{{package[0]}}}'
        else:
            out += f'{{{package}}}'
        return out + '\n'


class Text(__main):
    def __init__(self, *args, align: str = None):
        self.text = ''
        for arg in args:
            if type(arg) is str:
                self.text += f'{arg} '
        self.align = align
        super().__init__(['ragged2e']) if self.align is not None else super().__init__()

    def generate_TeX(self):
        out = ''
        if self.align:
            out += f'\\begin{{flush{self.align}}}\n'
            out += f'{self.text}\n'
            out += f'\\end{{flush{self.align}}}\n'
        else:
            out += f'{self.text}\n'
        return out

    def __repr__(self):
        return f'Text > [\"{self.text}\", align > {self.align} ]'


class Equation(__main):
    def __init__(self, equation: str = ''):
        super().__init__()
        self.equation = equation

    def generate_Tex(self):
        out = '\\begin{equation}\n'
        out += self.equation
        out += '\\end{equation}\n'

        return out


class List(__main):
    def __init__(self, list_type: str = 'numbered', items: list = []):
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
    def __init__(self, items: list = []):
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

        out = self.out[:-1]

        Axis = (self.coordinates[0][0], 'x') if self.coordinates[0][0] == self.coordinates[1][0] else (self.coordinates[0][1], 'y')

        out += f'}};\n\\node at (axis cs:'
        out += f'{Axis[0]}, {self.label_offset})' if Axis[1] == 'x' else f'{self.label_offset}, {Axis[0]})'
        out += f'{{{Axis[1]}={Axis[0]}}};\n'

        return out


class plot(__main):
    def __init__(self, function: str, domain: tuple = None, color=None, name: str = None):
        super().__init__(['tikz', 'pfgplots'])
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


class axis(__main):
    def __init__(self, samples: int = 100, labels: list = [None] * 2, minMax: list = [None] * 4, showTickMarks: bool = True, clip: bool = False):
        super().__init__()
        self.ymax = minMax[3]
        self.ymin = minMax[2]
        self.xmax = minMax[1]
        self.xmin = minMax[0]
        self.ylab = labels[1]
        self.xlab = labels[0]
        self.samples = samples
        self.showTickMarks = showTickMarks
        self.clip = clip
        self.plots = []

        self.generate_TeX()

    def generate_TeX(self):
        out = '\\begin{center}\n\\begin{tikzpicture}\n\\begin{axis}[\naxis lines=middle,'
        out += f'\nclip={str(self.clip).lower()},'
        out += f'\nsamples={self.samples},' if self.samples else ''
        out += f'\nxlabel={self.xlab},' if self.xlab else ''
        out += f'\nylabel={self.ylab},' if self.ylab else ''
        out += f'\nxmin={self.xmin},' if self.xmin else ''
        out += f'\nxmax={self.xmax},' if self.xmax else ''
        out += f'\nymin={self.ymin},' if self.ymin else ''
        out += f'\nymax={self.ymax},' if self.ymax else ''
        out += '\nticks=none' if not self.showTickMarks else ''
        out += ']\n'

        for i in self.plots:
            out += i.generate_TeX()

        out += '\\end{axis}\n\\end{tikzpicture}\n\\end{center}\n'

        return out

    def add_plot(self, new_plot: plot or line):
        self.plots.append(new_plot)

    def __repr__(self):
        return f'x-label: {self.xlab}\ny-label: {self.ylab}\nPlot(s):\n{self.plots}'
