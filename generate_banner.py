import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1200
HEIGHT = 440

def create_storm_background():
    """Generates a deep, multi-layered cosmic storm background with atmospheric clouds and volumetric lightning glow."""
    # 1. Base gradient in numpy: dark obsidian to deep midnight thunder navy
    y_coords, x_coords = np.ogrid[:HEIGHT, :WIDTH]
    
    # Radial glow from lightning epicenter (hammer position ~ x=235, y=95)
    dist_epicenter = np.sqrt(((x_coords - 235) ** 2) * 0.9 + ((y_coords - 95) ** 2) * 1.8)
    epicenter_glow = np.clip(1.0 - (dist_epicenter / 700.0), 0.0, 1.0)
    
    # Dark storm color palette
    r = (3 + epicenter_glow * 16).astype(np.uint8)
    g = (6 + epicenter_glow * 32).astype(np.uint8)
    b = (14 + epicenter_glow * 65).astype(np.uint8)
    
    base_rgb = np.dstack((r, g, b))
    bg_img = Image.fromarray(base_rgb, mode="RGB")
    
    # 2. Layered storm cloud puffs with dark indigo & cyan tints
    cloud_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cloud_draw = ImageDraw.Draw(cloud_layer)
    random.seed(101)
    
    for _ in range(35):
        cx = random.randint(-40, WIDTH + 40)
        cy = random.randint(10, 280)
        rx = random.randint(130, 290)
        ry = random.randint(50, 130)
        # Mix of dark moody indigo and distant lightning highlights
        tint = random.choice([
            (10, 22, 50, 50),
            (6, 14, 38, 65),
            (14, 38, 80, 40),
            (2, 6, 20, 80)
        ])
        cloud_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=tint)
        
    cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(32))
    bg_img.paste(cloud_layer, (0, 0), cloud_layer)
    
    # 3. Fine technical coordinate grid (astronomy / data science aesthetics)
    grid_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_layer)
    for y in range(30, HEIGHT, 40):
        alpha = int(14 * (1.0 - y / HEIGHT))
        grid_draw.line([(0, y), (WIDTH, y)], fill=(0, 242, 254, alpha), width=1)
    for x in range(50, WIDTH, 75):
        grid_draw.line([(x, 0), (x, HEIGHT)], fill=(0, 242, 254, 8), width=1)
        
    bg_img.paste(grid_layer, (0, 0), grid_layer)
    return bg_img

def generate_branching_lightning(start, end, depth=0, max_depth=4, jitter=30):
    """Recursively generates realistic fractal lightning branch paths."""
    if depth >= max_depth:
        return [(start, end)]
    
    mid_x = (start[0] + end[0]) / 2 + random.uniform(-jitter, jitter)
    mid_y = (start[1] + end[1]) / 2 + random.uniform(-jitter * 0.7, jitter * 0.7)
    mid = (mid_x, mid_y)
    
    lines = []
    lines.extend(generate_branching_lightning(start, mid, depth + 1, max_depth, jitter * 0.65))
    lines.extend(generate_branching_lightning(mid, end, depth + 1, max_depth, jitter * 0.65))
    
    # Sub-branch discharge
    if random.random() > 0.52 and depth < max_depth - 1:
        branch_dx = (end[0] - start[0]) * 0.45 + random.uniform(-60, 60)
        branch_dy = (end[1] - start[1]) * 0.45 + random.uniform(25, 75)
        sub_end = (mid[0] + branch_dx, mid[1] + branch_dy)
        lines.extend(generate_branching_lightning(mid, sub_end, depth + 1, max_depth, jitter * 0.5))
        
    return lines

def render_lightning_glow(draw, glow_draw, p1, p2, width=2, intensity=1.0):
    """Draws multi-tiered energetic glow with cyan core and pure white arc center."""
    # Outer diffuse cyan aura
    glow_draw.line([p1, p2], fill=(0, 242, 254, int(150 * intensity)), width=width + 7)
    # Mid-layer sky-blue ionization
    glow_draw.line([p1, p2], fill=(56, 189, 248, int(210 * intensity)), width=width + 3)
    # Bright incandescent white core
    draw.line([p1, p2], fill=(255, 255, 255, int(255 * intensity)), width=width)

