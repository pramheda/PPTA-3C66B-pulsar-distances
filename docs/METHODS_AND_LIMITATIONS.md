# Methods and limits of the inference

## Table 2 distances

`scripts/check_paper.py` parses all 31 rows of Table 2 from the verbatim LaTeX excerpt (`sources/tremblay2026_v2_excerpts.tex`, original lines 706–762). For the three rows examined, it converts the cited parallax ϖ to a distance with d = 1000/ϖ pc. Errors use linear propagation, σ_d = 1000 σ_ϖ / ϖ². A larger-parallax error corresponds to a smaller distance, so asymmetric error sides swap.

- **J1643−1224:** 1000/1.31 = 763.36 pc. The printed central value, 4763.36 pc, differs by exactly 4000 pc. The printed errors, +99.06/−104.89 pc, equal the propagated errors 1000·0.17/1.31² and 1000·0.18/1.31² without the side swap.
- **J0613−0200:** Verbiest et al. (2009) print 0.8(7) mas, and their Table 3 caption, which Table 5 refers to, states that bracketed numbers are twice the formal standard deviation. This gives 0.8 ± 0.35 mas and 1250 ± 546.875 pc. The printed 125 ± 54.69 pc is that value divided by ten.
- **J2129−5721:** the printed 2358.49 ± 489.50 pc equals the inversion of 0.424 ± 0.088 mas. Jennings et al. (2018), Table 2, give that parallax for J2129−0429, a different binary pulsar at a different sky position. Their paper has no J2129−5721 entry.

The other 28 rows were parsed but not audited here.

## Reported statistics

The paper states that the trials factor is one (excerpt line 483) and that the background distribution is chi-squared with four degrees of freedom (line 484), following Ellis et al. (2012). For 2F_e ~ χ²₄ the tail probability is P(χ²₄ > 2F_e) = exp(−F_e)(1 + F_e). This gives 0.04393 for the Section 4.5 value F_e = 4.90 and 0.03910 for the conclusion's F_e = 5.04. Both paragraphs print FAP = 0.50 alongside p = 0.04. With a single trial these are the same quantity, so the printed 0.50 is inconsistent with the paper's own p-value.

Section 4.2 (line 380) reports the conservative uniform-in-mass prior limit with the pulsar term as 10.63×10⁸ M☉. The conclusion (line 569) reports the conservative-prior chirp-mass limit as 9.55×10⁸ M☉. The conservative strain limit, log₁₀ h₀ < −14.20, agrees between line 414 and line 569; the latter omits the log₁₀.

## Pulsar-term frequencies

`scripts/pulsar_term.py` uses the leading-order frequency evolution of a circular binary,

```text
f_p = f_E [1 + (256/5) (π f_E)^(8/3) (G M_c / c³)^(5/3) L (1 − cos θ) / c]^(−3/8)
```

with f_E = 60.4 nHz and M_c = 6.90×10⁸ M☉, both from the paper. θ is the angle between the pulsar and 3C 66B. Pulsar positions are the ecliptic coordinates in the public PPTA DR3 timing models, converted with the IERS 2010 obliquity and checked against the pulsar names. Redshift, eccentricity and higher-order evolution are ignored. The calculation shows how strongly the modelled signal depends on the distance; it is not a likelihood.

## What is not established

- **Runtime exposure.** The public PPTA/enterprise reading path, any local distance files and any serialized pulsar objects used in the published run have not been recovered. The table might not reflect the values used.
- **Effect on the limits.** A changed prior moves a posterior only as far as the data constrain the pulsar term. That needs the original noise model, likelihood and samples.
- **Cause of the statistic mismatches.** We do not know whether 0.50, 4.90/5.04 or 10.63/9.55 are typing errors or values from different runs.
