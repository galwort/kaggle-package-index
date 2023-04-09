from PIL import Image, ImageDraw


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
    vertical_perspective=45,
):
    if vertical_perspective < 0:
        vertical_perspective = 0
    elif vertical_perspective > 90:
        vertical_perspective = 90
    vc = vertical_perspective / 90

    img = Image.open(image)
    img = Image.new("RGB", img.size, color="white")
    draw = ImageDraw.Draw(img)

    cube_coords = [
        (x, y),  # Middle
        (x + edge_size, y - vc * edge_size),  # Top-right
        (x + edge_size, y + edge_size - vc * edge_size),  # Bottom-right
        (x, y + edge_size),  # Bottom-middle
        (x - edge_size, y + edge_size - vc * edge_size),  # Bottom-left
        (x - edge_size, y - vc * edge_size),  # Top-left
        (x, y - 2 * vc * edge_size),  # Top-middle
    ]

    draw.polygon(cube_coords[:4], fill=color, outline=outline)  # Front face
    color = shade_color(color) if shaded else color
    draw.polygon(
        cube_coords[0:1] + cube_coords[3:6], fill=color, outline=outline
    )  # Side face
    draw.polygon(
        cube_coords[0:2] + cube_coords[6:7] + cube_coords[5:6], fill=color, outline=outline
    )  # Top face

    img.save("kpi-logo.png")


make_cube("kpi-logo.png", 200, 200, 100, (32, 190, 255), shaded=True)
