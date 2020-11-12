from ETeX import *

doc = Document(title='ETeX Documentation', subtitle='V0.1', author='RosiePuddles', contents=True)
doc.new_section(title='Preface')
doc.add(Text('This package is designed to allow the user to generate \\LaTeX\\ files and associated pdf files in a more user friendly way. '
             'Please note, however, this package is still currently heavily in development, and things will go wrong. Any bugs can be reported on '
             'the \\href{https:////github.com//RosiePuddles//ETeX\\_from\\_python//issues}{issues page} of the GitHub repository. You can request any features you cannot find and want adding to the package.'
             ' Having said that, I hope you find this package useful and fairly easy to use as intended.\\\\\nPlease note that every class inherits from the '
             ' Having said that, I hope you find this package useful and fairly easy to use as intended.\\\\\nPlease note that every class inherits from the '
             '\\verb|_main| class unless specified otherwise. Each class that inherits from \\verb|_main| may overwrite methods defined in the \\verb|_main| class. If '
             'a class does overwrite a predefined method this will be documented, otherwise there will be no specific documentation if the method is inherited.'))

############################################################
# BASE SECTIONS
############################################################
doc.new_section(title='Main Classes')
doc.add(Text('This section is for the documentation of the classes contained within \\verb|ETeX|.\\\\\nEach of the classes in this section, except for the '
             '\\verb|Document| class, inherit from the \\verb|_main| class'))
doc.add(Footnote('See \\autoref{subsubsec:child_classes} for a full list of classes that directly or indirectly inherit from the \\_main class.'))
doc.add(Text('. As such please be aware that when looking for documentation on a certain method that the method may be inherited and '
             'documentation will be contained within the \\verb|_main| class section.'))

# DOCUMENT
doc.new_section(title='Document', _type=1)
doc.add(Code('class Document:\n\tdef __init__(self, *args, **kwargs) -> None', language='python'))
doc.add(Text('The \\verb|Document| class is the main class used in ETeX. It handles all tex code'
             'generation, and contains all information about the document as well as the actual contents themself.'))
#   GENERATE_TEX
doc.new_section(title='generate\\_TeX method', _type=2)
doc.add(Code('Document.generate_TeX(self, _compile: bool = True, **kwargs) -> str', language='python'))
doc.add(Text('The \\verb|generate_TeX| function is used to firstly generate the .tex file which is then compiled and the resulting .pdf file is opened.'
             ' The parameter \\verb|_compile| is set to \\verb|False| by default. If it is changed to \\verb|True|, then only the .tex file will be generated, but not compiled. '
             'For the \\verb|kwargs|, you can pass in \\verb|debug=True| to see the logs from pdflatex as it compiles the .tex file.\nThe output .tex file name will be a '
             'formatted version of the value for the title given on instantiation of a new instance of the \\verb|Document| class. Any of the following characters are removes:'))
temp = List(list_type='bullet')
temp.add(Text('\\$'))
temp.add(Text('\\%'))
temp.add(Text('//'))
temp.add(Text('\\textbackslash'))
doc.add(temp)
doc.add(Text('Full stops are also formatted and turned into underscores. The resulting formatted filename is then used for all of the resulting output files.'))
#   ADD
doc.new_section(title='add method', _type=2)
doc.add(Code('Document.add(self, item: _main) -> None', language='python'))
doc.add(Text('The \\verb|add| method adds items to the document. The added item must inherit from the \\verb|_main| class. Only items added to the \\verb|Document| class instance '
             'will be included in the final document.'))
#   NEW_SECTION
doc.new_section(title='new\\_section method', _type=2)
doc.add(Code('Document.new_section(self, title: str, _type: int = 0) -> None', language='python'))
doc.add(Text('The \\verb|new_section| function is used to add a new section to a \\verb|Document| class instance.'
             ' The \\verb|_type| argument is used to identify the type of section with 0 being a section, 1 being a subsection, and 2 being a subsubsection.'))

# _MAIN
doc.new_section(title='\\_main', _type=1)
doc.add(Text('The \\verb|_main| class is the base class for all other classes the user interfaces with and provides several important '
             'functions and alterations to base functions that are used throughout.'))
doc.new_section(title='Child classes', _type=2)
doc.add(Text('This section provides a list of all the different child classes of the \\verb|_main| class. This is split up into two parts. Those that directly inherit'
             ' from the \\verb|_main| class, and those that inherit from the \\verb|_main| class through inheriting from the \\verb|_holder| class.\\\\\nClasses '
             'that inherit from \\verb|_main|:'))
