import random
from PIL import Image, ImageDraw
import math
from copy import deepcopy
import numpy as np

PI = 3.14

# class that represents a member of population
class Picture:
    def __init__(self, style):
        
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
        
        # shape options for different types of pictures
        # e.g. cluster option only uses rotated rectangles
        if (self.style == "cluster"):
            self.shape_functions = [self.random_rotated_rectangle] 
        
        # all other variations use all of the shapes
        else:
            self.shape_functions = [self.random_circle, self.random_rectangle, self.random_triangle, self.random_rotated_rectangle]
        
        # populate picture objects with shapes
        for _ in range(self.max_shapes):
            newShape = random.choice(self.shape_functions)()
            self.shapes.append(newShape)
    
    # deep copy function
    def copy(self):
        copyPic = deepcopy(self)
        return copyPic
        
    # create a tuple that contains all the information necessary for representing circle
    def random_circle(self):
        radius = random.randint(20, 100)
        # generate two random points on plain
        x = random.randint(radius, self.width - radius)
        y = random.randint(radius, self.height - radius)
        color = random.choice(self.colors)
        #draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=color)
        newShape = ('circle', ((x - radius, y - radius), (x + radius, y + radius)), color, 0)
        return newShape
        
    # create a tuple that contains all the information necessary for representing rotated rectangle
    def random_rotated_rectangle(self):
        #width_rect = random.randint(20, 150)
        #height_rect = random.randint(20, 150)
        
        width_rect = random.randint(10, 500)
        height_rect = random.randint(10, 500)
        
        
        # generate two random points on plain
        x = random.randint(0, self.width - width_rect)
        y = random.randint(0, self.height - height_rect)
        angle = random.randint(0, 360)
        color = random.choice(self.colors)

        # apply corner-rotation calculation
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

    # create a tuple that contains all the information necessary for representing regular rectangle
    def random_rectangle(self):
        width_rect = random.randint(20, 150)
        height_rect = random.randint(20, 150)
        # generate two random points on plain
        x = random.randint(0, self.width - width_rect)
        y = random.randint(0, self.height - height_rect)
        color = random.choice(self.colors)
        #draw.rectangle((x, y, x + width_rect, y + height_rect), fill=color, outline=color)
        newShape = ('rectangle', ((x, y), (x + width_rect, y + height_rect)), color, 0)
        return newShape

    # create a tuple that contains all the information necessary for representing triangle
    def random_triangle(self):
        # generate three random points on plain
        x1, y1 = random.randint(0, self.width), random.randint(0, self.height)
        x2, y2 = random.randint(0, self.width), random.randint(0, self.height)
        x3, y3 = random.randint(0, self.width), random.randint(0, self.height)
        color = random.choice(self.colors)
        #draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color, outline=color)
        newShape = ('triangle', ((x1, y1), (x2, y2), (x3, y3)), color, 0)
        return newShape

    # identify if the point is below the channel's top line
    def lowerTopLine(self, x, y):
        # find slope
        m = (1000 - 300) / (700 - 0)

        # find b
        b = 300 - m * 0 

        # find expected y value that would be on the line for such x
        y_line = m * x + b

        # Check if the point is below the line
        return y < y_line   
    
    # identify if the point is above the channel's bottom line
    def aboveLowerLine(self, x, y):
        m = (700 - 0) / (1000 - 300) 

        b = 0 - m * 300

        y_line = m * x + b

        return y > y_line
    
    # find fitness based on vertical boundaries and color
    def verticalAndColorFitness(self):
        overallFitness = 0
        inside = 0
        outside = 0
        colorBalance = 0
        
        # iterate through each shape in a picture object
        # +1 if vertice is inside the guide lines, -1 otherwise
        for shape1_type, shape_coords, color, angle in self.shapes:
            for point in shape_coords:
                if point[0] < 300 or point[0] > 700:
                    outside += 1
                else:
                    inside += 1
                
            # include the color in fitness calculation, +1 if shape's color is suprematistic
            if color in ('#000000', '#FF0000', '#FFFF00', '#000080', '#006400'):
                colorBalance += 1
            else:
                colorBalance -= 1
          
        overallFitness = inside - outside + colorBalance

        return overallFitness
    
    # find fitness based on diagonal boundaries and color
    def diagonalAndColorFitness(self):
        overallFitness = 0
        inside = 0
        outside = 0
        colorBalance = 0
        
        # iterate through each shape in a picture object
        # +1 if vertice is inside the guide lines, -1 otherwise
        for shape_type, shape_coords, color, angle in self.shapes:
            for point in shape_coords:
                
                if (self.aboveLowerLine(point[0], point[1]) and self.lowerTopLine(point[0], point[1])):
                    inside += 1
                else:
                    outside += 1
                
            # include the color in fitness calculation, +1 if shape's color is suprematistic
            if color in ('#000000', '#FF0000', '#FFFF00', '#000080', '#006400'):
                colorBalance += 1
            else:
                colorBalance -= 1
                    
        overallFitness = inside - outside + colorBalance

        return overallFitness
    
    def getShapes(self):
        return self.shapes
        
    # display the shapes stored in the array
    def display(self):
        canvas = Image.new("RGB", (self.width, self.height), "#fff1c3")
        draw = ImageDraw.Draw(canvas)

        # shpow guidelines for vertical approach
        if (self.style == "vertical"):
            draw.line((300, 0, 300, self.height), fill="black", width=3)
            draw.line((700, 0, 700, self.height), fill="black", width=3)
        
        # shpow guidelines for diagonal approach
        elif (self.style == "diagonal"):
            draw.line((0, 300, 700, 1000), fill="black", width=3)
            draw.line((300, 0, 1000, 700), fill="black", width=3)
            
        # shpow guidelines for cluster approach
        elif (self.style == "cluster"):
            draw.ellipse((0, 0, 500, 500), fill=None, outline="black")
        
        # draw all the shapes
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
        
        # display resulting canvas
        canvas.show()
    
    # mutation logic: replace random shape with a freshly randomly created shape
    def mutate(self):
        randomIndex = random.randint(0, len(self.shapes)-1)
        

        randomShapeIndex = random.randint(0,4)
        
        # only create rectangles for cluster picture
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

    # do one point crossover in random shapes array location
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

        # create deep copy of two parents
        child1 = pic1.copy()  
        child2 = pic2.copy()

        # do crossover 
        child1.cross(pic2) 
        child2.cross(pic1)

        # apply mutations
        child1.mutate()
        child2.mutate()
        
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

        clusterAreaSurface = 250*250*PI #because the area has a diameter of 500

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


    def withinClusterRadius(self, x, y):
        return (math.sqrt((x - 250)**2 + (y - 250)**2)) <= 250
    
    def calcTriangleArea(self, pointA, pointB, pointC):
        x1 = pointA[0]
        y1 = pointA[1]
        x2 = pointB[0]
        y2 = pointB[1]
        x3 = pointC[0]
        y3 = pointC[1]
        
        return 0.5 * abs(x1 * y2 + x2 * y3 + x3 * y1 - y1 * x2 - y2 * x3 - y3 * x1)
    

    def isWithinCurrentRectangle(self, allVertices, targetLocation):
        point1 = allVertices[0]
        point2 = allVertices[1]
        point3 = allVertices[2]
        point4 = allVertices[3]
        
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        x3 = point3[0]
        y3 = point3[1]
        x4 = point4[0]
        y4 = point4[1]
        
        combinedTriangleArea = self.calcTriangleArea(point1, point2, targetLocation)
        combinedTriangleArea += self.calcTriangleArea(point2, point3, targetLocation)
        combinedTriangleArea += self.calcTriangleArea(point3, point4, targetLocation)
        combinedTriangleArea += self.calcTriangleArea(point4, point1, targetLocation)
        
        rectangleArea = area = 0.5 * abs(x1*y2 + x2*y3 + x3*y4 + x4*y1 - (y1*x2 + y2*x3 + y3*x4 + y4*x1))
        
        return combinedTriangleArea <= rectangleArea
    
        
    def is_point_inside_rotated_rectangle(self, px, py, corners, angle):
        # Calculate the center of the rectangle
        cx = sum(corner[0] for corner in corners) / 4
        cy = sum(corner[1] for corner in corners) / 4
        
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        # Translate the point to the rectangle's local coordinate system
        px_rel = px - cx
        py_rel = py - cy
        
        # Apply the inverse rotation matrix
        px_rot = math.cos(angle_rad) * px_rel + math.sin(angle_rad) * py_rel
        py_rot = -math.sin(angle_rad) * px_rel + math.cos(angle_rad) * py_rel
        
        # Get the width and height from the corner points (assuming the rectangle is axis-aligned before rotation)
        w = math.dist(corners[0], corners[1])  # Distance between corner 1 and corner 2 (width)
        h = math.dist(corners[1], corners[2])  # Distance between corner 2 and corner 3 (height)
        
        # Check if the point is inside the axis-aligned bounding box
        if -w / 2 <= px_rot <= w / 2 and -h / 2 <= py_rot <= h / 2:
            return True
        return False
        
    
    
    def clusterAndColorFitness(self, idealAngle):    #find fitness
        
        paralFitness = 0
        insideFitness = 0
        noOverlapFitness = 0
        colorBalance = 0
        
        for shape_type, shape_coords, color, angle in self.shapes:
            if (shape_type == "rotatedRectangle"):
                w = shape_coords[2][0] - shape_coords[0][0]
                h = shape_coords[2][1] - shape_coords[0][1]
                
                cx = w / 2
                cy = h / 2

                if (angle  < idealAngle + 10 and angle > idealAngle - 10):
                    paralFitness += 4
                else:
                    paralFitness -= 4
                
                for coords in shape_coords:
                    if (self.withinClusterRadius(coords[0], coords[1])):
                        insideFitness += 1.7
                
                for shape_type2, shape_coords2, color2, angle2 in self.shapes:
                    for targetCoords in shape_coords2:
                        if (self.is_point_inside_rotated_rectangle(targetCoords[0], targetCoords[1], shape_coords, angle)):
                            noOverlapFitness -= 1
                            break;
                            
                # include the color in fitness calculation, +1 if shape's color is suprematistic
                if color in ('#000000', '#FF0000', '#FFFF00', '#000080', '#006400'):
                    colorBalance += 1
                else:
                    colorBalance -= 1
                
        #print (paralFitness , " " , insideFitness , " " ,noOverlapFitness)
        return paralFitness + insideFitness + noOverlapFitness + colorBalance
