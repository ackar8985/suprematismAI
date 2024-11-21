from Picture import Picture
import random


POP = 20

class Population:
    def __init__(self, style):
        self.population = []
        self.style = style
        self.fitnessToPlot = []  
        self.idealAngle = random.randint(0, 360)
        for i in range(POP):
            self.population.append(Picture(self.style))
    
    #print function for array
    def printPopulation(self):
        for pic in self.population:
            print(pic.getShapes())
            #pic.display()

    #natural selection
    def natural_selection(self):
        #array[2] for winners and losers
        winnersIndex = []
        losersIndex = []
        #while i in POPULATION
            #Fight between 2 fitness -> fitness calculation
            #winner index goes to winner array
            #loser index goes to loser array
        
        i = 0
        while i in range(POP):
            # print("Index i: " + str(i))
            
            winnersIndex.clear()    #clear the lists after each tournament of 4
            losersIndex.clear()

            for j in range(i, i+3, 2):
                # print(self.population[j])
                # print(self.population[j+1])
                # print("Index j: " + str(j))
                if (self.fight(self.population[j], self.population[j+1]) == self.population[j]):
                    winnersIndex.append(j)
                    losersIndex.append(j+1)
                else:
                    winnersIndex.append(j+1)
                    losersIndex.append(j)
                
            
            # print("Winners: " + str(winnersIndex[0]) + " " + str(winnersIndex[1]))
            # print("Losers: " + str(losersIndex[0]) + " " + str(losersIndex[1]))
            
            #2 children = breed 2 winners
            #2 children replace 2 losers
            #i += 4
            children = Picture.breedingStep(self.population[winnersIndex[0]], self.population[winnersIndex[1]])
            self.population[losersIndex[0]] = children[0]
            self.population[losersIndex[1]] = children[1]

            i = i+4


#shuffle
    #temp object
    #while(i in population-4)
        #switch place picture i with picture i+4
        #i+=2
    
    def shuffle(self):
        temp = Picture(self.style)
        i = 0
        while i in range(POP-4):
            temp = self.population[i]
            self.population[i] = self.population[i+4]
            self.population[i+4] = temp
            i = i+4

#fight
    #compare fitness, return winner
    def fight(self, pic1, pic2):
        
        if (self.style == "vertical"):
            if (pic1.verticalAndColorFitness() >= pic2.verticalAndColorFitness()): 
                return pic1
            else: 
                return pic2
        elif (self.style == "diagonal"):
            if (pic1.diagonalAndColorFitness() >= pic2.diagonalAndColorFitness()):
                return pic1
            else: 
                return pic2
            
        elif (self.style == "cluster"):
            if (pic1.clusterAndColorFitness(self.idealAngle) >= pic2.clusterAndColorFitness(self.idealAngle)):
                return pic1
            else: 
                return pic2
            
        
    
#population fitness
    def overallFitness(self):
        sum = 0
        for pic in self.population:
             
                sum = sum + pic.clusterAndColorFitness(self.idealAngle)
                
        return sum

#simulation
    #while i in 20
        #natural selection
        #calculate fitness
        #shuffle
        #i++
    
    def simulation(self):
        
        for i in range(10000):
            # display first element from first and 99 iteration
            if (i == 0 or i == 9999):
                self.population[19].display()
                print("Fitness: ", self.population[19].clusterAndColorFitness(self.idealAngle))
                
            self.natural_selection()

            self.fitnessToPlot.append(self.overallFitness())
            
            self.shuffle()
            
