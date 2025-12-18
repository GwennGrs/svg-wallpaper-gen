from PIL import Image
import math
import sys
import os

def load_image(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
        
    return img


def get_hexagone_grid_centers(img_width, img_height, size):
    """
    Generate the center of each hexagone of our picture.
    Using : point-top paradigm
    """

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
            if 0 <= x < img_width and 0 <= y < img_height:
                yield (x, y)

if __name__ == "__main__":

    INPUT_FILE = "img/screenshot.jpg" 
    image = load_image(INPUT_FILE)

    count = 0
    for x, y in get_hexagone_grid_centers(image.width, image.height, 20):
        count += 1
        
    print("Nombre d'hexagone", count)