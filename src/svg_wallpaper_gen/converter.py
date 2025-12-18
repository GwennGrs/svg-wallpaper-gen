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

    num_cols = int(img_width / horizontal_spacing) + 1
    num_rows = int(img_height / vertical_spacing) + 1
    
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * horizontal_spacing
            y = row * vertical_spacing
            if row % 2 == 1:
                x += hexa_witdh / 2 
            if ((0 <= x) and (x < img_width)) and ((0 <= y) and ( y < img_height)):
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

if __name__ == "__main__":

    INPUT_FILE = "img/screenshot.jpg" 
    image = load_image(INPUT_FILE)

    count = 0
    points = get_grid_points(image.width, image.height, 10)
    for point in points:
        count += 1
        
    print("Nombre d'hexagone", count)
    
    sample_col_first = sample_color(image, points[0][0], points[0][1], 2)
    print(sample_col_first)
