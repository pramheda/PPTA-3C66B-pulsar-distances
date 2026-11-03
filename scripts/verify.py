"""Verify file integrity, rerun both checks and compare with the saved results (standard library only)."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_paper
import pulsar_term

ROOT = Path(__file__).resolve().parents[1]


def run(skip_hashes=False):
    checks = 0
    if not skip_hashes:
        for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
            sha, name = line.split('  ', 1)
            p = ROOT / name
            assert p.is_file() and not p.is_symlink(), name
            assert hashlib.sha256(p.read_bytes()).hexdigest() == sha, name
            checks += 1
    paper = check_paper.check()
    term = pulsar_term.run()
    assert paper == json.loads((ROOT / 'results/paper_checks.json').read_text()); checks += 1
    assert term == json.loads((ROOT / 'results/pulsar_term_frequencies.json').read_text()); checks += 1

    d = {r['pulsar']: r for r in paper['distances']}
    assert d['J1643-1224']['distance_from_cited_parallax_pc'] == 763.36
    assert round(d['J1643-1224']['printed_distance_pc'] - 4000, 2) == 763.36  # a stray leading "4"
    assert d['J0613-0200']['printed_over_implied'] == 0.1                       # a factor of ten
    assert d['J2129-5721']['cited_object'] == 'J2129-0429' and not d['J2129-5721']['same_object']
    f = paper['frequentist_search']
    assert f['section_4_5']['printed_FAP'] == 0.5 and abs(f['section_4_5']['FAP_from_stated_convention'] - 0.04393) < 1e-5
    assert f['section_4_5']['F_e'] != f['conclusion']['F_e'] and f['nondetection_unchanged']
    assert not paper['conservative_chirp_mass_limit']['consistent']
    checks += 7
    return dict(status='PASS', checks=checks, hashes_checked=not skip_hashes,
                distances={k: [v['printed_distance_pc'], v['distance_from_cited_parallax_pc'], v['cited_object']] for k, v in d.items()},
                FAP_printed_vs_stated_convention=[f['section_4_5']['printed_FAP'], f['section_4_5']['FAP_from_stated_convention']],
                pulsar_term_nHz={r['pulsar']: [r['pulsar_term_frequency_printed_nHz'], r['pulsar_term_frequency_cited_nHz']] for r in term['pulsars']})


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--skip-hashes', action='store_true')
    print(json.dumps(run(p.parse_args().skip_hashes), indent=2))
