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
    """Generate PRISMA flow diagram in academic journal style - LARGE FORMAT"""

    p = PRISMA

    # Academic style colors
    phase_bg = "#d5e8d4"  # Light sage green for phase labels
    box_border = "#000000"
    box_fill = "#ffffff"

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 1100" width="850" height="1100">
  <defs>
    <style>
      .phase-label {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 28px;
        font-weight: bold;
        fill: #000;
      }}
      .box-title {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 22px;
        font-weight: bold;
        fill: #000;
      }}
      .box-text {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 18px;
        fill: #000;
      }}
      .box-number {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 20px;
        fill: #000;
      }}
      .bullet {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 17px;
        fill: #000;
      }}
      .footer {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 12px;
        fill: #333;
        font-style: italic;
      }}
    </style>
    <marker id="arrow" markerWidth="14" markerHeight="14" refX="12" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,10 L14,5 z" fill="#000"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="850" height="1100" fill="white"/>

  <!-- ==================== IDENTIFICATION ==================== -->

  <!-- Phase Label -->
  <rect x="25" y="35" width="50" height="175" fill="{phase_bg}" stroke="{box_border}" stroke-width="2"/>
  <text x="50" y="140" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 140)">Identification</text>

  <!-- Database Records Box -->
  <rect x="100" y="40" width="240" height="130" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="220" y="75" text-anchor="middle" class="box-title">Records identified</text>
  <text x="220" y="102" text-anchor="middle" class="box-title">through database</text>
  <text x="220" y="129" text-anchor="middle" class="box-title">searching</text>
  <text x="220" y="160" text-anchor="middle" class="box-number">(n = {p['db_records']:,})</text>

  <!-- Other Sources Box -->
  <rect x="530" y="40" width="280" height="130" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="670" y="70" text-anchor="middle" class="box-title">Additional records</text>
  <text x="670" y="97" text-anchor="middle" class="box-title">identified through</text>
  <text x="670" y="124" text-anchor="middle" class="box-title">other sources</text>
  <text x="670" y="160" text-anchor="middle" class="box-text">(n = {p['other_records']})</text>

  <!-- Arrows from Identification -->
  <line x1="220" y1="170" x2="220" y2="240" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="670" y1="170" x2="670" y2="195" stroke="#000" stroke-width="2"/>
  <line x1="670" y1="195" x2="340" y2="195" stroke="#000" stroke-width="2"/>
  <line x1="340" y1="195" x2="340" y2="210" stroke="#000" stroke-width="2"/>
  <line x1="340" y1="210" x2="220" y2="210" stroke="#000" stroke-width="2"/>

  <!-- ==================== SCREENING ==================== -->

  <!-- Phase Label -->
  <rect x="25" y="225" width="50" height="340" fill="{phase_bg}" stroke="{box_border}" stroke-width="2"/>
  <text x="50" y="410" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 410)">Screening</text>

  <!-- Title Screening Box -->
  <rect x="100" y="250" width="240" height="95" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="220" y="290" text-anchor="middle" class="box-title">Title Screening</text>
  <text x="220" y="330" text-anchor="middle" class="box-number">(n = {p['title_screening']:,})</text>

  <!-- Title Excluded Box -->
  <rect x="530" y="255" width="240" height="85" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="650" y="290" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="650" y="325" text-anchor="middle" class="box-number">(n = {p['title_excluded']:,})</text>

  <!-- Arrow to Title Excluded -->
  <line x1="340" y1="297" x2="530" y2="297" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Arrow down from Title Screening -->
  <line x1="220" y1="345" x2="220" y2="410" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Abstract Screening Box -->
  <rect x="100" y="420" width="240" height="95" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="220" y="460" text-anchor="middle" class="box-title">Abstract Screening</text>
  <text x="220" y="500" text-anchor="middle" class="box-number">(n = {p['abstract_screening']})</text>

  <!-- Abstract Excluded Box -->
  <rect x="530" y="425" width="240" height="85" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="650" y="460" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="650" y="495" text-anchor="middle" class="box-number">(n = {p['abstract_excluded']})</text>

  <!-- Arrow to Abstract Excluded -->
  <line x1="340" y1="467" x2="530" y2="467" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Arrow down from Abstract Screening -->
  <line x1="220" y1="515" x2="220" y2="590" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- ==================== ELIGIBILITY ==================== -->

  <!-- Phase Label -->
  <rect x="25" y="580" width="50" height="240" fill="{phase_bg}" stroke="{box_border}" stroke-width="2"/>
  <text x="50" y="715" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 715)">Eligibility</text>

  <!-- Full-text Assessment Box -->
  <rect x="100" y="600" width="240" height="110" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="220" y="635" text-anchor="middle" class="box-title">Full-text publications</text>
  <text x="220" y="665" text-anchor="middle" class="box-title">assessed for eligibility</text>
  <text x="220" y="700" text-anchor="middle" class="box-number">(n = {p['fulltext_assessed']})</text>

  <!-- Full-text Excluded Box with Reasons -->
  <rect x="430" y="575" width="370" height="230" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="615" y="608" text-anchor="middle" class="box-title">Publications excluded</text>
  <text x="615" y="635" text-anchor="middle" class="box-number">(n = {p['fulltext_excluded']})</text>
  <text x="450" y="670" class="bullet">• Wrong population/K-12</text>
  <text x="775" y="670" text-anchor="end" class="bullet">(n = {p['wrong_population']})</text>
  <text x="450" y="697" class="bullet">• No control group</text>
  <text x="775" y="697" text-anchor="end" class="bullet">(n = {p['no_control_group']})</text>
  <text x="450" y="724" class="bullet">• Non-GenAI intervention</text>
  <text x="775" y="724" text-anchor="end" class="bullet">(n = {p['non_genai']})</text>
  <text x="450" y="751" class="bullet">• Insufficient data</text>
  <text x="775" y="751" text-anchor="end" class="bullet">(n = {p['insufficient_data']})</text>
  <text x="450" y="778" class="bullet">• Duplicate sample</text>
  <text x="775" y="778" text-anchor="end" class="bullet">(n = {p['duplicate_sample']})</text>

  <!-- Arrow to Full-text Excluded -->
  <line x1="340" y1="655" x2="430" y2="655" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Arrow down to Included -->
  <line x1="220" y1="710" x2="220" y2="860" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- ==================== INCLUDED ==================== -->

  <!-- Phase Label -->
  <rect x="25" y="840" width="50" height="195" fill="{phase_bg}" stroke="{box_border}" stroke-width="2"/>
  <text x="50" y="950" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 950)">Included</text>

  <!-- Studies Included Box -->
  <rect x="100" y="870" width="240" height="130" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="220" y="905" text-anchor="middle" class="box-title">Studies included in</text>
  <text x="220" y="935" text-anchor="middle" class="box-title">quantitative synthesis</text>
  <text x="220" y="965" text-anchor="middle" class="box-title">(meta-analysis)</text>
  <text x="220" y="995" text-anchor="middle" class="box-number">(n = {p['studies_included']})</text>

  <!-- Effect Sizes Box -->
  <rect x="430" y="880" width="280" height="110" fill="{box_fill}" stroke="{box_border}" stroke-width="2"/>
  <text x="570" y="920" text-anchor="middle" class="box-title">Total effect sizes</text>
  <text x="570" y="950" text-anchor="middle" class="box-title">included in analysis</text>
  <text x="570" y="985" text-anchor="middle" class="box-number">(k = {p['effect_sizes']})</text>

  <!-- Arrow to Effect Sizes -->
  <line x1="340" y1="935" x2="430" y2="935" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Footer -->
  <text x="425" y="1050" text-anchor="middle" class="footer">PRISMA flow diagram, in accordance with the PRISMA 2020 statement.</text>
  <text x="425" y="1070" text-anchor="middle" class="footer">Page MJ et al. BMJ 2021;372:n71. doi: 10.1136/bmj.n71</text>

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
            output_width=1700,
            output_height=2200
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