def draw_heroic_thor(draw, glow_draw, cx, cy, scale=1.1, is_strike=False):
    """Draws an impressive, armored thunder-god hero silhouette with silver armor, cape, and glowing Mjolnir."""
    # 1. Dark Asgardian / Monolith Crag
    crag_pts = [
        (cx - 180 * scale, cy + 185 * scale),
        (cx - 90 * scale, cy + 115 * scale),
        (cx + 70 * scale, cy + 118 * scale),
        (cx + 180 * scale, cy + 195 * scale),
        (cx + 240 * scale, HEIGHT),
        (cx - 220 * scale, HEIGHT),
    ]
    draw.polygon(crag_pts, fill=(5, 11, 24))
    
    # Runes etched into the crag rim
    for i in range(len(crag_pts) - 2):
        glow_draw.line([crag_pts[i], crag_pts[i+1]], fill=(0, 242, 254, 85), width=3)
        draw.line([crag_pts[i], crag_pts[i+1]], fill=(148, 163, 184, 180), width=1)

    # 2. Majestic Flowing Crimson Cape (Billowing in storm gale)
    cape_main = (225, 29, 72) if is_strike else (190, 18, 60)
    cape_dark = (136, 19, 55)
    cape_highlight = (251, 113, 133)
    
    cape_pts = [
        (cx - 18 * scale, cy - 24 * scale),   # left shoulder
        (cx - 110 * scale, cy + 12 * scale),  # billowing apex upper
        (cx - 165 * scale, cy + 95 * scale),  # billow tip
        (cx - 105 * scale, cy + 135 * scale), # lower flap
        (cx - 35 * scale, cy + 105 * scale),  # hem base
        (cx + 15 * scale, cy + 45 * scale),   # back fold
        (cx + 24 * scale, cy - 22 * scale),   # right shoulder
    ]
    draw.polygon(cape_pts, fill=cape_main)
    # Cape inner shadows & fold creases
    draw.line([(cx - 110 * scale, cy + 12 * scale), (cx - 35 * scale, cy + 105 * scale)], fill=cape_dark, width=3)
    draw.line([(cx - 165 * scale, cy + 95 * scale), (cx - 85 * scale, cy + 60 * scale)], fill=cape_dark, width=3)
    draw.line([(cx - 18 * scale, cy - 24 * scale), (cx - 110 * scale, cy + 12 * scale)], fill=cape_highlight, width=2)

    # 3. Armored Legs & Brushed Silver Greaves
    # Undersuit (dark obsidian carbon)
    draw.rectangle([cx - 22 * scale, cy + 55 * scale, cx - 9 * scale, cy + 115 * scale], fill=(15, 23, 42))
    draw.rectangle([cx + 7 * scale, cy + 55 * scale, cx + 20 * scale, cy + 118 * scale], fill=(15, 23, 42))
    
    # Silver Greaves & knee plates
    silver = (248, 250, 252) if is_strike else (226, 232, 240)
    silver_shade = (148, 163, 184)
    
    draw.polygon([
        (cx - 24 * scale, cy + 74 * scale),
        (cx - 8 * scale, cy + 74 * scale),
        (cx - 10 * scale, cy + 110 * scale),
        (cx - 25 * scale, cy + 110 * scale),
    ], fill=silver)
    draw.polygon([
        (cx + 6 * scale, cy + 76 * scale),
        (cx + 22 * scale, cy + 76 * scale),
        (cx + 19 * scale, cy + 112 * scale),
        (cx + 5 * scale, cy + 112 * scale),
    ], fill=silver)
    # Knee cops
    draw.ellipse([cx - 21 * scale, cy + 66 * scale, cx - 11 * scale, cy + 76 * scale], fill=silver_shade)
    draw.ellipse([cx + 9 * scale, cy + 68 * scale, cx + 19 * scale, cy + 78 * scale], fill=silver_shade)

    # 4. Sculpted Silver Torso Cuirass & Norse Discs
    cuirass_pts = [
        (cx - 26 * scale, cy - 22 * scale),
        (cx + 26 * scale, cy - 22 * scale),
        (cx + 20 * scale, cy + 55 * scale),
        (cx - 20 * scale, cy + 55 * scale),
    ]
    draw.polygon(cuirass_pts, fill=silver)
    # Armor plate bevel shading
    draw.polygon([(cx - 26 * scale, cy - 22 * scale), (cx - 13 * scale, cy - 22 * scale), (cx - 10 * scale, cy + 55 * scale), (cx - 20 * scale, cy + 55 * scale)], fill=silver_shade)

    # 6 Norse Chest Medallions with cyan runic rims
    discs = [
        (cx - 14 * scale, cy - 11 * scale),
        (cx + 14 * scale, cy - 11 * scale),
        (cx - 12 * scale, cy + 11 * scale),
        (cx + 12 * scale, cy + 11 * scale),
        (cx - 9 * scale, cy + 33 * scale),
        (cx + 9 * scale, cy + 33 * scale),
    ]
    for dx, dy in discs:
        draw.ellipse([dx - 8 * scale, dy - 8 * scale, dx + 8 * scale, dy + 8 * scale], fill=(30, 41, 59))
        draw.ellipse([dx - 5 * scale, dy - 5 * scale, dx + 5 * scale, dy + 5 * scale], fill=(71, 85, 105))
        glow_draw.ellipse([dx - 7 * scale, dy - 7 * scale, dx + 7 * scale, dy + 7 * scale], outline=(0, 242, 254, 200), width=1)
        if is_strike:
            draw.ellipse([dx - 3 * scale, dy - 3 * scale, dx + 3 * scale, dy + 3 * scale], fill=(0, 242, 254))

    # Belt & Glowing Rune Buckle
    draw.rectangle([cx - 20 * scale, cy + 51 * scale, cx + 20 * scale, cy + 57 * scale], fill=(15, 23, 42))
    glow_draw.rectangle([cx - 7 * scale, cy + 50 * scale, cx + 7 * scale, cy + 58 * scale], fill=(0, 242, 254, 255))
    draw.rectangle([cx - 5 * scale, cy + 51 * scale, cx + 5 * scale, cy + 57 * scale], fill=(255, 255, 255))

    # 5. Left Arm (Braced at side)
    draw.line([
        (cx - 24 * scale, cy - 20 * scale),
        (cx - 48 * scale, cy + 10 * scale),
        (cx - 40 * scale, cy + 40 * scale)
    ], fill=silver, width=int(11 * scale))
    draw.line([(cx - 48 * scale, cy + 10 * scale), (cx - 40 * scale, cy + 40 * scale)], fill=(0, 242, 254), width=int(3 * scale))

    # 6. Right Arm (Raised aloft to command the storm)
    shoulder_r = (cx + 24 * scale, cy - 20 * scale)
    elbow_r = (cx + 56 * scale, cy - 64 * scale)
    hand_r = (cx + 82 * scale, cy - 110 * scale)
    draw.line([shoulder_r, elbow_r, hand_r], fill=silver, width=int(12 * scale))
    # Bracer neon energy
    glow_draw.line([elbow_r, hand_r], fill=(0, 242, 254, 220), width=int(6 * scale))

    # 7. Legendary Hammer — Mjolnir
    hx, hy = hand_r
    haft_top = (hx + 15 * scale, hy - 36 * scale)
    haft_bot = (hx - 14 * scale, hy + 28 * scale)
    # Leather grip & silver pommel
    draw.line([haft_bot, haft_top], fill=(148, 163, 184), width=int(7 * scale))
    draw.line([(hx - 9 * scale, hy + 18 * scale), haft_bot], fill=(190, 18, 60), width=int(8 * scale))

    # Titanium Mjolnir Head
    head_cx = haft_top[0] + 7 * scale
    head_cy = haft_top[1] - 9 * scale
    hw, hh = 54 * scale, 36 * scale
    
    head_pts = [
        (head_cx - hw/2 + 7, head_cy - hh/2),
        (head_cx + hw/2 - 7, head_cy - hh/2),
        (head_cx + hw/2, head_cy - hh/2 + 7),
        (head_cx + hw/2, head_cy + hh/2 - 7),
        (head_cx + hw/2 - 7, head_cy + hh/2),
        (head_cx - hw/2 + 7, head_cy + hh/2),
        (head_cx - hw/2, head_cy + hh/2 - 7),
        (head_cx - hw/2, head_cy - hh/2 + 7),
    ]
    draw.polygon(head_pts, fill=silver)
    draw.line(head_pts + [head_pts[0]], fill=(15, 23, 42), width=2)
    
    # Glowing Runic Inscription on Mjolnir
    rune_fill = (255, 255, 255) if is_strike else (0, 242, 254)
    glow_draw.line([(head_cx - hw/2 + 11, head_cy), (head_cx + hw/2 - 11, head_cy)], fill=(0, 242, 254, 255), width=4)
    draw.line([(head_cx - hw/2 + 11, head_cy), (head_cx + hw/2 - 11, head_cy)], fill=rune_fill, width=2)
    glow_draw.ellipse([head_cx - 6, head_cy - 6, head_cx + 6, head_cy + 6], fill=(0, 242, 254, 255))
    draw.ellipse([head_cx - 3, head_cy - 3, head_cx + 3, head_cy + 3], fill=(255, 255, 255))

    # Plasma discharge aura around Mjolnir head
    aura_radius = 45 if not is_strike else 80
    glow_draw.ellipse(
        [head_cx - aura_radius, head_cy - aura_radius, head_cx + aura_radius, head_cy + aura_radius],
        fill=(0, 242, 254, 60 if not is_strike else 150)
    )

    # 8. Head, Helmet with Winged Crest & Glowing Eyes
    head_x, head_y = cx, cy - 38 * scale
    # Golden-brown flowing locks
    hair_pts1 = [(head_x - 11 * scale, head_y - 4 * scale), (head_x - 38 * scale, head_y + 25 * scale), (head_x - 22 * scale, head_y + 38 * scale), (head_x - 5 * scale, head_y + 14 * scale)]
    hair_pts2 = [(head_x + 9 * scale, head_y - 2 * scale), (head_x + 27 * scale, head_y + 22 * scale), (head_x + 14 * scale, head_y + 34 * scale)]
    draw.polygon(hair_pts1, fill=(53, 40, 28))
    draw.polygon(hair_pts2, fill=(53, 40, 28))

    # Silver Helmet Dome
    draw.ellipse([head_x - 11 * scale, head_y - 14 * scale, head_x + 11 * scale, head_y + 9 * scale], fill=silver)
    # Majestic Wings on Helmet
    draw.polygon([(head_x - 11 * scale, head_y - 6 * scale), (head_x - 28 * scale, head_y - 27 * scale), (head_x - 9 * scale, head_y - 14 * scale)], fill=silver)
    draw.polygon([(head_x + 11 * scale, head_y - 6 * scale), (head_x + 28 * scale, head_y - 27 * scale), (head_x + 9 * scale, head_y - 14 * scale)], fill=silver)

    # Piercing Cyan Lightning Eyes
    glow_draw.ellipse([head_x - 6 * scale, head_y - 2 * scale, head_x - 2 * scale, head_y + 2 * scale], fill=(0, 242, 254, 255))
    glow_draw.ellipse([head_x + 2 * scale, head_y - 2 * scale, head_x + 6 * scale, head_y + 2 * scale], fill=(0, 242, 254, 255))
    draw.ellipse([head_x - 5 * scale, head_y - 1 * scale, head_x - 3 * scale, head_y + 1 * scale], fill=(255, 255, 255))
    draw.ellipse([head_x + 3 * scale, head_y - 1 * scale, head_x + 5 * scale, head_y + 1 * scale], fill=(255, 255, 255))

    return (head_cx, head_cy)

