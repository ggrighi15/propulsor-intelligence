from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Criar imagem branca
img = Image.new("RGB", (800, 400), color=(255, 255, 255))
d = ImageDraw.Draw(img)

# Texto principal
title = "Propulsor Intelligence"
subtitle = "Upload automático gerado por GitHub Actions"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Tenta carregar 'arial.ttf' e recorre à fonte padrão se indisponível
try:
    font_title = ImageFont.truetype("arial.ttf", 32)
    font_sub = ImageFont.truetype("arial.ttf", 20)
except:
    font_title = font_sub = None

d.text((50, 50), title, fill=(0, 0, 0), font=font_title)
d.text((50, 120), subtitle, fill=(0, 0, 0), font=font_sub)
d.text((50, 180), f"Gerado em: {timestamp}", fill=(0, 0, 0), font=font_sub)

# Salvar imagem
img.save("output_card.png")
print("✅ Imagem gerada: output_card.png")
