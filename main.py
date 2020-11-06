from ETeX.main import *

doc = Document(title='ETeX Documentation', subtitle='V0.1', author='RosiePuddles', contents=True)
doc.new_section(title='Preface')
doc.add(Text('This package is designed to allow the user to generate \\LaTeX  files and associated pdf files in a more user friendly way. '
             'Please note, however, this package is still currently heavily in development, and things will go wrong. Any bugs can be reported on '
             'the \\href{https://github.com/RosiePuddles/ETeX_from_python/issues}{issues page} of the GitHub repository. You can request any features you cannot find and want adding to the package.'
             ' Having said that, I hope you find this package useful and fairly easy to use as intended.'))

############################################################
# BASE SECTIONS
############################################################
doc.new_section(title='Base Classes')

# DOCUMENT
doc.new_section(title='Document', _type=1)
doc.add(Code('class Document(*args, **kwargs) -> None', language='Python'))
doc.add(Text('The \\verb|Document| class is the main class used in ETeX. It handles all tex code'
             'generation, and contains all information about the document as well as the actual contents themself.'))
# GENERATE_TEX
doc.new_section(title='generate\\_TeX function', _type=2)
doc.add(Code('Document.generate_TeX(self, _compile: bool = True, **kwargs) -> str', language='Python'))
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
doc.add(Text('Bullet points are also formatted and turned into underscores. The resulting formatted filename is then used for all of the resulting output files.'))
# ADD
doc.new_section(title='add function', _type=2)
doc.add(Code('Document.add(self, item: _main) -> None:\n\tself.contains.append(item)', language='Python'))
doc.add(Text('The \\verb|add| function adds a class that inherits from the class \\verb|_main|'))
doc.add(Footnote('See section 2.5.1 for a full list of classes that directly or indirectly inherit from the \\_main class.'))
doc.add(Text(' to the list of contents inside an instance of the \\verb|Document| class. The function is used'
             ' to add items into the document.'))
# NEW_SECTION
doc.new_section(title='new\\_section function', _type=2)
doc.add(Code('Document.add(self, title: str, _type: int = 0) -> None:\n\t_type = _type % 3\n\tself.contains.append(_section(title, _type))', language='Python'))
doc.add(Text('The \\verb|new_section| function is used to add a new section to a \\verb|Document| class instance.'
             ' The \\verb|_type| argument is used to identify the type of section with 0 being a section, 1 being a subsection, and 2 being a subsubsection.'))

# TEXT
doc.new_section(title='Text', _type=1)
doc.add(Code('class Text(self, text: str, align: str = None) -> None', language='Python'))
doc.add(Text('The \\verb|Text| class is the class used for the handling of text inside of ETeX. The class contains some general string formatting features allowing for '
             '*bold*, **italic**, ~highlighted~, and ~~underlined~~ text inside of the document. To read more on this see section 2.2.1. The text can also be aligned to either the left, center,'
             ' or right using the \\verb|align| argument. This will only apply to the current \\verb|Text| class instance and will not be applied to any subsequent instances of the class.'))
doc.new_section(title='String formatting', _type=2)
doc.add(Text('To format a string in ETeX, you use the /* and \\/~{} characters. The following table shows the formatting character and the relevant format.\\\\'))
formattingTable = [[Text('Formatting character'), Text('Associated formatting')],
                   [Text('/*'), Text('*Bold*')],
                   [Text('/*/*'), Text('**Italic**')],
                   [Text('\\/~{}'), Text('~Highlight~')],
                   [Text('\\/~{}\\/~{}'), Text('~~Underline~~')]]
doc.add(Table(values=formattingTable, format=['c', 'l']))
# LIST
doc.new_section(title='List', _type=1)
doc.add(Code('class List(self, list_type: str = \'numbered\', items: list = None) -> None', language='Python'))
doc.add(Text('The \\verb|List| class is used to created lists inside of ETeX. These list can be either a numbered list or a '
             'bullet point list through the use of the \\verb|list_type| argument'))
doc.add(Footnote('See section 2.3.1 for list types'))
doc.add(Text('. The list can also be initialised with items already inside of it, so long as the items inherit from the \\verb|_main| class'))
doc.add(Footnote('See section 2.5.1 for a full list of classes that directly or indirectly inherit from the \\_main class.'))
doc.add(Text('. The list can also be left empty upon initialisation and later on have items added to it using the \\verb|add| function.'))
doc.new_section(title='List types', _type=2)
doc.add(Text('To change the type of list, you can use the \\verb|list_type| argument, which takes in'
             ' a string of wither \\verb|numbered| or \\verb|bullet|, which correspond to a numbered list, or a '
             'bullet point list.'))
doc.new_section(title='add function', _type=2)
doc.add(Code('List.add(self, item: _main) -> None:\n\tself.items.append(item)\n\tself.add_super(item.packages)', language='Python'))
doc.add(Text('The add function adds the given item to the end of the list instance\'s list. The item has to inherit from the \\verb|_main| class'
             ' to be added. The second line of the function is part of the process of ensuing all the required packages are declared '
             'in the preamble of the .tex document.'))
# GROUP
doc.new_section(title='Group', _type=1)

# _MAIN
doc.new_section(title='\\_main', _type=1)
doc.add(Text('The \\verb|_main| class is the base class for all other classes the user interfaces with and provides several important '
             'functions and alterations to base functions that are used throughout.'))
doc.new_section(title='Child classes', _type=2)
doc.add(Text('This section provides a list of all the different child classes of the \\verb|_main| class:'))
temp = Columns(2)
types = List(list_type='bullet')
types.add(Text('\\verb|Text|'))
types.add(Text('\\verb|Footnote|'))
types.add(Text('\\verb|Columns|'))
types.add(Text('\\verb|Equation|'))
types.add(Text('\\verb|List|'))
types.add(Text('\\verb|group|'))
types.add(Text('\\verb|line|'))
types.add(Text('\\verb|plot|'))
types.add(Text('\\verb|coordinates|'))
types.add(Text('\\verb|axis|'))
types.add(Text('\\verb|Code|'))
types.add(Text('\\verb|Chemical|'))
types.add(Text('\\verb|ChemEquation|'))
temp.add(types)
doc.add(temp)
doc.new_section(title='generate\\_TeX method', _type=2)
doc.add(Code('_main.generate_TeX(self, *args, **kwargs) -> str', language='Python'))
doc.add(Text('The \\verb|generate_TeX| method generates raises an exception if run. All classes that inherit from \\verb|_main|'
             ' will overwrite this method with their own method to generate their unique \\LaTeX  code.'))
doc.new_section(title='Maths Classes')
doc.new_section(title='Plotting Classes')
doc.new_section(title='Chemistry Classes')
doc.generate_TeX(debug=True)
