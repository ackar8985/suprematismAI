from Picture import Picture
from Population import Population
import matplotlib.pyplot as plt



#population = Population("vertical")
#population = Population("diagonal")
population = Population("cluster")

population.simulation()


plt.plot(population.fitnessToPlot)
plt.show()
