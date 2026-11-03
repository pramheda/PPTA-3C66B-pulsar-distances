"""Check three Table 2 distances and three reported statistics in Cardinal Tremblay et al. (2026).

Python standard library only. Reads the verbatim LaTeX excerpts in sources/ and the cited source
values in data/, then prints a JSON report.
"""
from pathlib import Path
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
EXCERPTS = ROOT / 'sources/tremblay2026_v2_excerpts.tex'


def blocks():
    """Map each original line number to its text, using the '%% lines a-b' headers."""
    lines, current = {}, None
    for text in EXCERPTS.read_text().splitlines():
        m = re.match(r'%% lines (\d+)-(\d+)$', text)
        if m:
            current = int(m.group(1))
        elif current is not None:
            lines[current] = text
            current += 1
    return lines


def table2(lines):
    rows = {}
    for n, text in lines.items():
        m = re.match(r'\s*(J\d{4}[+-]\d{4}A?)\s*&\s*\$(.*?)\$\s*&\s*(.*?)\s*&\s*\\citet\{([^}]*)\}', text)
        if not m:
            continue
        name, value, method, cite = m.groups()
        sym = re.fullmatch(r'([\d.]+)\s*\\pm\s*([\d.]+)', value)
        asym = re.fullmatch(r'([\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}', value)
        d, plus, minus = (float(sym[1]), float(sym[2]), float(sym[2])) if sym else \
                         (float(asym[1]), float(asym[2]), float(asym[3]))
        rows[name] = dict(line=n, distance_pc=d, plus_pc=plus, minus_pc=minus, method=method.strip(), citation=cite)
    return rows


def value_on(lines, n, pattern):
    m = re.search(pattern, lines[n])
    assert m, (n, pattern)
    return float(m.group(1))


def check():
    lines = blocks()
    rows = table2(lines)
    assert len(rows) == 31, len(rows)
    cited = json.loads((ROOT / 'data/cited_measurements.json').read_text())['rows']

    distances = []
    for c in cited:
        p, s = c['pulsar'], c['cited_source']
        printed = rows[p]
        assert printed['distance_pc'] == c['paper_table2']['distance_pc']
        implied = 1000 / s['parallax_mas']
        # Linear propagation: a larger parallax error side gives the smaller-distance side.
        implied_plus = 1000 * s['minus_mas'] / s['parallax_mas']**2
        implied_minus = 1000 * s['plus_mas'] / s['parallax_mas']**2
        distances.append(dict(
            pulsar=p, table2_line=printed['line'],
            printed_distance_pc=printed['distance_pc'], printed_errors_pc=[printed['plus_pc'], printed['minus_pc']],
            cited_object=s['object'], cited_parallax_mas=[s['parallax_mas'], s['plus_mas'], s['minus_mas']],
            cited_location=s['location'],
            distance_from_cited_parallax_pc=round(implied, 2),
            errors_from_cited_parallax_pc=[round(implied_plus, 2), round(implied_minus, 2)],
            printed_over_implied=round(printed['distance_pc'] / implied, 6),
            same_object=s['object'] == p))

    fe_section = value_on(lines, 481, r'mathcal\{F\}_\\text\{e\}=([\d.]+)')
    fap_section = value_on(lines, 481, r'FAP\}=([\d.]+)')
    p_section = value_on(lines, 485, r'p\\text\{-value\} = ([\d.]+)')
    fe_conclusion = value_on(lines, 563, r'mathcal\{F\}_e = ([\d.]+)')
    fap_conclusion = value_on(lines, 563, r'FAP\}=([\d.]+)')
    assert 'trials factor for our search is one' in lines[483]
    assert 'chi-squared distribution with four degrees of freedom' in lines[484]
    fap = lambda f: math.exp(-f) * (1 + f)          # P(chi2_4 > 2F) for the stated null distribution
    frequentist = dict(
        section_4_5=dict(line=481, F_e=fe_section, printed_FAP=fap_section, printed_p_value=p_section,
                         FAP_from_stated_convention=round(fap(fe_section), 5)),
        conclusion=dict(line=563, F_e=fe_conclusion, printed_FAP=fap_conclusion,
                        FAP_from_stated_convention=round(fap(fe_conclusion), 5)),
        detection_threshold_FAP=1e-4,
        nondetection_unchanged=fap(fe_section) > 1e-4 and fap(fe_conclusion) > 1e-4)

    results_limit = value_on(lines, 380, r'< ([\d.]+)\\ \\times 10\^\{8\} ~M_\\odot\$ when the pulsar term')
    conclusion_limit = value_on(lines, 569, r'chirp mass of \$\\mathcal\{M\} < ([\d.]+) \\times 10\^8')
    conservative = dict(
        description='95% chirp-mass limit with the pulsar term under the conservative uniform-in-mass prior',
        results_section_4_2=dict(line=380, value_1e8_Msun=results_limit),
        conclusion=dict(line=569, value_1e8_Msun=conclusion_limit),
        consistent=results_limit == conclusion_limit)

    return dict(source=EXCERPTS.name, table2_rows_parsed=len(rows), distances=distances,
                frequentist_search=frequentist, conservative_chirp_mass_limit=conservative)


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
