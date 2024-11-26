import random
from PIL import Image, ImageDraw
import math
from copy import deepcopy
import numpy as np

PI = 3.14

class Picture:

    def __init__(self, style):
        # Define instance variables with self.

        # array of colors to be chosen from
        self.colors = [
            '#000000',  # Black
            '#FF0000',  # Red
            '#FFFF00',  # Yellow
            '#000080',  # Navy
            '#006400',  # Dark Green
            '#FF00FF',  # Magenta
            '#00FFFF',  # Cyan
            '#FFA500',  # Orange
            '#800080',  # Purple
            '#A52A2A']  # Brown
            
        self.shapes = []
        self.max_shapes = 10 
        self.width, self.height = 1000, 1000
        self.style = style
        
        # Generate random shapes
        if (self.style == "cluster"):
            self.shape_functions = [self.random_rotated_rectangle] 
        else:
            self.shape_functions = [self.random_circle, self.random_rectangle, self.random_triangle, self.random_rotated_rectangle]
        
        # populate picture objects with shapes
        for _ in range(self.max_shapes):
            newShape = random.choice(self.shape_functions)()
            self.shapes.append(newShape)
         
    def copy(self):
        copyPic = deepcopy(self)
        return copyPic

    def random_circle(self):
        radius = random.randint(20, 100)
        x = random.randint(radius, self.width - radius)
        y = random.randint(radius, self.height - radius)
        color = random.choice(self.colors)
        #draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=color)
        newShape = ('circle', ((x - radius, y - radius), (x + radius, y + radius)), color, 0)
        return newShape

    def random_rotated_rectangle(self):
        width_rect = random.randint(20, 150)
        height_rect = random.randint(20, 150)
        x = random.randint(0, self.width - width_rect)
        y = random.randint(0, self.height - height_rect)
        angle = random.randint(0, 360)
        color = random.choice(self.colors)

        # Calculate corners after rotation
        half_w, half_h = width_rect / 2, height_rect / 2
        corners = ((-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h))
        rotated_corners = []
        cos_theta = math.cos(math.radians(angle))
        sin_theta = math.sin(math.radians(angle))
        for cx, cy in corners:
            rx = x + half_w + (cx * cos_theta - cy * sin_theta)
            ry = y + half_h + (cx * sin_theta + cy * cos_theta)
            rotated_corners.append((rx, ry))

        #draw.polygon(rotated_corners, fill=color, outline=color)
        newShape = ('rotatedRectangle', rotated_corners, color, angle)
        return newShape

   

    def random_rectangle(self):
        width_rect = random.randint(20, 150)
        height_rect = random.randint(20, 150)
        x = random.randint(0, self.width - width_rect)
        y = random.randint(0, self.height - height_rect)
        color = random.choice(self.colors)
        #draw.rectangle((x, y, x + width_rect, y + height_rect), fill=color, outline=color)
        newShape = ('rectangle', ((x, y), (x + width_rect, y + height_rect)), color, 0)
        return newShape

    def random_triangle(self):
        x1, y1 = random.randint(0, self.width), random.randint(0, self.height)
        x2, y2 = random.randint(0, self.width), random.randint(0, self.height)
        x3, y3 = random.randint(0, self.width), random.randint(0, self.height)
        color = random.choice(self.colors)
        #draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color, outline=color)
        newShape = ('triangle', ((x1, y1), (x2, y2), (x3, y3)), color, 0)
        return newShape

    # identify if the point is below the line on the top
    def lowerTopLine(self, x, y):
        # Calculate the slope (m) of the line
        m = (1000 - 300) / (700 - 0)  # slope formula TOP LINE

        # Calculate the y-intercept (b) of the line
        b = 300 - m * 0  # using point (x1, y1) to calculate b

        # Calculate the y-value of the line at x = px
        y_line = m * x + b

        # Check if the point is above the line(because its inverted))
        return y < y_line   
    
    # identify if the point is above the line on the bottom
    def aboveLowerLine(self, x, y):
        # Calculate the slope (m) of the line
        m = (700 - 0) / (1000 - 300)  # slope formula LOWER LINE

        # Calculate the y-intercept (b) of the line
        b = 0 - m * 300  # using point (x1, y1) to calculate b

        # Calculate the y-value of the line at x = px
        y_line = m * x + b

        # Check if the point is below the line
        return y > y_line
    
    def verticalAndColorFitness(self):    #find fitness
        overallFitness = 0
        inside = 0
        outside = 0
        colorBalance = 0
        
        for shape1_type, shape_coords, color, angle in self.shapes:
            for point in shape_coords:
                if point[0] < 300 or point[0] > 700:
                    outside += 1
                else:
                    inside += 1
                    
                if color in ('#000000', '#FF0000', '#FFFF00', '#000080', '#006400'):
                    colorBalance += 1
                else:
                    colorBalance -= 1
        
                    
        overallFitness = inside - outside + colorBalance

        return overallFitness
    
    def diagonalAndColorFitness(self):    #find fitness
        overallFitness = 0
        inside = 0
        outside = 0
        colorBalance = 0
        
        for shape_type, shape_coords, color, angle in self.shapes:
            for point in shape_coords:
                
                # if the point is between the lines increase the fitness by 1, else - decrease by 1
                if (self.aboveLowerLine(point[0], point[1]) and self.lowerTopLine(point[0], point[1])):
                    inside += 1
                else:
                    outside += 1
                
                #check if shape color is one of the suprematism colors
                if color in ('#000000', '#FF0000', '#FFFF00', '#000080', '#006400'):
                    colorBalance += 1
                else:
                    colorBalance -= 1
                    
        overallFitness = inside - outside + colorBalance

        return overallFitness
        

        

    def getShapes(self):
        return self.shapes
        
    def display(self): #display pictures as png
        canvas = Image.new("RGB", (self.width, self.height), "#fff1c3")
        draw = ImageDraw.Draw(canvas)

        if (self.style == "vertical"):
            draw.line((300, 0, 300, self.height), fill="black", width=3)
            draw.line((700, 0, 700, self.height), fill="black", width=3)
        
                
        elif (self.style == "diagonal"):
            draw.line((0, 300, 700, 1000), fill="black", width=3)
            draw.line((300, 0, 1000, 700), fill="black", width=3)
            
        elif (self.style == "cluster"):
            draw.ellipse((0, 0, 500, 500), fill=None, outline="black")
        
        for shape in self.shapes:
            if (shape[0] == 'circle'):
                x1 = shape[1][0][0]
                y1 = shape[1][0][1]
                x2 = shape[1][1][0]
                y2 = shape[1][1][1]
                color = shape[2]
                draw.ellipse((x1, y1, x2, y2), fill=color, outline=color)
                
            elif (shape[0] == 'triangle'):
                x1 = shape[1][0][0]
                y1 = shape[1][0][1]
                x2 = shape[1][1][0]
                y2 = shape[1][1][1]
                x3 = shape[1][2][0]
                y3 = shape[1][2][1]
                color = shape[2]
                draw.polygon(((x1, y1), (x2, y2), (x3, y3)), fill=color, outline=color)
            
            elif (shape[0] == 'rectangle'):

                x1 = shape[1][0][0]
                y1 = shape[1][0][1]
                x2 = shape[1][1][0]
                y2 = shape[1][1][1]
                color = shape[2]
                draw.rectangle(((x1, y1), (x2, y2)), fill=color, outline=color)
            
            elif (shape[0] == 'rotatedRectangle'):
                x1 = shape[1][0][0]
                y1 = shape[1][0][1]
                x2 = shape[1][1][0]
                y2 = shape[1][1][1]
                x3 = shape[1][2][0]
                y3 = shape[1][2][1]
                x4 = shape[1][3][0]
                y4 = shape[1][3][1]
                color = shape[2]
                draw.polygon(((x1, y1), (x2, y2), (x3, y3), (x4, y4)), fill=color, outline=color)

        # Calculate inside and outside counts
        #self.findInsideOutside()

        # Show canvas and results
        canvas.show()
    
    def mutate(self):
        randomIndex = random.randint(0, len(self.shapes)-1)
        

        randomShapeIndex = random.randint(0,4)
        
        if (self.style == "cluster"):
            self.shapes[randomIndex] = self.random_rotated_rectangle()
        
        else:
            match randomShapeIndex:
                case 0:
                    self.shapes[randomIndex] = self.random_circle()
                case 1:
                    self.shapes[randomIndex] = self.random_rectangle()
                case 2:
                    self.shapes[randomIndex] = self.random_rotated_rectangle()
                case 3:
                    self.shapes[randomIndex] = self.random_triangle()

        
    
    def cross(self, target):
        if len(self.shapes) <= len(target.shapes):
            crossIndex = random.randint(len(self.shapes)//2, len(self.shapes)) #the target picture may have more shapes than the crosser
            for i in range(crossIndex, len(self.shapes)):
                self.shapes[i] = target.shapes[i]
        else:
            crossIndex = random.randint(len(target.shapes)//2, len(target.shapes)) #vice versa
            for i in range(crossIndex, len(target.shapes)):
                self.shapes[i] = target.shapes[i]              

    def breedingStep(pic1, pic2):
        
        child1 = pic1.copy()  
        child2 = pic2.copy()

        child1.cross(pic2) #bug: doesn't cross when the parent only has 1 shape
        child2.cross(pic1)

        #len1 = len(child1.getShapes())

        child1.mutate()
        child2.mutate()
        
        #len2= len(child1.getShapes())
        
        #print("The length is: ", len1, " ", len2)
        
        children = [child1, child2]

        return children
       


















    def getDistanceFromCenter(self, x, y):
        return math.sqrt(math.pow(x - 250, 2) + math.pow(y - 250, 2))
    
    def checkOverlapCluster(self):
        overlaps = [] #array to store shapes that are overlapping the cluster

        for shape in self.shapes:
            for vertex in shape[1]:
                x = vertex[0]
                y = vertex[1]

                distanceFromCenter = self.getDistanceFromCenter(x, y)

                if distanceFromCenter < 250:
                    overlaps.append(shape)
                    break
            
        return overlaps
        
    #Reference: https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    def calcArea(self,x,y): 
        #x and y are lists of latitudes and longitudes of the vertices of a shape
        return 0.5*np.abs(np.dot(x,np.roll(y,1)) - np.dot(y,np.roll(x,1)))

    def calcOverlapFitness(self):
        global PI

        clusterAreaSurface = 250*250*PI #because the area has a diameter of 700

        x = []
        y = []
        areas = []
        overlaps = self.checkOverlapCluster() #array to store all overlapping shapes

        #get coordinates of each shape in the picture
        for shape in overlaps:
            if(shape[0] == 'triangle'):
                for i in range(3):
                    x.append(shape[1][i][0])
                    y.append(shape[1][i][1])
            elif(shape[0] == 'rectangle'): #coordinates have to be in an order
                x.append(shape[1][0][0])    #top left vertex
                y.append(shape[1][0][1])

                x.append(shape[1][1][0]) #top right vertex
                y.append(shape[1][0][1])

                x.append(shape[1][1][0]) #bottom right vetex
                y.append(shape[1][1][1])

                x.append(shape[1][0][0]) #bottom left vertex
                y.append(shape[1][1][1])
            
            elif(shape[0] == 'rotatedRectangle'):
                x.append(shape[1][0][0])    #top left vertex
                y.append(shape[1][0][1])

                x.append(shape[1][1][0]) #top right vertex
                y.append(shape[1][1][1])

                x.append(shape[1][2][0]) #bottom right vetex
                y.append(shape[1][2][1])

                x.append(shape[1][3][0]) #bottom left vertex
                y.append(shape[1][3][1])

            # calculate area of each shape that overlaps the cluster circle
            areas.append(self.calcArea(x, y))

            #do the relevant math to find the area of the overlapping parts
            #find the percentage of overlap
        
        sumOverlapShapes = 0

        for i in range(len(overlaps)): #print areas/surfaces of shapes that overlap the circle
            sumOverlapShapes += areas[i]
            #print(areas[i])

        #print(sumOverlapShapes)

        ####system of equations (if possible):
        #2*clusterAreaSurface - sumOverlapShapes = 2 * S_remain + S_overlap - S_not_overlap
        #clusterAreaSurface = S_remain + S_overlap
        #sumOverlapShapes = S_overlap + S_not_overlap

        fitness = sumOverlapShapes/clusterAreaSurface #the higher, the better
        return fitness



    def clusterAndColorFitness(self, idealAngle):    #find fitness
        
        paralFitness = 0
        
        for shape1_type, shape2_coords, color1, angle1 in self.shapes:
            if (shape1_type == "rotatedRectangle"):
                
                #print(angle1  < idealAngle + 15 and angle1 > idealAngle - 15)
                
                if (angle1  < idealAngle + 10 and angle1 > idealAngle - 10):
                    paralFitness += 1
                else:
                    paralFitness -= 1  
                     
        
        coverageFitness = self.calcOverlapFitness()   # bigger the better
        
        
        return paralFitness * 0.45 + coverageFitness * 100
