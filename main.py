from Picture import Picture
from Population import Population
import matplotlib.pyplot as plt

# picture1 = Picture()
# picture2 = Picture()

# picture1.display()
# picture2.display()

# children = Picture.breedingStep(picture1, picture2)

# for i in range(2):
#     print(children[i].getShapes())
#     print("\n")
#     children[i].display()

population = Population()
#population.printPopulation()

population.simulation()


plt.plot(population.fitnessToPlot)
plt.show()
