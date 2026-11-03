# 3C 66B pulsar-timing search: wrong pulsar distances in Cardinal Tremblay et al. (2026)

**[Cardinal Tremblay et al. (2026), ApJL 998, L42](https://doi.org/10.3847/2041-8213/ae3c98) list three pulsar distances in their Table 2 that do not match the measurements they cite. One has a stray leading digit, one is ten times too small, and one belongs to a different pulsar.**

**These distances set the priors for the pulsar-term model behind the paper's tightest limit, a chirp mass M < 6.90×10⁸ M☉. The paper also prints a false-alarm probability of 0.50 where its stated method gives 0.044, and reports two different values for one of its limits.**

This repository contains the source excerpts, the cited values and the checking code.

## Three distances in Table 2

| Pulsar | Table 2 distance | Cited measurement | Distance it implies |
|---|---:|---|---:|
| J1643−1224 | **4763.36** +99.06/−104.89 pc | Parallax 1.31 +0.17/−0.18 mas, [Ding et al. 2023](https://doi.org/10.1093/mnras/stac3725), Table 5 | **763.36** +104.89/−99.06 pc |
| J0613−0200 | **125** ± 54.69 pc | Parallax 0.8 ± 0.35 mas, [Verbiest et al. 2009](https://doi.org/10.1111/j.1365-2966.2009.15508.x), Table 5 | **1250** ± 546.9 pc |
| J2129−5721 | 2358.49 ± 489.50 pc | Parallax 0.424 ± 0.088 mas of **J2129−0429**, [Jennings et al. 2018](https://doi.org/10.3847/1538-4357/aad084), Table 2 | a different pulsar |

**How each conversion works:** a parallax in milliarcseconds gives a distance in parsecs as 1000 / parallax.

```text
1000 / 1.31  =  763.36 pc     the printed error bars (99.06, 104.89) are exactly those of 763.36 pc
1000 / 0.8   = 1250    pc     printed: 125 pc, and its error 54.69 = 546.9 / 10
1000 / 0.424 = 2358.49 pc     matches the printed value, but Jennings et al. list this parallax for J2129−0429
```

Verbiest et al. print J0613's parallax as 0.8(7) and state that bracketed numbers are twice the standard deviation, hence ±0.35 mas. Jennings et al. have no entry for J2129−5721. The same three values appear in the journal's Table 2 (version of record) and in the arXiv v2 source.

## Two reported statistics disagree with the paper's own numbers

| Quantity | Section 4.5 | Conclusion | Under the paper's stated convention |
|---|---:|---:|---:|
| Frequentist statistic F_e | 4.90 | 5.04 | — |
| False-alarm probability | **0.50** (and p = 0.04 in the same paragraph) | **0.50** (and p = 0.04) | **0.044** (F_e = 4.90), **0.039** (F_e = 5.04) |
| Conservative-prior chirp-mass limit, pulsar term | 10.63×10⁸ M☉ (Section 4.2) | **9.55**×10⁸ M☉ | — |

The paper states that the trials factor is one and that 2F_e follows a chi-squared distribution with four degrees of freedom. The false-alarm probability is then exp(−F_e)(1 + F_e). Both corrected values remain far above the 10⁻⁴ detection threshold, so **the non-detection stands**.

## Why the distances matter

In the pulsar-term model, each pulsar sees the gravitational wave as it was emitted a light-travel time earlier. That delay is proportional to the pulsar's distance, so the distance sets the frequency the model predicts. At the published limit (6.90×10⁸ M☉, Earth-term frequency 60.4 nHz):

| Pulsar | Delay, printed → cited distance | Pulsar-term frequency, printed → cited distance |
|---|---:|---:|
| J1643−1224 | 26,892 → 4,310 years | **15.05 → 28.57 nHz** |
| J0613−0200 | 258 → 2,579 years | **53.52 → 33.52 nHz** |

These are model predictions at central values, not a likelihood or a revised limit.

## Limits of the finding

- **We have not recovered the distances loaded in the authors' run.** The table could be a transcription error affecting only the text, or the values could have entered the likelihood. The effect on the 6.90×10⁸ M☉ limit and on the "rules out 58% of the EM-model uncertainty region" statement needs the authors' run configuration and posterior samples. It is not computed here.
- **The Bayesian detection statistic and the frequentist search use only the Earth term**, which does not depend on pulsar distances. Neither result is affected by the distance errors.
- **We do not propose replacement distances.** For J2129−5721 we note only that Verbiest et al. (2009) list a weak timing parallax, 1.9 ± 0.85 mas.

## Reproduce the checks

Everything runs with the Python standard library (Python 3.8 or later):

```bash
python3 scripts/check_paper.py      # Table 2 rows, cited parallaxes, false-alarm probability, reported limits
python3 scripts/pulsar_term.py      # pulsar-term frequencies at printed and cited distances
python3 scripts/verify.py           # file checksums, reruns both and compares with results/
```

[Methods and limitations](docs/METHODS_AND_LIMITATIONS.md) · [Evidence guide](docs/EVIDENCE.md) · [Saved results](results/) · [File checksums](SHA256SUMS) · [Attribution and licensing](THIRD_PARTY_NOTICES.md)

Independent, AI-assisted audit dated 3 November 2026, examining [arXiv:2508.20007v2](https://arxiv.org/abs/2508.20007v2) and the version of record. This is not an author-issued correction.
