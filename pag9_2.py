from LaTeX import *

doc = Document(title="PAG 9.2", subtitle="The rate of reaction of calcium carbonate and hydrochloric acid", author="Rosie Bartlett", left=15, right=15, bottom=25, top=20)

doc.new_section("Mass experiment")
doc.new_section("Results", 1)

axis1 = axis(title='Mass of reaction vessel with respect to time', labels=["Time (s)", "Mass (g)"], xmin=0, xmax=360, ymin=30.4, ymax=31.2, width=15, height=7)
plot1 = coordinates([(0, 31.16),
                     (10, 31.12),
                     (20, 31.08),
                     (30, 31.04),
                     (40, 31.01),
                     (50, 30.98),
                     (60, 30.94),
                     (70, 30.91),
                     (80, 30.87),
                     (90, 30.84),
                     (100, 30.82),
                     (110, 30.80),
                     (120, 30.77),
                     (130, 30.75),
                     (140, 30.74),
                     (150, 30.73),
                     (160, 30.72),
                     (170, 30.71),
                     (180, 30.70),
                     (190, 30.68),
                     (200, 30.68),
                     (210, 30.67),
                     (220, 30.66),
                     (230, 30.66),
                     (240, 30.65),
                     (250, 30.65),
                     (260, 30.65),
                     (270, 30.64),
                     (280, 30.64),
                     (290, 30.64),
                     (300, 30.64),
                     (310, 30.64),
                     (320, 30.63),
                     (330, 30.63),
                     (340, 30.63),
                     (350, 30.63),
                     (360, 30.62)], name='Mass of reaction vessel')
axis1.add_plot(plot1)
plot10 = coordinates([(0, 31.16), (190, 30.4)], color=[255, 0, 0], name='$\\frac{\mathrm{d}M}{\mathrm{d}t}$ at $t=0$')
plot11 = coordinates([(0, 31.11), (710/3, 30.4)], color=[0, 255, 125], name='$\\frac{\mathrm{d}M}{\mathrm{d}t}$ at $t=T_{\\frac12}$')
axis1.add_plot(plot10)
axis1.add_plot(plot11)
doc.add(axis1)

doc.new_section('Analysis of results', 1)
list1 = List()
list1.add(Text('Half life 1 -> 75s\\\\Half life 2 -> 55s\\\\Half life 3 -> 55s'))
list1.add(Text('The half live values above include one anomaly, which when excluded give a constant half life.'))
doc.add(list1)

doc.new_section('Gas reaction')
doc.new_section('Results', 1)
doc.add(Text('By using the formula below, we can calculate the concentration of HCl from the volume of gas produced.',
             'Where $V(\\text{CO}_2)$ is the volume of CO$_2$ produced.'))
eq1 = Equation('[\\text{HCl}]=\\frac{120-V(\\text{CO}_2)}{240}', False)
doc.add(eq1)

axis2 = axis(title='Concentration of HCl with respect to time', labels=['Time (s)', '{[HCl]} (mol dm$^{-3}$)'], xmin=0, xmax=260, ymin=0, ymax=0.5, width=15, height=7)
plot2 = coordinates([
    (0, 0.50000),
    (10, 0.45833),
    (20, 0.42917),
    (30, 0.39583),
    (40, 0.36667),
    (50, 0.34167),
    (60, 0.32917),
    (70, 0.31250),
    (80, 0.30000),
    (90, 0.28750),
    (100, 0.27500),
    (110, 0.26667),
    (120, 0.25833),
    (130, 0.25000),
    (140, 0.24167),
    (150, 0.23750),
    (160, 0.23333),
    (170, 0.22917),
    (180, 0.22500),
    (190, 0.22500),
    (200, 0.22083),
    (210, 0.21667),
    (220, 0.21667),
    (230, 0.21250),
    (240, 0.21250),
    (250, 0.21250),
    (260, 0.21250)
], name='Concentration of HCl')
axis2.add_plot(plot2)
plot20 = coordinates([(0, 0.5), (120, 0)], color=[255, 0, 0], name='$\\frac{\\mathrm{d}[\\text{HCl}]}{\\mathrm{d}t}$ at $t=0$')
plot21 = coordinates([(0, 7/15), (560/3, 0)], color=[0, 255, 125], name='$\\frac{\\mathrm{d}[\\text{HCl}]}{\\mathrm{d}t}$ at $t=T_\\frac12$')
axis2.add_plot(plot20)
axis2.add_plot(plot21)
doc.add(axis2)

doc.new_section('Analysis of results', 1)
list2 = List()
list2.add(Text('Half life 1 -> 43.5s\nHalf life 2 -> 50s\nHalf life 3 -> 45.5s'))
list2.add(Text('Since all the half lives are similar, we can suggest that the reaction is first order.'))
doc.add(list2)

doc.new_section('Extension opportunities')
qs = List()
q1 = List()
q1.add(Text('Mass lost:\nSince there was an excess of CaCO$_3$, when the reaction reached completion, there would have been 0.04 mol of CO$_2$ produced. this would hav had a mass of 0.88g, meaning 0.88g would have been lost. In the reaction we only saw a loss of 0.5g, so the reaction did not go to completion.\n',
            'Gas produced:\nAgain the CaCO$_3$ was in excess, so at the end of the reaction, 0.01 mol of CO$_2$ would have been produced, with a volume of 120cm$^3$. we only saw a maximum volume of 69cm$^3$, so the reaction did not go to completion.'))
q1.add(Text('As the reaction progresses, the concentration of HCl is constantly decreasing, which constantly decreases the rate, meaning a very long long time would be required to run the reaction to completion.'))
q1.add(Text('For the reaction to go to completion, we would need a larger gas syringe to account for the extra 20cm3 of CO2 produced.'))
qs.add(q1)
qs.add(Text('Mass lost:\nAt $t=0$, $\\frac{\mathrm{d}M}{\mathrm{d}t}$ was $-4\\times10^{-3}$ g s$^{-1}$. At $t=T_\\frac12$, $\\frac{\mathrm{d}M}{\mathrm{d}t}$ was $-3\\times10^{-3}$ g s$^{-1}$.\n',
            'Gas produced:\nAt $t=0$, $\\frac{\\mathrm{d}[\\text{HCl}]}{\mathrm{d}t}$ was $\\frac1{240}$ mol dm$^3$ s$^{-1}$ or approximately $4.17\\times10^{-3}$ mol dm$^3$ s$^{-1}$. At $t=T_\\frac12$, $\\frac{\\mathrm{d}[\\text{HCl}]}{\mathrm{d}t}$ was $2.5\\times10^{-3}$ mol dm$^3$ s$^{-1}$.\n',
            'In both cases, the gradient at $T_\\frac12$ is approximately half of what t was at $t=0$, giving further evidence that the reaction is first order.'))
doc.add(qs)

doc.new_section("Extra proofs")


# r=-0.942691569, pmcc(0.00000000000000001 -> 1*10^-17)=0.9358423 #
# b=-3.087939*10^-3 #

doc.generate_TeX(debug=True)
