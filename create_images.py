#!/usr/bin/env python3
"""Script de création des images du jeu"""
from PIL import Image, ImageDraw, ImageFont
import os

# Créer dossier images
os.makedirs('kivy_app/data/images', exist_ok=True)

# Logo du jeu (512x512)
logo = Image.new('RGB', (512, 512), color=(30, 58, 138))
draw = ImageDraw.Draw(logo)

# Gradient bleu
for i in range(512):
    shade = int(138 + (100 * i / 512))
    draw.line([(0, i), (512, i)], fill=(30, 58, shade))

# Ajouter les emojis
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 150)
except:
    font = ImageFont.load_default()

draw.text((256, 200), "🎮", fill='white', font=font, anchor='mm')
draw.text((256, 320), "🧠", fill='white', font=font, anchor='mm')

logo.save('kivy_app/data/images/logo.png')
print("✓ Logo 512x512 créé")

# Favicons
for size in [64, 32, 16]:
    favicon = Image.new('RGB', (size, size), color=(30, 58, 138))
    draw = ImageDraw.Draw(favicon)
    
    # Gradient
    for i in range(size):
        shade = int(138 + (100 * i / size))
        draw.line([(0, i), (size, i)], fill=(30, 58, shade))
    
    # Emoji
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", int(size * 0.6))
    except:
        f = ImageFont.load_default()
    
    draw.text((size//2, size//2), "🧠", fill='white', font=f, anchor='mm')
    favicon.save(f'kivy_app/data/images/favicon_{size}x{size}.png')
    print(f"✓ Favicon {size}x{size} créé")

print("\n✅ Tous les fichiers image sont prêts!")
