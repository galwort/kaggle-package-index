from PIL import Image, ImageDraw

def make_cube(image, x, y, size=20, color=(255, 255, 255), outline=(0, 0, 0), shaded=False):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    
    cube_coords = [
        (x, y),                         # Middle
        (x, y - size * 4),              # Middle-bottom
        (x + size * 3, y - size * 3),   # Right-bottom
        (x + size * 3, y + size),       # Right-top
    ]

    draw.polygon(cube_coords[:4], fill=color, outline=outline) # Front face

    img.save('kpi-logo.png')

make_cube('kpi-logo.png', 100, 100)