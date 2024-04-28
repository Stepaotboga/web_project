from PIL import Image, ImageDraw, ImageFont


scale = 20
step = 1
im = Image.new('RGB', (604, 600), (255, 255, 255))
draw = ImageDraw.Draw(im)

for i in range(scale):
    draw.line((i * (600 / scale), 0, i * (600 / scale), 600), fill='#f0f0f0')
    draw.line((0, i * (600 / scale), 600, i * (600 / scale)), fill='#f0f0f0')
for i in range(scale):
    if i != 0 and i != scale / 2 and scale in range(40):
        font = ImageFont.truetype("arial.ttf", 15)
        draw.text((i * (600 / scale) - 10, 300), f'{i - scale // 2}', fill='#000000', font=font)
        draw.text((304, i * (600 / scale) - 10), f'{-i + scale // 2}', fill='#000000', font=font)
draw.text((290, 284), '0', fill='#000000', font=font)
draw.line((300, 0, 300, 600), fill='#000000', width=3)
draw.line((0, 300, 600, 300), fill='#000000', width=3)
font = ImageFont.truetype("arial.ttf", 20)
draw.text((590, 305), 'x', fill='#000000', font=font)
draw.text((285, 5), 'y', fill='#000000', font=font)
font = ImageFont.truetype("bahnschrift.ttf", 38)
draw.rectangle((600, 0, 900, 600), fill='#f5f5f5')
draw.text((590, 282), '>', fill='#000000', font=font)
draw.text((291, -4), '^', fill='#000000', font=font)

im.save('static/img/origin.png')