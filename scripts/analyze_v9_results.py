#!/usr/bin/env python3
"""
Analyze v9.0 Extraction Results
Following Universal Codebook v2.2 + GenAI-HE Extension
"""

import json
import os
from pathlib import Path
from collections import Counter
import pandas as pd

def load_all_extractions(extraction_dir: str) -> list:
    """Load all JSON extraction files."""
    extractions = []
    for f in sorted(Path(extraction_dir).glob("*_extraction.json")):
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['_filename'] = f.name
            extractions.append(data)
    return extractions

def analyze_layer1(extractions: list) -> dict:
    """Analyze Layer 1: Study Identifiers"""
    years = Counter()
    countries = Counter()
    journals = Counter()
    design_types = Counter()

    for ext in extractions:
        layer1 = ext.get('layer1', {})
        if layer1.get('year', {}).get('value'):
            years[layer1['year']['value']] += 1
        if layer1.get('country', {}).get('value'):
            countries[layer1['country']['value']] += 1
        if layer1.get('journal', {}).get('value'):
            journals[layer1['journal']['value']] += 1
        if layer1.get('design_type', {}).get('value'):
            design_types[layer1['design_type']['value']] += 1

    return {
        'years': dict(sorted(years.items())),
        'countries': dict(countries.most_common(15)),
        'top_journals': dict(journals.most_common(10)),
        'design_types': dict(design_types.most_common())
    }

def analyze_layer2(extractions: list) -> dict:
    """Analyze Layer 2: Effect Size Statistics"""
    total_es = 0
    with_hedges_g = 0
    missing_sd = 0
    outcome_names = Counter()
    es_types = Counter()

    for ext in extractions:
        stats_list = ext.get('layer2_statistics', [])
        total_es += len(stats_list)

        for stat in stats_list:
            # Check for Hedges' g
            if stat.get('hedges_g', {}).get('value') is not None:
                with_hedges_g += 1

            # Check for missing SD
            sd_treatment = stat.get('sd_treatment', {}).get('value')
            sd_control = stat.get('sd_control', {}).get('value')
            if sd_treatment is None or sd_control is None:
                missing_sd += 1

            # Outcome names
            if stat.get('outcome_name', {}).get('value'):
                outcome_names[stat['outcome_name']['value']] += 1

            # Effect size types
            if stat.get('es_type', {}).get('value'):
                es_types[stat['es_type']['value']] += 1

    return {
        'total_effect_sizes': total_es,
        'with_hedges_g': with_hedges_g,
        'hedges_g_rate': f"{with_hedges_g/total_es*100:.1f}%" if total_es > 0 else "N/A",
        'missing_sd': missing_sd,
        'missing_sd_rate': f"{missing_sd/total_es*100:.1f}%" if total_es > 0 else "N/A",
        'top_outcomes': dict(outcome_names.most_common(15)),
        'es_types': dict(es_types.most_common())
    }

