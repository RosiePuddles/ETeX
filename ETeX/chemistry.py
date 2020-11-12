from ETeX import _main, _package, _handler

__all__ = ['Chromatography']

chromaCall = {'width': ('width=', 'cm'),
              'height': ('height=', 'cm'),
              'title': ('title=', ''),
              'labels': ('xticklabels={', '}')}


class Chromatography(_main):
    def __init__(self, points: list, solventFront: int or float, *args, **kwargs):
        super().__init__([_package('tikz'), _package('pgfplots', postPre='\\pgfplotsset{compat=newest} \n')])
        self.points = points
        self.solventFront = solventFront
        self.__dict__.update(kwargs)

    def generate_TeX(self) -> str:
        give = f'\n\\begin{{center}}\n\\begin{{tikzpicture}}\n\\begin{{axis}}[\nymin=0,\nymax={self.solventFront},\nhide y axis,\n'
        temp = dict(self.__dict__.items())
        for i in temp.keys():
            if i in chromaCall.keys():
                give += f'{chromaCall[i][0]}{temp[i]}{chromaCall[i][1]},\n'
        give += f'xtick={{{",".join([str(i) for i in range(len(self.points))])}}}\n]\n\\addplot[only marks]\ncoordinates{{\n'
        for i in range(len(self.points)):
            if isinstance(self.points[i], list):
                for n in self.points[i]:
                    give += f'({i},{n})'
            else:
                give += f'({i},{self.points[i]})'
        give += '\n};\n\\end{axis}\n\\end{tikzpicture}\n\\end{center}\n'

        return give
