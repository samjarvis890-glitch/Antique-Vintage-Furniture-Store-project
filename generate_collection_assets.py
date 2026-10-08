import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

# Ensure directories exist
os.makedirs('assets/images/collection', exist_ok=True)
os.makedirs('assets/images/collection/products', exist_ok=True)

def add_film_grain(img, intensity=12):
    w, h = img.size
    grain = Image.new('RGB', (w, h))
    pixels = grain.load()
    for y in range(h):
        for x in range(0, w, 2):
            val = 128 + random.randint(-intensity, intensity)
            pixels[x, y] = (val, val, val)
            if x + 1 < w:
                pixels[x + 1, y] = (val, val, val)
    
    # Blend grain subtly
    from PIL import ImageChops
    return ImageChops.soft_light(img, grain)

def create_rich_editorial_scene(w, h, scene_type='hero', seed=101):
    random.seed(seed)
    # Warm editorial palette
    # Wall colors
    wall_top = (245, 239, 228)    # Cream
    wall_mid = (235, 225, 210)    # Warm Stone
    wall_bot = (220, 208, 190)    # Soft Taupe
    
    # Floor colors
    floor_far = (75, 52, 40)      # Deep Aged Oak
    floor_near = (50, 34, 25)     # Deep Walnut
    floor_line = (38, 25, 18)
    
    # Wood accents
    wood_main = (68, 46, 34)
    wood_dark = (42, 28, 20)
    wood_light = (112, 80, 58)
    brass = (176, 138, 87)
    brass_bright = (212, 175, 120)
    linen = (238, 230, 215)
    
    img = Image.new('RGB', (w, h), wall_top)
    draw = ImageDraw.Draw(img)
    
    # 1. Architectural Wall Rendering
    wall_h = int(h * 0.72)
    for y in range(wall_h):
        f = y / wall_h
        r = int(wall_top[0] * (1 - f) + wall_mid[0] * f)
        g = int(wall_top[1] * (1 - f) + wall_mid[1] * f)
        b = int(wall_top[2] * (1 - f) + wall_mid[2] * f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Moulding & Wainscoting
    mould_y = int(h * 0.52)
    draw.rectangle([0, mould_y, w, mould_y + 8], fill=(210, 198, 180))
    draw.line([(0, mould_y), (w, mould_y)], fill=(250, 245, 238), width=1)
    draw.line([(0, mould_y + 8), (w, mould_y + 8)], fill=(160, 145, 130), width=2)
    
    # Classical Wall Panels
    panel_gap = int(w * 0.04)
    panel_w = int(w * 0.24)
    for px in range(int(w * 0.05), int(w * 0.95), panel_w + panel_gap):
        # Upper panel
        draw.rectangle([px, int(h * 0.1), px + panel_w, mould_y - 25], outline=(205, 192, 175), width=2)
        draw.rectangle([px + 6, int(h * 0.1) + 6, px + panel_w - 6, mould_y - 31], outline=(250, 246, 238), width=1)
        # Lower panel
        draw.rectangle([px, mould_y + 20, px + panel_w, wall_h - 20], outline=(195, 180, 165), width=2)
        
    # Skirting
    draw.rectangle([0, wall_h - 18, w, wall_h], fill=(190, 175, 160))
    draw.line([(0, wall_h - 18), (w, wall_h - 18)], fill=(240, 230, 218), width=2)
    
    # 2. Floor with Parquet / Chevron Timber Planks
    floor_h = h - wall_h
    for y in range(wall_h, h):
        f = (y - wall_h) / floor_h
        r = int(floor_far[0] * (1 - f) + floor_near[0] * f)
        g = int(floor_far[1] * (1 - f) + floor_near[1] * f)
        b = int(floor_far[2] * (1 - f) + floor_near[2] * f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Perspective Floor Lines
    num_planks = 18
    for i in range(-5, num_planks + 6):
        x1 = int(w * 0.5 + i * (w * 0.07))
        x2 = int(w * 0.5 + (i * 2.3) * (w * 0.07))
        draw.line([(x1, wall_h), (x2, h)], fill=floor_line, width=1)
        
    # 3. Soft Window Daylight Gradient
    light_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(light_layer)
    ldraw.polygon([
        (0, 0),
        (int(w * 0.48), 0),
        (int(w * 0.82), h),
        (int(w * 0.12), h)
    ], fill=(255, 250, 238, 42))
    
    # Furniture Drop Shadow
    ldraw.ellipse([int(w * 0.18), int(wall_h - 8), int(w * 0.82), int(wall_h + floor_h * 0.7)], fill=(18, 12, 9, 135))
    img.paste(Image.alpha_composite(img.convert('RGBA'), light_layer).convert('RGB'))
    
    # 4. Draw Specific Furniture Configurations
    fdraw = ImageDraw.Draw(img)
    
    if scene_type == 'hero':
        # Majestic Restored French / Georgian Sideboard with Tall Gilt Mirror Frame
        cx = int(w * 0.5)
        sb_w = int(w * 0.58)
        sb_h = int(h * 0.28)
        sb_y = int(wall_h - sb_h + h * 0.04)
        
        # Arch Antique Mirror above
        mir_w = int(w * 0.28)
        mir_h = int(h * 0.36)
        mir_x = cx - mir_w // 2
        mir_y = sb_y - mir_h - 15
        fdraw.rectangle([mir_x, mir_y, mir_x + mir_w, mir_y + mir_h], fill=(215, 222, 226), outline=brass, width=6)
        fdraw.rectangle([mir_x + 6, mir_y + 6, mir_x + mir_w - 6, mir_y + mir_h - 6], outline=brass_bright, width=2)
        # Mirror subtle reflection highlight
        fdraw.polygon([(mir_x + 10, mir_y + 10), (mir_x + int(mir_w*0.6), mir_y + 10), (mir_x + int(mir_w*0.2), mir_y + mir_h - 10), (mir_x + 10, mir_y + mir_h - 10)], fill=(235, 240, 245, 80))
        
        # Sideboard Main Body
        fdraw.rectangle([cx - sb_w//2, sb_y, cx + sb_w//2, sb_y + sb_h], fill=wood_dark)
        # Marble or Walnut Top Plinth
        fdraw.rectangle([cx - sb_w//2 - 12, sb_y - 12, cx + sb_w//2 + 12, sb_y], fill=(225, 218, 205), outline=(180, 170, 155), width=2)
        
        # Door panels with carved mouldings
        panel_count = 3
        pw = (sb_w - 40) // panel_count
        for pi in range(panel_count):
            px1 = cx - sb_w//2 + 15 + pi * (pw + 6)
            px2 = px1 + pw
            py1 = sb_y + 14
            py2 = sb_y + sb_h - 18
            fdraw.rectangle([px1, py1, px2, py2], fill=wood_main, outline=wood_light, width=2)
            fdraw.rectangle([px1 + 8, py1 + 8, px2 - 8, py2 - 8], outline=wood_dark, width=1)
            # Antique brass keyholes / pulls
            k_x = px1 + pw // 2
            k_y = py1 + (py2 - py1) // 2
            fdraw.ellipse([k_x - 5, k_y - 10, k_x + 5, k_y + 10], fill=brass)
            fdraw.arc([k_x - 6, k_y, k_x + 6, k_y + 12], 0, 180, fill=brass_bright, width=2)
            
        # Heavy turned feet
        for fx in [cx - sb_w//2 + 25, cx - sb_w//4, cx + sb_w//4, cx + sb_w//2 - 25]:
            fdraw.ellipse([fx - 14, sb_y + sb_h - 4, fx + 14, sb_y + sb_h + 16], fill=wood_dark)
            fdraw.ellipse([fx - 10, sb_y + sb_h + 8, fx + 10, sb_y + sb_h + 16], fill=brass)
            
        # Ceramic Urn & Botanical sprig on top
        ux = cx - int(sb_w * 0.3)
        uy = sb_y - 65
        fdraw.ellipse([ux - 18, uy + 20, ux + 18, uy + 55], fill=(230, 222, 208))
        fdraw.polygon([(ux - 10, uy + 25), (ux + 10, uy + 25), (ux + 6, uy), (ux - 6, uy)], fill=(240, 235, 220))
        
    elif scene_type == 'scale':
        # 4 distinct scales of furniture: S (Stool/Side Table), M (Chair/Desk), L (Cabinet), XL (Large Armoire)
        positions = [
            {'x': int(w * 0.16), 'label': 'S', 'type': 'stool'},
            {'x': int(w * 0.38), 'label': 'M', 'type': 'chair'},
            {'x': int(w * 0.62), 'label': 'L', 'type': 'credenza'},
            {'x': int(w * 0.86), 'label': 'XL', 'type': 'armoire'}
        ]
        
        # Small Stool / Pedestal
        sx = positions[0]['x']
        fdraw.rectangle([sx - 35, wall_h - 75, sx + 35, wall_h - 65], fill=wood_main)
        fdraw.polygon([(sx - 30, wall_h - 65), (sx - 38, wall_h + 15), (sx - 28, wall_h + 15), (sx - 20, wall_h - 65)], fill=wood_dark)
        fdraw.polygon([(sx + 30, wall_h - 65), (sx + 38, wall_h + 15), (sx + 28, wall_h + 15), (sx + 20, wall_h - 65)], fill=wood_dark)
        fdraw.line([(sx - 38, wall_h + 10), (sx + 38, wall_h + 10)], fill=brass, width=2)
        
        # Medium Carver Chair
        mx = positions[1]['x']
        # Backrest
        fdraw.rectangle([mx - 42, wall_h - 165, mx + 42, wall_h - 75], fill=wood_dark, outline=wood_light, width=2)
        fdraw.rectangle([mx - 32, wall_h - 155, mx + 32, wall_h - 85], fill=linen)
        # Seat
        fdraw.rectangle([mx - 48, wall_h - 75, mx + 48, wall_h - 55], fill=linen, outline=wood_main, width=2)
        # Legs
        fdraw.polygon([(mx - 44, wall_h - 55), (mx - 46, wall_h + 25), (mx - 38, wall_h + 25), (mx - 36, wall_h - 55)], fill=wood_dark)
        fdraw.polygon([(mx + 44, wall_h - 55), (mx + 46, wall_h + 25), (mx + 38, wall_h + 25), (mx + 36, wall_h - 55)], fill=wood_dark)
        
        # Large Credenza / Chest
        lx = positions[2]['x']
        fdraw.rectangle([lx - 90, wall_h - 140, lx + 90, wall_h + 10], fill=wood_dark, outline=wood_light, width=2)
        for di in range(3):
            dy = wall_h - 130 + di * 42
            fdraw.rectangle([lx - 80, dy, lx + 80, dy + 34], fill=wood_main, outline=wood_dark, width=1)
            fdraw.ellipse([lx - 45, dy + 14, lx - 35, dy + 22], fill=brass)
            fdraw.ellipse([lx + 35, dy + 14, lx + 45, dy + 22], fill=brass)
            
        # Room-Scale Tall Armoire
        xlx = positions[3]['x']
        fdraw.rectangle([xlx - 75, wall_h - 260, xlx + 75, wall_h + 15], fill=wood_dark, outline=wood_light, width=2)
        # Cornice
        fdraw.polygon([(xlx - 85, wall_h - 260), (xlx + 85, wall_h - 260), (xlx + 75, wall_h - 245), (xlx - 75, wall_h - 245)], fill=wood_main)
        # Double doors
        fdraw.rectangle([xlx - 68, wall_h - 240, xlx - 4, wall_h], fill=wood_main, outline=wood_dark, width=2)
        fdraw.rectangle([xlx + 4, wall_h - 240, xlx + 68, wall_h], fill=wood_main, outline=wood_dark, width=2)
        fdraw.ellipse([xlx - 12, wall_h - 130, xlx - 4, wall_h - 110], fill=brass)
        fdraw.ellipse([xlx + 4, wall_h - 130, xlx + 12, wall_h - 110], fill=brass)
        
    elif scene_type == 'category':
        # Refined catalogue arrangement with Chair, Table, Bookcase and Floor Lamp
        cx = int(w * 0.5)
        # Mid-Century Bookcase on Left
        fdraw.rectangle([int(w * 0.12), wall_h - 210, int(w * 0.36), wall_h + 10], fill=wood_dark, outline=wood_light, width=2)
        for sy in range(wall_h - 180, wall_h, 45):
            fdraw.line([(int(w * 0.12), sy), (int(w * 0.36), sy)], fill=wood_main, width=3)
            # Books and ceramics
            fdraw.rectangle([int(w * 0.15), sy - 28, int(w * 0.22), sy], fill=(185, 140, 110))
            fdraw.rectangle([int(w * 0.23), sy - 24, int(w * 0.29), sy], fill=(130, 145, 125))
            fdraw.ellipse([int(w * 0.31), sy - 22, int(w * 0.34), sy], fill=(225, 215, 195))
            
        # Central Oval Table
        fdraw.ellipse([cx - 85, wall_h - 70, cx + 85, wall_h - 40], fill=wood_main, outline=wood_light, width=2)
        fdraw.polygon([(cx - 10, wall_h - 45), (cx + 10, wall_h - 45), (cx + 35, wall_h + 20), (cx - 35, wall_h + 20)], fill=wood_dark)
        
        # Occasional Bergère Chair on Right
        rx = int(w * 0.75)
        fdraw.rectangle([rx - 55, wall_h - 140, rx + 55, wall_h - 50], fill=linen, outline=wood_dark, width=3)
        fdraw.rectangle([rx - 65, wall_h - 50, rx + 65, wall_h - 25], fill=linen, outline=wood_dark, width=2)
        # Tapered Legs
        fdraw.polygon([(rx - 55, wall_h - 25), (rx - 58, wall_h + 22), (rx - 48, wall_h + 22), (rx - 45, wall_h - 25)], fill=wood_dark)
        fdraw.polygon([(rx + 55, wall_h - 25), (rx + 58, wall_h + 22), (rx + 48, wall_h + 22), (rx + 45, wall_h - 25)], fill=wood_dark)
        
    elif scene_type == 'era':
        # Chronological showcase: Classical Georgian, Victorian Fluting, Art Deco Geometry, Mid-Century Taper
        cx = int(w * 0.5)
        # Architectural Vignette with 3 Period silhouettes
        # 1. Art Deco Geometric Credenza in Centre
        fdraw.rectangle([cx - 110, wall_h - 120, cx + 110, wall_h + 10], fill=wood_dark)
        # Parquetry sunburst pattern
        fdraw.polygon([(cx - 100, wall_h - 110), (cx, wall_h - 110), (cx, wall_h), (cx - 100, wall_h)], fill=(85, 55, 38))
        fdraw.polygon([(cx, wall_h - 110), (cx + 100, wall_h - 110), (cx + 100, wall_h), (cx, wall_h)], fill=(105, 72, 48))
        fdraw.line([(cx, wall_h - 110), (cx, wall_h)], fill=brass, width=3)
        # Sled Brass Base
        fdraw.rectangle([cx - 95, wall_h + 8, cx + 95, wall_h + 16], fill=brass)
        
        # 2. Victorian Pedestal Urn Stand Left
        vx = int(w * 0.2)
        fdraw.rectangle([vx - 28, wall_h - 150, vx + 28, wall_h - 138], fill=wood_main)
        fdraw.polygon([(vx - 14, wall_h - 138), (vx + 14, wall_h - 138), (vx + 18, wall_h + 15), (vx - 18, wall_h + 15)], fill=wood_dark)
        fdraw.ellipse([vx - 22, wall_h + 10, vx + 22, wall_h + 22], fill=brass)
        
        # 3. Mid-Century Sculptural Chair Right
        mx = int(w * 0.8)
        fdraw.ellipse([mx - 48, wall_h - 110, mx + 48, wall_h - 40], fill=(195, 180, 160), outline=wood_dark, width=2)
        fdraw.polygon([(mx - 38, wall_h - 40), (mx - 52, wall_h + 25), (mx - 42, wall_h + 25), (mx - 28, wall_h - 40)], fill=wood_dark)
        fdraw.polygon([(mx + 38, wall_h - 40), (mx + 52, wall_h + 25), (mx + 42, wall_h + 25), (mx + 28, wall_h - 40)], fill=wood_dark)
        
    elif scene_type.startswith('between'):
        idx = int(scene_type[-1])
        cx = int(w * 0.5)
        if idx == 1:
            # Unusual Architectural Canterbury / Magazine Folio Stand
            fdraw.rectangle([cx - 70, wall_h - 95, cx + 70, wall_h - 15], fill=wood_dark, outline=wood_light, width=2)
            for div in [-35, 0, 35]:
                fdraw.polygon([(cx + div - 4, wall_h - 135), (cx + div + 4, wall_h - 135), (cx + div + 4, wall_h - 15), (cx + div - 4, wall_h - 15)], fill=wood_main)
            fdraw.ellipse([cx - 45, wall_h + 5, cx - 35, wall_h + 20], fill=brass)
            fdraw.ellipse([cx + 35, wall_h + 5, cx + 45, wall_h + 20], fill=brass)
        elif idx == 2:
            # Architectural Apothecary / Specimen Cabinet with 16 tiny drawers
            fdraw.rectangle([cx - 85, wall_h - 150, cx + 85, wall_h], fill=wood_dark, outline=wood_light, width=2)
            rows, cols = 4, 4
            rw = 160 // cols
            rh = 140 // rows
            for r in range(rows):
                for c in range(cols):
                    dx = cx - 80 + c * rw
                    dy = wall_h - 145 + r * rh
                    fdraw.rectangle([dx + 2, dy + 2, dx + rw - 2, dy + rh - 2], fill=wood_main, outline=wood_dark, width=1)
                    fdraw.ellipse([dx + rw//2 - 3, dy + rh//2 - 3, dx + rw//2 + 3, dy + rh//2 + 3], fill=brass)
            # Tapered bracket feet
            fdraw.polygon([(cx - 85, wall_h), (cx - 75, wall_h + 16), (cx - 50, wall_h + 16), (cx - 50, wall_h)], fill=wood_dark)
            fdraw.polygon([(cx + 85, wall_h), (cx + 75, wall_h + 16), (cx + 50, wall_h + 16), (cx + 50, wall_h)], fill=wood_dark)
        else:
            # Hybrid Campaign Chest with Brass Strap Corners
            fdraw.rectangle([cx - 95, wall_h - 110, cx + 95, wall_h], fill=wood_dark, outline=wood_light, width=2)
            # Brass strapping
            for bx in [cx - 95, cx + 80]:
                for by in [wall_h - 110, wall_h - 15]:
                    fdraw.rectangle([bx, by, bx + 15, by + 15], fill=brass)
            fdraw.line([(cx - 95, wall_h - 55), (cx + 95, wall_h - 55)], fill=brass, width=2)
            # Flush campaign handles
            fdraw.rectangle([cx - 35, wall_h - 85, cx + 35, wall_h - 75], fill=brass)
            fdraw.rectangle([cx - 35, wall_h - 35, cx + 35, wall_h - 25], fill=brass)
            
    elif scene_type == 'closing':
        # Quiet Evening Atmosphere - Warm light from right, single elegant writing bureau in shadows
        # Adjust light for evening mood
        cx = int(w * 0.5)
        fdraw.rectangle([cx - 75, wall_h - 125, cx + 75, wall_h + 10], fill=wood_dark, outline=wood_light, width=2)
        # Slanted bureau desk top
        fdraw.polygon([(cx - 75, wall_h - 85), (cx - 55, wall_h - 135), (cx + 55, wall_h - 135), (cx + 75, wall_h - 85)], fill=wood_main)
        # Brass keyhole
        fdraw.ellipse([cx - 4, wall_h - 92, cx + 4, wall_h - 80], fill=brass_bright)
        # Slender cabriole legs
        fdraw.polygon([(cx - 72, wall_h + 10), (cx - 65, wall_h + 35), (cx - 55, wall_h + 35), (cx - 62, wall_h + 10)], fill=wood_dark)
        fdraw.polygon([(cx + 72, wall_h + 10), (cx + 65, wall_h + 35), (cx + 55, wall_h + 35), (cx + 62, wall_h + 10)], fill=wood_dark)
        # Single glowing candleholder on desk
        fdraw.polygon([(cx + 35, wall_h - 135), (cx + 45, wall_h - 135), (cx + 42, wall_h - 155), (cx + 38, wall_h - 155)], fill=brass_bright)
        fdraw.ellipse([cx + 37, wall_h - 168, cx + 43, wall_h - 158], fill=(255, 220, 140))

    # Apply artistic finishing (softness, grain, color curve)
    img = img.filter(ImageFilter.SMOOTH)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = add_film_grain(img, intensity=10)
    return img

def create_product_shot(w, h, ptype, seed):
    random.seed(seed)
    # Neutral gallery studio setting: warm ivory backdrop
    bg_top = (250, 246, 238)
    bg_bot = (236, 228, 216)
    floor_far = (80, 58, 44)
    floor_near = (55, 38, 28)
    
    wood_main = (72, 48, 35)
    wood_dark = (45, 30, 22)
    wood_light = (118, 85, 62)
    brass = (176, 138, 87)
    brass_bright = (215, 178, 122)
    linen = (235, 225, 208)
    boucle = (244, 238, 226)
    velvet = (92, 54, 46)
    
    img = Image.new('RGB', (w, h), bg_top)
    draw = ImageDraw.Draw(img)
    
    # Backdrop gradient
    wall_h = int(h * 0.72)
    for y in range(wall_h):
        f = y / wall_h
        r = int(bg_top[0] * (1 - f) + bg_bot[0] * f)
        g = int(bg_top[1] * (1 - f) + bg_bot[1] * f)
        b = int(bg_top[2] * (1 - f) + bg_bot[2] * f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Floor gradient
    floor_h = h - wall_h
    for y in range(wall_h, h):
        f = (y - wall_h) / floor_h
        r = int(floor_far[0] * (1 - f) + floor_near[0] * f)
        g = int(floor_far[1] * (1 - f) + floor_near[1] * f)
        b = int(floor_far[2] * (1 - f) + floor_near[2] * f)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Studio lighting & soft product shadow
    shadow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    sdraw.ellipse([int(w * 0.15), int(wall_h - 10), int(w * 0.85), int(wall_h + floor_h * 0.65)], fill=(20, 14, 10, 120))
    # Soft side lighting
    sdraw.polygon([(0, 0), (int(w * 0.4), 0), (int(w * 0.7), h), (0, h)], fill=(255, 255, 245, 30))
    img.paste(Image.alpha_composite(img.convert('RGBA'), shadow_layer).convert('RGB'))
    
    pdraw = ImageDraw.Draw(img)
    cx = int(w * 0.5)
    
    if ptype == 'georgian_table':
        # Georgian Writing Table
        tw, th = int(w * 0.62), int(h * 0.05)
        ty = int(wall_h - h * 0.22)
        pdraw.rectangle([cx - tw//2, ty, cx + tw//2, ty + th], fill=wood_main, outline=wood_light, width=2)
        # Apron & 2 drawers
        pdraw.rectangle([cx - tw//2 + 15, ty + th, cx + tw//2 - 15, ty + th + int(h*0.1)], fill=wood_dark)
        dw = (tw - 50) // 2
        for di in range(2):
            dx = cx - tw//2 + 20 + di * (dw + 10)
            pdraw.rectangle([dx, ty + th + 6, dx + dw, ty + th + int(h*0.1) - 6], fill=wood_main, outline=wood_light, width=1)
            pdraw.ellipse([dx + dw//2 - 8, ty + th + int(h*0.05) - 3, dx + dw//2 + 8, ty + th + int(h*0.05) + 5], fill=brass)
        # Turned fluted legs
        for lx in [cx - tw//2 + 25, cx - tw//2 + 75, cx + tw//2 - 75, cx + tw//2 - 25]:
            pdraw.polygon([(lx - 6, ty + th + int(h*0.1)), (lx + 6, ty + th + int(h*0.1)), (lx + 4, wall_h + int(floor_h*0.35)), (lx - 4, wall_h + int(floor_h*0.35))], fill=wood_dark)
            pdraw.rectangle([lx - 4, wall_h + int(floor_h*0.35) - 6, lx + 4, wall_h + int(floor_h*0.35)], fill=brass)
            
    elif ptype == 'french_armoire':
        # French Oak Armoire with Carved Crown
        aw, ah = int(w * 0.52), int(h * 0.55)
        ay = int(wall_h - ah + h * 0.05)
        pdraw.rectangle([cx - aw//2, ay, cx + aw//2, ay + ah], fill=wood_dark, outline=wood_light, width=2)
        # Ornate Cornice
        pdraw.polygon([(cx - aw//2 - 15, ay), (cx + aw//2 + 15, ay), (cx + aw//2, ay + 20), (cx - aw//2, ay + 20)], fill=wood_main)
        # Dual doors with recessed panels
        dw = (aw - 20) // 2
        for di in range(2):
            dx = cx - aw//2 + 8 + di * (dw + 4)
            pdraw.rectangle([dx, ay + 28, dx + dw, ay + ah - 20], fill=wood_main, outline=wood_dark, width=2)
            pdraw.rectangle([dx + 8, ay + 36, dx + dw - 8, ay + ah - 28], outline=wood_light, width=1)
            # Long brass espagnolette bolt
            bx = dx + dw - 4 if di == 0 else dx + 4
            pdraw.line([(bx, ay + 40), (bx, ay + ah - 30)], fill=brass, width=3)
            pdraw.ellipse([bx - 6, ay + ah//2 - 6, bx + 6, ay + ah//2 + 6], fill=brass_bright)
        # Feet
        for fx in [cx - aw//2 + 20, cx + aw//2 - 20]:
            pdraw.polygon([(fx - 12, ay + ah), (fx + 12, ay + ah), (fx + 8, ay + ah + 18), (fx - 8, ay + ah + 18)], fill=wood_dark)
            
    elif ptype == 'art_deco_chair':
        # Art Deco Curved Club Chair in Natural Bouclé & Walnut
        cw, ch = int(w * 0.5), int(h * 0.38)
        cy = int(wall_h - ch + h * 0.05)
        # Backrest curve
        pdraw.ellipse([cx - cw//2, cy, cx + cw//2, cy + ch], fill=boucle, outline=wood_dark, width=4)
        # Sculpted Arms
        pdraw.ellipse([cx - cw//2 - 15, cy + int(ch*0.35), cx - cw//2 + 35, cy + ch], fill=wood_main, outline=wood_dark, width=2)
        pdraw.ellipse([cx + cw//2 - 35, cy + int(ch*0.35), cx + cw//2 + 15, cy + ch], fill=wood_main, outline=wood_dark, width=2)
        # Deep Seat Cushion
        pdraw.rectangle([cx - cw//2 + 10, cy + int(ch*0.55), cx + cw//2 - 10, cy + ch], fill=boucle, outline=(210, 200, 185), width=2)
        # Walnut Block / Taper Feet
        for fx in [cx - cw//2 + 25, cx + cw//2 - 25]:
            pdraw.polygon([(fx - 10, cy + ch), (fx + 10, cy + ch), (fx + 6, cy + ch + 22), (fx - 6, cy + ch + 22)], fill=wood_dark)
            pdraw.rectangle([fx - 6, cy + ch + 16, fx + 6, cy + ch + 22], fill=brass)

    elif ptype == 'edwardian_bookcase':
        # Edwardian Glazed Library Bookcase
        bw, bh = int(w * 0.54), int(h * 0.52)
        by = int(wall_h - bh + h * 0.04)
        pdraw.rectangle([cx - bw//2, by, cx + bw//2, by + bh], fill=wood_dark, outline=wood_light, width=2)
        # Glazed Astragal Bar Windows
        gw = (bw - 24) // 2
        for gi in range(2):
            gx = cx - bw//2 + 8 + gi * (gw + 8)
            pdraw.rectangle([gx, by + 20, gx + gw, by + bh - 20], fill=(225, 232, 236), outline=wood_main, width=3)
            # Astragal geometric grid
            pdraw.line([(gx + gw//2, by + 20), (gx + gw//2, by + bh - 20)], fill=wood_light, width=2)
            pdraw.line([(gx, by + bh//3), (gx + gw, by + bh//3)], fill=wood_light, width=2)
            pdraw.line([(gx, by + 2*bh//3), (gx + gw, by + 2*bh//3)], fill=wood_light, width=2)
            # Book spines visible through glass
            pdraw.rectangle([gx + 6, by + 2*bh//3 + 8, gx + gw - 6, by + bh - 24], fill=(120, 85, 65))
            
    elif ptype == 'midcentury_credenza':
        # Mid-Century Teak Credenza with Sliding Tambour Doors
        cw, ch = int(w * 0.68), int(h * 0.22)
        cy = int(wall_h - ch - h * 0.05)
        # Low sleek body
        pdraw.rectangle([cx - cw//2, cy, cx + cw//2, cy + ch], fill=(135, 88, 55), outline=(95, 60, 36), width=2)
        # Tambour vertical slat lines
        for sx in range(cx - cw//2 + 10, cx + cw//2 - 10, 8):
            pdraw.line([(sx, cy + 4), (sx, cy + ch - 4)], fill=(105, 68, 42), width=1)
        # Recessed round pulls
        pdraw.ellipse([cx - cw//4 - 8, cy + ch//2 - 8, cx - cw//4 + 8, cy + ch//2 + 8], fill=(75, 48, 30))
        pdraw.ellipse([cx + cw//4 - 8, cy + ch//2 - 8, cx + cw//4 + 8, cy + ch//2 + 8], fill=(75, 48, 30))
        # Splayed tapered legs
        for lx, angle in [(cx - cw//2 + 35, -12), (cx + cw//2 - 35, 12)]:
            pdraw.polygon([(lx - 6, cy + ch), (lx + 6, cy + ch), (lx + angle + 4, wall_h + int(floor_h*0.25)), (lx + angle - 4, wall_h + int(floor_h*0.25))], fill=(85, 52, 32))
            pdraw.rectangle([lx + angle - 4, wall_h + int(floor_h*0.25) - 6, lx + angle + 4, wall_h + int(floor_h*0.25)], fill=brass)

    elif ptype == 'regency_dining':
        # Regency Mahogany Dining Table
        tw, th = int(w * 0.7), int(h * 0.045)
        ty = int(wall_h - h * 0.18)
        # Polished bullnose top
        pdraw.rectangle([cx - tw//2, ty, cx + tw//2, ty + th], fill=(85, 42, 32), outline=(130, 68, 52), width=2)
        # Central twin pedestals with splayed tripod sabre legs & brass paw casters
        for px in [cx - int(tw*0.25), cx + int(tw*0.25)]:
            # Turned pillar
            pdraw.polygon([(px - 14, ty + th), (px + 14, ty + th), (px + 10, ty + th + 60), (px - 10, ty + th + 60)], fill=(65, 32, 24))
            # Sabre legs
            pdraw.polygon([(px - 8, ty + th + 55), (px - 55, wall_h + int(floor_h*0.25)), (px - 45, wall_h + int(floor_h*0.25)), (px, ty + th + 60)], fill=(55, 26, 20))
            pdraw.polygon([(px + 8, ty + th + 55), (px + 55, wall_h + int(floor_h*0.25)), (px + 45, wall_h + int(floor_h*0.25)), (px, ty + th + 60)], fill=(55, 26, 20))
            # Brass paws
            pdraw.ellipse([px - 58, wall_h + int(floor_h*0.25) - 4, px - 42, wall_h + int(floor_h*0.25) + 6], fill=brass)
            pdraw.ellipse([px + 42, wall_h + int(floor_h*0.25) - 4, px + 58, wall_h + int(floor_h*0.25) + 6], fill=brass)

    elif ptype == 'brass_mirror':
        # Art Deco Brass Floor Cheval Mirror
        mw, mh = int(w * 0.38), int(h * 0.58)
        my = int(wall_h - mh + h * 0.02)
        # Polished Arch Mirror Frame
        pdraw.rectangle([cx - mw//2, my, cx + mw//2, my + mh], fill=(222, 230, 235), outline=brass, width=6)
        pdraw.rectangle([cx - mw//2 + 6, my + 6, cx + mw//2 - 6, my + mh - 6], outline=brass_bright, width=2)
        # Stepped Art Deco Top Crown
        pdraw.rectangle([cx - mw//3, my - 14, cx + mw//3, my], fill=brass)
        # Stand side pivots
        pdraw.polygon([(cx - mw//2 - 12, my + mh//2), (cx - mw//2 - 16, wall_h + int(floor_h*0.28)), (cx - mw//2 - 6, wall_h + int(floor_h*0.28)), (cx - mw//2, my + mh//2)], fill=brass)
        pdraw.polygon([(cx + mw//2 + 12, my + mh//2), (cx + mw//2 + 16, wall_h + int(floor_h*0.28)), (cx + mw//2 + 6, wall_h + int(floor_h*0.28)), (cx + mw//2, my + mh//2)], fill=brass)

    elif ptype == 'walnut_desk':
        # Mid-Century Walnut Partner Desk
        dw, dh = int(w * 0.65), int(h * 0.28)
        dy = int(wall_h - dh + h * 0.05)
        # Floating desk top
        pdraw.rectangle([cx - dw//2, dy, cx + dw//2, dy + 18], fill=wood_main, outline=wood_light, width=2)
        # Twin drawer pedestals
        pw = int(dw * 0.28)
        for px in [cx - dw//2 + 10, cx + dw//2 - pw - 10]:
            pdraw.rectangle([px, dy + 28, px + pw, dy + dh], fill=wood_dark, outline=wood_light, width=2)
            # 3 drawers each
            for ri in range(3):
                ry = dy + 32 + ri * (int(dh - 36) // 3)
                pdraw.rectangle([px + 4, ry, px + pw - 4, ry + (int(dh - 36) // 3) - 4], fill=wood_main, outline=wood_dark, width=1)
                pdraw.line([(px + 15, ry + 12), (px + pw - 15, ry + 12)], fill=brass, width=2)
        # Splayed legs under pedestals
        for lx in [cx - dw//2 + 20, cx - dw//2 + pw, cx + dw//2 - pw, cx + dw//2 - 20]:
            pdraw.polygon([(lx - 5, dy + dh), (lx + 5, dy + dh), (lx + 3, wall_h + int(floor_h*0.3)), (lx - 3, wall_h + int(floor_h*0.3))], fill=wood_dark)

    elif ptype == 'victorian_settee':
        # Victorian Velvet Salon Settee in Deep Olive / Ochre
        sw, sh = int(w * 0.62), int(h * 0.36)
        sy = int(wall_h - sh + h * 0.05)
        # Button-tufted backrest with serpentine carved walnut cresting
        pdraw.polygon([(cx - sw//2, sy + sh//2), (cx - sw//3, sy), (cx, sy + 15), (cx + sw//3, sy), (cx + sw//2, sy + sh//2), (cx + sw//2, sy + sh), (cx - sw//2, sy + sh)], fill=velvet, outline=wood_dark, width=3)
        # Tufting dots
        for ty_off in [sy + 40, sy + 75]:
            for tx_off in range(cx - sw//3, cx + sw//3 + 1, 35):
                pdraw.ellipse([tx_off - 4, ty_off - 4, tx_off + 4, ty_off + 4], fill=(60, 32, 28))
        # Deep bolster arms & cushion
        pdraw.rectangle([cx - sw//2 - 10, sy + int(sh*0.55), cx + sw//2 + 10, sy + sh], fill=velvet, outline=wood_dark, width=2)
        # Carved cabriole legs
        for lx in [cx - sw//2 + 15, cx - sw//4, cx + sw//4, cx + sw//2 - 15]:
            pdraw.polygon([(lx - 8, sy + sh), (lx + 8, sy + sh), (lx + 5, wall_h + int(floor_h*0.28)), (lx - 5, wall_h + int(floor_h*0.28))], fill=wood_dark)
            pdraw.ellipse([lx - 7, wall_h + int(floor_h*0.28) - 4, lx + 7, wall_h + int(floor_h*0.28) + 4], fill=brass)

    # Post processing
    img = img.filter(ImageFilter.SMOOTH)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = add_film_grain(img, intensity=8)
    return img

print('Generating Collection Section Images...')

# 1. Collection Hero (1376 x 768)
hero = create_rich_editorial_scene(1376, 768, scene_type='hero', seed=101)
hero.save('assets/images/collection/collection-hero.jpg', 'JPEG', quality=92)
print('Saved collection-hero.jpg')

# 2. Scale Guide (1264 x 848)
scale = create_rich_editorial_scene(1264, 848, scene_type='scale', seed=202)
scale.save('assets/images/collection/scale-guide.jpg', 'JPEG', quality=92)
print('Saved scale-guide.jpg')

# 3. Category Index (1200 x 896)
cat = create_rich_editorial_scene(1200, 896, scene_type='category', seed=303)
cat.save('assets/images/collection/category-index.jpg', 'JPEG', quality=92)
print('Saved category-index.jpg')

# 4. Era Index (1200 x 896)
era = create_rich_editorial_scene(1200, 896, scene_type='era', seed=404)
era.save('assets/images/collection/era-index.jpg', 'JPEG', quality=92)
print('Saved era-index.jpg')

# 5. Between Pieces (01, 02, 03)
b1 = create_rich_editorial_scene(1200, 896, scene_type='between1', seed=501)
b1.save('assets/images/collection/between-01.jpg', 'JPEG', quality=92)

b2 = create_rich_editorial_scene(1024, 1024, scene_type='between2', seed=502)
b2.save('assets/images/collection/between-02.jpg', 'JPEG', quality=92)

b3 = create_rich_editorial_scene(1024, 1024, scene_type='between3', seed=503)
b3.save('assets/images/collection/between-03.jpg', 'JPEG', quality=92)
print('Saved between-01.jpg, between-02.jpg, between-03.jpg')

# 6. Collection Closing (1376 x 768)
closing = create_rich_editorial_scene(1376, 768, scene_type='closing', seed=606)
closing.save('assets/images/collection/collection-closing.jpg', 'JPEG', quality=92)
print('Saved collection-closing.jpg')

# 7. Products (9 Curated Products)
products = [
    ('product-01.jpg', 'georgian_table', 701),
    ('product-02.jpg', 'french_armoire', 702),
    ('product-03.jpg', 'art_deco_chair', 703),
    ('product-04.jpg', 'edwardian_bookcase', 704),
    ('product-05.jpg', 'midcentury_credenza', 705),
    ('product-06.jpg', 'regency_dining', 706),
    ('product-07.jpg', 'brass_mirror', 707),
    ('product-08.jpg', 'walnut_desk', 708),
    ('product-09.jpg', 'victorian_settee', 709)
]

for filename, ptype, seed in products:
    pimg = create_product_shot(1200, 900, ptype, seed)
    pimg.save(f'assets/images/collection/products/{filename}', 'JPEG', quality=92)
    print(f'Saved products/{filename}')

print('All collection and product images generated successfully!')