def draw_cyber_typography(draw, glow_draw, fonts, flash_val=0.0):
    """Renders crisp, metallic 3D chiseled BARATH title and data science badges."""
    title_font, sub_font, badge_font, tag_font = fonts
    text_x = 450

    # 1. Top Category Pill: "⚡ M.SC. DATA SCIENCE SCHOLAR"
    tag_y = 65
    pill_w = 285
    glow_draw.rounded_rectangle([text_x, tag_y, text_x + pill_w, tag_y + 28], radius=14, outline=(0, 242, 254, 200), width=1)
    draw.rounded_rectangle([text_x, tag_y, text_x + pill_w, tag_y + 28], radius=14, fill=(6, 18, 42), outline=(0, 242, 254), width=1)
    
    # Electric bolt icon inside pill
    ix = text_x + 14
    iy = tag_y + 7
    draw.polygon([(ix + 7, iy), (ix, iy + 9), (ix + 6, iy + 9), (ix + 2, iy + 15), (ix + 10, iy + 6), (ix + 5, iy + 6)], fill=(0, 242, 254))
    draw.text((text_x + 30, tag_y + 6), "M.SC. DATA SCIENCE SCHOLAR", font=tag_font, fill=(0, 242, 254))

    # 2. Main Title: "BARATH" (Metallic 3D chiseled chrome)
    title_y = 100
    title_text = "BARATH"
    
    # Multi-layered glowing halo
    halo_alpha = int(120 + flash_val * 120)
    for offset in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-4, 2), (4, -2)]:
        glow_draw.text((text_x + offset[0], title_y + offset[1]), title_text, font=title_font, fill=(0, 242, 254, halo_alpha))
        
    # Dark bevel shadow
    draw.text((text_x + 3, title_y + 3), title_text, font=title_font, fill=(15, 23, 42))
    draw.text((text_x + 2, title_y + 2), title_text, font=title_font, fill=(30, 41, 59))
    
    # Brushed titanium face
    draw.text((text_x + 1, title_y + 1), title_text, font=title_font, fill=(203, 213, 225))
    # Specular white top face
    draw.text((text_x, title_y), title_text, font=title_font, fill=(255, 255, 255))

    # 3. Moniker Subtitle: "// THE THUNDERVERSE //"
    sub_y = 205
    draw.text((text_x + 4, sub_y), "// THE THUNDERVERSE //", font=sub_font, fill=(56, 189, 248))

    # 4. Mission Statement
    desc_y = 240
    mission_text = "Forging high-throughput data streams, rigorous statistical models,\nand production-grade AI systems with algorithmic integrity."
    draw.text((text_x + 4, desc_y), mission_text, font=sub_font, fill=(203, 213, 225), spacing=6)

    # 5. Core Arsenal Tech Badges
    badges = [
        ("PYTHON", (56, 189, 248)),
        ("SQL", (0, 242, 254)),
        ("DATA SCIENCE", (96, 165, 250)),
        ("AI / ML", (248, 113, 113)),
        ("DEEP LEARNING", (167, 139, 250)),
    ]
    bx = text_x + 4
    by = 325
    for label, color in badges:
        bw = len(label) * 9 + 32
        # Badge container
        draw.rounded_rectangle([bx, by, bx + bw, by + 32], radius=7, fill=(10, 18, 36), outline=color, width=1)
        glow_draw.rounded_rectangle([bx, by, bx + bw, by + 32], radius=7, outline=(*color, 95), width=2)
        # Glowing status dot
        draw.ellipse([bx + 11, by + 12, bx + 19, by + 20], fill=color)
        glow_draw.ellipse([bx + 9, by + 10, bx + 21, by + 22], fill=(*color, 120))
        # Text label
        draw.text((bx + 26, by + 8), label, font=badge_font, fill=(248, 250, 252))
        bx += bw + 12

