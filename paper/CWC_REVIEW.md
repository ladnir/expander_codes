# Controlled-writing review

This checklist records the section-by-section review against Controlled
Writing for Cryptography. It is an editorial artifact, not part of the paper.

## Resolved audit findings

- CWC-03 and CWC-09: quantified the distance target in the wrapped-EC
  asymptotic theorem before it appears in the hypothesis.
- CWC-05: preserved the paper-wide meanings of $p$ (field order) and $R$
  (code rate). Local support fractions now use $\theta$, and central support
  endpoints use $r_{\mathrm{mid}}$.
- CWC-08 and CWC-09: made the expander and convolution sampling experiments
  explicit in the finite wrapped-EC, regular-expander, and nonwrapping
  statements.
- CWC-03 and CWC-06: exposed the parameter of the degree-three conditional
  random variables as $Z_s^{(3)}(\theta)$ and separated its parity index from
  block endpoints.
- CWC-05: normalized the field-size theorem to the global field-order symbol
  and the established notation $\delta_{p,\mathrm{GV}}(R)$.
- CWC-05: separated the failure exponent $b$ from the field-order bit length
  $s$ in the adjacent certificate and discussion sections.
- CWC-15: the field-size discussion distinguishes interval-certified rows
  from frozen-marker diagnostics and identifies the source of the observed
  decline as a moving target rather than weaker mixing at fixed distance.

## Abstract and introduction

- Leads with the construction, the proof gap, and the concrete result.
- Separates the binary case from genuine finite-field mixing near 128-bit
  field orders before presenting either parameter family.
- Defines EA, EC, PCG, the enumerator idea, relative distance, and the role of
  the GV benchmark before relying on them.
- Separates changes to the analysis from changes to the construction.
- States the probability observer and excludes decoding and protocol-security
  claims.
- Compares the proof method with Block--Accumulate and recent large-field RAA
  analyses. The comparison defines RAA before use, identifies the shared
  projective accounting principle, and states why EA and EC need different
  structural traces.

## Code ensembles and distance events

- Defines messages, generators, support, Hamming weight, minimum distance,
  relative distance, rate, Hamming balls, and the GV benchmark.
- Gives the accumulator and convolution as explicit interfaces before using
  their properties.
- States all randomness and independence assumptions locally.
- Defines left and right vertices and both meanings of regularity; it also
  warns that "expander" does not assert a graph-expansion theorem.

## Enumerator method

- Defines the enumerator as an expectation and identifies the probability
  space in the first-moment step.
- States the symmetry required for composition. The finite-field hypothesis is
  monomial invariance; the binary specialization needs only permutations.
- Introduces state, input marker, and output marker before coefficient
  extraction. The positive-marker relaxation follows the exact identity.
- Requires an explicit partition of all nonzero support sizes.  The certified
  support-partition lemma now states the shared endpoint calculation and the
  verifier's exact responsibilities.

## Binary EA

- Keeps the construction fixed and says so before presenting the proof.
- Defines the activation probability and every state of the two-state matrix.
- Places the exact first moment before spectral and asymptotic relaxations.
- Separates sparse, intermediate, and dense supports and distinguishes
  asymptotic comparisons from finite certificates.

## Binary EC

- Defines the wrapping convention and the reduced state before the matrix.
- Explains every exceptional transition, including the fixed oldest tap and
  the all-zero state.
- States which prior comparison changes the analyzed ensemble and which holds
  the ensemble fixed.
- Defers only the lengthy endpoint calculation to a named appendix.

## Regular expander variants

- Presents regular incidence as a construction change, not a proof trick.
- Defines a unit vector and the regional shell recurrence before its use.
- Explains Poisson conditioning and point-mass terminology in place.
- Retains recursive state across region boundaries.
- Defines the binary two-sided probability space before its exact transfer.
- Presents the certified degree-$10/5$ and degree-$6/3$ statements as a
  degree--memory tradeoff, together with the intermediate $14/7$ and $18/9$
  profiles.  It explains why degree $8/4$ is structurally invalid.
- Defines scalar extension and limits its use. The proof identifies the binary
  basis components and thereby explains why scalar extension does not provide
  the cross-component mixing required by field-valued Silent VOLE.
- Introduces the common odd-degree conditional enumerator before using its
  real-rooted factorization in the central-block lemma.
- Places the right-degree parity proposition before all usable binary
  parameters.
- Grounds the local-limit variables before the point-mass claim and states
  the monotonic endpoint facts used by the interval verifier.