def analyze_layer3(extractions: list) -> dict:
    """Analyze Layer 3: GenAI-HE Moderators"""
    genai_tools = Counter()
    genai_versions = Counter()
    blooms_levels = Counter()
    study_designs = Counter()
    education_levels = Counter()
    disciplines = Counter()
    learning_domains = Counter()
    outcome_dimensions = Counter()
    intervention_types = Counter()
    control_conditions = Counter()
    publication_types = Counter()
    intervention_durations = Counter()

    for ext in extractions:
        mods = ext.get('layer3_moderators', {})

        if mods.get('genai_tool', {}).get('value'):
            genai_tools[mods['genai_tool']['value']] += 1
        if mods.get('genai_tool_version', {}).get('value'):
            genai_versions[mods['genai_tool_version']['value']] += 1
        if mods.get('blooms_level', {}).get('value'):
            blooms_levels[mods['blooms_level']['value']] += 1
        if mods.get('study_design', {}).get('value'):
            study_designs[mods['study_design']['value']] += 1
        if mods.get('education_level', {}).get('value'):
            education_levels[mods['education_level']['value']] += 1
        if mods.get('discipline', {}).get('value'):
            disciplines[mods['discipline']['value']] += 1
        if mods.get('learning_domain', {}).get('value'):
            learning_domains[mods['learning_domain']['value']] += 1
        if mods.get('outcome_dimension', {}).get('value'):
            outcome_dimensions[mods['outcome_dimension']['value']] += 1
        if mods.get('intervention_type', {}).get('value'):
            intervention_types[mods['intervention_type']['value']] += 1
        if mods.get('control_condition', {}).get('value'):
            control_conditions[mods['control_condition']['value']] += 1
        if mods.get('publication_type', {}).get('value'):
            publication_types[mods['publication_type']['value']] += 1
        if mods.get('intervention_duration', {}).get('value'):
            intervention_durations[mods['intervention_duration']['value']] += 1

    return {
        'genai_tools': dict(genai_tools.most_common()),
        'genai_versions': dict(genai_versions.most_common(10)),
        'blooms_levels': dict(blooms_levels.most_common()),
        'study_designs': dict(study_designs.most_common()),
        'education_levels': dict(education_levels.most_common()),
        'disciplines': dict(disciplines.most_common()),
        'learning_domains': dict(learning_domains.most_common()),
        'outcome_dimensions': dict(outcome_dimensions.most_common()),
        'intervention_types': dict(intervention_types.most_common()),
        'control_conditions': dict(control_conditions.most_common()),
        'publication_types': dict(publication_types.most_common()),
        'intervention_durations': dict(intervention_durations.most_common())
    }

def analyze_validation(extractions: list) -> dict:
    """Analyze validation status and warnings"""
    statuses = Counter()
    warning_types = Counter()

    for ext in extractions:
        status = ext.get('validation_status', 'UNKNOWN')
        statuses[status] += 1

        for warning in ext.get('validation_warnings', []):
            # Extract warning type
            if ':' in warning:
                warning_type = warning.split(':')[0]
                warning_types[warning_type] += 1

    return {
        'validation_statuses': dict(statuses.most_common()),
        'warning_types': dict(warning_types.most_common())
    }

def generate_report(analysis: dict) -> str:
    """Generate markdown report"""
    report = []
    report.append("# GenAI-HE Meta-Analysis v9.0 추출 결과 분석")
    report.append(f"\n**총 연구 수**: {analysis['total_studies']}")
    report.append(f"**총 효과크기 수**: {analysis['layer2']['total_effect_sizes']}")
    report.append(f"**Hedges' g 계산률**: {analysis['layer2']['hedges_g_rate']}")
    report.append(f"**SD 누락률**: {analysis['layer2']['missing_sd_rate']}")

    report.append("\n## 1. 연도별 분포 (Layer 1)")
    for year, count in analysis['layer1']['years'].items():
        report.append(f"- {year}: {count}편")

    report.append("\n## 2. 국가별 분포 (Layer 1)")
    for country, count in analysis['layer1']['countries'].items():
        report.append(f"- {country}: {count}편")

    report.append("\n## 3. 연구 설계 (Layer 1)")
    for design, count in analysis['layer1']['design_types'].items():
        report.append(f"- {design}: {count}편")

    report.append("\n## 4. GenAI 도구 (Layer 3)")
    for tool, count in analysis['layer3']['genai_tools'].items():
        report.append(f"- {tool}: {count}편")

    report.append("\n## 5. GenAI 버전 (Layer 3)")
    for version, count in analysis['layer3']['genai_versions'].items():
        report.append(f"- {version}: {count}편")

    report.append("\n## 6. Bloom's Level (Layer 3)")
    for level, count in analysis['layer3']['blooms_levels'].items():
        report.append(f"- {level}: {count}편")

    report.append("\n## 7. 교육 수준 (Layer 3)")
    for level, count in analysis['layer3']['education_levels'].items():
        report.append(f"- {level}: {count}편")

    report.append("\n## 8. 학문 분야 (Layer 3)")
    for disc, count in analysis['layer3']['disciplines'].items():
        report.append(f"- {disc}: {count}편")

    report.append("\n## 9. 학습 영역 (Layer 3)")
    for domain, count in analysis['layer3']['learning_domains'].items():
        report.append(f"- {domain}: {count}편")

    report.append("\n## 10. 결과 차원 (Layer 3)")
    for dim, count in analysis['layer3']['outcome_dimensions'].items():
        report.append(f"- {dim}: {count}편")

    report.append("\n## 11. 개입 유형 (Layer 3)")
    for itype, count in analysis['layer3']['intervention_types'].items():
        report.append(f"- {itype}: {count}편")

    report.append("\n## 12. 통제 조건 (Layer 3)")
    for cond, count in analysis['layer3']['control_conditions'].items():
        report.append(f"- {cond}: {count}편")

    report.append("\n## 13. 개입 기간 (Layer 3)")
    for dur, count in analysis['layer3']['intervention_durations'].items():
        report.append(f"- {dur}: {count}편")

    report.append("\n## 14. 효과크기 유형 (Layer 2)")
    for es_type, count in analysis['layer2']['es_types'].items():
        report.append(f"- {es_type}: {count}개")

    report.append("\n## 15. 주요 결과 변수 (Layer 2)")
    for outcome, count in list(analysis['layer2']['top_outcomes'].items())[:15]:
        report.append(f"- {outcome}: {count}개")

    report.append("\n## 16. 검증 상태 (Layer 5)")
    for status, count in analysis['validation']['validation_statuses'].items():
        report.append(f"- {status}: {count}편")

    report.append("\n## 17. 주요 경고 유형")
    for warning, count in analysis['validation']['warning_types'].items():
        report.append(f"- {warning}: {count}회")

    return "\n".join(report)

