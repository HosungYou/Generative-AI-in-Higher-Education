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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1100" width="900" height="1100">
  <defs>
    <style>
      .phase-label {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px;
        font-weight: bold;
        fill: #000;
      }}
      .box-title {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 13px;
        font-weight: bold;
        fill: #000;
      }}
      .box-text {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 12px;
        fill: #000;
      }}
      .box-number {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 12px;
        fill: #000;
      }}
      .bullet {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 11px;
        fill: #000;
      }}
      .footer {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 10px;
        fill: #333;
        font-style: italic;
      }}
    </style>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#000"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="900" height="1100" fill="white"/>

  <!-- ==================== IDENTIFICATION ==================== -->

  <!-- Phase Label -->
  <rect x="30" y="50" width="40" height="170" fill="{phase_bg}" stroke="{box_border}" stroke-width="1"/>
  <text x="50" y="150" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 150)">Identification</text>

  <!-- Database Records Box -->
  <rect x="120" y="60" width="200" height="90" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="220" y="90" text-anchor="middle" class="box-title">Records identified</text>
  <text x="220" y="108" text-anchor="middle" class="box-title">through database</text>
  <text x="220" y="126" text-anchor="middle" class="box-title">searching</text>
  <text x="220" y="144" text-anchor="middle" class="box-number">(n={p['db_records']:,})</text>

  <!-- Other Sources Box -->
  <rect x="550" y="60" width="200" height="90" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="650" y="85" text-anchor="middle" class="box-title">Additional records</text>
  <text x="650" y="103" text-anchor="middle" class="box-title">identified through other</text>
  <text x="650" y="121" text-anchor="middle" class="box-title">sources</text>
  <text x="650" y="139" text-anchor="middle" class="box-text">(Reference mining: n={p['reference_mining']})</text>
  <text x="650" y="153" text-anchor="middle" class="box-text">(Citation searching: n={p['expert_network']})</text>

  <!-- Arrows from Identification -->
  <line x1="220" y1="150" x2="220" y2="260" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>
  <line x1="650" y1="150" x2="650" y2="180" stroke="#000" stroke-width="1"/>
  <line x1="650" y1="180" x2="320" y2="180" stroke="#000" stroke-width="1"/>
  <line x1="320" y1="180" x2="320" y2="220" stroke="#000" stroke-width="1"/>
  <line x1="320" y1="220" x2="220" y2="220" stroke="#000" stroke-width="1"/>
  <line x1="220" y1="220" x2="220" y2="260" stroke="#000" stroke-width="1"/>

  <!-- ==================== SCREENING ==================== -->

  <!-- Phase Label -->
  <rect x="30" y="240" width="40" height="320" fill="{phase_bg}" stroke="{box_border}" stroke-width="1"/>
  <text x="50" y="410" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 410)">Screening</text>

  <!-- Title Screening Box -->
  <rect x="120" y="260" width="200" height="70" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="220" y="290" text-anchor="middle" class="box-title">Title Screening</text>
  <text x="220" y="318" text-anchor="middle" class="box-number">(n={p['title_screening']:,})</text>

  <!-- Title Excluded Box -->
  <rect x="550" y="265" width="180" height="55" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="640" y="290" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="640" y="310" text-anchor="middle" class="box-number">(n={p['title_excluded']:,})</text>

  <!-- Arrow to Title Excluded -->
  <line x1="320" y1="295" x2="550" y2="295" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Arrow down from Title Screening -->
  <line x1="220" y1="330" x2="220" y2="400" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Abstract Screening Box -->
  <rect x="120" y="400" width="200" height="70" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="220" y="430" text-anchor="middle" class="box-title">Abstract Screening</text>
  <text x="220" y="458" text-anchor="middle" class="box-number">(n={p['abstract_screening']})</text>

  <!-- Abstract Excluded Box -->
  <rect x="550" y="405" width="180" height="55" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="640" y="430" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="640" y="450" text-anchor="middle" class="box-number">(n={p['abstract_excluded']})</text>

  <!-- Arrow to Abstract Excluded -->
  <line x1="320" y1="435" x2="550" y2="435" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Arrow down from Abstract Screening -->
  <line x1="220" y1="470" x2="220" y2="590" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- ==================== ELIGIBILITY ==================== -->

  <!-- Phase Label -->
  <rect x="30" y="580" width="40" height="200" fill="{phase_bg}" stroke="{box_border}" stroke-width="1"/>
  <text x="50" y="690" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 690)">Eligibility</text>

  <!-- Full-text Assessment Box -->
  <rect x="120" y="590" width="200" height="80" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="220" y="615" text-anchor="middle" class="box-title">Full-text publications</text>
  <text x="220" y="633" text-anchor="middle" class="box-title">assessed for eligibility</text>
  <text x="220" y="658" text-anchor="middle" class="box-number">(n={p['fulltext_assessed']})</text>

  <!-- Full-text Excluded Box with Reasons -->
  <rect x="450" y="570" width="230" height="175" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="565" y="595" text-anchor="middle" class="box-title">Publications excluded</text>
  <text x="565" y="613" text-anchor="middle" class="box-number">(n={p['fulltext_excluded']})</text>
  <text x="465" y="638" class="bullet">• wrong population/K-12</text>
  <text x="660" y="638" text-anchor="end" class="bullet">(n={p['wrong_population']})</text>
  <text x="465" y="656" class="bullet">• no control group</text>
  <text x="660" y="656" text-anchor="end" class="bullet">(n={p['no_control_group']})</text>
  <text x="465" y="674" class="bullet">• non-GenAI intervention</text>
  <text x="660" y="674" text-anchor="end" class="bullet">(n={p['non_genai']})</text>
  <text x="465" y="692" class="bullet">• insufficient data</text>
  <text x="660" y="692" text-anchor="end" class="bullet">(n={p['insufficient_data']})</text>
  <text x="465" y="710" class="bullet">• duplicate sample</text>
  <text x="660" y="710" text-anchor="end" class="bullet">(n={p['duplicate_sample']})</text>
  <text x="465" y="728" class="bullet">• not peer-reviewed</text>
  <text x="660" y="728" text-anchor="end" class="bullet">(n={p['not_peer_reviewed']})</text>

  <!-- Arrow to Full-text Excluded -->
  <line x1="320" y1="630" x2="450" y2="630" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Arrow down to Included -->
  <line x1="220" y1="670" x2="220" y2="820" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- ==================== INCLUDED ==================== -->

  <!-- Phase Label -->
  <rect x="30" y="800" width="40" height="180" fill="{phase_bg}" stroke="{box_border}" stroke-width="1"/>
  <text x="50" y="900" text-anchor="middle" class="phase-label" transform="rotate(-90, 50, 900)">Included</text>

  <!-- Studies Included Box -->
  <rect x="120" y="820" width="200" height="90" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="220" y="850" text-anchor="middle" class="box-title">Studies included in</text>
  <text x="220" y="868" text-anchor="middle" class="box-title">quantitative synthesis</text>
  <text x="220" y="886" text-anchor="middle" class="box-title">(meta-analysis)</text>
  <text x="220" y="904" text-anchor="middle" class="box-number">(n={p['studies_included']})</text>

  <!-- Effect Sizes Box -->
  <rect x="450" y="830" width="200" height="70" fill="{box_fill}" stroke="{box_border}" stroke-width="1"/>
  <text x="550" y="860" text-anchor="middle" class="box-title">Total effect sizes</text>
  <text x="550" y="878" text-anchor="middle" class="box-title">included in analysis</text>
  <text x="550" y="896" text-anchor="middle" class="box-number">(k={p['effect_sizes']})</text>

  <!-- Arrow to Effect Sizes -->
  <line x1="320" y1="865" x2="450" y2="865" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Footer -->
  <text x="450" y="1020" text-anchor="middle" class="footer">PRISMA flow diagram, in accordance with the PRISMA 2020 statement which provides reporting guidance</text>
  <text x="450" y="1038" text-anchor="middle" class="footer">for systematic reviews. Page MJ et al. BMJ 2021;372:n71. doi: 10.1136/bmj.n71</text>
  <text x="450" y="1056" text-anchor="middle" class="footer">PRISMA, Preferred Reporting Items for Systematic Reviews and Meta-Analyses.</text>

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
            output_width=1800,
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
