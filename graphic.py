import numpy as np
from matplotlib import pyplot
from textwrap import wrap
import matplotlib.ticker as ticker

with open ("settings.txt", "r") as settings:
    tmp = [float(i) for i in settings.read().split("\n")]

data_array = np.loadtxt("data.txt", dtype = int)*tmp[0]

fig, ax = pyplot.subplots(figsize = (14, 10), dpi = 400)

ax.plot(np.linspace(0, tmp[1]*(len(data_array)-1), len(data_array)), data_array )

ax.set_xlabel('Время, с')
ax.set_ylabel('Напряжение, В')


ax.set_title("\n".join(wrap('Процесс разряда и заряда конденсатора в RC-цепи', 60)), loc = 'center')
ax.grid(which = 'major', color = 'gray')
ax.minorticks_on()
ax.grid(which = 'minor', color = 'gray', linestyle = ':')
ax.grid(color='gray', linestyle='-', linewidth=2)
ax.legend('V(t)')
fig.savefig('graphic.svg')
pyplot.show()