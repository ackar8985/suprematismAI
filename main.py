from Picture import Picture
from Population import Population

# picture1 = Picture()
# picture2 = Picture()

# picture1.display()
# picture2.display()


# print(picture1.getShapes())
# print("\n\n")
# print(picture2.getShapes())
# print("\n\n")

# children = Picture.breedingStep(picture1, picture2)

# for i in range(2):
#     print(children[i].getShapes())
#     print("\n")
#     children[i].display()

population = Population()
population.printPopulation()

population.natural_selection()
print("\nafter: ")
population.printPopulation()

population.simulation()
population.population[0].display()