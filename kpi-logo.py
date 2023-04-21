from PIL import Image, ImageDraw, ImageFont, ImageOps


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

    img_size = (edge_size * 3, edge_size * 3)
    img = Image.new("RGB", img_size, color="white")
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
        cube_coords[0:2] + cube_coords[6:7] + cube_coords[5:6],
        fill=color,
        outline=outline,
    )  # Top face

    img.save(image + ".png", "PNG")


def get_letter_coords(letter, font="arial.ttf", size=20):
    img = Image.new("RGB", (size, size), color="white")
    draw = ImageDraw.Draw(img)
    font_obj = ImageFont.truetype(font, size)
    bbox = draw.textbbox((0, 0), letter, font=font_obj)  # Get bounding box
    letter_w, letter_h = bbox[2] - bbox[0], bbox[3] - bbox[1]  # Calculate width and height
    x = (size - letter_w) // 2
    y = (size - letter_h) // 2
    draw.text((x, y), letter, font=font_obj, fill="black")

    grayscale_img = ImageOps.grayscale(img)
    img = grayscale_img.point(lambda x: 0 if x < 128 else 255, "1")

    letter_coords = []
    pixels = img.getdata()
    for i, pixel in enumerate(pixels):
        if pixel == 0:
            x = i % img.width
            y = i // img.width
            letter_coords.append((x, y))
    return sorted(letter_coords, key=lambda x: (x[0], x[1]))

def make_letter_logo(image_name, letter, font="arial.ttf", font_size=20):
    list = get_letter_coords(letter, font=font, size=font_size)
    max_w = max(list, key=lambda x: x[0])[0]
    max_h = max(list, key=lambda x: x[1])[1]
    max_d = max(max_w, max_h) + 20

    img_size = (max_d, max_d)
    img = Image.new("RGB", img_size, color="white")
    draw = ImageDraw.Draw(img)

    img.save(image_name + ".png", "PNG")

make_letter_logo("kpi-logo.py", "i")