from os import path
from PIL import Image, ImageDraw, ImageFont, ImageOps


def shade_color(color, shade=0.85):
    return tuple(int(c * shade) for c in color)


def make_cube(
    image,
    x,
    y,
    edge_size=100,
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

    image_file = image + ".png"
    if path.isfile(image_file):
        img = Image.open(image_file)
    else:
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

    img.save(image_file, "PNG")


def get_letter_coords(letter, font="arial.ttf", size=15):
    img = Image.new("RGB", (size, size), color="white")
    draw = ImageDraw.Draw(img)
    font_obj = ImageFont.truetype(font, size)
    bbox = draw.textbbox((0, 0), letter, font=font_obj)  # Get bounding box
    letter_w, letter_h = (
        bbox[2] - bbox[0],
        bbox[3] - bbox[1],
    )  # Calculate width and height
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
    return sorted(letter_coords, key=lambda x: (-x[0], -x[1]))


def make_letter_logo(image_name, letter, font="arial.ttf", font_size=15):
    letter_coords = get_letter_coords(letter, font=font, size=font_size)
    letter_coords = [(100 * x, 100 * y) for (x, y) in letter_coords]
    max_w = max(letter_coords, key=lambda x: x[0])[0]
    max_h = max(letter_coords, key=lambda x: x[1])[1]
    min_w = min(letter_coords, key=lambda x: x[0])[0]
    min_h = min(letter_coords, key=lambda x: x[1])[1]
    max_d = max(max_w, max_h) + 100

    img_size = [max_d, max_d]
    img = Image.new("RGB", img_size, color="white")
    img.save(image_name + ".png", "PNG")

    for x, y in letter_coords:
        make_cube(image_name, x, y, color=(32, 190, 255), shaded=True)

    cropbox = (min_w - 100, min_h - 100, max_w + 100, max_h + 100)
    img = Image.open(image_name + ".png")
    img = img.crop(cropbox)
    img = img.convert("RGBA")

    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(image_name + ".png", "PNG")


make_letter_logo("kpi-logo", "k")
