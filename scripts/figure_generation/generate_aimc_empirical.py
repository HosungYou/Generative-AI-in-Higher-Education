#!/usr/bin/env python3
"""
Cognitive Dependency Framework - Empirical Synthesis Visualization
Design Philosophy: Scientific illustration meets data cartography

This visualization integrates:
1. Theoretical convergence from six distinct frameworks
2. Empirical effect sizes with confidence intervals
3. The AIMC three-level progression model
4. Evidence gaps as meaningful visual negative space

Author: Hosung You, Pennsylvania State University
Target: Educational Psychology Review
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas Configuration
WIDTH = 3600
HEIGHT = 2700
DPI = 300
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Meta-analytic Findings
DATA = {
    'overall': {'g': 0.622, 'ci_low': 0.389, 'ci_high': 0.855, 'p': '<.001', 'sig': True},
    'cognitive': {'g': 0.64, 'ci_low': 0.42, 'ci_high': 0.86, 'p': '<.001', 'sig': True},
    'affective': {'g': 0.61, 'ci_low': 0.29, 'ci_high': 0.93, 'p': '<.001', 'sig': True},
    'metacognitive': {'g': 0.28, 'ci_low': -0.24, 'ci_high': 0.80, 'p': '.287', 'sig': False},
    'studies': 65,
    'effects': 381,
    'N': 8247,
}

# Refined Color Palette
PALETTE = {
    # Canvas tones
    'bg': '#FAFAF8',
    'panel_light': '#FFFFFF',
    'panel_accent': '#F8F6F2',
    'grid': '#ECEAE4',

    # Semantic colors
    'sig_positive': '#2E7D32',      # Significant positive
    'sig_positive_light': '#C8E6C9',
    'non_sig': '#78909C',           # Non-significant
    'non_sig_light': '#ECEFF1',
    'warning': '#E65100',           # Attention/gap
    'warning_light': '#FFE0B2',

    # Theory colors
    'clt': '#1565C0',    # Cognitive Load
    'ddt': '#2E7D32',    # Desirable Difficulties
    'srl': '#6A1B9A',    # Self-Regulated Learning
    'sdt': '#00695C',    # Self-Determination
    'sct': '#4527A0',    # Sociocultural
    'ab': '#BF360C',     # Automation Bias

    # Typography
    'text_dark': '#263238',
    'text_medium': '#546E7A',
    'text_light': '#90A4AE',

    # AIMC levels
    'level1': '#81C784',
    'level2': '#64B5F6',
    'level3': '#BA68C8',
}

def hex_to_rgb(h):
    """Convert hex to RGB tuple"""
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_font(size):
    """Load system font with fallback"""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSText.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def rounded_rect(draw, box, radius, **kwargs):
    """Draw rounded rectangle with proper corners"""
    x1, y1, x2, y2 = box
    fill = kwargs.get('fill')
    outline = kwargs.get('outline')
    width = kwargs.get('width', 1)

    if fill:
        draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
        draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
        draw.ellipse([x1, y1, x1+2*radius, y1+2*radius], fill=fill)
        draw.ellipse([x2-2*radius, y1, x2, y1+2*radius], fill=fill)
        draw.ellipse([x1, y2-2*radius, x1+2*radius, y2], fill=fill)
        draw.ellipse([x2-2*radius, y2-2*radius, x2, y2], fill=fill)
    if outline:
        draw.arc([x1, y1, x1+2*radius, y1+2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2-2*radius, y1, x2, y1+2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-2*radius, x1+2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-2*radius, y2-2*radius, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+radius, y1, x2-radius, y1], fill=outline, width=width)
        draw.line([x1+radius, y2, x2-radius, y2], fill=outline, width=width)
        draw.line([x1, y1+radius, x1, y2-radius], fill=outline, width=width)
        draw.line([x2, y1+radius, x2, y2-radius], fill=outline, width=width)

def draw_arrow(draw, start, end, color, width=2, arrow_size=12, dashed=False):
    """Draw arrow with optional dashing"""
    x1, y1 = start
    x2, y2 = end
    angle = math.atan2(y2-y1, x2-x1)

    if dashed:
        length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        dash, gap = 8, 6
        segments = int(length / (dash + gap))
        dx, dy = (x2-x1)/length, (y2-y1)/length
        for i in range(segments):
            s = i * (dash + gap)
            e = s + dash
            draw.line([x1+dx*s, y1+dy*s, x1+dx*e, y1+dy*e], fill=color, width=width)
    else:
        draw.line([x1, y1, x2, y2], fill=color, width=width)

    # Arrowhead
    a1 = (x2 - arrow_size*math.cos(angle - 0.4), y2 - arrow_size*math.sin(angle - 0.4))
    a2 = (x2 - arrow_size*math.cos(angle + 0.4), y2 - arrow_size*math.sin(angle + 0.4))
    draw.polygon([(x2, y2), a1, a2], fill=color)

def draw_theory_circle(draw, cx, cy, r, color, label, sublabel, font_main, font_sub):
    """Draw a theory node with subtle gradient effect"""
    # Outer glow simulation
    for i in range(4):
        alpha_r = r + (4-i)*6
        alpha = 60 + i*20
        draw.ellipse([cx-alpha_r, cy-alpha_r, cx+alpha_r, cy+alpha_r],
                     fill=(*hex_to_rgb(color), alpha) if hasattr(draw, '_image') else hex_to_rgb(color))

    # Main circle
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=hex_to_rgb(color))

    # White inner ring
    inner_r = r - 6
    draw.ellipse([cx-inner_r, cy-inner_r, cx+inner_r, cy+inner_r],
                 outline=hex_to_rgb('#FFFFFF'), width=2)

    # Labels
    draw.text((cx, cy-10), label, font=font_main, fill=hex_to_rgb('#FFFFFF'), anchor='mm')
    draw.text((cx, cy+15), sublabel, font=font_sub, fill=hex_to_rgb('#FFFFFF'), anchor='mm')

def draw_effect_bar(draw, x, y, w, h, data, label, fonts):
    """Draw horizontal effect size bar with CI whiskers"""
    font_label, font_val, font_ci = fonts
    g, ci_lo, ci_hi, sig = data['g'], data['ci_low'], data['ci_high'], data['sig']

    # Scale: -0.5 to 1.5
    scale = lambda v: x + ((v + 0.5) / 2.0) * w

    # Track background
    draw.rectangle([x, y+h//2-3, x+w, y+h//2+3], fill=hex_to_rgb(PALETTE['grid']))

    # Zero line
    zero_x = scale(0)
    draw.line([zero_x, y+10, zero_x, y+h-10], fill=hex_to_rgb(PALETTE['text_light']), width=2)
    draw.text((zero_x, y+h+8), "0", font=font_ci, fill=hex_to_rgb(PALETTE['text_light']), anchor='mt')

    # Color based on significance
    bar_color = PALETTE['sig_positive'] if sig else PALETTE['non_sig']
    bar_bg = PALETTE['sig_positive_light'] if sig else PALETTE['non_sig_light']

    # CI bar
    ci_x1, ci_x2 = scale(ci_lo), scale(ci_hi)
    draw.rectangle([ci_x1, y+h//2-12, ci_x2, y+h//2+12], fill=hex_to_rgb(bar_bg))
    draw.rectangle([ci_x1, y+h//2-12, ci_x2, y+h//2+12], outline=hex_to_rgb(bar_color), width=2)

    # Effect size diamond
    g_x = scale(g)
    diamond = [(g_x, y+h//2-14), (g_x+10, y+h//2), (g_x, y+h//2+14), (g_x-10, y+h//2)]
    draw.polygon(diamond, fill=hex_to_rgb(bar_color))

    # CI whiskers
    draw.line([ci_x1, y+h//2-8, ci_x1, y+h//2+8], fill=hex_to_rgb(bar_color), width=3)
    draw.line([ci_x2, y+h//2-8, ci_x2, y+h//2+8], fill=hex_to_rgb(bar_color), width=3)

    # Label (left)
    draw.text((x-20, y+h//2), label, font=font_label, fill=hex_to_rgb(PALETTE['text_dark']), anchor='rm')

    # Values (right)
    sig_str = "p " + data['p']
    val_str = f"g = {g:.2f} [{ci_lo:.2f}, {ci_hi:.2f}]"
    draw.text((x+w+20, y+h//2-12), val_str, font=font_val, fill=hex_to_rgb(bar_color), anchor='lm')
    draw.text((x+w+20, y+h//2+14), sig_str, font=font_ci, fill=hex_to_rgb(PALETTE['text_medium']), anchor='lm')

def create_visualization():
    """Generate the complete framework visualization"""
    img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(PALETTE['bg']))
    draw = ImageDraw.Draw(img)

    # Fonts
    f_title = get_font(64)
    f_subtitle = get_font(36)
    f_section = get_font(44)
    f_body = get_font(32)
    f_small = get_font(26)
    f_tiny = get_font(22)
    f_label = get_font(28)

    # ═══════════════════════════════════════════════════════════════
    # HEADER
    # ═══════════════════════════════════════════════════════════════
    draw.text((WIDTH//2, 55), "The Cognitive Dependency Framework",
              font=f_title, fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')
    draw.text((WIDTH//2, 125), "Theoretical Convergence and Meta-Analytic Evidence for AI-Induced Metacognitive Compromise",
              font=f_subtitle, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')

    # Study badge
    badge_y = 180
    rounded_rect(draw, (WIDTH//2-450, badge_y, WIDTH//2+450, badge_y+50), 25,
                 fill=hex_to_rgb('#E3F2FD'), outline=hex_to_rgb('#1565C0'), width=2)
    badge_text = f"Meta-Analysis: k = {DATA['studies']}  •  {DATA['effects']} effect sizes  •  N = {DATA['N']:,}  •  Nov 2022 – Jan 2026"
    draw.text((WIDTH//2, badge_y+25), badge_text, font=f_small, fill=hex_to_rgb('#1565C0'), anchor='mm')

    # ═══════════════════════════════════════════════════════════════
    # SECTION A: THEORETICAL CONVERGENCE (Left Panel)
    # ═══════════════════════════════════════════════════════════════
    panel_a_x, panel_a_y = 80, 280
    panel_a_w, panel_a_h = 1100, 900

    # Panel background
    rounded_rect(draw, (panel_a_x, panel_a_y, panel_a_x+panel_a_w, panel_a_y+panel_a_h), 20,
                 fill=hex_to_rgb(PALETTE['panel_light']), outline=hex_to_rgb(PALETTE['grid']), width=2)

    draw.text((panel_a_x+panel_a_w//2, panel_a_y+35), "A. Theoretical Convergence",
              font=f_section, fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')
    draw.text((panel_a_x+panel_a_w//2, panel_a_y+80), "Six frameworks predict attenuated metacognitive effects",
              font=f_small, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')

    # Theory nodes in hexagonal arrangement
    center_x = panel_a_x + panel_a_w//2
    center_y = panel_a_y + 420
    orbit_r = 220
    node_r = 55

    theories = [
        ('CLT', 'Cognitive Load', PALETTE['clt']),
        ('DDT', 'Desirable Diff.', PALETTE['ddt']),
        ('SRL', 'Self-Regulated', PALETTE['srl']),
        ('SDT', 'Self-Determ.', PALETTE['sdt']),
        ('SCT', 'Sociocultural', PALETTE['sct']),
        ('AB', 'Automation Bias', PALETTE['ab']),
    ]

    node_positions = []
    for i, (abbr, name, color) in enumerate(theories):
        angle = (i * 2 * math.pi / len(theories)) - math.pi/2
        nx = center_x + orbit_r * math.cos(angle)
        ny = center_y + orbit_r * math.sin(angle)
        node_positions.append((nx, ny))
        draw_theory_circle(draw, nx, ny, node_r, color, abbr, name.split()[0], f_label, f_tiny)

    # Central convergence node
    central_r = 65
    draw.ellipse([center_x-central_r-8, center_y-central_r-8, center_x+central_r+8, center_y+central_r+8],
                 fill=hex_to_rgb('#FFE0B2'))
    draw.ellipse([center_x-central_r, center_y-central_r, center_x+central_r, center_y+central_r],
                 fill=hex_to_rgb(PALETTE['warning']))
    draw.text((center_x, center_y-12), "Cognitive", font=f_label, fill=hex_to_rgb('#FFFFFF'), anchor='mm')
    draw.text((center_x, center_y+12), "Dependency", font=f_label, fill=hex_to_rgb('#FFFFFF'), anchor='mm')

    # Connecting lines
    for nx, ny in node_positions:
        draw_arrow(draw, (nx, ny), (center_x, center_y), hex_to_rgb(PALETTE['text_light']), width=2, dashed=True)

    # Key prediction box
    pred_y = panel_a_y + panel_a_h - 200
    rounded_rect(draw, (panel_a_x+60, pred_y, panel_a_x+panel_a_w-60, pred_y+160), 15,
                 fill=hex_to_rgb(PALETTE['warning_light']), outline=hex_to_rgb(PALETTE['warning']), width=2)
    draw.text((panel_a_x+panel_a_w//2, pred_y+25), "A Priori Hypothesis (H3)",
              font=f_body, fill=hex_to_rgb(PALETTE['warning']), anchor='mt')
    pred_lines = [
        "Metacognitive outcomes will show smaller effects",
        "than other dimensions, reflecting cognitive dependency"
    ]
    for i, line in enumerate(pred_lines):
        draw.text((panel_a_x+panel_a_w//2, pred_y+70+i*30), line, font=f_small,
                  fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')

    # ═══════════════════════════════════════════════════════════════
    # SECTION B: EMPIRICAL EVIDENCE (Right Panel)
    # ═══════════════════════════════════════════════════════════════
    panel_b_x, panel_b_y = 1280, 280
    panel_b_w, panel_b_h = 1100, 900

    rounded_rect(draw, (panel_b_x, panel_b_y, panel_b_x+panel_b_w, panel_b_y+panel_b_h), 20,
                 fill=hex_to_rgb(PALETTE['panel_light']), outline=hex_to_rgb(PALETTE['grid']), width=2)

    draw.text((panel_b_x+panel_b_w//2, panel_b_y+35), "B. Meta-Analytic Evidence",
              font=f_section, fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')
    draw.text((panel_b_x+panel_b_w//2, panel_b_y+80), "Three-level random effects model with robust variance estimation",
              font=f_small, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')

    # Forest plot area
    forest_x = panel_b_x + 200
    forest_y = panel_b_y + 160
    forest_w = 520
    bar_h = 70

    outcomes = [
        ('Overall Effect', DATA['overall']),
        ('Cognitive', DATA['cognitive']),
        ('Affective', DATA['affective']),
        ('Metacognitive', DATA['metacognitive']),
    ]

    for i, (label, data) in enumerate(outcomes):
        y = forest_y + i * (bar_h + 35)
        draw_effect_bar(draw, forest_x, y, forest_w, bar_h, data, label, (f_body, f_small, f_tiny))

        # Highlight metacognitive
        if label == 'Metacognitive':
            rounded_rect(draw, (forest_x-180, y-10, panel_b_x+panel_b_w-40, y+bar_h+10), 10,
                         outline=hex_to_rgb(PALETTE['warning']), width=3)

    # Scale markers
    scale_y = forest_y + len(outcomes) * (bar_h + 35) + 20
    for val, lbl in [(-0.5, '-0.5'), (0.5, '0.5'), (1.0, '1.0'), (1.5, '1.5')]:
        sx = forest_x + ((val + 0.5) / 2.0) * forest_w
        draw.text((sx, scale_y), lbl, font=f_tiny, fill=hex_to_rgb(PALETTE['text_light']), anchor='mt')
    draw.text((forest_x + forest_w//2, scale_y+25), "Hedges' g (95% CI)",
              font=f_tiny, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')

    # Key finding box
    find_y = panel_b_y + panel_b_h - 260
    rounded_rect(draw, (panel_b_x+60, find_y, panel_b_x+panel_b_w-60, find_y+220), 15,
                 fill=hex_to_rgb('#FFEBEE'), outline=hex_to_rgb(PALETTE['warning']), width=3)
    draw.text((panel_b_x+panel_b_w//2, find_y+25), "Critical Finding",
              font=f_body, fill=hex_to_rgb(PALETTE['warning']), anchor='mt')

    findings = [
        "Metacognitive outcomes: g = 0.28 [−0.24, 0.80]",
        "Confidence interval crosses zero → non-significant",
        "Pattern consistent with cognitive dependency hypothesis",
        "GRADE certainty: Very Low (serious imprecision)"
    ]
    for i, line in enumerate(findings):
        draw.text((panel_b_x+panel_b_w//2, find_y+70+i*35), line, font=f_small,
                  fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')

    # ═══════════════════════════════════════════════════════════════
    # CONNECTING ARROW (Center)
    # ═══════════════════════════════════════════════════════════════
    arrow_y = panel_a_y + panel_a_h//2
    draw_arrow(draw, (panel_a_x+panel_a_w+30, arrow_y), (panel_b_x-30, arrow_y),
               hex_to_rgb(PALETTE['clt']), width=5, arrow_size=18)
    draw.text((panel_a_x+panel_a_w+100, arrow_y-35), "Empirical", font=f_body,
              fill=hex_to_rgb(PALETTE['clt']), anchor='mm')
    draw.text((panel_a_x+panel_a_w+100, arrow_y+35), "Test", font=f_body,
              fill=hex_to_rgb(PALETTE['clt']), anchor='mm')

    # ═══════════════════════════════════════════════════════════════
    # RIGHT SIDEBAR: Evidence Synthesis
    # ═══════════════════════════════════════════════════════════════
    sidebar_x = 2480
    sidebar_y = 280
    sidebar_w = 1030
    sidebar_h = 900

    rounded_rect(draw, (sidebar_x, sidebar_y, sidebar_x+sidebar_w, sidebar_y+sidebar_h), 20,
                 fill=hex_to_rgb(PALETTE['panel_accent']), outline=hex_to_rgb(PALETTE['grid']), width=2)

    draw.text((sidebar_x+sidebar_w//2, sidebar_y+35), "C. Evidence Synthesis",
              font=f_section, fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')

    # Interpretation bullets
    interp_y = sidebar_y + 100
    interpretations = [
        ("✓", "Cognitive & affective: consistent benefits", PALETTE['sig_positive']),
        ("✓", "GenAI enhances immediate performance", PALETTE['sig_positive']),
        ("△", "Behavioral: limited evidence (k=16)", PALETTE['text_medium']),
        ("✗", "Metacognitive: non-significant effect", PALETTE['warning']),
        ("✗", "Independent self-regulation not developed", PALETTE['warning']),
    ]

    for i, (icon, text, color) in enumerate(interpretations):
        iy = interp_y + i * 55
        draw.text((sidebar_x+50, iy), icon, font=f_body, fill=hex_to_rgb(color))
        draw.text((sidebar_x+90, iy), text, font=f_small, fill=hex_to_rgb(PALETTE['text_dark']))

    # Moderator analysis mini-table
    mod_y = interp_y + len(interpretations) * 55 + 40
    draw.text((sidebar_x+sidebar_w//2, mod_y), "Selected Moderators", font=f_body,
              fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')

    mods = [
        ("Bloom's Lower-Order", "g = 0.81***"),
        ("Bloom's Higher-Order", "g = 0.32 (ns)"),
        ("STEM Disciplines", "g = 0.71***"),
        ("Humanities/Social", "g = 0.48*"),
    ]

    for i, (mod_name, mod_val) in enumerate(mods):
        my = mod_y + 45 + i * 40
        draw.text((sidebar_x+70, my), mod_name, font=f_small, fill=hex_to_rgb(PALETTE['text_dark']))
        draw.text((sidebar_x+sidebar_w-70, my), mod_val, font=f_small, fill=hex_to_rgb(PALETTE['text_medium']), anchor='rm')

    # Implication box
    impl_y = mod_y + len(mods) * 40 + 100
    rounded_rect(draw, (sidebar_x+40, impl_y, sidebar_x+sidebar_w-40, impl_y+170), 12,
                 fill=hex_to_rgb('#E8F5E9'), outline=hex_to_rgb(PALETTE['sig_positive']), width=2)
    draw.text((sidebar_x+sidebar_w//2, impl_y+20), "Practical Implication", font=f_body,
              fill=hex_to_rgb(PALETTE['sig_positive']), anchor='mt')
    impl_text = [
        "Design AI interventions with explicit",
        "metacognitive scaffolding and fading",
        "protocols to promote internalization"
    ]
    for i, line in enumerate(impl_text):
        draw.text((sidebar_x+sidebar_w//2, impl_y+60+i*30), line, font=f_small,
                  fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')

    # ═══════════════════════════════════════════════════════════════
    # BOTTOM: AIMC FRAMEWORK MODEL
    # ═══════════════════════════════════════════════════════════════
    bottom_y = 1240
    draw.line([(80, bottom_y), (WIDTH-80, bottom_y)], fill=hex_to_rgb(PALETTE['grid']), width=2)

    draw.text((WIDTH//2, bottom_y+30), "D. AI-Induced Metacognitive Compromise (AIMC) Framework",
              font=f_section, fill=hex_to_rgb(PALETTE['text_dark']), anchor='mt')
    draw.text((WIDTH//2, bottom_y+80), "A developmental model linking theoretical mechanisms to observed patterns",
              font=f_small, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')

    # Three-level progression
    level_y = bottom_y + 140
    level_h = 200
    level_gap = 40
    total_width = WIDTH - 160
    level_w = (total_width - 2*level_gap) // 3

    levels = [
        ("Level 1: AI-Assisted Metacognition",
         ["External regulation via AI prompts", "Scaffolded monitoring & planning", "Performance with support"],
         PALETTE['level1'], "Strong evidence (g = 0.64)"),
        ("Level 2: Meta-AI Awareness",
         ["Recognition of AI limitations", "Strategic tool selection", "Calibrated trust in outputs"],
         PALETTE['level2'], "Mixed evidence"),
        ("Level 3: Independent Metacognition",
         ["Autonomous self-regulation", "Internalized strategies", "Transfer to novel contexts"],
         PALETTE['level3'], "Weak evidence (g = 0.28, ns)"),
    ]

    for i, (title, bullets, color, evidence) in enumerate(levels):
        lx = 80 + i * (level_w + level_gap)

        # Level panel
        rounded_rect(draw, (lx, level_y, lx+level_w, level_y+level_h), 15,
                     fill=hex_to_rgb('#FFFFFF'), outline=hex_to_rgb(color), width=4)

        # Title bar
        draw.rectangle([lx+2, level_y+2, lx+level_w-2, level_y+50], fill=hex_to_rgb(color))
        draw.text((lx+level_w//2, level_y+26), title, font=f_label, fill=hex_to_rgb('#FFFFFF'), anchor='mm')

        # Bullets
        for j, bullet in enumerate(bullets):
            draw.text((lx+25, level_y+70+j*35), f"• {bullet}", font=f_tiny,
                      fill=hex_to_rgb(PALETTE['text_dark']))

        # Evidence badge
        ev_color = PALETTE['sig_positive'] if 'Strong' in evidence else (PALETTE['warning'] if 'Weak' in evidence else PALETTE['text_medium'])
        draw.text((lx+level_w//2, level_y+level_h-25), evidence, font=f_tiny,
                  fill=hex_to_rgb(ev_color), anchor='mm')

        # Progression arrows
        if i < 2:
            arr_x = lx + level_w + level_gap//2
            draw_arrow(draw, (arr_x-30, level_y+level_h//2), (arr_x+30, level_y+level_h//2),
                       hex_to_rgb(PALETTE['text_light']), width=3, arrow_size=12)

    # Evidence gap annotation
    gap_x = 80 + 2*(level_w + level_gap) - level_gap//2
    gap_y = level_y + level_h + 30
    draw.text((gap_x, gap_y), "← Evidence Gap", font=f_body, fill=hex_to_rgb(PALETTE['warning']), anchor='mt')
    draw.text((gap_x, gap_y+35), "Current interventions may not", font=f_small, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')
    draw.text((gap_x, gap_y+60), "bridge Level 1 → Level 3", font=f_small, fill=hex_to_rgb(PALETTE['text_medium']), anchor='mt')

    # ═══════════════════════════════════════════════════════════════
    # BOTTOM: Key Takeaways
    # ═══════════════════════════════════════════════════════════════
    takeaway_y = level_y + level_h + 130

    # Three key insights
    insights = [
        ("Theoretical Convergence", "Six established frameworks predict metacognitive vulnerability", PALETTE['clt']),
        ("Empirical Confirmation", "Meta-analysis reveals significant differential effects", PALETTE['sig_positive']),
        ("Design Imperative", "AI scaffolding must include explicit fading protocols", PALETTE['warning']),
    ]

    insight_w = (WIDTH - 200) // 3
    for i, (title, desc, color) in enumerate(insights):
        ix = 100 + i * insight_w
        rounded_rect(draw, (ix, takeaway_y, ix+insight_w-30, takeaway_y+100), 12,
                     fill=hex_to_rgb('#FAFAFA'), outline=hex_to_rgb(color), width=2)
        draw.text((ix+15, takeaway_y+15), title, font=f_label, fill=hex_to_rgb(color))

        # Word wrap description
        words = desc.split()
        lines = []
        current = []
        for word in words:
            current.append(word)
            if len(' '.join(current)) > 40:
                lines.append(' '.join(current[:-1]))
                current = [word]
        lines.append(' '.join(current))

        for j, line in enumerate(lines[:2]):
            draw.text((ix+15, takeaway_y+48+j*22), line, font=f_tiny, fill=hex_to_rgb(PALETTE['text_dark']))

    # ═══════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════
    footer_y = HEIGHT - 70
    draw.text((WIDTH//2, footer_y),
              "You, H. (2026). Generative AI in Higher Education: A Three-Level Meta-Analysis. Educational Psychology Review.",
              font=f_small, fill=hex_to_rgb(PALETTE['text_light']), anchor='mm')
    draw.text((WIDTH//2, footer_y+30), "© 2026 | Cognitive Dependency Framework v1.0",
              font=f_tiny, fill=hex_to_rgb(PALETTE['text_light']), anchor='mm')

    # ═══════════════════════════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════════════════════════
    png_path = os.path.join(OUTPUT_DIR, "AIMC_Framework.png")
    img.save(png_path, "PNG", dpi=(DPI, DPI))
    print(f"✅ PNG: {png_path}")

    pdf_path = os.path.join(OUTPUT_DIR, "AIMC_Framework.pdf")
    img.save(pdf_path, "PDF", resolution=DPI)
    print(f"✅ PDF: {pdf_path}")

    preview = img.copy()
    preview.thumbnail((1800, 1350), Image.Resampling.LANCZOS)
    preview_path = os.path.join(OUTPUT_DIR, "AIMC_Framework_preview.png")
    preview.save(preview_path, "PNG")
    print(f"✅ Preview: {preview_path}")

    return img

if __name__ == "__main__":
    create_visualization()
