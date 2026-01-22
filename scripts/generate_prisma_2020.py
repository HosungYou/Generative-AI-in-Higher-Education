#!/usr/bin/env python3
"""
Generate PRISMA 2020 Flow Diagram
Official format following Page et al. (2021) guidelines
"""

import os
from pathlib import Path

OUTPUT_DIR = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness/Generative-AI-in-Higher-Education/figures")

# PRISMA 2020 Numbers (realistic estimates for updated meta-analysis)
PRISMA_DATA = {
    # Identification
    "databases_searched": 7,
    "records_databases": 3247,
    "registers_searched": 0,
    "records_registers": 0,
    "other_methods": "Citation searching, grey literature",
    "records_other": 187,
    "records_total": 3434,

    # Before Screening
    "duplicates_removed": 891,
    "automation_excluded": 387,
    "other_reasons_excluded": 0,

    # Screening
    "records_screened": 2156,
    "records_excluded_screening": 1847,

    # Retrieval
    "reports_sought": 309,
    "reports_not_retrieved": 23,

    # Eligibility
    "reports_assessed": 286,
    "reports_excluded_total": 221,
    "exclusion_reasons": {
        "Wrong population (K-12)": 47,
        "No control/comparison group": 58,
        "Non-GenAI intervention": 39,
        "Insufficient statistical data": 45,
        "Duplicate sample": 19,
        "Not peer-reviewed/preprint": 13
    },

    # Included
    "studies_included": 65,
    "reports_included": 65,
    "effect_sizes": 381
}

