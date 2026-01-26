#!/usr/bin/env python3
"""
AIMC Framework - Professional Academic Visualization
Design Philosophy: Cognitive Stratification
Author: Hosung You, Pennsylvania State University
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

# Configuration
WIDTH = 2400
HEIGHT = 1800
DPI = 300
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Font paths
FONT_DIR = "/Users/hosung/.claude/plugins/cache/anthropic-agent-skills/example-skills/c74d647e56e6/canvas-design/canvas-fonts"

# Color Palette - Cognitive Stratification
COLORS = {
    'background': '#FAFBFC',
    'header_dark': '#1A1F36',
    'header_accent': '#2D3561',

    # Level 3 - Amethyst Transcendence
    'level3_primary': '#7C3AED',
    'level3_secondary': '#5B21B6',
    'level3_accent': '#DDD6FE',
    'level3_text': '#FFFFFF',

    # Level 2 - Cerulean Awareness
    'level2_primary': '#2563EB',
    'level2_secondary': '#1D4ED8',
    'level2_accent': '#BFDBFE',
    'level2_text': '#FFFFFF',

    # Level 1 - Verdant Emergence
    'level1_primary': '#059669',
    'level1_secondary': '#047857',
    'level1_accent': '#A7F3D0',
    'level1_text': '#FFFFFF',

    # Warning Zone
    'warning_bg': '#FEF3C7',
    'warning_border': '#F59E0B',
    'warning_text': '#92400E',

    # Neutral
    'arrow': '#6B7280',
    'label_dark': '#374151',
    'label_light': '#9CA3AF',
    'divider': '#E5E7EB',
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def load_fonts():
    """Load fonts with fallbacks."""
    fonts = {}
    try:
        # Title fonts
        fonts['title'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Bold.ttf", 72)
        fonts['subtitle'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Regular.ttf", 32)

        # Level fonts
        fonts['level_title'] = ImageFont.truetype(f"{FONT_DIR}/WorkSans-Bold.ttf", 48)
        fonts['level_subtitle'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Regular.ttf", 24)
        fonts['content'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Regular.ttf", 28)
        fonts['content_bold'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Bold.ttf", 28)

        # Labels and annotations
        fonts['badge'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Bold.ttf", 36)
        fonts['label'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Regular.ttf", 20)
        fonts['arrow_label'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Italic.ttf", 22)

        # Warning and citation
        fonts['warning'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Bold.ttf", 24)
        fonts['warning_text'] = ImageFont.truetype(f"{FONT_DIR}/InstrumentSans-Regular.ttf", 22)
        fonts['citation'] = ImageFont.truetype(f"{FONT_DIR}/IBMPlexMono-Regular.ttf", 18)

    except Exception as e:
        print(f"Font loading error: {e}")
        # Fallback to default
        for key in ['title', 'subtitle', 'level_title', 'level_subtitle', 'content',
                    'content_bold', 'badge', 'label', 'arrow_label', 'warning',
                    'warning_text', 'citation']:
            fonts[key] = ImageFont.load_default()

    return fonts

def draw_rounded_rect(draw, coords, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = coords

    if fill:
        # Draw filled rounded rectangle
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
        draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)

    if outline:
        # Draw outline
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)

def draw_arrow(draw, start, end, color, width=3):
    """Draw an arrow with head."""
    x1, y1 = start
    x2, y2 = end

    # Draw line
    draw.line([x1, y1, x2, y2], fill=color, width=width)

    # Calculate arrow head
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 20
    arrow_angle = math.pi / 6

    # Arrow head points
    left_x = x2 - arrow_length * math.cos(angle - arrow_angle)
    left_y = y2 - arrow_length * math.sin(angle - arrow_angle)
    right_x = x2 - arrow_length * math.cos(angle + arrow_angle)
    right_y = y2 - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([(x2, y2), (left_x, left_y), (right_x, right_y)], fill=color)

def draw_content_box(draw, x, y, width, height, texts, fonts, bg_color, text_color):
    """Draw a content box with text."""
    draw_rounded_rect(draw, [x, y, x + width, y + height], 12,
                     fill=bg_color)

    # Center text vertically
    total_text_height = len(texts) * 34
    start_y = y + (height - total_text_height) // 2

    for i, text in enumerate(texts):
        bbox = draw.textbbox((0, 0), text, font=fonts['content'])
        text_width = bbox[2] - bbox[0]
        text_x = x + (width - text_width) // 2
        draw.text((text_x, start_y + i * 34), text, fill=text_color, font=fonts['content'])

def create_aimc_framework():
    """Create the AIMC Framework visualization."""
    # Create image
    img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(COLORS['background']))
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    # Margins and spacing
    MARGIN = 100
    CONTENT_WIDTH = WIDTH - 2 * MARGIN

    # === HEADER ===
    header_height = 140
    draw_rounded_rect(draw, [MARGIN, 50, WIDTH - MARGIN, 50 + header_height], 20,
                     fill=hex_to_rgb(COLORS['header_dark']))

    # Title
    title = "AI-Integrated Metacognition (AIMC) Framework"
    bbox = draw.textbbox((0, 0), title, font=fonts['title'])
    title_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((title_x, 75), title, fill=hex_to_rgb('#FFFFFF'), font=fonts['title'])

    # Subtitle
    subtitle = "Reconceptualizing Metacognition in AI-Augmented Learning Environments"
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((subtitle_x, 145), subtitle, fill=hex_to_rgb('#94A3B8'), font=fonts['subtitle'])

    # === LEVEL 3 - Independent Metacognition ===
    level3_y = 230
    level3_height = 280

    # Main container
    draw_rounded_rect(draw, [MARGIN, level3_y, WIDTH - MARGIN, level3_y + level3_height], 24,
                     fill=hex_to_rgb(COLORS['level3_primary']))

    # Gradient overlay effect (darker at top)
    for i in range(40):
        alpha = int(255 * (1 - i/40) * 0.3)
        overlay_color = (91, 33, 182, alpha)  # level3_secondary with alpha
        draw.line([MARGIN + 24, level3_y + i, WIDTH - MARGIN - 24, level3_y + i],
                  fill=hex_to_rgb(COLORS['level3_secondary']))

    # Level title
    draw.text((MARGIN + 40, level3_y + 30), "Level 3: Independent Metacognition",
              fill=hex_to_rgb(COLORS['level3_text']), font=fonts['level_title'])
    draw.text((MARGIN + 40, level3_y + 85), "(Without-AI Transfer)",
              fill=hex_to_rgb(COLORS['level3_accent']), font=fonts['level_subtitle'])

    # Badge
    badge_x = WIDTH - MARGIN - 100
    badge_y = level3_y + 35
    draw.ellipse([badge_x - 40, badge_y - 40, badge_x + 40, badge_y + 40],
                 fill=hex_to_rgb(COLORS['level3_accent']))
    draw.text((badge_x - 22, badge_y - 18), "L3",
              fill=hex_to_rgb(COLORS['level3_secondary']), font=fonts['badge'])

    # Content boxes
    box_y = level3_y + 130
    box_height = 120
    box_spacing = 40
    box_width = (CONTENT_WIDTH - 80 - 2 * box_spacing) // 3

    content_bg = (255, 255, 255, 40)  # Semi-transparent white

    boxes_l3 = [
        ["Self-regulated learning", "without AI support"],
        ["Internalized monitoring", "& evaluation skills"],
        ["Transfer to novel contexts", "(Cognitive Dependency Test)"]
    ]

    for i, texts in enumerate(boxes_l3):
        box_x = MARGIN + 40 + i * (box_width + box_spacing)
        draw_rounded_rect(draw, [box_x, box_y, box_x + box_width, box_y + box_height], 16,
                         fill=hex_to_rgb('#8B5CF6'))  # Lighter purple
        for j, text in enumerate(texts):
            bbox = draw.textbbox((0, 0), text, font=fonts['content'])
            text_width = bbox[2] - bbox[0]
            text_x = box_x + (box_width - text_width) // 2
            draw.text((text_x, box_y + 35 + j * 36), text,
                     fill=hex_to_rgb(COLORS['level3_text']), font=fonts['content'])

    # === ARROW L3 to L2 ===
    arrow_y1 = level3_y + level3_height + 10
    arrow_y2 = arrow_y1 + 50
    draw_arrow(draw, (WIDTH // 2, arrow_y1), (WIDTH // 2, arrow_y2),
               hex_to_rgb(COLORS['arrow']), 4)
    draw.text((WIDTH // 2 + 20, arrow_y1 + 10), "Internalization",
              fill=hex_to_rgb(COLORS['label_dark']), font=fonts['arrow_label'])

    # === LEVEL 2 - Meta-AI Awareness ===
    level2_y = arrow_y2 + 20
    level2_height = 280

    draw_rounded_rect(draw, [MARGIN, level2_y, WIDTH - MARGIN, level2_y + level2_height], 24,
                     fill=hex_to_rgb(COLORS['level2_primary']))

    # Level title
    draw.text((MARGIN + 40, level2_y + 30), "Level 2: Meta-AI Awareness",
              fill=hex_to_rgb(COLORS['level2_text']), font=fonts['level_title'])
    draw.text((MARGIN + 40, level2_y + 85), "(About-AI Knowledge)",
              fill=hex_to_rgb(COLORS['level2_accent']), font=fonts['level_subtitle'])

    # Badge
    badge_y = level2_y + 35
    draw.ellipse([badge_x - 40, badge_y - 40, badge_x + 40, badge_y + 40],
                 fill=hex_to_rgb(COLORS['level2_accent']))
    draw.text((badge_x - 22, badge_y - 18), "L2",
              fill=hex_to_rgb(COLORS['level2_secondary']), font=fonts['badge'])

    # Content boxes
    box_y = level2_y + 130
    boxes_l2 = [
        ["Understanding AI", "capabilities & limitations"],
        ["Evaluating AI output", "reliability & accuracy"],
        ["Knowing when to use/", "not use AI assistance"]
    ]

    for i, texts in enumerate(boxes_l2):
        box_x = MARGIN + 40 + i * (box_width + box_spacing)
        draw_rounded_rect(draw, [box_x, box_y, box_x + box_width, box_y + box_height], 16,
                         fill=hex_to_rgb('#3B82F6'))  # Lighter blue
        for j, text in enumerate(texts):
            bbox = draw.textbbox((0, 0), text, font=fonts['content'])
            text_width = bbox[2] - bbox[0]
            text_x = box_x + (box_width - text_width) // 2
            draw.text((text_x, box_y + 35 + j * 36), text,
                     fill=hex_to_rgb(COLORS['level2_text']), font=fonts['content'])

    # === ARROW L2 to L1 ===
    arrow_y1 = level2_y + level2_height + 10
    arrow_y2 = arrow_y1 + 50
    draw_arrow(draw, (WIDTH // 2, arrow_y1), (WIDTH // 2, arrow_y2),
               hex_to_rgb(COLORS['arrow']), 4)
    draw.text((WIDTH // 2 + 20, arrow_y1 + 10), "Reflection",
              fill=hex_to_rgb(COLORS['label_dark']), font=fonts['arrow_label'])

    # === LEVEL 1 - AI-Assisted Metacognition ===
    level1_y = arrow_y2 + 20
    level1_height = 280

    draw_rounded_rect(draw, [MARGIN, level1_y, WIDTH - MARGIN, level1_y + level1_height], 24,
                     fill=hex_to_rgb(COLORS['level1_primary']))

    # Level title
    draw.text((MARGIN + 40, level1_y + 30), "Level 1: AI-Assisted Metacognition",
              fill=hex_to_rgb(COLORS['level1_text']), font=fonts['level_title'])
    draw.text((MARGIN + 40, level1_y + 85), "(With-AI Context)",
              fill=hex_to_rgb(COLORS['level1_accent']), font=fonts['level_subtitle'])

    # Badge
    badge_y = level1_y + 35
    draw.ellipse([badge_x - 40, badge_y - 40, badge_x + 40, badge_y + 40],
                 fill=hex_to_rgb(COLORS['level1_accent']))
    draw.text((badge_x - 22, badge_y - 18), "L1",
              fill=hex_to_rgb(COLORS['level1_secondary']), font=fonts['badge'])

    # Content boxes
    box_y = level1_y + 130
    boxes_l1 = [
        ["Prompt engineering", "as planning"],
        ["Output evaluation", "as monitoring"],
        ["Iterative refinement", "as self-regulation"]
    ]

    for i, texts in enumerate(boxes_l1):
        box_x = MARGIN + 40 + i * (box_width + box_spacing)
        draw_rounded_rect(draw, [box_x, box_y, box_x + box_width, box_y + box_height], 16,
                         fill=hex_to_rgb('#10B981'))  # Lighter green
        for j, text in enumerate(texts):
            bbox = draw.textbbox((0, 0), text, font=fonts['content'])
            text_width = bbox[2] - bbox[0]
            text_x = box_x + (box_width - text_width) // 2
            draw.text((text_x, box_y + 35 + j * 36), text,
                     fill=hex_to_rgb(COLORS['level1_text']), font=fonts['content'])

    # === KEY FINDING BOX ===
    warning_y = level1_y + level1_height + 40
    warning_height = 100

    draw_rounded_rect(draw, [MARGIN, warning_y, WIDTH - MARGIN, warning_y + warning_height], 16,
                     fill=hex_to_rgb(COLORS['warning_bg']),
                     outline=hex_to_rgb(COLORS['warning_border']), width=3)

    # Warning icon and text
    warning_title = "⚠ Key Finding"
    draw.text((MARGIN + 40, warning_y + 20), warning_title,
              fill=hex_to_rgb(COLORS['warning_text']), font=fonts['warning'])

    warning_line1 = "Current evidence primarily assesses Level 1. The Cognitive Dependency Hypothesis"
    warning_line2 = "predicts divergent effects at Level 3 (independent metacognition transferable to AI-absent contexts)."

    bbox1 = draw.textbbox((0, 0), warning_line1, font=fonts['warning_text'])
    bbox2 = draw.textbbox((0, 0), warning_line2, font=fonts['warning_text'])

    draw.text(((WIDTH - (bbox1[2] - bbox1[0])) // 2, warning_y + 25), warning_line1,
              fill=hex_to_rgb(COLORS['warning_text']), font=fonts['warning_text'])
    draw.text(((WIDTH - (bbox2[2] - bbox2[0])) // 2, warning_y + 58), warning_line2,
              fill=hex_to_rgb(COLORS['warning_text']), font=fonts['warning_text'])

    # === CITATION ===
    citation = "You, H. (2026). Generative AI in Higher Education: A Three-Level Meta-Analysis. Pennsylvania State University"
    bbox = draw.textbbox((0, 0), citation, font=fonts['citation'])
    citation_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((citation_x, HEIGHT - 60), citation,
              fill=hex_to_rgb(COLORS['label_light']), font=fonts['citation'])

    # === SAVE ===
    output_path = os.path.join(OUTPUT_DIR, "AIMC_Framework.png")
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"✅ Saved: {output_path}")

    # Also save as PDF
    pdf_path = os.path.join(OUTPUT_DIR, "AIMC_Framework.pdf")
    img.save(pdf_path, 'PDF', resolution=DPI)
    print(f"✅ Saved: {pdf_path}")

    return output_path

if __name__ == "__main__":
    create_aimc_framework()
