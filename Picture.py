import random
from PIL import Image, ImageDraw
import math


class Picture:
    def __init__(self):
        # Define instance variables with self.
        self.colors = ["red", "blue", "green", "yellow", "black"]
        self.shapes = []
        self.outside = 0
        self.inside = 0
        self.max_shapes = 20
        self.width, self.height = 1000, 1000
        
        # Generate random shapes
        shape_functions = [self.random_circle, self.random_square, self.random_rectangle, self.random_triangle, self.random_rotated_rectangle]
        num_shapes = random.randint(1, self.max_shapes)

        for _ in range(num_shapes):
            random.choice(shape_functions)() #(draw)
            
            
        

    def random_circle(self):
        radius = random.randint(20, 100)
        x = random.randint(radius, self.width - radius)
        y = random.randint(radius, self.height - radius)
        color = random.choice(self.colors)
        #draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=color)
        self.shapes.append(('circle', ((x - radius, y - radius), (x + radius, y + radius)), color))

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
        self.shapes.append(('rotatedRectangle', rotated_corners, color))

    def random_square(self):
        side = random.randint(20, 100)
        x = random.randint(side, self.width - side)
        y = random.randint(side, self.height - side)
        color = random.choice(self.colors)
        #draw.rectangle((x, y, x + side, y + side), fill=color, outline=color)
        self.shapes.append(('rectangle', ((x, y), (x + side, y + side)), color))

    def random_rectangle(self):
        width_rect = random.randint(20, 150)
        height_rect = random.randint(20, 150)
        x = random.randint(0, self.width - width_rect)
        y = random.randint(0, self.height - height_rect)
        color = random.choice(self.colors)
        #draw.rectangle((x, y, x + width_rect, y + height_rect), fill=color, outline=color)
        self.shapes.append(('rectangle', ((x, y), (x + width_rect, y + height_rect)), color))

    def random_triangle(self):
        x1, y1 = random.randint(0, self.width), random.randint(0, self.height)
        x2, y2 = random.randint(0, self.width), random.randint(0, self.height)
        x3, y3 = random.randint(0, self.width), random.randint(0, self.height)
        color = random.choice(self.colors)
        #draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color, outline=color)
        self.shapes.append(('triangle', ((x1, y1), (x2, y2), (x3, y3)), color))

    def findInsideOutside(self):    #find fitness
        overallFitness = 0
        for shape_type, shape_coords, _ in self.shapes:
            for point in shape_coords:
                if point[0] < 300 or point[0] > 700:
                    self.outside += 1
                else:
                    self.inside += 1
        overallFitness = self.inside
        print("Outside:", self.outside)
        print("Inside:", self.inside)
        print("Fitness:", (self.inside - self.outside))
        print("Total shapes:", len(self.shapes))
        return overallFitness

    def getShapes(self):
        return self.shapes
        
    def display(self):
        canvas = Image.new("RGB", (self.width, self.height), "white")
        draw = ImageDraw.Draw(canvas)

        # Draw guide lines
        draw.line((300, 0, 300, self.height), fill="black", width=3)
        draw.line((700, 0, 700, self.height), fill="black", width=3)

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
       
