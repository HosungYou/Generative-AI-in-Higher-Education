#!/usr/bin/env python3
"""
AIMC Framework - Museum-Quality Academic Visualization
Design Philosophy: Cognitive Stratification
Second Pass: Refined for pristine, masterpiece-level craftsmanship

Author: Hosung You, Pennsylvania State University
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

# Configuration - High Resolution for Print
WIDTH = 3200
HEIGHT = 2400
DPI = 300
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Font paths
FONT_DIR = "/Users/hosung/.claude/plugins/cache/anthropic-agent-skills/example-skills/c74d647e56e6/canvas-design/canvas-fonts"

# Refined Color Palette - Cognitive Stratification
# More muted, sophisticated academic tones
COLORS = {
    'background': '#F8FAFC',
    'background_subtle': '#F1F5F9',

    # Header - Deep scholarly navy
    'header_primary': '#0F172A',
    'header_secondary': '#1E293B',
    'header_text': '#F8FAFC',
    'header_accent': '#64748B',

    # Level 3 - Refined Amethyst (transcendence)
    'level3_bg': '#6D28D9',
    'level3_gradient': '#7C3AED',
    'level3_box': '#8B5CF6',
    'level3_text': '#FFFFFF',
    'level3_subtext': '#DDD6FE',
    'level3_badge_bg': '#EDE9FE',
    'level3_badge_text': '#5B21B6',

    # Level 2 - Refined Cerulean (awareness)
    'level2_bg': '#1D4ED8',
    'level2_gradient': '#2563EB',
    'level2_box': '#3B82F6',
    'level2_text': '#FFFFFF',
    'level2_subtext': '#BFDBFE',
    'level2_badge_bg': '#DBEAFE',
    'level2_badge_text': '#1E40AF',

    # Level 1 - Refined Emerald (emergence)
    'level1_bg': '#047857',
    'level1_gradient': '#059669',
    'level1_box': '#10B981',
    'level1_text': '#FFFFFF',
    'level1_subtext': '#A7F3D0',
    'level1_badge_bg': '#D1FAE5',
    'level1_badge_text': '#065F46',

    # Warning/Key Finding - Warm amber
    'warning_bg': '#FFFBEB',
    'warning_border': '#D97706',
    'warning_icon': '#B45309',
    'warning_title': '#92400E',
    'warning_text': '#78350F',

    # Structural elements
    'arrow': '#475569',
    'arrow_label': '#64748B',
    'divider': '#CBD5E1',
    'citation': '#94A3B8',
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def blend_colors(color1, color2, factor):
    """Blend two hex colors."""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return (r, g, b)

def load_fonts():
    """Load fonts with careful selection for academic elegance."""
    fonts = {}
    try:
        # Primary header - Bold and authoritative
        fonts['title'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Bold.ttf", 96)
        fonts['subtitle'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Regular.ttf", 40)

        # Level headers
        fonts['level_title'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Bold.ttf", 64)
        fonts['level_subtitle'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Regular.ttf", 32)

        # Content
        fonts['content'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Regular.ttf", 36)
        fonts['content_secondary'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Regular.ttf", 32)

        # Badges and labels
        fonts['badge'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Bold.ttf", 48)
        fonts['arrow_label'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Italic.ttf", 28)

        # Warning section
        fonts['warning_icon'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Bold.ttf", 36)
        fonts['warning_title'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Bold.ttf", 32)
        fonts['warning_text'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Regular.ttf", 28)

        # Citation
        fonts['citation'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Regular.ttf", 24)

    except Exception as e:
        print(f"Font loading error: {e}")
        for key in fonts.keys():
            fonts[key] = ImageFont.load_default()

    return fonts

def draw_rounded_rect_smooth(draw, coords, radius, fill=None, outline=None, width=1):
    """Draw a smooth rounded rectangle with anti-aliasing consideration."""
    x1, y1, x2, y2 = coords
    diameter = radius * 2

    if fill:
        # Main rectangle body
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)

        # Corners
        draw.ellipse([x1, y1, x1 + diameter, y1 + diameter], fill=fill)
        draw.ellipse([x2 - diameter, y1, x2, y1 + diameter], fill=fill)
        draw.ellipse([x1, y2 - diameter, x1 + diameter, y2], fill=fill)
        draw.ellipse([x2 - diameter, y2 - diameter, x2, y2], fill=fill)

    if outline:
        # Draw outline arcs
        draw.arc([x1, y1, x1 + diameter, y1 + diameter], 180, 270, fill=outline, width=width)
        draw.arc([x2 - diameter, y1, x2, y1 + diameter], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - diameter, x1 + diameter, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - diameter, y2 - diameter, x2, y2], 0, 90, fill=outline, width=width)

        # Draw outline lines
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)

def draw_gradient_rect(img, coords, color_top, color_bottom, radius=0):
    """Draw a rectangle with vertical gradient."""
    x1, y1, x2, y2 = coords
    height = y2 - y1

    # Create gradient
    for i in range(int(height)):
        factor = i / height
        color = blend_colors(color_top, color_bottom, factor)
        img.line([(x1, y1 + i), (x2, y1 + i)], fill=color)

def draw_arrow_elegant(draw, start, end, color, width=4):
    """Draw an elegant arrow with refined proportions."""
    x1, y1 = start
    x2, y2 = end

    # Main line
    draw.line([x1, y1, x2, y2 - 8], fill=color, width=width)

    # Arrow head - more elegant proportions
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 24
    arrow_angle = math.pi / 7  # Narrower angle

    left_x = x2 - arrow_length * math.cos(angle - arrow_angle)
    left_y = y2 - arrow_length * math.sin(angle - arrow_angle)
    right_x = x2 - arrow_length * math.cos(angle + arrow_angle)
    right_y = y2 - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([(x2, y2), (left_x, left_y), (right_x, right_y)], fill=color)

def draw_level_block(draw, fonts, y_start, level_num, title, subtitle, boxes_content,
                    bg_color, gradient_color, box_color, text_color, subtext_color,
                    badge_bg, badge_text, margin, width):
    """Draw a complete level block with meticulous attention to spacing."""

    block_height = 360
    box_margin = 50
    content_width = width - 2 * margin
    box_spacing = 50
    box_width = (content_width - 2 * box_margin - 2 * box_spacing) // 3
    box_height = 140

    # Main container with gradient effect
    draw_rounded_rect_smooth(draw, [margin, y_start, width - margin, y_start + block_height],
                            32, fill=hex_to_rgb(bg_color))

    # Subtle gradient overlay at top
    for i in range(60):
        alpha_factor = 1 - (i / 60)
        overlay = blend_colors(gradient_color, bg_color, 1 - alpha_factor * 0.4)
        draw.line([margin + 32, y_start + i, width - margin - 32, y_start + i], fill=overlay)

    # Level title
    draw.text((margin + box_margin, y_start + 40), title,
              fill=hex_to_rgb(text_color), font=fonts['level_title'])

    # Subtitle
    draw.text((margin + box_margin, y_start + 110), subtitle,
              fill=hex_to_rgb(subtext_color), font=fonts['level_subtitle'])

    # Badge
    badge_x = width - margin - 120
    badge_y = y_start + 55
    badge_radius = 50

    draw.ellipse([badge_x - badge_radius, badge_y - badge_radius,
                  badge_x + badge_radius, badge_y + badge_radius],
                 fill=hex_to_rgb(badge_bg))

    badge_text_str = f"L{level_num}"
    bbox = draw.textbbox((0, 0), badge_text_str, font=fonts['badge'])
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text((badge_x - text_w // 2, badge_y - text_h // 2 - 5), badge_text_str,
              fill=hex_to_rgb(badge_text), font=fonts['badge'])

    # Content boxes
    box_y = y_start + 170

    for i, (line1, line2) in enumerate(boxes_content):
        box_x = margin + box_margin + i * (box_width + box_spacing)

        # Box background
        draw_rounded_rect_smooth(draw, [box_x, box_y, box_x + box_width, box_y + box_height],
                                20, fill=hex_to_rgb(box_color))

        # Text - centered
        bbox1 = draw.textbbox((0, 0), line1, font=fonts['content'])
        bbox2 = draw.textbbox((0, 0), line2, font=fonts['content_secondary'])

        text1_x = box_x + (box_width - (bbox1[2] - bbox1[0])) // 2
        text2_x = box_x + (box_width - (bbox2[2] - bbox2[0])) // 2

        draw.text((text1_x, box_y + 40), line1,
                 fill=hex_to_rgb(text_color), font=fonts['content'])
        draw.text((text2_x, box_y + 85), line2,
                 fill=hex_to_rgb(text_color), font=fonts['content_secondary'])

    return y_start + block_height

def create_aimc_framework_v2():
    """Create the refined AIMC Framework visualization - museum quality."""

    # Create high-resolution image
    img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(COLORS['background']))
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    # Layout constants
    MARGIN = 140
    CONTENT_WIDTH = WIDTH - 2 * MARGIN

    # Subtle background texture - fine grid lines
    for x in range(0, WIDTH, 80):
        draw.line([(x, 0), (x, HEIGHT)], fill=hex_to_rgb(COLORS['background_subtle']), width=1)
    for y in range(0, HEIGHT, 80):
        draw.line([(0, y), (WIDTH, y)], fill=hex_to_rgb(COLORS['background_subtle']), width=1)

    # ════════════════════════════════════════
    # HEADER
    # ════════════════════════════════════════
    header_y = 70
    header_height = 180

    draw_rounded_rect_smooth(draw, [MARGIN, header_y, WIDTH - MARGIN, header_y + header_height],
                            28, fill=hex_to_rgb(COLORS['header_primary']))

    # Title
    title = "AI-Integrated Metacognition (AIMC) Framework"
    bbox = draw.textbbox((0, 0), title, font=fonts['title'])
    title_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((title_x, header_y + 35), title,
              fill=hex_to_rgb(COLORS['header_text']), font=fonts['title'])

    # Subtitle
    subtitle = "Reconceptualizing Metacognition in AI-Augmented Learning Environments"
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((subtitle_x, header_y + 125), subtitle,
              fill=hex_to_rgb(COLORS['header_accent']), font=fonts['subtitle'])

    # ════════════════════════════════════════
    # LEVEL 3 - Independent Metacognition
    # ════════════════════════════════════════
    level3_y = 300
    level3_boxes = [
        ("Self-regulated learning", "without AI support"),
        ("Internalized monitoring", "& evaluation skills"),
        ("Transfer to novel contexts", "(Cognitive Dependency Test)")
    ]

    level3_end = draw_level_block(
        draw, fonts, level3_y, 3,
        "Level 3: Independent Metacognition",
        "(Without-AI Transfer)",
        level3_boxes,
        COLORS['level3_bg'], COLORS['level3_gradient'], COLORS['level3_box'],
        COLORS['level3_text'], COLORS['level3_subtext'],
        COLORS['level3_badge_bg'], COLORS['level3_badge_text'],
        MARGIN, WIDTH
    )

    # Arrow: L3 → L2
    arrow1_y1 = level3_end + 15
    arrow1_y2 = arrow1_y1 + 70
    draw_arrow_elegant(draw, (WIDTH // 2, arrow1_y1), (WIDTH // 2, arrow1_y2),
                       hex_to_rgb(COLORS['arrow']), 5)

    # Arrow label
    label = "Internalization"
    bbox = draw.textbbox((0, 0), label, font=fonts['arrow_label'])
    draw.text((WIDTH // 2 + 20, arrow1_y1 + 18), label,
              fill=hex_to_rgb(COLORS['arrow_label']), font=fonts['arrow_label'])

    # ════════════════════════════════════════
    # LEVEL 2 - Meta-AI Awareness
    # ════════════════════════════════════════
    level2_y = arrow1_y2 + 25
    level2_boxes = [
        ("Understanding AI", "capabilities & limitations"),
        ("Evaluating AI output", "reliability & accuracy"),
        ("Knowing when to use/", "not use AI assistance")
    ]

    level2_end = draw_level_block(
        draw, fonts, level2_y, 2,
        "Level 2: Meta-AI Awareness",
        "(About-AI Knowledge)",
        level2_boxes,
        COLORS['level2_bg'], COLORS['level2_gradient'], COLORS['level2_box'],
        COLORS['level2_text'], COLORS['level2_subtext'],
        COLORS['level2_badge_bg'], COLORS['level2_badge_text'],
        MARGIN, WIDTH
    )

    # Arrow: L2 → L1
    arrow2_y1 = level2_end + 15
    arrow2_y2 = arrow2_y1 + 70
    draw_arrow_elegant(draw, (WIDTH // 2, arrow2_y1), (WIDTH // 2, arrow2_y2),
                       hex_to_rgb(COLORS['arrow']), 5)

    # Arrow label
    label = "Reflection"
    bbox = draw.textbbox((0, 0), label, font=fonts['arrow_label'])
    draw.text((WIDTH // 2 + 20, arrow2_y1 + 18), label,
              fill=hex_to_rgb(COLORS['arrow_label']), font=fonts['arrow_label'])

    # ════════════════════════════════════════
    # LEVEL 1 - AI-Assisted Metacognition
    # ════════════════════════════════════════
    level1_y = arrow2_y2 + 25
    level1_boxes = [
        ("Prompt engineering", "as planning"),
        ("Output evaluation", "as monitoring"),
        ("Iterative refinement", "as self-regulation")
    ]

    level1_end = draw_level_block(
        draw, fonts, level1_y, 1,
        "Level 1: AI-Assisted Metacognition",
        "(With-AI Context)",
        level1_boxes,
        COLORS['level1_bg'], COLORS['level1_gradient'], COLORS['level1_box'],
        COLORS['level1_text'], COLORS['level1_subtext'],
        COLORS['level1_badge_bg'], COLORS['level1_badge_text'],
        MARGIN, WIDTH
    )

    # ════════════════════════════════════════
    # KEY FINDING BOX
    # ════════════════════════════════════════
    warning_y = level1_end + 50
    warning_height = 130

    draw_rounded_rect_smooth(draw, [MARGIN, warning_y, WIDTH - MARGIN, warning_y + warning_height],
                            20, fill=hex_to_rgb(COLORS['warning_bg']),
                            outline=hex_to_rgb(COLORS['warning_border']), width=4)

    # Warning icon and title
    icon_text = "⚠"
    draw.text((MARGIN + 50, warning_y + 25), "Key Finding",
              fill=hex_to_rgb(COLORS['warning_title']), font=fonts['warning_title'])

    # Warning content
    line1 = "Current evidence primarily assesses Level 1. The Cognitive Dependency Hypothesis predicts"
    line2 = "divergent effects at Level 3 (independent metacognition transferable to AI-absent contexts)."

    bbox1 = draw.textbbox((0, 0), line1, font=fonts['warning_text'])
    bbox2 = draw.textbbox((0, 0), line2, font=fonts['warning_text'])

    center_x1 = (WIDTH - (bbox1[2] - bbox1[0])) // 2
    center_x2 = (WIDTH - (bbox2[2] - bbox2[0])) // 2

    draw.text((center_x1, warning_y + 40), line1,
              fill=hex_to_rgb(COLORS['warning_text']), font=fonts['warning_text'])
    draw.text((center_x2, warning_y + 80), line2,
              fill=hex_to_rgb(COLORS['warning_text']), font=fonts['warning_text'])

    # ════════════════════════════════════════
    # CITATION
    # ════════════════════════════════════════
    citation = "You, H. (2026). Generative AI in Higher Education: A Three-Level Meta-Analysis. Pennsylvania State University"
    bbox = draw.textbbox((0, 0), citation, font=fonts['citation'])
    citation_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((citation_x, HEIGHT - 80), citation,
              fill=hex_to_rgb(COLORS['citation']), font=fonts['citation'])

    # ════════════════════════════════════════
    # SAVE OUTPUTS
    # ════════════════════════════════════════

    # Save PNG (high quality)
    png_path = os.path.join(OUTPUT_DIR, "AIMC_Framework.png")
    img.save(png_path, 'PNG', dpi=(DPI, DPI))
    print(f"✅ Saved PNG: {png_path}")

    # Save PDF
    pdf_path = os.path.join(OUTPUT_DIR, "AIMC_Framework.pdf")
    img.save(pdf_path, 'PDF', resolution=DPI)
    print(f"✅ Saved PDF: {pdf_path}")

    # Save smaller version for web/preview
    img_small = img.resize((1600, 1200), Image.Resampling.LANCZOS)
    preview_path = os.path.join(OUTPUT_DIR, "AIMC_Framework_preview.png")
    img_small.save(preview_path, 'PNG', dpi=(150, 150))
    print(f"✅ Saved preview: {preview_path}")

    return png_path

if __name__ == "__main__":
    create_aimc_framework_v2()
