from Picture import Picture
from Population import Population

picture1 = Picture()
picture2 = Picture()

picture1.display()
picture2.display()


print(picture1.getShapes())
print("\n\n")
print(picture2.getShapes())
print("\n\n")

# picture3 = picture1.copy()
# print(picture3.shapes)

children = Picture.breedingStep(picture1, picture2)

for i in range(2):
    print(children[i].getShapes())
    print("\n")
    children[i].display()
