from PIL import ImageDraw

def make_cube(image, x, y, size=20, color=(255, 255, 255), outline=(0, 0, 0), shaded=False):
    draw = ImageDraw.Draw(image)
    
    cube_coords = [
        (x, y),                        # Front-left
        (x + size, y),                 # Front-right
        (x + size * 2, y),             # Back-right
        (x + size, y - size),          # Top
        (x, y - size),                 # Left-top
        (x + size * 2, y - size),      # Right-top
        (x + size * 2, y - size * 2),  # Back-right-top
        (x + size, y - size * 2),      # Back-left-top
        (x, y - size * 2),             # Left-top
    ]

    draw.polygon(cube_coords[:4], fill=color, outline=outline) # Front face
    draw.polygon(cube_coords[3:5] + cube_coords[7:9], fill=color) # Top face
    draw.polygon(cube_coords[1:3] + cube_coords[5:7], fill=color) # Right face
    draw.line(cube_coords[0:2], fill=outline, width=1) # Front-left edge
    draw.line(cube_coords[1:3], fill=outline, width=1) # Front-right edge
    draw.line(cube_coords[2:4], fill=outline, width=1) # Top edge
    draw.line(cube_coords[0:2] + cube_coords[4:6], fill=outline, width=1)  # Left edge
    draw.line(cube_coords[3:5] + cube_coords[7:9], fill=outline, width=1)  # Back edge
    draw.line(cube_coords[4:6] + cube_coords[8:9] + cube_coords[0:1], fill=outline, width=1) # Bottom edge

    image.save('kpi-logo.png') 