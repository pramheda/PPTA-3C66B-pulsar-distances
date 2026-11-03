# Claim-to-evidence map

| Claim | Inspect | Reproduce |
|---|---|---|
| J1643−1224 is printed as 4763.36 pc; the cited parallax gives 763.36 pc | Excerpt line 740; `data/cited_measurements.json` | `python3 scripts/check_paper.py` |
| J0613−0200 is printed ten times too small | Excerpt line 727; Verbiest et al. (2009) Table 5 | `python3 scripts/check_paper.py` |
| J2129−5721 carries J2129−0429's parallax | Excerpt line 752; Jennings et al. (2018) Table 2 | `python3 scripts/check_paper.py` |
| FAP = 0.50 is inconsistent with the stated null distribution and with p = 0.04 | Excerpt lines 476–488 and 557–570 | `python3 scripts/check_paper.py` |
| The conservative pulsar-term mass limit is given as 10.63 and as 9.55 ×10⁸ M☉ | Excerpt lines 380 and 569 | `python3 scripts/check_paper.py` |
| The Bayes factor and F_e use only the Earth term | Excerpt lines 355 and 479 | Read the excerpt |
| The distance errors change the predicted pulsar-term frequencies | `data/sky_positions.json`; `results/pulsar_term_frequencies.json` | `python3 scripts/pulsar_term.py` |

The arXiv v2 source and the version of record print the same values in Table 2 and in both frequentist-search passages. The values in `data/cited_measurements.json` were transcribed from the cited tables, at the locations recorded in that file.

## Primary sources

1. J. Cardinal Tremblay, B. Goncharov, R. van Haasteren et al., *A Multimessenger Search for the Supermassive Black Hole Binary in 3C 66B with the Parkes Pulsar Timing Array*, [ApJL 998, L42 (2026)](https://doi.org/10.3847/2041-8213/ae3c98); [arXiv:2508.20007v2](https://arxiv.org/abs/2508.20007v2) and its [source archive](https://arxiv.org/src/2508.20007v2) (`main_final.tex`, SHA-256 `3564d5b3cbc984520fce5f0527123e276c6698db6d69579b2bed21511f0ec63c`).
2. H. Ding, A. T. Deller, B. W. Stappers et al., *The MSPSRπ catalogue: VLBA astrometry of 18 millisecond pulsars*, [MNRAS 519, 4982 (2023)](https://doi.org/10.1093/mnras/stac3725), Table 5.
3. J. P. W. Verbiest, M. Bailes, W. A. Coles et al., *Timing stability of millisecond pulsars and prospects for gravitational-wave detection*, [MNRAS 400, 951 (2009)](https://doi.org/10.1111/j.1365-2966.2009.15508.x), Tables 3 and 5.
4. R. J. Jennings, D. L. Kaplan, S. Chatterjee, J. M. Cordes, A. T. Deller, *Binary Pulsar Distances and Velocities from Gaia Data Release 2*, [ApJ 864, 26 (2018)](https://doi.org/10.3847/1538-4357/aad084), Table 2.
5. J. A. Ellis, X. Siemens, J. D. E. Creighton, *Optimal strategies for continuous gravitational wave detection in pulsar timing arrays*, [ApJ 756, 175 (2012)](https://doi.org/10.1088/0004-637X/756/2/175); [arXiv:1204.4218](https://arxiv.org/abs/1204.4218).
6. PPTA DR3 timing models, [danielreardon/PPTA-DR3 at fdbe6eb](https://github.com/danielreardon/PPTA-DR3/tree/fdbe6eb1c86d4c6cf2f1f518711e44ad1a9fd3fa/analysis_codes/data/all), for the two pulsar positions.
