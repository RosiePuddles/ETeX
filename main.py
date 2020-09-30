import os


class Document:
    def __init__(self):
        self.contains = []

    def generate_TeX(self):
        out = '\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{tikz}\n\\usepackage{pgfplots}\n\n'

        for i in self.contains:
            out += i.generate_TeX()

        out += '\\end{document}$'

        return out

    def add_item(self, item):
        self.contains.append(item)

    def __repr__(self):
        return self.contains


class plot:
    def __init__(self, function: str, domain: tuple = None, samples: int = 100, color=None, name: str = None):
        super().__init__()
        self.function = function
        self.name = name
        self.color = color
        self.samples = samples
        self.domain = domain

        self.generate_TeX()

    def generate_TeX(self):
        out = f'\\addplot['
        out += f'domain={self.domain[0]}:{self.domain[1]},\n' if self.domain else ''
        out += f'samples={self.samples},\n'
        out += f'color={self.color},\n' if self.color else ''
        out += f']\n{{{self.function}}};\n'
        out += f'\\addlegendentry{{{self.name}}}\n' if self.name else ''
        return out


class axis:
    def __init__(self, xlab: str = None, ylab: str = None):
        super().__init__()
        self.ylab = ylab
        self.xlab = xlab
        self.plots = []

        self.generate_TeX()

    def generate_TeX(self):
        out = '\\begin{tikzpicture}\n\\begin{axis}['
        out += f'\nxlabel={self.xlab},' if self.xlab else ''
        out += f'\nylabel={self.ylab},' if self.ylab else ''
        out += ']\n'

        for i in self.plots:
            out += i.generate_TeX()

        out += '\\end{axis}$\n\\end{tikzpicture}$\n'

        return out

    def add_plot(self, new_plot: plot):
        self.plots.append(new_plot)

    def __repr__(self):
        return f'x-label: {self.xlab}\ny-label: {self.ylab}\nPlot(s):\n{self.plots}'


Doc = Document()

Axis = axis()
Axis.add_plot(plot('x^2', (0, 2), color='red', name='test_name'))

Doc.add_item(Axis)

print((Doc.generate_TeX()+'\n\n\n'))

katex = open("basic.tex", "w+")
katex.truncate()
katex = katex.write(Doc.generate_TeX())

os.system("pdflatex basic.tex")
