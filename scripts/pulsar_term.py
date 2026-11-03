"""Pulsar-term gravitational-wave frequency at the printed and the cited-parallax distances.

Python standard library only. For a circular binary evolving under leading-order radiation
reaction, the pulsar term samples the wave emitted a time L(1 - cos theta)/c earlier, where L is
the pulsar distance and theta the sky angle between pulsar and source:

    f_p = f_E [1 + (256/5) (pi f_E)^(8/3) (G Mc / c^3)^(5/3) L (1 - cos theta) / c]^(-3/8)

This is a central-value illustration of how much the distance errors change the modelled signal.
It is not a likelihood, a posterior or a revised limit.
"""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
G, C, MSUN, PC = 6.67430e-11, 299792458.0, 1.98840987e30, 3.0856775814913673e16
OBLIQUITY = math.radians(84381.406 / 3600)   # IERS 2010 mean obliquity at J2000


def ecliptic_to_equatorial(lon_deg, lat_deg):
    lon, lat = math.radians(lon_deg), math.radians(lat_deg)
    x, y, z = math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)
    y, z = y * math.cos(OBLIQUITY) - z * math.sin(OBLIQUITY), y * math.sin(OBLIQUITY) + z * math.cos(OBLIQUITY)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(z))


def sexagesimal(text, hours):
    sign = -1 if text.strip().startswith('-') else 1
    a, b, c = (abs(float(v)) for v in text.split(':'))
    return sign * (a + b / 60 + c / 3600) * (15 if hours else 1)


def cos_angle(ra1, dec1, ra2, dec2):
    r1, d1, r2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    return math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)


def pulsar_term_frequency(f_earth, chirp_mass, distance_pc, cos_theta):
    tau = distance_pc * PC * (1 - cos_theta) / C
    k = 256 / 5 * (math.pi * f_earth) ** (8 / 3) * (G * chirp_mass * MSUN / C ** 3) ** (5 / 3)
    return f_earth * (1 + k * tau) ** (-3 / 8)


def run():
    pos = json.loads((ROOT / 'data/sky_positions.json').read_text())
    src = pos['source_3C66B']
    ra_s, dec_s = sexagesimal(src['ra_hms'], True), sexagesimal(src['dec_dms'], False)
    f_e, mc = src['gw_frequency_nHz'] * 1e-9, src['chirp_mass_limit_Msun']
    cited = {r['pulsar']: r for r in json.loads((ROOT / 'data/cited_measurements.json').read_text())['rows']}
    rows = []
    for p in pos['pulsars']:
        ra, dec = ecliptic_to_equatorial(p['ELONG_deg'], p['ELAT_deg'])
        # The J-name encodes truncated J2000 RA (hhmm) and Dec (ddmm): a coordinate sanity check.
        name = p['pulsar']
        assert int(ra / 15) == int(name[1:3]) and int((ra / 15 % 1) * 60) == int(name[3:5]), (name, ra)
        assert int(abs(dec)) == int(name[6:8]) and int(abs(dec) % 1 * 60) == int(name[8:10]), (name, dec)
        mu = cos_angle(ra, dec, ra_s, dec_s)
        c = cited[name]
        printed = c['paper_table2']['distance_pc']
        implied = 1000 / c['cited_source']['parallax_mas']
        fp_printed = pulsar_term_frequency(f_e, mc, printed, mu)
        fp_implied = pulsar_term_frequency(f_e, mc, implied, mu)
        rows.append(dict(pulsar=name, ra_deg=round(ra, 6), dec_deg=round(dec, 6),
                         angle_to_3C66B_deg=round(math.degrees(math.acos(mu)), 3),
                         printed_distance_pc=printed, cited_parallax_distance_pc=round(implied, 2),
                         light_travel_delay_printed_yr=round(printed * PC * (1 - mu) / C / 3.15576e7, 1),
                         light_travel_delay_cited_yr=round(implied * PC * (1 - mu) / C / 3.15576e7, 1),
                         pulsar_term_frequency_printed_nHz=round(fp_printed * 1e9, 2),
                         pulsar_term_frequency_cited_nHz=round(fp_implied * 1e9, 2)))
    return dict(earth_term_frequency_nHz=src['gw_frequency_nHz'], chirp_mass_Msun=mc,
                scope='Central-value waveform illustration; not a likelihood or a revised limit.', pulsars=rows)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