temp = Columns(2)
types = List(list_type='bullet')
types.add(Text('\\verb|Text|'))
types.add(Text('\\verb|Footnote|'))
types.add(Text('\\verb|Equation|'))
types.add(Text('\\verb|line|'))
types.add(Text('\\verb|plot|'))
types.add(Text('\\verb|coordinates|'))
types.add(Text('\\verb|axis|'))
types.add(Text('\\verb|Code|'))
types.add(Text('\\verb|Chemical|'))
types.add(Text('\\verb|ChemEquation|'))
temp.add(types)
doc.add(temp)
doc.add(Text('Classes that inherit from \\verb|_holder|:'))
temp = Columns(2)
types = List(list_type='bullet')
types.add(Text('\\verb|Columns|'))
types.add(Text('\\verb|List|'))
types.add(Text('\\verb|Group|'))
temp.add(types)
doc.add(temp)
doc.new_section(title='\\_holder', _type=1)
doc.add(Code('class _holder(_main):\n\tdef __init__(self, packages) -> None', language='python'))
doc.add(Text('The \\verb|_holder| class is a second base class that inherits from the \\verb|_main| class. The class adds the \\verb|add| method and allows for child classes to have class ins'
             'tances added to them. For a full list of classes that inherit from \\verb|_holder| see \\autoref{subsubsec:child_classes}.'))
doc.new_section(title='add method', _type=2)

# TEXT
doc.new_section(title='Text', _type=1)
doc.add(Code('class Text(_main):\n\tdef __init__(self, text: str, align: str = None) -> None', language='python'))
doc.add(Text('The \\verb|Text| class is the class used for the handling of text inside of ETeX. The class contains some general string formatting features allowing for '
             '*bold*, **italic**, ~highlighted~, and ~~underlined~~ text inside of the document. To read more on this see \\autoref{subsubsec:inbuilt_formatting}. The text can also be aligned to either the left, center,'
             ' or right using the \\verb|align| argument. This will only apply to the current \\verb|Text| class instance and will not be applied to any subsequent instances of the class.'))
#   STRING FORMATTING
doc.new_section(title='Inbuilt formatting', _type=2)
doc.add(Text('To format a string in ETeX, you use the /* and \\ /~{} characters. The following table shows the formatting character and the relevant format.\/'))
formattingTable = [[Text('Formatting character'), Text('Associated formatting')],
                   [Text('/*'), Text('*Bold*')],
                   [Text('/*/*'), Text('**Italic**')],
                   [Text('$\\sim$'), Text('~Highlight~')],
                   [Text('$\\sim\\sim$'), Text('~~Underline~~')]]
doc.add(Table(values=formattingTable, format=['c', 'l']))
#   LATEX COMMANDS
doc.new_section(title='Extra formatting', _type=2)
doc.add(Text('Withing the text environment regular \\LaTeX  commands can be used. Some useful examples are given below:'))
doc.add(List(list_type='bullet', items=[Text('{\\textbackslash}verb$\\mid${foo}$\\mid$ produces text in a code-like font as seen below:\/\\verb|foo|'),
                                        Text('\\$\\\\The \\$ character allows you to write inline maths equations such as the example below:\/'
                                             '\\$2x+y\\^{}3=-1\\$ $\\rightarrow\\ 2x+y^3=-1$')]))

# LIST
doc.new_section(title='List', _type=1)
doc.add(Code('class List(_holder):\n\tdef __init__(self, list_type: str = \'numbered\', items: list = None) -> None', language='python'))
doc.add(Text('The \\verb|List| class is used to created lists inside of ETeX. These list can be either a numbered list or a '
             'bullet point list through the use of the \\verb|list_type| argument'))
doc.add(Text('. The list can also be initialised with items already inside of it, so long as the items inherit from the \\verb|_main| class. '
             'The list can also be left empty upon initialisation and later on have items added to it using the \\verb|add| function.'))
#   LIST TYPES
doc.new_section(title='List types', _type=2)
doc.add(Text('To change the type of list, you can use the \\verb|list_type| argument, which takes in'
             ' a string of wither \\verb|numbered| or \\verb|bullet|, which correspond to a numbered list, or a '
             'bullet point list.'))

# GROUP
doc.new_section(title='Group', _type=1)
doc.add(Code('class Group(_holder):\n\tdef __init__(self, items: list = None) -> None', language='python'))
doc.add(Text('The \\verb|Group| class is a holding class used for storing other classes. The primary use for this class is alongside '
             'lists. When an item is added to a list it is added as a new item, however if the user wants to add several different '
             'classes to a list as the same point they can put all the items into a \\verb|Group| class and add that to the list.'))

