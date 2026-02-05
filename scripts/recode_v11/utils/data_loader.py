"""
Data loader for v8.1 CSV and Study_ID to PDF mapping.
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import csv

logger = logging.getLogger(__name__)


def load_v81_csv(csv_path: str) -> List[Dict]:
    """Load v8.1 CSV and return list of row dicts."""
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            for field in ['n_Treatment', 'n_Control', 'Year']:
                if row.get(field):
                    try:
                        row[field] = float(row[field])
                    except (ValueError, TypeError):
                        pass
            for field in ['M_Treatment', 'SD_Treatment', 'M_Control', 'SD_Control',
                         'Hedges_g', 'SE_g', 'Variance_g']:
                if row.get(field):
                    try:
                        row[field] = float(row[field])
                    except (ValueError, TypeError):
                        row[field] = None
            rows.append(row)
    logger.info(f"Loaded {len(rows)} rows from {csv_path}")
    return rows


def get_unique_studies(rows: List[Dict]) -> Dict[str, List[Dict]]:
    """Group rows by Study_ID, returning {study_id: [rows]}."""
    studies = {}
    for row in rows:
        sid = str(row.get('Study_ID', ''))
        studies.setdefault(sid, []).append(row)
    logger.info(f"Found {len(studies)} unique studies")
    return studies


def build_study_pdf_mapping(
    pdf_directory: str,
    rows: List[Dict]
) -> Dict[str, Optional[str]]:
    """
    Map Study_ID to PDF file path.
    PDF naming convention: {NNN}_{Author}_{Year}_{Title}.pdf
    Study_ID is the numeric prefix (e.g., '1' maps to '001_*')
    """
    pdf_dir = Path(pdf_directory)
    pdf_files = sorted(pdf_dir.glob("*.pdf"))

    # Build index: numeric prefix -> pdf path
    pdf_index = {}
    for pdf in pdf_files:
        match = re.match(r'^(\d+)', pdf.name)
        if match:
            num = int(match.group(1))
            pdf_index[num] = str(pdf)

    # Map Study_ID to PDF
    mapping = {}
    study_ids = set(str(row.get('Study_ID', '')) for row in rows)

    for sid in study_ids:
        try:
            num = int(float(sid))
            mapping[sid] = pdf_index.get(num)
        except (ValueError, TypeError):
            mapping[sid] = None

    found = sum(1 for v in mapping.values() if v)
    logger.info(f"Mapped {found}/{len(mapping)} studies to PDFs")
    return mapping


def get_study_metadata(rows: List[Dict], study_id: str) -> Dict:
    """Get metadata for a study from the first row with that Study_ID."""
    for row in rows:
        if str(row.get('Study_ID', '')) == str(study_id):
            return {
                'study_id': study_id,
                'title': row.get('Title', ''),
                'year': row.get('Year', ''),
                'authors': row.get('Authors', ''),
            }
    return {'study_id': study_id}