def render_frame(frame_idx, total_frames, fonts):
    """Renders a single high-definition composite frame."""
    img = create_storm_background()
    draw = ImageDraw.Draw(img)
    
    # Dedicated high-dynamic range glow overlay
    glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    # Lightning strike rhythm
    is_strike = frame_idx in [2, 3, 9, 10]
    flash_val = 1.0 if frame_idx in [2, 9] else (0.55 if is_strike else 0.0)

    # Draw Thor & obtain hammer coordinates
    hammer_pos = draw_heroic_thor(draw, glow_draw, cx=215, cy=245, scale=1.08, is_strike=is_strike)

    # Render branching electric arcs
    random.seed(frame_idx * 37 + 13)
    if is_strike:
        # Skyward celestial strike
        sky_tree = generate_branching_lightning(hammer_pos, (random.randint(60, 460), 0), max_depth=4, jitter=30)
        for p1, p2 in sky_tree:
            render_lightning_glow(draw, glow_draw, p1, p2, width=3, intensity=1.0)
            
        # Dramatic horizontal storm discharge across the banner
        arc_tree = generate_branching_lightning(hammer_pos, (random.randint(680, 1180), random.randint(15, 50)), max_depth=4, jitter=34)
        for p1, p2 in arc_tree:
            render_lightning_glow(draw, glow_draw, p1, p2, width=3, intensity=0.95)

        # Ground spark discharge
        ground_tree = generate_branching_lightning(hammer_pos, (hammer_pos[0] + 95, hammer_pos[1] + 135), max_depth=3, jitter=18)
        for p1, p2 in ground_tree:
            render_lightning_glow(draw, glow_draw, p1, p2, width=2, intensity=0.75)
    else:
        # Ambient resting lightning crackles around hammer
        spark_end = (hammer_pos[0] + math.sin(frame_idx * 0.75) * 50, hammer_pos[1] - 42 - abs(math.cos(frame_idx * 0.55)) * 28)
        tree = generate_branching_lightning(hammer_pos, spark_end, max_depth=2, jitter=14)
        for p1, p2 in tree:
            render_lightning_glow(draw, glow_draw, p1, p2, width=2, intensity=0.65)

    # Distant atmospheric flashes in the background
    if frame_idx in [5, 6, 13]:
        dist_tree = generate_branching_lightning((960, 0), (1060, 180), max_depth=3, jitter=24)
        for p1, p2 in dist_tree:
            render_lightning_glow(draw, glow_draw, p1, p2, width=2, intensity=0.8)

    # Floating cyan data sparks / motes
    for i in range(36):
        sx = (i * 37 + frame_idx * 18) % WIDTH
        sy = (HEIGHT - (i * 29 + frame_idx * 11) % HEIGHT)
        alpha = int(150 + 95 * math.sin(frame_idx + i))
        glow_draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(0, 242, 254, alpha))
        draw.point((sx, sy), fill=(255, 255, 255, 255))

    # Render Typography & Badges
    draw_cyber_typography(draw, glow_draw, fonts, flash_val=flash_val)

    # Bottom metallic neon laser accent line
    for x in range(WIDTH):
        c_alpha = int(150 + 85 * math.sin(x * 0.035 + frame_idx * 0.45))
        draw.point((x, HEIGHT - 1), fill=(0, 242, 254, c_alpha))
        draw.point((x, HEIGHT - 2), fill=(148, 163, 184, c_alpha // 2))

    # Blur glow layer slightly and composite over base
    blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(3))
    img.paste(blurred_glow, (0, 0), blurred_glow)
    
    return img

def main():
    print("Loading fonts for banner...")
    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 92)
        sub_font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
        badge_font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
        tag_font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
    except Exception as e:
        print(f"Font loading fallback: {e}")
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()
        tag_font = ImageFont.load_default()

    fonts = (title_font, sub_font, badge_font, tag_font)

    # 1. Generate Static PNG Banner (assets/thor-banner.png)
    print("Rendering assets/thor-banner.png...")
    static_img = render_frame(2, 16, fonts)
    static_img.save("assets/thor-banner.png", "PNG", optimize=True)
    
    # Also save to github-profile/assets/thor-banner.png
    import os
    os.makedirs("github-profile/assets", exist_ok=True)
    static_img.save("github-profile/assets/thor-banner.png", "PNG", optimize=True)
    print("[OK] Saved assets/thor-banner.png and github-profile/assets/thor-banner.png")

    # 2. Generate Animated GIF Banner (assets/thor-banner.gif)
    print("Rendering assets/thor-banner.gif (16 frames)...")
    total_frames = 16
    gif_frames = []
    for i in range(total_frames):
        frame = render_frame(i, total_frames, fonts)
        paletted = frame.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        gif_frames.append(paletted)

    gif_frames[0].save(
        "assets/thor-banner.gif",
        save_all=True,
        append_images=gif_frames[1:],
        duration=85,
        loop=0,
        optimize=True
    )
    gif_frames[0].save(
        "github-profile/assets/thor-banner.gif",
        save_all=True,
        append_images=gif_frames[1:],
        duration=85,
        loop=0,
        optimize=True
    )
    print("[OK] Saved assets/thor-banner.gif and github-profile/assets/thor-banner.gif")

if __name__ == "__main__":
    main()