- Introduces the degree-three conditional Bernoulli variables before the new
  central-block lemma.  Its proof identifies the conditioning event, the
  observer, the variance comparison, and the complementary-support mapping.

## Finite fields and field-size scaling

- Motivates random edge labels by the exact symmetry they provide.
- Defines projective message lines before counting them.
- Separates the theorem for each fixed field from the finite
  cryptographic-size certificates. The argument is stated for prime-power
  field orders, including characteristic two.
- Defines occupied coordinates and fresh-equation markers before the
  constraint matrices. It distinguishes exact full-field mixing from the
  point-mass bound also supplied by independent nonzero feedback.
- States which factors depend on the field order and distinguishes the
  fixed-field asymptotic theorem from finite results near 128 bits.

## Certified finite evaluation

- Defines the failure exponent and the outward-rounded ball representation.
- States the trust boundary: the optimizer is untrusted and independent
  verification bypasses the numerical cache, while the
  verifier checks domain, coverage, arithmetic, and the final endpoint.
- Identifies every parameter in the headline theorems and states which
  support ranges each verifier covers.
- Gives both $\mathbb{F}_{2^{128}}$ results their own labeled finite-field
  certificates instead of deriving an application claim by scalar extension.
- The binary and $\mathbb{F}_{2^{128}}$ theorem parameters match their
  checked-in certificate files and complete support partitions.
- Separates exact, outer, central, and full-support contributions for the
  binary two-sided regular EC result.
- Grounds the frozen marker file and the independent structural checker before
  claiming that verification does not run the optimizer.
- Gives a branch-to-equation correspondence table.  Every numerical verifier
  validates its schema, marker domains, parameter identities, and support
  partition.  The independent standard-library checker is claimed only for
  the two binary two-sided formats that implement it.

## Discussion and appendices

- Discussion separates distance, decoding, deterministic construction, and
  application security.
- The implementation paragraph assigns the binary profile to Silent OT and
  the field-valued profile to Silent VOLE. It distinguishes the independently
  labeled proof ensemble from the structured streaming heuristic.
- The field-size discussion defines fixed-cutoff and field-relative-cutoff
  comparisons before presenting them.  It separates interval certificates
  from the remaining frozen-marker diagnostics.
- The additional-ensemble appendix defines fixed-column, fixed-row,
  Krawtchouk, conditioning, and dense Fourier terms before conclusions.
- The nonwrapping appendix distinguishes the sampled-oldest-tap construction
  from wrapping and gives its own exact matrix.
- The analytic appendix preserves the order state classes, effective
  generator, optimization, uniform prefactor, then endpoint conclusion.
- The artifact appendix maps every finite result to the checked-in manifest.
  The manifest pins certificate and source hashes and supplies one serial
  runner.

## Final scope checks

- The abstract now leads with asymptotic GV distance and `O(n log n)`
  expected encoding cost. Theorem `thm:gv-log-degree` supplies the shrinking
  gap and quantifies every desired exponent `A` before choosing the degree
  constant `C`. Corollary `cor:gv-negligible` gives the stronger failure
  guarantee at `O(n log^2 n)` expected cost (CWC-08, CWC-09).
- Negligibility is defined in the length `n`, with the field held fixed.
  The corollary covers field-valued EA and binary wrapped EC, not the
  fixed-memory full-field EC ensemble. Finite constant-degree certificates
  are explicitly separate (CWC-08, CWC-09).
- The proof uses the actual rate `k/n` in the moving GV target. It fixes a
  larger distance for uniform sparse/intermediate bounds and uses an
  independent point-mass argument for the shrinking dense gap (CWC-11).

- The independent core audit replaces a nonuniform sparse approximation with
  fixed thresholds and explicit slack (CWC-08, CWC-11).
- The singleton lemma now quantifies an existence event over sampled codes,
  rather than implying a bound on trace multiplicity (CWC-03, CWC-08).
- The finite-field discussion distinguishes the exact uniform feedback law
  from the weaker point-mass bound sufficient for the theorem (CWC-09).
- The new independent finite checks support these arguments but are not
  presented as universal proofs (CWC-01).
- The finite-field construction now states its zero initialization explicitly
  and uses a sampling assignment for the feedback vector (CWC-04, CWC-07).
- The EC proof fixes incidence before taking the capped projective union,
  and states that the lines share one sampled code (CWC-08, CWC-11).
- A separate lemma supplies both marker domains and the high-equation factor
  `1/(p-1)`. Regional normalization and block convexity are derived before
  their use in certificate claims (CWC-01, CWC-09).
- The rounded GF128 upper bounds retain enough digits for both displayed
  inequalities to hold. The certified exponents are unchanged.