def main():
    extraction_dir = "/Volumes/External SSD/Projects/GenAI-HE-Review-AIMC/data/extractions_v9"
    output_dir = "/Volumes/External SSD/Projects/GenAI-HE-Review-AIMC/data/03_final"

    print("Loading extractions...")
    extractions = load_all_extractions(extraction_dir)
    print(f"Loaded {len(extractions)} extractions")

    print("\nAnalyzing...")
    analysis = {
        'total_studies': len(extractions),
        'layer1': analyze_layer1(extractions),
        'layer2': analyze_layer2(extractions),
        'layer3': analyze_layer3(extractions),
        'validation': analyze_validation(extractions)
    }

    # Save analysis JSON
    with open(f"{output_dir}/v9_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\nSaved analysis to {output_dir}/v9_analysis.json")

    # Generate and save report
    report = generate_report(analysis)
    with open(f"{output_dir}/v9_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Saved report to {output_dir}/v9_analysis_report.md")

    # Print summary
    print("\n" + "="*60)
    print("V9.0 EXTRACTION SUMMARY")
    print("="*60)
    print(f"\n총 연구 수: {len(extractions)}")
    print(f"총 효과크기 수: {analysis['layer2']['total_effect_sizes']}")
    print(f"Hedges' g 계산률: {analysis['layer2']['hedges_g_rate']}")
    print(f"SD 누락률: {analysis['layer2']['missing_sd_rate']}")

    print("\n--- GenAI Tools ---")
    for tool, count in analysis['layer3']['genai_tools'].items():
        print(f"  {tool}: {count}")

    print("\n--- Study Designs ---")
    for design, count in analysis['layer3']['study_designs'].items():
        print(f"  {design}: {count}")

    print("\n--- Education Levels ---")
    for level, count in analysis['layer3']['education_levels'].items():
        print(f"  {level}: {count}")

    print("\n--- Bloom's Levels ---")
    for level, count in analysis['layer3']['blooms_levels'].items():
        print(f"  {level}: {count}")

    print("\n--- Validation Status ---")
    for status, count in analysis['validation']['validation_statuses'].items():
        print(f"  {status}: {count}")

if __name__ == "__main__":
    main()
