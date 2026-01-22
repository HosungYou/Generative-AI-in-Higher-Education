#!/usr/bin/env python3
"""
Effect Size Data Extraction Script for Meta-Analysis
Extracts effect sizes, sample sizes, and statistics from PDFs
"""

import os
import re
import json
import fitz  # PyMuPDF
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

@dataclass
class EffectSizeData:
    """Data structure for extracted effect size information"""
    filename: str
    study_id: str = ""

    # Sample size
    n_total: Optional[int] = None
    n_treatment: Optional[int] = None
    n_control: Optional[int] = None

    # Effect sizes
    cohens_d: Optional[float] = None
    hedges_g: Optional[float] = None
    correlation_r: Optional[float] = None
    eta_squared: Optional[float] = None
    partial_eta_squared: Optional[float] = None
    omega_squared: Optional[float] = None

    # Statistics for conversion
    t_value: Optional[float] = None
    f_value: Optional[float] = None
    p_value: Optional[float] = None
    df1: Optional[int] = None
    df2: Optional[int] = None

    # Means and SDs
    mean_treatment: Optional[float] = None
    mean_control: Optional[float] = None
    sd_treatment: Optional[float] = None
    sd_control: Optional[float] = None

    # Context
    outcome_type: str = ""
    notes: str = ""
    raw_excerpts: List[str] = None

    def __post_init__(self):
        if self.raw_excerpts is None:
            self.raw_excerpts = []


