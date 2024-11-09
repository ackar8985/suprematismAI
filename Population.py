from Picture import Picture

POP = 20

class Population:
    def __init__(self):
        population = []    
        for i in range(POP):
            self.population.append(Picture())
    
    #print function for array
    def printPopulation(self):
        for pic in self.population:
            print(pic.getShapes())
            #pic.display()

#natural selection
    #array[2] for winners and losers
    #while i in POPULATION
        #Fight between 2 fitness -> fitness calculation
        #winner index goes to winner array
        #loser index goes to loser array
        #2 children = breed 2 winners
        #2 children replace 2 losers
        #i += 4
    

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
    def fight(pic1, pic2):
        if (pic1.findInsideOutside() > pic2.findInsideOutside()):
            return pic1
        else: return pic2

#simulation
    #while i in 20
        #natural selection
        #calculate fitness
        #shuffle
        #i++