# COLUMN
doc.new_section(title='Columns', _type=1)
doc.add(Code('class Columns(_holder):\n\tdef __init__(self, columns: int, items: list = None, unbalanced: bool = False) -> None', 'Python'))
doc.add(Text('The \\verb|Columns| class is used to add columns to the document. It is similar to the \\verb|Group| class in that it stores classes to be contained within it\'s formatting.'
             ' Only items added to the class will be put into columns. To make the columns unbalances, i.e. with the contents not spread out equally over all the columns, you can '
             'change the \\verb|unbalanced| argument to \\verb|True|.'))


############################################################
# MATHS SECTIONS
############################################################
doc.new_section(title='Maths Classes')
doc.new_section(title='Equation', _type=1)
########################################################################################################################


############################################################
# PLOTTING SECTIONS
############################################################
doc.new_section(title='Plotting Classes')
doc.add(Text('This section is for classes contained within \\verb|ETeX.maths.plots|. All classes inherit from \\verb|_main| unless stated otherwise.'))
doc.new_section(title='Axis', _type=1)
doc.add(Code('class Axis(_main):\n\tdef __init__(self, *args, **kwargs) -> None', language='python'))
doc.add(Text('The \\verb|Axis| class is the handler for all plots. It is centre justified. Within the \\verb|/*/*kwargs| argument there are a large number of parameters '
             'that we can pass in. these are listed below:'))
options = List(list_type='bullet')
options.add(Text('\\verb|title: str|\\\\This is the title of the axis and is positioned centre justified above the axis'))
options.add(Text('\\verb|width: int or float|\\\\This is the width of the axis. This is measured in cm.'))
options.add(Text('\\verb|height: int or float|\\\\This is the height of the axis. This is measured in cm.'))
minMax = Group()
minMax.add(Text('Min and max values:\\\\\nThese correspond to the minimum and maximum $x$ and $y$ values on the axi. If none are specified the minimum or maximum values of the plots '
                'contained within the axis will be used instead. The following options are available:'))
minMax.add(List(list_type='bullet', items=[Text('\\verb|xmin: int or float|'),
                                           Text('\\verb|xmax: int or float|'),
                                           Text('\\verb|ymin: int or float|'),
                                           Text('\\verb|ymax: int or float|')]))
options.add(minMax)
names = Group(items=[Text('Axis labels:\\\\\nThese correspond to the $x$ and $y$ axis labels. The following options are available:'), List(list_type='bullet', items=[
    Text('\\verb|xlab: str|'),
    Text('\\verb|ylab: str|')
])])
options.add(names)
options.add(Text('\\verb|samples: int|\\\\This is the number of samples used for plotting functions. By default it is set to 100.'))
options.add(Text('\\verb|showTickMarks: bool|\\\\This bool controls weather or not tick marks are shown on the $x$ and $y$ axes. This is set to \\verb|True| by default.'))
options.add(Text('\\verb|clip: bool|\\\\This bool controls weather or not the plots can be clipped to fit within the axis. This is set to \\verb|False| by default.'))
doc.add(options)
doc.new_section(title='add\\_plot method', _type=2)
doc.add(Code('Axis.add_plot(self, new_plot: plot or coordinates) -> None', language='python'))
doc.add(Text('The \\verb|add_plot| method adds a plot to the current \\verb|Axis| instance. The plot must be an instance of either a \\verb|plot| or \\verb|coordinates| class.'))
# Plot
doc.new_section(title='Plot', _type=1)
doc.add(Code('class Plot(_main)\n\tdef __init__(self, function: str, *args, **kwargs) -> None', language='python'))
doc.add(Text('The \\verb|Plot| class is used for plotting mathematically defined functions. These then have to be added '
             'to an \\verb|Axis| class to be shown. The class has several options for the presentation of the function, which'
             ' are listed below:'))
doc.add(List(list_type='bullet', items=[Text('\\verb|domain: tuple|\\\\This controls the domain of the function. '
                                             'It must be a tuple with two values in in ascending order, for example '
                                             '(1,5).'),
                                        Text('\\verb|color: str|\\\\This sets the colour of the plot. this colour must either be'
                                             ' native to \\LaTeX\\ or defined in the \\verb|DocumentSettings| class\\footnote{Soon to be added}.')]))
doc.new_section(title='Coordinates', _type=1)
########################################################################################################################

############################################################
# CHEMISTRY SECTIONS
############################################################
doc.new_section(title='Chemistry Classes')
doc.add(Text('This section is for classes contained within \\verb|ETeX.chemistry|. All classes inherit from \\verb|_main| '
             'unless specified otherwise.'))
doc.new_section(title='Chemical', _type=1)
doc.new_section(title='ChemEquation', _type=1)
doc.new_section(title='Chromatography', _type=1)
########################################################################################################################
doc.generate_TeX(debug=True)
