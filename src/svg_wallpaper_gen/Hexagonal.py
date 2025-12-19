import math 
from PIL import Image

class Hexagonal:
    '''
    Hexagonal class use to create wallpaper with hexagonal method
    '''
    def __init__(self, input_file, size):
        self.size = size        
        img = Image.open(input_file)
        self.image = img.convert('RGB')
        self.hexagons = []
        self.img_width = img.width
        self.img_height = img.height

    def get_grid_points(self):
        '''
        Generate the center of each hexagone of our picture and return each points in a list.
        Using : point-top paradigm
        
        :param self: Hexagonal previously generated
        '''
        points = []
        hexa_witdh = math.sqrt(3) * self.size
        hexa_height = 2 * self.size
        
        # Spacing according to point-top 
        horizontal_spacing = hexa_witdh
        vertical_spacing = hexa_height * 0.75 

        num_cols = int(self.img_width / horizontal_spacing) + 5
        num_rows = int(self.img_height / vertical_spacing) + 5
        
        half_w = hexa_witdh / 2
        half_h = hexa_height / 2

        for row in range(num_rows):
            for col in range(num_cols):
                x = col * horizontal_spacing
                y = row * vertical_spacing
                if row % 2 == 1:
                    x += hexa_witdh / 2 
                if (x - half_w < self.img_width) and (x + half_w > 0) and (y - half_h < self.img_height) and (y + half_h > 0):
                    points.append((x, y))
        return points
    
    def sample_color(self, x_center, y_center):
        '''
        Take the color of the pixels around our center and return the average color
        
        :param self: our Hexagon with size and the image
        :param x_center: the x-coordinates of the center
        :param y_center: the y-coordinates of the center
        '''
        radius = int(self.size / 2) 

        x_start = max(0, int(x_center - radius))
        x_end = min(self.img_width, int(x_center + radius))
        y_start = max(0, int(y_center - radius))
        y_end = min(self.img_height, int(y_center + radius))

        array_r = [] 
        array_g = []
        array_b = [] 
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                pixel = self.image.getpixel((x, y))
                array_r.append(pixel[0])
                array_g.append(pixel[1])
                array_b.append(pixel[2])

        total_pix = len(array_b)
        if total_pix > 0:
            return ( (sum(array_r)) // total_pix, (sum(array_g)) // total_pix, (sum(array_b)) // total_pix )
        else:
            return (0, 0, 0)

    def create_unique_hexa_svm(self, center, color):
        '''
        Create a unique hexagon using the parameter define, return a unique svg hexagon
        
        :param self: our Hexagon with size and the image
        :param center: coordinates of the point we want to draw the hexagon around
        :param color: color we want to give at the hexagon
        '''
        x, y = center
        points = []

        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi/180 * angle_deg
            
            pt_x = x + self.size * math.cos(angle_rad)
            pt_y = y + self.size * math.sin(angle_rad)
            
            points.append(f"{pt_x:.2f} {pt_y:.2f}")
        
        str_points = ",".join(points)

        rgb = f"rgb({color[0]},{color[1]},{color[2]})"
        return f'<polygon points="{str_points}" fill="{rgb}" stroke="{rgb}" stroke-width="1"/>'

    def create_hexas(self):
        '''
        Create all the hexagons
        
        :param self: our Hexagon with size and the image
        '''
        hexagone_center = self.get_grid_points()
        colors = []
        for point in hexagone_center:
            colors.append(self.sample_color(point[0], point[1]))
        
        for color, hex_point in zip(colors, hexagone_center):
            self.hexagons.append(self.create_unique_hexa_svm(hex_point, color))

    def generate_img(self, output_file):
        '''
        Generate the hexagonal svg version of our original picture and create it.
        
        :param self: our Hexagon with size and the image
        :param output_file: path of the ouput file.
        '''
        with open(output_file, 'w') as f:
            header = f'<svg width="{self.img_width}" height="{self.img_height}">'
            f.write(header + '\n')
            
            for element in self.hexagons:
                f.write(f'  {element}\n')
                
            f.write('</svg>\n')