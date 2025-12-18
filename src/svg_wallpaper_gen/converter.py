from PIL import Image
import math
import sys
import os

def load_image(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
        
    return img


def get_grid_points(img_width, img_height, size):
    """
    Generate the center of each hexagone of our picture.
    Using : point-top paradigm
    """

    points = []
    hexa_witdh = math.sqrt(3) * size
    hexa_height = 2 * size
    
    # Spacing according to point-top 
    horizontal_spacing = hexa_witdh
    vertical_spacing = hexa_height * 0.75 

    num_cols = int(img_width / horizontal_spacing) + 5
    num_rows = int(img_height / vertical_spacing) + 5
    
    half_w = hexa_witdh / 2
    half_h = hexa_height / 2

    for row in range(num_rows):
        for col in range(num_cols):
            x = col * horizontal_spacing
            y = row * vertical_spacing
            if row % 2 == 1:
                x += hexa_witdh / 2 
            if (x - half_w < img_width) and (x + half_w > 0) and (y - half_h < img_height) and (y + half_h > 0):
                points.append((x, y))
    return points

def sample_color(img, x_center, y_center, size):
    radius = int(size / 2) 

    x_start = max(0, int(x_center - radius))
    x_end = min(img.width, int(x_center + radius))
    y_start = max(0, int(y_center - radius))
    y_end = min(img.height, int(y_center + radius))

    array_r = [] 
    array_g = []
    array_b = [] 
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            pixel = img.getpixel((x, y))
            array_r.append(pixel[0])
            array_g.append(pixel[1])
            array_b.append(pixel[2])

    total_pix = len(array_b)
    if total_pix > 0:
        return ( (sum(array_r)) // total_pix, (sum(array_g)) // total_pix, (sum(array_b)) // total_pix )
    else:
        return (0, 0, 0)

def create_hexa_svm(center, size, color):
    x, y = center
    points = []

    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi/180 * angle_deg
        
        pt_x = x + size * math.cos(angle_rad)
        pt_y = y + size * math.sin(angle_rad)
        
        points.append(f"{pt_x:.2f} {pt_y:.2f}")
    
    str_points = ",".join(points)

    rgb = f"rgb({color[0]},{color[1]},{color[2]})"
    return f'<polygon points="{str_points}" fill="{rgb}" stroke="{rgb}" stroke-width="1"/>'

def generate_img(output_path, image, hexagones):
    with open(output_path, 'w') as f:
        header = f'<svg width="{image.width}" height="{image.height}">'
        f.write(header + '\n')
        
        for element in hexagones:
            f.write(f'  {element}\n')
            
        f.write('</svg>\n')

if __name__ == "__main__":

    INPUT_FILE = "img/screenshot.jpg" 
    OUTPUT_FILE = "img/file.svg"
    image = load_image(INPUT_FILE)
    
    SIZE = 10

    hexagone_center = get_grid_points(image.width, image.height, SIZE)
    colors = []
    for point in hexagone_center:
        colors.append(sample_color(image, point[0], point[1], SIZE))
    
    hexagones = []
    for color, hex_point in zip(colors, hexagone_center):
        hexagones.append(create_hexa_svm(hex_point, SIZE, color))

    generate_img(OUTPUT_FILE, image, hexagones)