from Picture import Picture
from Population import Population
import matplotlib.pyplot as plt


#choose what kind of suprematistic would you like to generate

# population = Population("vertical")
# population = Population("diagonal")
population = Population("cluster")

# executes the GA
population.simulation()

# plotting the population fitness results on a chart
plt.plot(population.fitnessToPlot)
plt.show()
