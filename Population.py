from Picture import Picture


POP = 20

class Population:
    def __init__(self):
        self.population = []  
        self.fitnessToPlot = []  
        for i in range(POP):
            self.population.append(Picture())
    
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
        temp = Picture()
        i = 0
        while i in range(POP-4):
            temp = self.population[i]
            self.population[i] = self.population[i+4]
            self.population[i+4] = temp
            i = i+4

#fight
    #compare fitness, return winner
    def fight(self, pic1, pic2):
        #if (pic1.verticalAndColorFitness() >= pic2.verticalAndColorFitness()):    # insert if condition here to switch between fitness functions
        if (pic1.diagonalAndColorFitness() >= pic2.diagonalAndColorFitness()):
            return pic1
        else: return pic2
    
#population fitness
    def overallFitness(self):
        sum = 0
        for pic in self.population:
            #sum = sum + pic.verticalAndColorFitness()    # insert if condition here to switch between fitness functions
            sum = sum + pic.diagonalAndColorFitness()
        self.fitnessToPlot.append(sum)
        return sum

#simulation
    #while i in 20
        #natural selection
        #calculate fitness
        #shuffle
        #i++
    
    def simulation(self):
        
        for i in range(100):
            # display first element from first and 99 iteration
            if (i == 0 or i == 99):
                self.population[0].display()
            
            self.natural_selection()

            self.fitnessToPlot.append(self.overallFitness())
            
            self.shuffle()
            
            
