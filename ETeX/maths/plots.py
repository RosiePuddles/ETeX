from ETeX import _main, _package, _handler

__all__ = ['Plot', 'Coordinates']

plotCall = {'domain': ('domain=', ':', ''), 'color': ('color=', '')}


class Plot(_main):
    def __init__(self, function: str, *args, **kwargs):
        super().__init__()
        self.function = function
        self.__dict__.update(kwargs)

        self.generate_TeX()

    def generate_TeX(self):
        give = f'\\addplot['
        temp = dict(self.__dict__.items())
        for i in temp.keys():
            if i in plotCall.keys():
                if isinstance(temp[i], str):
                    give += f'{plotCall[i][0]}{temp[i]}{plotCall[i][1]},\n'
                elif isinstance(temp[i], tuple):
                    give += f'{plotCall[i][0]}'
                    for n in range(len(temp[i])):
                        give += f'{temp[i][n]}{plotCall[i][n+1]}'
                    if len(plotCall[i][-1]) != 0: give = give[:-len(plotCall[i][-1])]
                    give += f'{plotCall[i][-1]},\n'
        give += f']\n{{{self.function}}};\n'
        if 'name' in temp.keys():
            give += f'\\addlegendentry{{{self.name}}}\n'

        return give


class Coordinates(_main):
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


class Axis(_main):
    def __init__(self, title: str = None, samples: int = 100, labels: list = [None] * 2, showTickMarks: bool = True, clip: bool = False, **kwargs):
        super().__init__([_package('tikz'), _package('pgfplots', postPre='\\pgfplotsset{compat=newest} \n')])
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

    def add_plot(self, new_plot: Plot or Coordinates):
        self.plots.append(new_plot)

    def __repr__(self):
        return f'x-label: {self.xlab}\ny-label: {self.ylab}\nPlot(s):\n{self.plots}'