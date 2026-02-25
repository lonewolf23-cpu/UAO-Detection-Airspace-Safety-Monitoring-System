from PIL import Image, ImageDraw
import os

def generate_icons():

    if not os.path.exists("assets"):
        os.makedirs("assets")

    # Aircraft Icon
    img = Image.new("RGBA", (60,60), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(30,0),(45,45),(30,35),(15,45)], fill="blue")
    img.save("assets/aircraft.png")

    # Drone Icon
    img = Image.new("RGBA", (60,60), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((10,10,50,50), outline="red", width=3)
    draw.line((0,30,60,30), fill="red", width=3)
    draw.line((30,0,30,60), fill="red", width=3)
    img.save("assets/drone.png")

    # Bird Icon
    img = Image.new("RGBA", (60,60), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(0,30),(30,10),(60,30),(30,50)], fill="green")
    img.save("assets/bird.png")

    # Unknown Icon
    img = Image.new("RGBA", (60,60), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.text((20,20),"?", fill="black")
    img.save("assets/unknown.png")

generate_icons()
