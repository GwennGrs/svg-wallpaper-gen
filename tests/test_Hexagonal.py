import pytest
import os
from PIL import Image
from svg_wallpaper_gen.Hexagonal import Hexagonal

@pytest.fixture
def red_gen():
    path = "img/test.jpg"
    img = Image.new('RGB', (100, 100), color='red')
    img.save(path)
    red_gen = Hexagonal(path, size=15)
    yield red_gen

    if os.path.exists(path):
        os.remove(path)


def test_init(red_gen):
    assert red_gen.img_width == 100
    assert red_gen.img_height == 100
    assert red_gen.size == 15

def test_grid_points(red_gen):
    points = red_gen.get_grid_points()
    assert len(points) > 0
    x, y = points[0]
    assert -10 < x < 110 
    assert -10 < y < 110

def test_sample_color(red_gen):
    assert red_gen.sample_color(50, 50) == (254, 0, 0)
    assert red_gen.sample_color(500, 500) == (0, 0, 0)

def test_create_svg_string(red_gen):
    svg_line = red_gen.create_unique_hexa_svm((10, 20), (255, 0, 0))
    assert '<polygon' in svg_line
    assert 'fill="rgb(255,0,0)"' in svg_line
    assert 'points="' in svg_line

def test_generate_full_img(red_gen, tmp_path):
    output_path = str(tmp_path) + "/test_result.svg"
    red_gen.create_hexas()
    red_gen.generate_img(output_path)
    
    with open(output_path, "r") as f:
        content = f.read()
        assert "polygon" in content
    os.remove(output_path)