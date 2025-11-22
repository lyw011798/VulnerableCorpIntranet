from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(filename, text, color):
    img = Image.new('RGB', (800, 400), color=color)
    d = ImageDraw.Draw(img)
    # simple text centering (approximate)
    d.text((350, 180), text, fill=(255, 255, 255))
    img.save(filename)

os.makedirs('app/static/img', exist_ok=True)
create_placeholder('app/static/img/employee.jpg', 'Employee Dashboard', (100, 149, 237)) # CornflowerBlue
create_placeholder('app/static/img/admin_secret.jpg', 'TOP SECRET ADMIN', (139, 0, 0)) # DarkRed
print("Placeholders created.")
