from ETeX import *

# We first instantiate the document with a title and an author #
# This is assigned to the variable doc so we can add items to it #
doc = Document(title="Equation Examples", author="RosiePuddles")

# This creates a new Text class instance and assigns it to variable introduction_text #
introduction_text = Text("In this document we will look at how we can use ETeX to generate different types of equations.")
# This adds introduction_text to the document #
doc.add(introduction_text)


# This creates a new section called "Simple Equations" #
doc.new_section("Simple Equations")

# This creates an equation that is centered in the page and numbered called identity1 #
identity1 = Equation("\\frac{1+\\mathrm{cosec}\\theta}{\\mathrm{cot}\\theta}=\\frac{1+\\mathrm{tan}\\frac\\theta 2}{1-\\mathrm{tan}\\frac\\theta 2}")
# We then create some explanationText to precede the equation #
explanationText = Text("We can write numbered equations:")
# We then need to add these to the document #
doc.add(explanationText)
doc.add(identity1)


# This adds a new section to out document called "Equations Without Numbers" #
doc.new_section("Equations Without Numbers")

# This adds a new equation called integral1 that is not numbered, but is still centered #
integral1 = Equation("\\int_{0}^{n}\\frac{1}{\\sqrt{1+x^2}}\\mathrm{d}x=\\pi", numbered=False)
# We will also add an explanation of the integral we just made #
integralExplanation = Text('We can also write equations without numbers:')
# This then adds the equation to the document #
doc.add(integral1)

# This generates the .tex and .pdf file for the document #
doc.generate_TeX()