class EffectSizeExtractor:
    """Extract effect size data from academic PDFs"""

    # Regex patterns for effect sizes
    PATTERNS = {
        # Cohen's d patterns
        'cohens_d': [
            r"Cohen['\u2019]?s?\s*d\s*[=:]\s*([+-]?\d+\.?\d*)",
            r"d\s*[=:]\s*([+-]?\d+\.?\d*)",
            r"effect\s+size\s*[=:]\s*([+-]?\d+\.?\d*)",
            r"ES\s*[=:]\s*([+-]?\d+\.?\d*)",
        ],

        # Hedges' g
        'hedges_g': [
            r"Hedges['\u2019]?\s*g\s*[=:]\s*([+-]?\d+\.?\d*)",
            r"g\s*[=:]\s*([+-]?\d+\.?\d*)",
        ],

        # Correlation
        'correlation_r': [
            r"r\s*[=:]\s*([+-]?\d*\.?\d+)",
            r"correlation\s*[=:]\s*([+-]?\d*\.?\d+)",
        ],

        # Eta squared
        'eta_squared': [
            r"η²\s*[=:]\s*(\d*\.?\d+)",
            r"eta[- ]?squared?\s*[=:]\s*(\d*\.?\d+)",
            r"η2\s*[=:]\s*(\d*\.?\d+)",
        ],

        # Partial eta squared
        'partial_eta_squared': [
            r"ηp²\s*[=:]\s*(\d*\.?\d+)",
            r"partial\s+η²\s*[=:]\s*(\d*\.?\d+)",
            r"partial\s+eta[- ]?squared?\s*[=:]\s*(\d*\.?\d+)",
            r"ηp2\s*[=:]\s*(\d*\.?\d+)",
        ],

        # Sample size patterns
        'n_total': [
            r"[Nn]\s*[=:]\s*(\d+)",
            r"sample\s+size\s*[=:]\s*(\d+)",
            r"(\d+)\s*participants",
            r"(\d+)\s*students",
            r"total\s+of\s+(\d+)",
        ],

        # T-value
        't_value': [
            r"t\s*\(\s*\d+\s*\)\s*[=:]\s*([+-]?\d+\.?\d*)",
            r"t\s*[=:]\s*([+-]?\d+\.?\d*)",
        ],

        # F-value
        'f_value': [
            r"F\s*\(\s*\d+\s*,\s*\d+\s*\)\s*[=:]\s*(\d+\.?\d*)",
            r"F\s*[=:]\s*(\d+\.?\d*)",
        ],

        # P-value
        'p_value': [
            r"p\s*[<>=]\s*\.?(\d+\.?\d*)",
            r"p\s*[=:]\s*\.?(\d+\.?\d*)",
        ],

        # Means
        'mean': [
            r"[Mm]ean\s*[=:]\s*(\d+\.?\d*)",
            r"M\s*[=:]\s*(\d+\.?\d*)",
        ],

        # Standard deviations
        'sd': [
            r"SD\s*[=:]\s*(\d+\.?\d*)",
            r"standard\s+deviation\s*[=:]\s*(\d+\.?\d*)",
        ],
    }

    # Keywords for finding relevant sections
    RESULT_KEYWORDS = [
        'results', 'findings', 'effect size', 'effect sizes',
        'statistical analysis', 'main effects', 'treatment effect',
        'experimental group', 'control group', 'pre-test', 'post-test',
        'ANCOVA', 'ANOVA', 't-test', 'regression'
    ]

    def __init__(self, pdf_dir: str, output_dir: str):
        self.pdf_dir = Path(pdf_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error reading {pdf_path.name}: {e}")
            return ""

    def find_relevant_sections(self, text: str) -> List[str]:
        """Find text sections likely to contain effect sizes"""
        sections = []
        lines = text.split('\n')

        in_relevant_section = False
        current_section = []

        for i, line in enumerate(lines):
            line_lower = line.lower()

            # Check if this line indicates a relevant section
            if any(kw in line_lower for kw in self.RESULT_KEYWORDS):
                in_relevant_section = True

            if in_relevant_section:
                current_section.append(line)

                # Check if we've left the section (new major heading)
                if len(current_section) > 100:  # Limit section size
                    sections.append('\n'.join(current_section))
                    current_section = []
                    in_relevant_section = False

        if current_section:
            sections.append('\n'.join(current_section))

        # If no sections found, return full text
        return sections if sections else [text]

    def extract_pattern(self, text: str, pattern_key: str) -> List[float]:
        """Extract values matching patterns for a given key"""
        values = []
        patterns = self.PATTERNS.get(pattern_key, [])

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match)
                    # Validate reasonable ranges
                    if pattern_key in ['cohens_d', 'hedges_g']:
                        if -5 <= value <= 5:
                            values.append(value)
                    elif pattern_key in ['eta_squared', 'partial_eta_squared', 'correlation_r']:
                        if 0 <= abs(value) <= 1:
                            values.append(value)
                    elif pattern_key == 'n_total':
                        if 10 <= value <= 10000:
                            values.append(int(value))
                    else:
                        values.append(value)
                except ValueError:
                    continue

        return values

    def extract_context_around_match(self, text: str, pattern: str, window: int = 200) -> List[str]:
        """Get text context around pattern matches"""
        contexts = []
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = max(0, match.start() - window)
            end = min(len(text), match.end() + window)
            contexts.append(text[start:end])
        return contexts

    def process_pdf(self, pdf_path: Path) -> EffectSizeData:
        """Process a single PDF and extract effect size data"""
        data = EffectSizeData(filename=pdf_path.name)

        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            data.notes = "Failed to extract text"
            return data

        # Find relevant sections
        sections = self.find_relevant_sections(text)
        combined_text = '\n'.join(sections)

        # Extract effect sizes
        cohens_d_values = self.extract_pattern(combined_text, 'cohens_d')
        if cohens_d_values:
            data.cohens_d = cohens_d_values[0]  # Take first found
            data.raw_excerpts.extend(
                self.extract_context_around_match(combined_text, r"Cohen['\u2019]?s?\s*d\s*[=:]")
            )

        hedges_g_values = self.extract_pattern(combined_text, 'hedges_g')
        if hedges_g_values:
            data.hedges_g = hedges_g_values[0]

        r_values = self.extract_pattern(combined_text, 'correlation_r')
        if r_values:
            data.correlation_r = r_values[0]

        eta_values = self.extract_pattern(combined_text, 'eta_squared')
        if eta_values:
            data.eta_squared = eta_values[0]

        partial_eta_values = self.extract_pattern(combined_text, 'partial_eta_squared')
        if partial_eta_values:
            data.partial_eta_squared = partial_eta_values[0]
            data.raw_excerpts.extend(
                self.extract_context_around_match(combined_text, r"η[p]?²?\s*[=:]")
            )

        # Extract sample sizes
        n_values = self.extract_pattern(combined_text, 'n_total')
        if n_values:
            data.n_total = max(n_values)  # Take largest (likely total N)

        # Extract statistics
        t_values = self.extract_pattern(combined_text, 't_value')
        if t_values:
            data.t_value = t_values[0]

        f_values = self.extract_pattern(combined_text, 'f_value')
        if f_values:
            data.f_value = f_values[0]

        p_values = self.extract_pattern(combined_text, 'p_value')
        if p_values:
            data.p_value = min(p_values)  # Take smallest (most significant)

        # Limit excerpts
        data.raw_excerpts = data.raw_excerpts[:5]

        return data

    def process_all_pdfs(self) -> List[EffectSizeData]:
        """Process all PDFs in the directory"""
        results = []
        pdf_files = list(self.pdf_dir.glob("*.pdf"))

        print(f"Found {len(pdf_files)} PDF files")

        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"Processing [{i}/{len(pdf_files)}]: {pdf_path.name}")
            data = self.process_pdf(pdf_path)
            results.append(data)

        return results

    def save_results(self, results: List[EffectSizeData], filename: str = "extracted_effect_sizes"):
        """Save results to JSON and CSV"""
        # Save to JSON
        json_path = self.output_dir / f"{filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in results], f, indent=2, ensure_ascii=False)
        print(f"Saved JSON: {json_path}")

        # Save to CSV (simplified)
        csv_path = self.output_dir / f"{filename}.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            headers = [
                'filename', 'n_total', 'cohens_d', 'hedges_g',
                'eta_squared', 'partial_eta_squared', 'correlation_r',
                't_value', 'f_value', 'p_value', 'notes'
            ]
            f.write(','.join(headers) + '\n')

            for r in results:
                row = [
                    r.filename,
                    str(r.n_total or ''),
                    str(r.cohens_d or ''),
                    str(r.hedges_g or ''),
                    str(r.eta_squared or ''),
                    str(r.partial_eta_squared or ''),
                    str(r.correlation_r or ''),
                    str(r.t_value or ''),
                    str(r.f_value or ''),
                    str(r.p_value or ''),
                    r.notes.replace(',', ';')
                ]
                f.write(','.join(row) + '\n')
        print(f"Saved CSV: {csv_path}")

        # Generate summary report
        self.generate_summary(results)

    def generate_summary(self, results: List[EffectSizeData]):
        """Generate a summary report"""
        report_path = self.output_dir / "extraction_summary.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Effect Size Extraction Summary\n\n")
            f.write(f"**Total PDFs processed:** {len(results)}\n\n")

            # Count successful extractions
            with_d = sum(1 for r in results if r.cohens_d is not None)
            with_eta = sum(1 for r in results if r.partial_eta_squared is not None or r.eta_squared is not None)
            with_n = sum(1 for r in results if r.n_total is not None)

            f.write("## Extraction Success Rate\n\n")
            f.write(f"| Metric | Found | Percentage |\n")
            f.write(f"|--------|-------|------------|\n")
            f.write(f"| Cohen's d | {with_d} | {with_d/len(results)*100:.1f}% |\n")
            f.write(f"| Eta squared | {with_eta} | {with_eta/len(results)*100:.1f}% |\n")
            f.write(f"| Sample size | {with_n} | {with_n/len(results)*100:.1f}% |\n")

            f.write("\n## Individual Results\n\n")
            f.write("| Filename | N | d | η² | Notes |\n")
            f.write("|----------|---|---|----|----- |\n")

            for r in results:
                d_val = f"{r.cohens_d:.2f}" if r.cohens_d else "-"
                eta_val = f"{r.partial_eta_squared or r.eta_squared:.3f}" if (r.partial_eta_squared or r.eta_squared) else "-"
                n_val = str(r.n_total) if r.n_total else "-"
                notes = r.notes[:50] if r.notes else ""
                f.write(f"| {r.filename[:40]}... | {n_val} | {d_val} | {eta_val} | {notes} |\n")

            f.write("\n## Next Steps\n\n")
            f.write("1. Review extracted values against source PDFs\n")
            f.write("2. Manually fill in missing values\n")
            f.write("3. Calculate effect sizes from statistics where needed\n")
            f.write("4. Convert all to Cohen's d for meta-analysis\n")

        print(f"Saved summary: {report_path}")


def main():
    # Paths
    pdf_dir = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness/Generative-AI-in-Higher-Education/pdfs")
    output_dir = Path("/Volumes/External SSD/Projects/Research/Done/January/GenAI_Effectiveness/Generative-AI-in-Higher-Education/data")

    # Run extraction
    extractor = EffectSizeExtractor(pdf_dir, output_dir)
    results = extractor.process_all_pdfs()
    extractor.save_results(results)

    print("\n✅ Extraction complete!")
    print(f"Results saved to: {output_dir}")


if __name__ == "__main__":
    main()
