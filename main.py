from LaTeX import *

# We first instantiate the document with a title and an author #
# This is assigned to the variable doc so we can add items to it #
doc = Document(title="t-formula Proofs", author="RosiePuddles")

# This creates a new Text class instance and assigns it to variable introduction_text #
introduction_text = Text("In this example we will use the $t$-formula to prove some simple trigonometric identities")
# This adds introduction_text to the document #
doc.add(introduction_text)

# This creates a new section called "Proof 1" #
doc.new_section("Proof 1")


# This generates the .tex and .pdf file for the document #
doc.generate_TeX()

# if __name__ == "__main__":
#     Doc = Document(title='Photoelectric Effect', author='Rosie Bartlett', top='5mm', left='15mm', right='15mm')
#     all_questions = List()
#     currentQ = List()
#
#     ans = Text("Photoelectric emission from a metal surface is the ",
#                "emission of electrons from a metal surface due to the photoelectric effect.")
#     currentQ.add(ans)
#     ans = Text("Since for each metal the valence electrons are attracted by different amounts by the nucleus, each photon that hits the metal must have a minimum amount of energy, called the work function $\phi$, to remove the valence electron. $\phi$ is different for each type of metal since it is dependant on the attraction between the atom and nucleus.")
#     currentQ.add(ans)
#     all_questions.add(currentQ)
#
#     currentQ = List()
#     part = List()
#     ans = Text("$E=hf=450\\times10^{-9}\\times h\\approx3.0\\times10^{-40}J$")
#     part.add(ans)
#     ans = Text("$E=hf=1500\\times10^{-9}\\times h\\approx9.9\\times10^{-40}J$")
#     part.add(ans)
#     currentQ.add(part)
#     ans = Text("Since $E=hf$, and $v=f\lambda$, as $\\lambda$ increases, $f$ must decrease, which means the energy of the photon must also decrease. When $\\lambda\\in\\langle 450\\times10^{-9}, 650\\times10^{-9} \\rangle$ then at some point $E=\\phi$, meaning that at a higher wavelength than when that occurs, no electrons can be emitted because the photons do not have enough energy to move them.")
#     currentQ.add(ans)
#     all_questions.add(currentQ)
#
#     currentQ = List()
#     aaaaa = group()
#     ans = Text("Using $f=\\frac{e\\phi_{eV}}{h}$:")
#     aaaaa.add(ans)
#     ans = Text("Caesium, potassium")
#     currentQ.add(ans)
#     ans = Text("Silver")
#     currentQ.add(ans)
#     ans = Text("Caesium")
#     currentQ.add(ans)
#     ans = Text("0. A photon with a wavelength of 300nm has less energy than $\\phi$")
#     currentQ.add(ans)
#     ans = Text("0.18V")
#     currentQ.add(ans)
#     aaaaa.add(currentQ)
#     all_questions.add(aaaaa)
#
#     all_questions.add(Text("1.3V"))
#     all_questions.add(Text("3.7$\\times10^{-25}$ms$^{-1}$"))
#
#     currentQ = List()
#     ans = Text("3.1$\\times10^{-19}$J")
#     currentQ.add(ans)
#     ans = Text("$\phi=$1.6$\\times10^{-19}$J")
#     currentQ.add(ans)
#     ans = Text("$f_0=$2.5$\\times10^{14}$Hz")
#     currentQ.add(ans)
#
#     all_questions.add(currentQ)
#
#     Doc.add(all_questions)
#
#     Doc.generate_TeX()