- The Bernoulli EA block formula now includes the spectral monotonicity
  argument used by its verifier. Positivity and continuity of the rate
  function have separate justifications (CWC-11).
- The generic transfer-matrix identity explicitly assumes a transition law
  independent of the earlier path conditional on the state (CWC-08).
- The introduction now distinguishes fixed-memory wrapped EC from the
  earlier logarithmic-memory nonwrapping theorem. Its quoted parameter
  restrictions are not presented as sufficient for vanishing failure
  (CWC-09).
- The Bernoulli EC interval envelope, dense point-mass bound, and increasing
  Poisson conditioning cost now connect the regular-ensemble formulas to
  their block verifiers. The Fourier bound explicitly handles negative
  character eigenvalues by pairing complementary subsets (CWC-11).

- The wrapped-EC appendix proves a uniform quadratic perturbation remainder
  through a two-class Schur-complement argument.
- The construction section states sampling and storage costs.  The discussion
  gives the exact additive rule for composing code-sampling failure with a
  protocol theorem, without claiming a protocol-specific reduction.
- The local field-size profile is interval-certified at orders $2^{127}$,
  $2^{128}$, $2^{129}$, and $2^{136}$.  Other displayed orders are labeled as
  diagnostics in both the paper and manifest.

## Encoding-cost wording, 2026-09-05

The abstract and introduction lead with `O(n log n)` expected field
operations at fixed rate, approaching GV with any fixed polynomial failure
exponent. The `O(n log^2 n)` negligible-failure result is a corollary.
Section 2 derives both costs from the sparse edge count and recursive map.
Finite degree/memory certificates are not presented as a linear-time
asymptotic result. This pass keeps the cost model and scope explicit
(CWC-03, CWC-08, CWC-09), without claiming unmeasured performance constants.

The new theorem's proof fixes a distance above the limiting GV target for
the sparse and intermediate estimates. Its constants do not depend on the
degree multiplier `C`. The choice `b'C > A+1` leaves strict slack after the
sparse union. In the dense range, the point-mass correction `n^-beta` is
smaller than `1/ln(n)` for every fixed `beta > 0`. The proof uses the actual
rate `k/n`, conditions on the independent recursive map, and then averages.
The length threshold may depend on the rate sequence; the constant `C` does
not. These dependencies prevent a hidden uniformity claim (CWC-08, CWC-11).

The rebuilt 51-page PDF has no LaTeX reference warnings or overfull/underfull
boxes. The updated abstract, introduction, cost paragraph, theorem and proof,
corollary, scope paragraph, and conclusion were rendered and visually checked.

The abstract's opening now states the distance result in plain English:
the codes approach GV as length grows. It retains the two encoding costs,
the field and memory scope, and the distinction between inverse-polynomial
and negligible failure. The exact shrinking gap, degree constants, and
failure formulas remain in the introduction and theorem statements. This
author-requested simplification changes presentation, not the result.

## EA-based PCF application framing, 2026-09-09

The abstract and introduction now identify the original EA-based PCF as an
application of the improved degree bounds. The introduction defines the PCF
interface and the role of distributed comparisons before discussing cost
(CWC-01, CWC-02, CWC-04). The discussion maps row weight to local evaluation
work using Sections 5.2 and 5.4 of the EA paper. It separates the approximately
64% reduction between sufficient asymptotic degree thresholds from finite
failure margins and the original empirical PCF estimates (CWC-08, CWC-09).
The finite degree-62 example retains the Bernoulli distribution explicitly.
The regular-row alternative is identified with the EA paper's Section 3.4
variant; expander regularity is not conflated with noise regularity (CWC-05).
The application retains the single accumulator and the original EA-LPN and
comparison-primitive assumptions. No new protocol-security theorem or measured
PCF speedup is claimed. No code parameter or certificate was changed.

## One-stage EA and parallel depth, 2026-09-09

The introduction now emphasizes that the improved EA distance result retains
one sparse expansion and one parallel prefix sum. Section 2 defines arithmetic
work and depth for a fixed sparse layout, excluding setup and data movement
(CWC-03, CWC-09). Balanced sums account for collisions in the sparse expansion;
the accumulator uses a work-efficient parallel scan. The RAA comparison concerns
its natural staged encoder, not a lower bound on arbitrary circuits. Both
constructions remain in the logarithmic-depth class. The transpose reverses
the two stages and uses a suffix sum under the paper's row-vector convention.
Full-vector encoding is distinguished from local PCF evaluation (CWC-05).
