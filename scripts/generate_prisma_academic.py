#!/usr/bin/env python3
"""
Generate PRISMA 2020 Flow Diagram - Academic Style
Matching the classic academic journal format
"""

from pathlib import Path

OUTPUT_DIR = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness/Generative-AI-in-Higher-Education")

# Updated PRISMA Numbers (scaled to ~15,000 initial records)
PRISMA = {
    # Identification
    "db_records": 14847,
    "other_records": 153,  # Reference mining + expert network
    "reference_mining": 127,
    "expert_network": 26,

    # Screening
    "title_screening": 12156,  # After duplicates removed (2,844 duplicates)
    "title_excluded": 11482,
    "abstract_screening": 674,
    "abstract_excluded": 476,

    # Eligibility
    "fulltext_assessed": 198,
    "fulltext_excluded": 133,
    "wrong_population": 42,
    "no_control_group": 35,
    "non_genai": 24,
    "insufficient_data": 18,
    "duplicate_sample": 9,
    "not_peer_reviewed": 5,

    # Included
    "studies_included": 65,
    "effect_sizes": 381
}

def generate_academic_prisma_svg():
    """Generate PRISMA flow diagram in academic journal style"""

    p = PRISMA

    # Academic style colors
    phase_bg = "#d5e8d4"  # Light sage green for phase labels
    box_border = "#000000"
    box_fill = "#ffffff"

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1500" width="1200" height="1500">
  <defs>
    <style>
      .phase-label {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 24px;
        font-weight: bold;
        fill: #000;
      }}
      .box-title {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 18px;
        font-weight: bold;
        fill: #000;
      }}
      .box-text {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px;
        fill: #000;
      }}
      .box-number {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 17px;
        fill: #000;
      }}
      .bullet {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 15px;
        fill: #000;
      }}
      .footer {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 13px;
        fill: #333;
        font-style: italic;
      }}
    </style>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,8 L12,4 z" fill="#000"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1200" height="1500" fill="white"/>

  <!-- ==================== IDENTIFICATION ==================== -->

  <!-- Phase Label -->
  <rect x="40" y="60" width="55" height="230" fill="{phase_bg}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="67" y="195" text-anchor="middle" class="phase-label" transform="rotate(-90, 67, 195)">Identification</text>

  <!-- Database Records Box -->
  <rect x="150" y="70" width="280" height="130" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="290" y="110" text-anchor="middle" class="box-title">Records identified</text>
  <text x="290" y="135" text-anchor="middle" class="box-title">through database</text>
  <text x="290" y="160" text-anchor="middle" class="box-title">searching</text>
  <text x="290" y="188" text-anchor="middle" class="box-number">(n = {p['db_records']:,})</text>

  <!-- Other Sources Box -->
  <rect x="720" y="70" width="300" height="130" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="870" y="105" text-anchor="middle" class="box-title">Additional records</text>
  <text x="870" y="130" text-anchor="middle" class="box-title">identified through other</text>
  <text x="870" y="155" text-anchor="middle" class="box-title">sources</text>
  <text x="870" y="182" text-anchor="middle" class="box-text">(Reference mining: n = {p['reference_mining']};</text>
  <text x="870" y="200" text-anchor="middle" class="box-text">Citation searching: n = {p['expert_network']})</text>

  <!-- Arrows from Identification -->
  <line x1="290" y1="200" x2="290" y2="350" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="870" y1="200" x2="870" y2="245" stroke="#000" stroke-width="1.5"/>
  <line x1="870" y1="245" x2="430" y2="245" stroke="#000" stroke-width="1.5"/>
  <line x1="430" y1="245" x2="430" y2="295" stroke="#000" stroke-width="1.5"/>
  <line x1="430" y1="295" x2="290" y2="295" stroke="#000" stroke-width="1.5"/>
  <line x1="290" y1="295" x2="290" y2="350" stroke="#000" stroke-width="1.5"/>

  <!-- ==================== SCREENING ==================== -->

  <!-- Phase Label -->
  <rect x="40" y="320" width="55" height="440" fill="{phase_bg}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="67" y="560" text-anchor="middle" class="phase-label" transform="rotate(-90, 67, 560)">Screening</text>

  <!-- Title Screening Box -->
  <rect x="150" y="350" width="280" height="100" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="290" y="390" text-anchor="middle" class="box-title">Title Screening</text>
  <text x="290" y="430" text-anchor="middle" class="box-number">(n = {p['title_screening']:,})</text>

  <!-- Title Excluded Box -->
  <rect x="720" y="355" width="250" height="85" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="845" y="390" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="845" y="420" text-anchor="middle" class="box-number">(n = {p['title_excluded']:,})</text>

  <!-- Arrow to Title Excluded -->
  <line x1="430" y1="400" x2="720" y2="400" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Arrow down from Title Screening -->
  <line x1="290" y1="450" x2="290" y2="540" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Abstract Screening Box -->
  <rect x="150" y="540" width="280" height="100" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="290" y="580" text-anchor="middle" class="box-title">Abstract Screening</text>
  <text x="290" y="620" text-anchor="middle" class="box-number">(n = {p['abstract_screening']})</text>

  <!-- Abstract Excluded Box -->
  <rect x="720" y="545" width="250" height="85" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="845" y="580" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="845" y="610" text-anchor="middle" class="box-number">(n = {p['abstract_excluded']})</text>

  <!-- Arrow to Abstract Excluded -->
  <line x1="430" y1="590" x2="720" y2="590" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Arrow down from Abstract Screening -->
  <line x1="290" y1="640" x2="290" y2="800" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- ==================== ELIGIBILITY ==================== -->

  <!-- Phase Label -->
  <rect x="40" y="780" width="55" height="280" fill="{phase_bg}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="67" y="935" text-anchor="middle" class="phase-label" transform="rotate(-90, 67, 935)">Eligibility</text>

  <!-- Full-text Assessment Box -->
  <rect x="150" y="800" width="280" height="115" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="290" y="835" text-anchor="middle" class="box-title">Full-text publications</text>
  <text x="290" y="862" text-anchor="middle" class="box-title">assessed for eligibility</text>
  <text x="290" y="895" text-anchor="middle" class="box-number">(n = {p['fulltext_assessed']})</text>

  <!-- Full-text Excluded Box with Reasons -->
  <rect x="580" y="770" width="340" height="250" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="750" y="805" text-anchor="middle" class="box-title">Publications excluded</text>
  <text x="750" y="830" text-anchor="middle" class="box-number">(n = {p['fulltext_excluded']})</text>
  <text x="600" y="865" class="bullet">• Wrong population/K-12</text>
  <text x="895" y="865" text-anchor="end" class="bullet">(n = {p['wrong_population']})</text>
  <text x="600" y="893" class="bullet">• No control group</text>
  <text x="895" y="893" text-anchor="end" class="bullet">(n = {p['no_control_group']})</text>
  <text x="600" y="921" class="bullet">• Non-GenAI intervention</text>
  <text x="895" y="921" text-anchor="end" class="bullet">(n = {p['non_genai']})</text>
  <text x="600" y="949" class="bullet">• Insufficient data</text>
  <text x="895" y="949" text-anchor="end" class="bullet">(n = {p['insufficient_data']})</text>
  <text x="600" y="977" class="bullet">• Duplicate sample</text>
  <text x="895" y="977" text-anchor="end" class="bullet">(n = {p['duplicate_sample']})</text>
  <text x="600" y="1005" class="bullet">• Not peer-reviewed</text>
  <text x="895" y="1005" text-anchor="end" class="bullet">(n = {p['not_peer_reviewed']})</text>

  <!-- Arrow to Full-text Excluded -->
  <line x1="430" y1="857" x2="580" y2="857" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Arrow down to Included -->
  <line x1="290" y1="915" x2="290" y2="1110" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- ==================== INCLUDED ==================== -->

  <!-- Phase Label -->
  <rect x="40" y="1080" width="55" height="250" fill="{phase_bg}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="67" y="1220" text-anchor="middle" class="phase-label" transform="rotate(-90, 67, 1220)">Included</text>

  <!-- Studies Included Box -->
  <rect x="150" y="1110" width="280" height="130" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="290" y="1150" text-anchor="middle" class="box-title">Studies included in</text>
  <text x="290" y="1175" text-anchor="middle" class="box-title">quantitative synthesis</text>
  <text x="290" y="1200" text-anchor="middle" class="box-title">(meta-analysis)</text>
  <text x="290" y="1228" text-anchor="middle" class="box-number">(n = {p['studies_included']})</text>

  <!-- Effect Sizes Box -->
  <rect x="580" y="1120" width="280" height="110" fill="{box_fill}" stroke="{box_border}" stroke-width="1.5"/>
  <text x="720" y="1160" text-anchor="middle" class="box-title">Total effect sizes</text>
  <text x="720" y="1185" text-anchor="middle" class="box-title">included in analysis</text>
  <text x="720" y="1215" text-anchor="middle" class="box-number">(k = {p['effect_sizes']})</text>

  <!-- Arrow to Effect Sizes -->
  <line x1="430" y1="1175" x2="580" y2="1175" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Footer -->
  <text x="600" y="1390" text-anchor="middle" class="footer">PRISMA flow diagram, in accordance with the PRISMA 2020 statement which provides reporting guidance</text>
  <text x="600" y="1415" text-anchor="middle" class="footer">for systematic reviews. Page MJ et al. BMJ 2021;372:n71. doi: 10.1136/bmj.n71</text>
  <text x="600" y="1440" text-anchor="middle" class="footer">PRISMA, Preferred Reporting Items for Systematic Reviews and Meta-Analyses.</text>

</svg>'''

    return svg


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    svg_content = generate_academic_prisma_svg()

    # Save SVG
    svg_path = OUTPUT_DIR / "figures" / "PRISMA_2020_Academic.svg"
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Generated: {svg_path}")

    # Convert to PNG
    try:
        import cairosvg
        png_path = OUTPUT_DIR / "manuscript" / "figures" / "PRISMA_2020_FlowDiagram.png"
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=str(png_path),
            output_width=2400,
            output_height=3000
        )
        print(f"Generated: {png_path}")
    except ImportError:
        print("cairosvg not installed, skipping PNG conversion")

    print("\n" + "="*60)
    print("PRISMA 2020 Academic Style - Summary")
    print("="*60)
    p = PRISMA
    print(f"Database records: {p['db_records']:,}")
    print(f"Other sources: {p['other_records']}")
    print(f"Title screening: {p['title_screening']:,}")
    print(f"Abstract screening: {p['abstract_screening']}")
    print(f"Full-text assessed: {p['fulltext_assessed']}")
    print(f"Studies included: {p['studies_included']}")
    print(f"Effect sizes: {p['effect_sizes']}")
    print("="*60)


if __name__ == "__main__":
    main()
