from PIL import Image, ImageDraw

# Create a 256x256 image with a transparent background
img = Image.new('RGBA', (256, 256), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw an eye icon
# Draw eye outline (circle)
draw.ellipse((48, 78, 208, 178), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=4)

# Draw iris (circle)
draw.ellipse((88, 98, 168, 158), fill=(70, 130, 180, 255), outline=(0, 0, 0, 255), width=2)

# Draw pupil (circle)
draw.ellipse((108, 113, 148, 143), fill=(0, 0, 0, 255))

# Draw eye shine (small circle)
draw.ellipse((118, 118, 128, 128), fill=(255, 255, 255, 200))

# Draw mouse cursor
cursor_points = [(190, 190), (210, 210), (190, 210)]
draw.polygon(cursor_points, fill=(0, 0, 0, 255))

# Save the image as an icon
img.save('icon.ico', format='ICO', sizes=[(256, 256)])
