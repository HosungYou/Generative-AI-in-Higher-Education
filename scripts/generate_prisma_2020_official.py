#!/usr/bin/env python3
"""
Generate PRISMA 2020 Flow Diagram - Official Template Style
Following Page et al. (2021) exact format
"""

from pathlib import Path

OUTPUT_DIR = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness/Generative-AI-in-Higher-Education/figures")

# PRISMA 2020 Numbers
PRISMA_DATA = {
    "records_databases": 3247,
    "records_other": 187,
    "duplicates_removed": 891,
    "automation_excluded": 387,
    "records_screened": 2156,
    "records_excluded_screening": 1847,
    "reports_sought": 309,
    "reports_not_retrieved": 23,
    "reports_assessed": 286,
    "reports_excluded_total": 221,
    "exclusion_reasons": {
        "Wrong population (K-12)": 47,
        "No control/comparison group": 58,
        "Non-GenAI intervention": 39,
        "Insufficient statistical data": 45,
        "Duplicate sample": 19,
        "Not peer-reviewed": 13
    },
    "other_reports_sought": 45,
    "other_reports_assessed": 38,
    "other_reports_excluded": 31,
    "studies_included": 65,
    "effect_sizes": 381
}

def generate_official_prisma_svg():
    """Generate PRISMA 2020 flow diagram matching official template"""

    d = PRISMA_DATA

    # Official PRISMA 2020 colors
    id_color = "#deebf7"  # Light blue for Identification
    sc_color = "#fff7bc"  # Light yellow for Screening
    inc_color = "#d9f0d3"  # Light green for Included
    border_color = "#333333"

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 850" width="1100" height="850">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&amp;display=swap');
      .title {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 20px; font-weight: 700; fill: #1a1a1a; }}
      .phase-label {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 14px; font-weight: 700; fill: #1a1a1a; }}
      .box-title {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 11px; font-weight: 600; fill: #1a1a1a; }}
      .box-text {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 10px; fill: #333; }}
      .box-number {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 11px; font-weight: 600; fill: #1a1a1a; }}
      .small-text {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 9px; fill: #555; }}
      .footer {{ font-family: 'Open Sans', Arial, sans-serif; font-size: 8px; fill: #666; }}
      .phase-box {{ stroke: {border_color}; stroke-width: 2; }}
      .content-box {{ fill: white; stroke: {border_color}; stroke-width: 1.5; }}
      .arrow {{ stroke: {border_color}; stroke-width: 1.5; fill: none; }}
    </style>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="{border_color}"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1100" height="850" fill="white"/>

  <!-- Title -->
  <text x="550" y="35" text-anchor="middle" class="title">PRISMA 2020 Flow Diagram for Systematic Reviews</text>

  <!-- ==================== IDENTIFICATION PHASE ==================== -->

  <!-- Phase Label Box -->
  <rect x="20" y="60" width="30" height="180" fill="{id_color}" class="phase-box" rx="3"/>
  <text x="35" y="160" text-anchor="middle" class="phase-label" transform="rotate(-90, 35, 160)">Identification</text>

  <!-- Left Column: Database Records -->
  <rect x="70" y="70" width="220" height="60" fill="{id_color}" class="content-box" rx="4"/>
  <text x="180" y="90" text-anchor="middle" class="box-title">Identification of new studies via databases</text>
  <text x="180" y="105" text-anchor="middle" class="box-text">and registers</text>
  <text x="180" y="120" text-anchor="middle" class="box-number">(n = {d['records_databases']:,})</text>

  <!-- Right Column: Other Methods -->
  <rect x="810" y="70" width="220" height="60" fill="{id_color}" class="content-box" rx="4"/>
  <text x="920" y="90" text-anchor="middle" class="box-title">Identification of new studies via</text>
  <text x="920" y="105" text-anchor="middle" class="box-text">other methods</text>
  <text x="920" y="120" text-anchor="middle" class="box-number">(n = {d['records_other']})</text>

  <!-- Center: Records Removed Before Screening -->
  <rect x="320" y="145" width="260" height="85" fill="white" class="content-box" rx="4"/>
  <text x="450" y="165" text-anchor="middle" class="box-title">Records removed before screening:</text>
  <text x="340" y="183" class="box-text">Duplicate records</text>
  <text x="550" y="183" text-anchor="end" class="box-number">(n = {d['duplicates_removed']})</text>
  <text x="340" y="198" class="box-text">Records marked as ineligible</text>
  <text x="550" y="198" text-anchor="end" class="box-number">(n = {d['automation_excluded']})</text>
  <text x="340" y="213" class="box-text">Records removed for other reasons</text>
  <text x="550" y="213" text-anchor="end" class="box-number">(n = 0)</text>

  <!-- Arrows from Identification -->
  <path d="M 180 130 L 180 260" class="arrow" marker-end="url(#arrowhead)"/>
  <path d="M 290 100 L 320 145" class="arrow"/>
  <path d="M 580 145 L 810 100" class="arrow" style="stroke-dasharray: 5,3"/>
  <path d="M 920 130 L 920 260" class="arrow" marker-end="url(#arrowhead)"/>

  <!-- ==================== SCREENING PHASE ==================== -->

  <!-- Phase Label Box -->
  <rect x="20" y="250" width="30" height="320" fill="{sc_color}" class="phase-box" rx="3"/>
  <text x="35" y="420" text-anchor="middle" class="phase-label" transform="rotate(-90, 35, 420)">Screening</text>

  <!-- Left: Records Screened -->
  <rect x="70" y="260" width="220" height="50" fill="{sc_color}" class="content-box" rx="4"/>
  <text x="180" y="282" text-anchor="middle" class="box-title">Records screened</text>
  <text x="180" y="300" text-anchor="middle" class="box-number">(n = {d['records_screened']:,})</text>

  <!-- Left: Records Excluded -->
  <rect x="320" y="260" width="180" height="50" fill="white" class="content-box" rx="4"/>
  <text x="410" y="282" text-anchor="middle" class="box-title">Records excluded</text>
  <text x="410" y="300" text-anchor="middle" class="box-number">(n = {d['records_excluded_screening']:,})</text>

  <path d="M 290 285 L 320 285" class="arrow" marker-end="url(#arrowhead)"/>
  <path d="M 180 310 L 180 340" class="arrow" marker-end="url(#arrowhead)"/>

  <!-- Left: Reports Sought -->
  <rect x="70" y="340" width="220" height="50" fill="{sc_color}" class="content-box" rx="4"/>
  <text x="180" y="362" text-anchor="middle" class="box-title">Reports sought for retrieval</text>
  <text x="180" y="380" text-anchor="middle" class="box-number">(n = {d['reports_sought']})</text>

  <!-- Left: Reports Not Retrieved -->
  <rect x="320" y="340" width="180" height="50" fill="white" class="content-box" rx="4"/>
  <text x="410" y="362" text-anchor="middle" class="box-title">Reports not retrieved</text>
  <text x="410" y="380" text-anchor="middle" class="box-number">(n = {d['reports_not_retrieved']})</text>

  <path d="M 290 365 L 320 365" class="arrow" marker-end="url(#arrowhead)"/>
  <path d="M 180 390 L 180 420" class="arrow" marker-end="url(#arrowhead)"/>

  <!-- Left: Reports Assessed -->
  <rect x="70" y="420" width="220" height="50" fill="{sc_color}" class="content-box" rx="4"/>
  <text x="180" y="442" text-anchor="middle" class="box-title">Reports assessed for eligibility</text>
  <text x="180" y="460" text-anchor="middle" class="box-number">(n = {d['reports_assessed']})</text>

  <!-- Left: Reports Excluded with Reasons -->
  <rect x="320" y="400" width="280" height="150" fill="white" class="content-box" rx="4"/>
  <text x="460" y="420" text-anchor="middle" class="box-title">Reports excluded (n = {d['reports_excluded_total']})</text>
  <text x="335" y="440" class="small-text">Wrong population (K-12)</text>
  <text x="580" y="440" text-anchor="end" class="small-text">(n = 47)</text>
  <text x="335" y="456" class="small-text">No control/comparison group</text>
  <text x="580" y="456" text-anchor="end" class="small-text">(n = 58)</text>
  <text x="335" y="472" class="small-text">Non-GenAI intervention</text>
  <text x="580" y="472" text-anchor="end" class="small-text">(n = 39)</text>
  <text x="335" y="488" class="small-text">Insufficient statistical data</text>
  <text x="580" y="488" text-anchor="end" class="small-text">(n = 45)</text>
  <text x="335" y="504" class="small-text">Duplicate sample</text>
  <text x="580" y="504" text-anchor="end" class="small-text">(n = 19)</text>
  <text x="335" y="520" class="small-text">Not peer-reviewed/preprint</text>
  <text x="580" y="520" text-anchor="end" class="small-text">(n = 13)</text>

  <path d="M 290 445 L 320 445" class="arrow" marker-end="url(#arrowhead)"/>

  <!-- Right Column: Other Methods Screening -->
  <rect x="810" y="260" width="220" height="50" fill="{sc_color}" class="content-box" rx="4"/>
  <text x="920" y="282" text-anchor="middle" class="box-title">Reports sought for retrieval</text>
  <text x="920" y="300" text-anchor="middle" class="box-number">(n = {d['other_reports_sought']})</text>

  <path d="M 920 310 L 920 340" class="arrow" marker-end="url(#arrowhead)"/>

  <rect x="810" y="340" width="220" height="50" fill="{sc_color}" class="content-box" rx="4"/>
  <text x="920" y="362" text-anchor="middle" class="box-title">Reports assessed for eligibility</text>
  <text x="920" y="380" text-anchor="middle" class="box-number">(n = {d['other_reports_assessed']})</text>

  <path d="M 920 390 L 920 420" class="arrow" marker-end="url(#arrowhead)"/>

  <rect x="810" y="420" width="220" height="50" fill="white" class="content-box" rx="4"/>
  <text x="920" y="442" text-anchor="middle" class="box-title">Reports excluded</text>
  <text x="920" y="460" text-anchor="middle" class="box-number">(n = {d['other_reports_excluded']})</text>

  <!-- ==================== INCLUDED PHASE ==================== -->

  <!-- Phase Label Box -->
  <rect x="20" y="580" width="30" height="140" fill="{inc_color}" class="phase-box" rx="3"/>
  <text x="35" y="660" text-anchor="middle" class="phase-label" transform="rotate(-90, 35, 660)">Included</text>

  <!-- Arrows to Included -->
  <path d="M 180 470 L 180 600" class="arrow" marker-end="url(#arrowhead)"/>
  <path d="M 920 470 L 920 520 L 700 520 L 700 600" class="arrow" marker-end="url(#arrowhead)"/>

  <!-- Studies Included in Review -->
  <rect x="70" y="600" width="300" height="110" fill="{inc_color}" class="content-box" rx="4"/>
  <text x="220" y="625" text-anchor="middle" class="box-title">New studies included in review</text>
  <text x="220" y="645" text-anchor="middle" class="box-number">(n = {d['studies_included']})</text>
  <text x="220" y="670" text-anchor="middle" class="box-text">Reports of new included studies</text>
  <text x="220" y="688" text-anchor="middle" class="box-number">(n = {d['studies_included']})</text>

  <!-- Arrow to Meta-analysis -->
  <path d="M 370 655 L 450 655" class="arrow" marker-end="url(#arrowhead)"/>

  <!-- Total Studies in Meta-analysis -->
  <rect x="450" y="600" width="300" height="110" fill="{inc_color}" class="content-box" rx="4"/>
  <text x="600" y="625" text-anchor="middle" class="box-title">Total studies included in</text>
  <text x="600" y="643" text-anchor="middle" class="box-title">quantitative synthesis (meta-analysis)</text>
  <text x="600" y="668" text-anchor="middle" class="box-number">(n = {d['studies_included']})</text>
  <text x="600" y="693" text-anchor="middle" class="box-text">Total effect sizes: k = {d['effect_sizes']}</text>

  <!-- Footer -->
  <text x="550" y="760" text-anchor="middle" class="footer">From: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews.</text>
  <text x="550" y="775" text-anchor="middle" class="footer">BMJ 2021;372:n71. doi: 10.1136/bmj.n71</text>
  <text x="550" y="795" text-anchor="middle" class="footer">For more information, visit: http://www.prisma-statement.org/</text>

  <!-- Dividing Lines -->
  <line x1="55" y1="245" x2="1050" y2="245" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="55" y1="575" x2="1050" y2="575" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>

</svg>'''

    return svg


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    svg_content = generate_official_prisma_svg()
    svg_path = OUTPUT_DIR / "PRISMA_2020_Flow_Diagram_Official.svg"
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Generated: {svg_path}")

    print("\n" + "="*60)
    print("PRISMA 2020 Official Template Generated")
    print("="*60)
    print(f"Studies included: {PRISMA_DATA['studies_included']}")
    print(f"Effect sizes: {PRISMA_DATA['effect_sizes']}")
    print("="*60)


if __name__ == "__main__":
    main()
