import random
from PIL import Image, ImageDraw
import math
from copy import deepcopy
import numpy as np

PI = 3.14

class ClusterPicture:

    def __init__(self):
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

        # Generate random shapes
        self.shape_functions = [self.random_rectangle, self.random_triangle, self.random_rotated_rectangle]
        num_shapes = random.randint(1, self.max_shapes)
        #num_shapes = 1
        
        # populate picture objects with shapes
        for _ in range(num_shapes):
            newShape = random.choice(self.shape_functions)()
            self.shapes.append(newShape)
         
    def copy(self):
        copyPic = deepcopy(self)
        return copyPic

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
        newShape = ('rotatedRectangle', rotated_corners, color)
        return newShape

    def random_rectangle(self):
        width_rect = random.randint(20, 150)
        height_rect = random.randint(20, 150)
        x = random.randint(0, self.width - width_rect)
        y = random.randint(0, self.height - height_rect)
        color = random.choice(self.colors)
        #draw.rectangle((x, y, x + width_rect, y + height_rect), fill=color, outline=color)
        newShape = ('rectangle', ((x, y), (x + width_rect, y + height_rect)), color)
        return newShape

    def random_triangle(self):
        x1, y1 = random.randint(0, self.width), random.randint(0, self.height)
        x2, y2 = random.randint(0, self.width), random.randint(0, self.height)
        x3, y3 = random.randint(0, self.width), random.randint(0, self.height)
        color = random.choice(self.colors)
        #draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color, outline=color)
        newShape = ('triangle', ((x1, y1), (x2, y2), (x3, y3)), color)
        return newShape

    def colorFitness(self):
            colorBalance = 0
            for shape_type, shape_coords, color in self.shapes:
                #check if shape color is one of the suprematism colors
                if color in ('#000000', '#FF0000', '#FFFF00', '#000080', '#006400'):
                    colorBalance += 1
                else:
                    colorBalance -= 1
            return colorBalance
    
    def inCluster(self):
        for shape in self.shapes:
            if shape[0] == 'rectangle':
                return
            elif shape[0] == 'triangle':
                return
            else:
                return
        
    def calcArea(self,x,y): #Reference: https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
        #x and y are lists of latitudes and longitudes of the vertices of a shape
        return 0.5*np.abs(np.dot(x,np.roll(y,1)) - np.dot(y,np.roll(x,1)))

    def calcOverlapFitness(self):
        global PI

        clusterAreaSurface = 350*350*PI #because the area has a diameter of 700

        x = []
        y = []
        areas = []

        #get coordinates of each shape in the picture
        for shape in self.shapes:
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

            # calculate area of each shape
            areas.append(self.calcArea(x, y))
        
        for i in range(len(self.shapes)):
            print(areas[i])

        

        fitness = 0


    def getShapes(self):
        return self.shapes
        
    def display(self): #display pictures as png
        canvas = Image.new("RGB", (self.width, self.height), "#fff1c3")
        draw = ImageDraw.Draw(canvas)

        # Draw guide area    
        draw.ellipse((0, 0, 700, 700), fill=None, outline="black")

        for shape in self.shapes:
            if (shape[0] == 'triangle'):
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
        randomShapeIndex = random.randint(0,2)
        match randomShapeIndex:
            case 0:
                self.shapes[randomIndex] = self.random_rectangle()
            case 1:
                self.shapes[randomIndex] = self.random_rotated_rectangle()
            case 2:
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

picture = ClusterPicture()
picture.calcOverlapFitness()
picture.display()
