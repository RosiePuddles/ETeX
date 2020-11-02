from LaTeX import *

doc = Document(title='Half Term Benzene Questions', author='Rosie B')
mainlist = List()

question = Text("Benzene is a perfect hexagon comprised of 6 $\\sigma$-bonds. Each carbon has a p orbital, which overlap it's neighbouring p-orbitals. \
                This overlap of p-orbitals creates two rings of delocalised electrons above and below the carbon ring, giving benzene it's distinctive properties.")
mainlist.add(question)

question = List()
part = List(list_type='bullet')
part.add(Text('Polymers'))
part.add(Text('Pharmaceuticals'))
question.add(part)
question.add(Text("To nitrate benzene, we need to react it at 55ºC."))
question.add(ChemEquation(['C6H6'], ['C6H5NO2', 'H^+'], ['H2SO4', 'HNO3'], '55ºC'))
part = List()
part.add(Text('The movement of 2 electrons'))
part.add(Text('\\ce{NO^+} is described as an electrophile because it accepts an electron pair from the benzene.'))
part.add(Text('The mechanism is described as a substitution because the benzene ring substitutes a hydrogen for a nitro group.'))
part.add(Text('Sulphuric acid is not used in the mechanism, showing it is used as a catalyst.'))
question.add(part)
question.add(Text('In the benzene ring, there are 6 electrons involved in $\\pi$ bonding, whereas there are 5 electrons involved in the intermediate. In the benzene ring, the electron density is even all around the ring. Whereas in the intermediate, the electron density is zero next to the carbon with the hydrogen and new group bonded to it, and the electron density elsewhere is similar to before.'))

mainlist.add(question)

question = List()
part = List()
part.add(ChemEquation(['C6H6', 'Cl2'], ['C6H5Cl', 'HCl'], 'AlCl3'))
part.add(Text('See attached sheet'))
part.add(Text('Electrophilic substitution'))
question.add(part)
question.add(Text('Because benzene has two rings of delocalised electrons which make it very electronegative, and so a very powerful nucleophile is required to react with it. this can only be produced by a reaction with a catalyst. In contrast, an alkene does not have such a large electronegativity and so a powerful electrophile if not required to react with it.'))

mainlist.add(question)

doc.add(mainlist)
doc.generate_TeX(debug=True)