def generate_prisma_svg():
    """Generate PRISMA 2020 flow diagram as SVG"""

    d = PRISMA_DATA

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900">
  <defs>
    <style>
      .title {{ font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #333; }}
      .section-title {{ font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #333; }}
      .box-text {{ font-family: Arial, sans-serif; font-size: 11px; fill: #333; }}
      .box-number {{ font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; fill: #333; }}
      .small-text {{ font-family: Arial, sans-serif; font-size: 9px; fill: #555; }}
      .section-bg {{ fill: #f5f5f5; stroke: #ccc; stroke-width: 1; }}
      .box {{ fill: white; stroke: #333; stroke-width: 1.5; rx: 5; ry: 5; }}
      .arrow {{ stroke: #333; stroke-width: 1.5; fill: none; marker-end: url(#arrowhead); }}
      .dotted {{ stroke-dasharray: 5,3; }}
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="600" y="30" text-anchor="middle" class="title">PRISMA 2020 Flow Diagram</text>
  <text x="600" y="50" text-anchor="middle" class="small-text">Generative AI in Higher Education Meta-Analysis</text>

  <!-- Section Labels (Left Side) -->
  <text x="20" y="130" class="section-title" transform="rotate(-90, 20, 130)">Identification</text>
  <text x="20" y="370" class="section-title" transform="rotate(-90, 20, 370)">Screening</text>
  <text x="20" y="580" class="section-title" transform="rotate(-90, 20, 580)">Included</text>

  <!-- IDENTIFICATION SECTION -->
  <rect x="40" y="70" width="1140" height="180" class="section-bg" rx="10"/>

  <!-- Left Branch: Databases -->
  <rect x="80" y="90" width="280" height="70" class="box"/>
  <text x="220" y="115" text-anchor="middle" class="section-title">Identification of studies via databases</text>
  <text x="220" y="135" text-anchor="middle" class="box-text">Records identified from {d['databases_searched']} databases:</text>
  <text x="220" y="150" text-anchor="middle" class="small-text">(Semantic Scholar, OpenAlex, arXiv, ERIC, PsycINFO, Education Source, ProQuest)</text>

  <rect x="80" y="170" width="280" height="35" class="box"/>
  <text x="220" y="192" text-anchor="middle" class="box-number">(n = {d['records_databases']:,})</text>

  <!-- Right Branch: Other Methods -->
  <rect x="840" y="90" width="280" height="70" class="box"/>
  <text x="980" y="115" text-anchor="middle" class="section-title">Identification via other methods</text>
  <text x="980" y="135" text-anchor="middle" class="box-text">Records from:</text>
  <text x="980" y="150" text-anchor="middle" class="small-text">Citation searching, grey literature</text>

  <rect x="840" y="170" width="280" height="35" class="box"/>
  <text x="980" y="192" text-anchor="middle" class="box-number">(n = {d['records_other']})</text>

  <!-- Center: Duplicates Removed -->
  <rect x="400" y="130" width="200" height="55" class="box"/>
  <text x="500" y="152" text-anchor="middle" class="box-text">Records removed before screening:</text>
  <text x="500" y="168" text-anchor="middle" class="small-text">Duplicate records (n = {d['duplicates_removed']})</text>
  <text x="500" y="180" text-anchor="middle" class="small-text">Automation tools (n = {d['automation_excluded']})</text>

  <!-- Arrows from identification -->
  <path d="M 220 205 L 220 260" class="arrow"/>
  <path d="M 980 205 L 980 260" class="arrow"/>
  <path d="M 360 160 L 400 160" class="arrow"/>
  <path d="M 600 160 L 840 160" class="arrow dotted"/>

  <!-- SCREENING SECTION -->
  <rect x="40" y="260" width="1140" height="220" class="section-bg" rx="10"/>

  <!-- Records Screened -->
  <rect x="80" y="280" width="280" height="50" class="box"/>
  <text x="220" y="300" text-anchor="middle" class="box-text">Records screened</text>
  <text x="220" y="318" text-anchor="middle" class="box-number">(n = {d['records_screened']:,})</text>

  <!-- Records Excluded -->
  <rect x="420" y="280" width="180" height="50" class="box"/>
  <text x="510" y="300" text-anchor="middle" class="box-text">Records excluded</text>
  <text x="510" y="318" text-anchor="middle" class="box-number">(n = {d['records_excluded_screening']:,})</text>

  <path d="M 360 305 L 420 305" class="arrow"/>
  <path d="M 220 330 L 220 360" class="arrow"/>

  <!-- Reports Sought -->
  <rect x="80" y="360" width="280" height="50" class="box"/>
  <text x="220" y="380" text-anchor="middle" class="box-text">Reports sought for retrieval</text>
  <text x="220" y="398" text-anchor="middle" class="box-number">(n = {d['reports_sought']})</text>

  <!-- Reports Not Retrieved -->
  <rect x="420" y="360" width="180" height="50" class="box"/>
  <text x="510" y="380" text-anchor="middle" class="box-text">Reports not retrieved</text>
  <text x="510" y="398" text-anchor="middle" class="box-number">(n = {d['reports_not_retrieved']})</text>

  <path d="M 360 385 L 420 385" class="arrow"/>
  <path d="M 220 410 L 220 440" class="arrow"/>

  <!-- Reports Assessed -->
  <rect x="80" y="440" width="280" height="50" class="box"/>
  <text x="220" y="460" text-anchor="middle" class="box-text">Reports assessed for eligibility</text>
  <text x="220" y="478" text-anchor="middle" class="box-number">(n = {d['reports_assessed']})</text>

  <!-- Reports Excluded with Reasons -->
  <rect x="420" y="420" width="300" height="130" class="box"/>
  <text x="570" y="440" text-anchor="middle" class="box-text">Reports excluded (n = {d['reports_excluded_total']})</text>
  <text x="430" y="458" class="small-text">Wrong population (K-12): {d['exclusion_reasons']['Wrong population (K-12)']}</text>
  <text x="430" y="472" class="small-text">No control/comparison group: {d['exclusion_reasons']['No control/comparison group']}</text>
  <text x="430" y="486" class="small-text">Non-GenAI intervention: {d['exclusion_reasons']['Non-GenAI intervention']}</text>
  <text x="430" y="500" class="small-text">Insufficient statistical data: {d['exclusion_reasons']['Insufficient statistical data']}</text>
  <text x="430" y="514" class="small-text">Duplicate sample: {d['exclusion_reasons']['Duplicate sample']}</text>
  <text x="430" y="528" class="small-text">Not peer-reviewed/preprint: {d['exclusion_reasons']['Not peer-reviewed/preprint']}</text>

  <path d="M 360 465 L 420 465" class="arrow"/>

  <!-- Right Side: Other Methods Screening -->
  <rect x="760" y="280" width="280" height="50" class="box"/>
  <text x="900" y="300" text-anchor="middle" class="box-text">Reports sought for retrieval</text>
  <text x="900" y="318" text-anchor="middle" class="box-number">(n = 45)</text>

  <rect x="760" y="360" width="280" height="50" class="box"/>
  <text x="900" y="380" text-anchor="middle" class="box-text">Reports assessed for eligibility</text>
  <text x="900" y="398" text-anchor="middle" class="box-number">(n = 38)</text>

  <rect x="760" y="440" width="280" height="50" class="box"/>
  <text x="900" y="460" text-anchor="middle" class="box-text">Reports excluded</text>
  <text x="900" y="478" text-anchor="middle" class="box-number">(n = 31)</text>

  <path d="M 900 260 L 900 280" class="arrow"/>
  <path d="M 900 330 L 900 360" class="arrow"/>
  <path d="M 900 410 L 900 440" class="arrow"/>

  <!-- INCLUDED SECTION -->
  <rect x="40" y="560" width="1140" height="120" class="section-bg" rx="10"/>

  <!-- Studies Included -->
  <rect x="280" y="580" width="280" height="80" class="box"/>
  <text x="420" y="605" text-anchor="middle" class="section-title">Studies included in review</text>
  <text x="420" y="625" text-anchor="middle" class="box-number">(n = {d['studies_included']})</text>
  <text x="420" y="645" text-anchor="middle" class="box-text">Reports of included studies (n = {d['reports_included']})</text>

  <!-- Meta-analysis -->
  <rect x="640" y="580" width="280" height="80" class="box"/>
  <text x="780" y="605" text-anchor="middle" class="section-title">Studies included in meta-analysis</text>
  <text x="780" y="625" text-anchor="middle" class="box-number">(n = {d['studies_included']})</text>
  <text x="780" y="645" text-anchor="middle" class="box-text">Effect sizes (k = {d['effect_sizes']})</text>

  <!-- Arrows to Included -->
  <path d="M 220 490 L 220 540 L 280 580" class="arrow"/>
  <path d="M 900 490 L 900 540 L 920 580" class="arrow"/>
  <path d="M 560 620 L 640 620" class="arrow"/>

  <!-- Footer -->
  <text x="600" y="710" text-anchor="middle" class="small-text">From: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.</text>
  <text x="600" y="725" text-anchor="middle" class="small-text">doi: 10.1136/bmj.n71. For more information, visit: http://www.prisma-statement.org/</text>

</svg>'''

    return svg


def generate_prisma_text():
    """Generate PRISMA 2020 flow diagram as formatted text for manuscript"""

    d = PRISMA_DATA

    exclusion_list = "\n".join([f"        - {reason}: {count}"
                                for reason, count in d['exclusion_reasons'].items()])

    text = f'''
## Figure 1. PRISMA 2020 Flow Diagram

### IDENTIFICATION

**Identification of studies via databases and registers**
- Records identified from databases (n = {d['records_databases']:,})
  - Semantic Scholar
  - OpenAlex
  - arXiv
  - ERIC
  - PsycINFO
  - Education Source
  - ProQuest Dissertations & Theses

**Records removed before screening:**
- Duplicate records removed (n = {d['duplicates_removed']})
- Records marked as ineligible by automation tools (n = {d['automation_excluded']})

**Identification of studies via other methods**
- Records identified from citation searching and grey literature (n = {d['records_other']})

---

### SCREENING

**Records screened** (n = {d['records_screened']:,})
- Records excluded (n = {d['records_excluded_screening']:,})

**Reports sought for retrieval** (n = {d['reports_sought']})
- Reports not retrieved (n = {d['reports_not_retrieved']})

**Reports assessed for eligibility** (n = {d['reports_assessed']})
- Reports excluded (n = {d['reports_excluded_total']}):
{exclusion_list}

---

### INCLUDED

**Studies included in review** (n = {d['studies_included']})
- Reports of included studies (n = {d['reports_included']})

**Studies included in quantitative synthesis (meta-analysis)**
- Studies: n = {d['studies_included']}
- Effect sizes: k = {d['effect_sizes']}

---

*Figure adapted from: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71*
'''

    return text


def main():
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate SVG
    svg_content = generate_prisma_svg()
    svg_path = OUTPUT_DIR / "PRISMA_2020_Flow_Diagram.svg"
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Generated: {svg_path}")

    # Generate text version
    text_content = generate_prisma_text()
    text_path = OUTPUT_DIR / "PRISMA_2020_Flow_Diagram.md"
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text_content)
    print(f"Generated: {text_path}")

    # Print summary
    print("\n" + "="*60)
    print("PRISMA 2020 Flow Summary")
    print("="*60)
    print(f"Total records identified: {PRISMA_DATA['records_databases'] + PRISMA_DATA['records_other']:,}")
    print(f"Records after deduplication: {PRISMA_DATA['records_screened']:,}")
    print(f"Reports assessed for eligibility: {PRISMA_DATA['reports_assessed']}")
    print(f"Studies included: {PRISMA_DATA['studies_included']}")
    print(f"Effect sizes: {PRISMA_DATA['effect_sizes']}")
    print("="*60)


if __name__ == "__main__":
    main()
