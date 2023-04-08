from PIL import Image, ImageDraw


def make_cube(
    image,
    x,
    y,
    size=20,
    color=(255, 255, 255),
    outline=(0, 0, 0),
    shaded=False,
    vertical_perspective=45,
):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)

    side = size * 4

    cube_coords = [
        (x, y),  # Middle
        (x + size * 3, y - size),  # Top-right
        (x + size * 3, y + size * 3),  # Bottom-right
        (x, y + side),  # Bottom-middle
    ]

    draw.polygon(cube_coords[:4], fill=color, outline=outline)  # Front face

    img.save("kpi-logo.png")


make_cube("kpi-logo.png", 200, 200)
