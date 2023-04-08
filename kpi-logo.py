from PIL import Image, ImageDraw
from math import cos, radians


def shade_color(color, shade=0.85):
    return tuple(int(c * shade) for c in color)


def make_cube(
    image,
    x,
    y,
    edge_size=20,
    color=(255, 255, 255),
    outline=(0, 0, 0),
    shaded=False,
    vertical_perspective=0,
):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)

    rad_vp = radians(vertical_perspective)
    scaling = cos(rad_vp)

    cube_coords = [
        (x, y),  # Middle
        (x + edge_size, y),  # Top-right
        (x + edge_size, y + edge_size),  # Bottom-right
        (x, y + edge_size),  # Bottom-middle
    ]

    draw.polygon(cube_coords[:4], fill=color, outline=outline)  # Front face

    # img.save("kpi-logo.png")


make_cube("kpi-logo.png", 200, 200)
