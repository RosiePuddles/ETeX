import os

packages = [('fontenc', 'T1'), ('inputenc', 'utf8'), 'lmodern', 'textcomp', 'tikz', 'pgfplots', 'ragged2e']
list_types = {'numbered': 'enumerate', 'bullet': 'something else'}


class Document:
    def __init__(self, title: str = None, author: str = None, top: str = None, bottom: str = None, left: str = None, right: str = None):
        self.title = title
        self.author = author
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.contains = []

    def generate_TeX(self):
        out = '\\documentclass{article}\n'
        for i in packages:
            out += self.add_package(i)

        out += self.add_package('geometry')
        out += '\\geometry{'
        out += f'\ntop={self.top},' if self.top else ''
        out += f'\nbottom={self.bottom},' if self.bottom else ''
        out += f'\nleft={self.left},' if self.left else ''
        out += f'\nright={self.right},' if self.right else ''
        out += '}\n'

        out += '\\pgfplotsset{compat=newest}'
        out += '\n'
        out += f'\n\\title{{{self.title}}}\n\\date{{}}' if self.title else ''
        out += f'\n\\author{{{self.author}}}' if self.author else ''
        out += f'\n\n\\begin{{document}}\n'
        out += '\\maketitle\n' if self.title else ''

        for i in self.contains:
            out += i.generate_TeX()

        out += '\\end{document}'

        katex = open("basic.tex", "w+")
        katex.truncate()
        katex = katex.write(out)

        # os.system(f'pdflatex -jobname=\"{self.title}\" basic.tex >/dev/null')
        os.system(f'pdflatex basic.tex >/dev/null')

    def add(self, item):
        self.contains.append(item)

    def add_package(self, package: str or tuple):
        out = '\\usepackage'
        if type(package) is tuple:
            out += f'[{package[1]}]{{{package[0]}}}'
        else:
            out += f'{{{package}}}'
        return out + '\n'


class Text:
    def __init__(self, text: str, align: str = None):
        self.text = text
        self.align = align

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


class vEnv:
    def __init__(self, _type: str = ''):
        self.type = _type

    def generate_Tex(self, extra: str = ''):
        out = f'\\begin{{{self.type}}}\n'

        out += extra

        out += f'\\end{{{self.type}}}\n'

        return out


class Equation(vEnv):
    def __init__(self, equation: str = ''):
        super().__init__('equation')
        self.equation = equation

    def generate_Tex(self):
        out = super().generate_Tex(self.equation)

        return out


class List(vEnv):
    def __init__(self, list_type: str = 'numbered', items: list = []):
        super().__init__(list_types.get(list_type))
        self.items = items
        self.clear_list() if items is not [] else None

    def clear_list(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def generate_TeX(self):
        extra = ''
        for item in self.items:
            extra += '\\item '
            if type(item) is list:
                extra += Text(str(item))
            else:
                extra += f'{item.generate_TeX()}\n'

        out = super().generate_Tex(extra)

        return out

    def __repr__(self):
        out = 'List > [\n'
        for i in self.items:
            out += f'{i}\n'
        out += ']'
        return out


class group:
    def __init__(self, items: list = []):
        self.items = items

    def add(self, item):
        self.items.append(item)

    def generate_TeX(self):
        out = ''
        for i in self.items:
            out += i.generate_TeX()
        return out


class line:
    def __init__(self, coordinates: list, color: str = None, mark: str = None, style: str = None, label_offset: int or float = -0.2):
        self.label_offset = label_offset
        self.coordinates = coordinates
        self.color = color
        self.mark = mark
        self.style = style

    def generate_TeX(self):
        self.out = '\\addplot['
        self.out += f'\ncolor={self.color}, ' if self.color else ''
        self.out += f'\nmark={self.mark}, ' if self.mark else ''
        self.out += f'\nstyle={self.style}, ' if self.style else ''
        self.out += ']\ncoordinates {'
        for i in self.coordinates:
            self.out += f'{i} '

        self.out = self.out[:-1]

        self.axis = (self.coordinates[0][0], 'x') if self.coordinates[0][0] == self.coordinates[1][0] else (self.coordinates[0][1], 'y')

        self.out += f'}};\n\\node at (axis cs:'
        self.out += f'{self.axis[0]}, {self.label_offset})' if self.axis[1] == 'x' else f'{self.label_offset}, {self.axis[0]})'
        self.out += f'{{{self.axis[1]}={self.axis[0]}}};\n'

        return self.out


class plot:
    def __init__(self, function: str, domain: tuple = None, color = None, name: str = None):
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


class axis:
    def __init__(self, samples: int = 100, labels: list = [None]*2, minMax: list = [None]*4, showTickMarks: bool = True, clip: bool = False):
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
