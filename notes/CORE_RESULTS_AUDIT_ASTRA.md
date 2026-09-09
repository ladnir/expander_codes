# Core-results audit, 2026-09-05

Scope: independent review of the main probability arguments and the finite
bounds they feed. The implementation and libOTe PR are unchanged. This is
not a formal verification or a claim that every certificate has been replayed.

## Conclusions and repairs

No counterexample to a headline distance bound was found in this pass.
The numerical parameters have not changed. Three substantive corrections were
made to the manuscript:

1. The asymptotic EA and EC proofs used `a_r = r rho (1-o(1))` over a range
   described only as `r rho` sufficiently small. That approximation is not
   uniform over a fixed nonzero range. The proofs now choose fixed positive
   epsilon and tau, retain strict slack in `C I > 1`, and use
   `r rho (1-r rho) <= a_r <= r rho`. This gives a uniform `K n^(-gamma r)`
   tail with `gamma > 1`. Intermediate supports use an explicit positive
   activation threshold; dense supports use the GV exponent. The same
   repair applies to fixed prime-power fields because `p/(p-1) <= 2`.
2. The singleton-free-region lemma must bound the event that some message
   has a qualifying trace, not the numerical sum over all such traces.
   The corrected statement defines that event. Its necessary incidence
   condition holds simultaneously for all messages and traces on a support.
   Therefore the support/region union bound incurs no trace multiplicity.
   The verifier already uses this event-level split for degree 22: it replaces
   the low-equation branch and retains the high-equation transfer branch.
3. The claim that independently sampled nonzero feedback coefficients
   invalidate the finite-field trace bound was too strong. For a nonzero
   state, expose all but one coefficient attached to a nonzero coordinate.
   A zero output fixes at most one value of that coefficient. Independent
   uniform sampling from the nonzero field elements therefore gives the same
   `1/(p-1)` bound as the trace theorem uses. Full-field coefficients give
   the stronger exact uniform law, but are not necessary for this upper
   bound. The stated construction and numerical instances remain unchanged.
   This does not justify deterministic all-one feedback or structured
   pseudorandom coefficient schedules.

The wrapped-EC analytic appendix now identifies the two-dimensional
one-eigenspace correctly, states the uniform positive eigenvalue separation,
specifies the optimized sparse marker, and justifies compactness of the
rate-function optimization. The odd-degree central lemma now explicitly
requires degree at least three, avoiding an undefined zero variance at one.

## Arguments checked

- Binary two-sided regional transfer: uniform subset normalization is
  `binom(k,r)` per region; independent regions compose by matrix products
  without resetting the recursive state.
- Binary dense bound: conditioning independent slot selections on total
  weight gives the uniform subset law. Conditional parity counts factor as
  sums of Bernoulli variables. The Fourier point-mass bound and regional
  independence justify multiplication over regions. Complementing a support
  preserves the maximum point-mass bound; it need not preserve the low-output
  event for a particular subsequent linear map.
- Degree-five variance formula, its derivative factorization, and the
  difference of the two conditional variances: checked as exact rational
  polynomial identities, not a grid of floating-point evaluations.
- Odd-degree extension: the displayed negative roots of the parity
  polynomials and unimodality of each Bernoulli variance justify taking
  the minimum at the parameter-interval endpoints.
- Wrapped sparse exponent: checked the compressed derivative against the
  active stationary distribution. The two effective eigenvalues have gap
  at least `2 sqrt(c_m)` for fixed memory. This supports the uniform
  Schur-complement expansion and positive-eigenvector prefactor.
- Finite-field trace: fix incidence before union-bounding message lines.
  For one line, each mark consumes fresh randomness at that time. The
  probability is at most `(p-1)^(-a)`. Union-bounding the `(p-1)^(r-1)`
  lines and capping at one is valid without independence between lines.
- Singleton refinement: each later all-zero-state interval needs `m`
  marked zeros to enter. A zero-state interval can partially traverse at most
  two singleton-containing regions. This gives the necessary lower bound
  on singleton-free regions independently of message values.
- Field block code: the structural marker bounds `a <= r-1`; the field
  marker bounds `a >= r`, using `v >= 1/(p-1)`. In each coefficient block,
  inverse binomial powers have a convex logarithm, so the two endpoint
  values dominate the interior. This matches the implemented branch split.
- Degree-6/3 layered arithmetic: the default 1,000-bit bands keep nonzero
  mantissas in `[2^-501,2^499)`. Products for 80-state matrices are normal
  and finite, including the rational scale in `[1/2,1]`. The positive
  dot-product inflation is conservative under ordinary binary64 rounded
  multiplication/addition (or fused multiply-add). The numerical guarantee
  still depends on the execution environment honoring that arithmetic model.

## Independent checks added

`scripts/test_core_proof_audit.py` does not obtain expected probability
values from the certificate implementation. It checks:

- exact inner-product distributions over GF(2), GF(3), GF(4), and GF(5),
  for memories one through three;
- the required point-mass bound for independent nonzero feedback;
- capped trace probabilities by enumerating common sampled labels and taps
  for every projective line on a two-symbol support;
- the singleton incidence implication over every small multiplicity pattern
  and realizable zero/nonzero trace in four regions;
- the wrapped compressed derivative with rational arithmetic;
- the degree-five identities with exact polynomial arithmetic.

These finite enumerations test the proof steps; they are not proofs for
arbitrary parameters. See the manuscript for the universal arguments.

## Verification and remaining work

The cache trust statement was incorrect: a content-addressed cache can be
consistent with its inputs yet contain a false stored bound. The manuscript
now distinguishes cached replay from independent verification. The manifest
and direct degree-22 command pass `--no-cache`. No numerical certificate
input or arithmetic implementation was changed by these repairs.

The fresh degree-6/3, memory-79 replay completed successfully, without a
numerical cache. It covered all 17 exact blocks, 103 outer blocks, 28 central
blocks, and the full support. Its final intervals agree with the paper:

| Component | Recomputed value (rounded here for reporting) |
| --- | ---: |
| Exact | 2.829173497299536e-7 |
| Outer | 7.292689659569745e-8 |
| Central | 1.397616686780478e-13 |
| Full support | 2.877002355067672e-315675 |
| Total | 3.558443860873197e-7 |
| Failure exponent | 21.422250188473890 bits |

The full test suite now passes all 221 tests, including the six independent
core-audit tests and six finite-field audit tests. The revised 48-page
manuscript at that checkpoint built successfully, with no overfull boxes or undefined references.
The edited pages have been visually checked. Strict manifest integrity and
dependency-version checks pass for all 12 claim groups and 18 frozen artifacts.

Before calling the independent audit complete:

1. Replay the finite-field headline certificates without cached results,
   including degree 22, and preserve the final component sums.
2. Check the final claim-to-table consistency after the replays. The later
   continuation below records the first-moment/spectral and primary-source
   comparison checks completed since this initial checklist.
3. Check the corrected left-regular binary EA replay command. The previous
   manifest invoked its rate-1/5 defaults instead of the claimed rate-1/2
   parameters. The current command fixes all four integer parameters.

The line-ending issue is repaired in manifest schema v2: text hashes normalize
CRLF to LF, and a test checks a simulated CRLF checkout of every pinned input
and source. The handoff tables now give the exact `k,n,L` for every main row.

Priority remains the core results, not packaging or benchmark tuning.

## Finite-field audit continuation

Both GF128 certificates were freshly recomputed, serially, without numerical
caches. Their component intervals reproduce the manuscript. Rounded values
below are reports of the intervals, not additional outward-rounding claims.

| GF128 profile | 26/13, memory 4 | 24/12, memory 5 |
| --- | ---: | ---: |
| `k` | 1048567 | 1048572 |
| `n` | 2097134 | 2097144 |
| `L` | 1015822 | 1015826 |
| Exact-regional contribution | 1.995985733803546e-41 | 2.780325701670770e-14 |
| Block contribution | 3.309300260467213e-47 | 5.300137177306505e-198 |
| Full support | 9.914850239523467e-46 | 4.649587233171219e-620977 |
| Total | 1.996088191606201e-41 | 2.780325701670770e-14 |
| Failure bits | 135.201876426829858 | 45.031739430847817 |
| Largest exact band | 97..128 | 129..160 |

The manuscript had rounded these total bounds so coarsely that the displayed
chains `2.781e-14 < 2^-45.0317` and `1.997e-41 < 2^-135.2018` were false.
They now use safe upper values `2.780326e-14` and `1.996089e-41`. The headline
exponents remain valid.

The main theorem-to-code correspondence was independently checked:

- Incidence is fixed before capping the union of message lines. Each line
  uses the same code. The proof requires conditional freshness in time, not
  independence between the lines.
- For trace polynomial `F_r(z,v)`, the low-equation contribution is bounded
  by `z^-L v^(1-r) F_r`. The high-equation contribution is bounded by
  `(p-1)^-1 z^-L v^-r F_r`, with the additional domain `v >= 1/(p-1)`.
- The positive regional coefficient marker contributes
  `binom(k,r)^(-d_L) x^(-d_L*r)`. After the support union, the remaining
  support factor is log-convex. This justifies the endpoint block calculation.
- The all-occupied transfer has row sum `z+v`, so its full-support moment is
  `(z+v)^n`, independently of convolution memory.

Section 7 now derives these inequalities explicitly. It also supplies the
positivity/continuity argument needed by fixed-field EA's intermediate
support range. Section 2 now states the field convolution's zero initialization.
Stale claims that full-field taps are essential were removed from Sections 2
and 9; the independently nonzero alternative remains a proved bound, not a
change to the main construction.

The degree-22 validator previously accepted missing sparse field bands.
The checked-in certificate has no missing band, but the checker now enforces
that branch's complete coverage. Common field EC checks now reject invalid
field orders, regional dimensions, and integer parameters. Full-support
marker domains are checked in both field EA and EC. No numerical formula,
positive marker, cutoff, degree, or memory was changed.

`test_field_trace_audit.py` adds independent rational enumeration of regional
slot choices and permitted traces, branch inequalities across two regions,
the scalar full-support formula, and malformed-input regressions.

### Where meaningful slack remains

For the GF128 26/13 profile, deleting the entire block and full-support
contributions would improve the total exponent by less than 0.000075 bits.
For 24/12, their contribution is negligible even at the displayed precision.
Thus tightening only the large-support bounds cannot materially improve these
certificates. Exact regional extraction still uses positive output/equation
markers and the capped projective union; it is not the exact bad-code
probability. Those small-support relaxations are the remaining meaningful
targets if parameter optimization is resumed. This audit does not establish
that a new degree becomes certifiable.

### Completed serial replays (2026-09-05)

Both outstanding replays completed successfully, in sequence:

- Degree-22, memory-12 field EC with `--no-cache`: every exact band through
  support 1400, every remaining block, and full support passed. The total
  bound is approximately `6.0719917187165531e-9`, giving
  `27.295183030850587` bits.
- The corrected rate-one-half left-regular EA command (`--k 1048576
  --regions 64 --region-length 32768 --cutoff 230718`) passed. The total
  bound is approximately `8.9823445254256326e-7`, giving
  `20.086404605243616` bits. Support two dominates the exact contribution.

Execution sessions `25215` and `65294` have both exited successfully. There
is no remaining queued replay in those sessions. The complete 225-test suite
then passed. After adding six exact checks for the constant-degree probe,
the complete 231-test suite also passed.

## Binary first-moment and comparison audit continuation

The EA block verifier uses the activation probability at the left endpoint.
The manuscript had lost the justification from the parked notes. Section 4
now derives it: the derivative of the symmetric transfer with respect to
activation is a negative rank-one matrix, so its largest eigenvalue decreases.
Combining this with increasing activation and the message count proves the
displayed support-interval formula. The positivity and continuity argument for
the EA rate function is now explicit as well.

For EC, the transition matrix is not entrywise monotone in activation.
The existing verifier instead bounds it by
`(1-a_lo) W(a_hi/(1-a_hi),z)` over the full activation interval. Section 5
now proves this envelope and the dense invertibility/point-mass bound.
Section 6 explains how increasing Poisson conditioning costs combine with
the EA spectral or EC transfer envelope. Its Fourier argument now explicitly
pairs complementary subsets before removing the absolute value.
The generic transfer description also states the conditional independence
assumption needed to multiply one-step expected transitions.

Three new independent tests check the EA negative-square identity, spectral
interval bounds against enumerated accumulator inputs, and EC interval bounds
against enumerated taps and inputs for memories 1, 2, and 3. These pass. The
previous full 221-test suite passed; the resulting 225-test suite has now also
passed after the serial numerical replays. Some tests themselves recompute
full EA certificates, so continue to keep full numerical runs serial.

An additional interval-arithmetic check proves that all five prime-field
EA/EC cutoffs advertised as floored GV really are the integer floors. For each
checked-in `(p,k,n,L)`, it verifies
`h_p(L/n) < (1-k/n) ln(p) < h_p((L+1)/n)` in the increasing part of the entropy
curve. This does not use the floating-point root finder. All five checks pass.

The expanded manuscript is now 49 pages. It builds with no overfull boxes or
undefined references, and all newly edited pages have been rendered and
visually checked. The final PDF is refreshed under `output/pdf/`.

### Primary-source comparison check

The original sources were freshly retrieved from the IACR ePrint archive:
[EA, report 2022/1014](https://eprint.iacr.org/2022/1014) and
[EC, report 2023/882](https://eprint.iacr.org/2023/882).
EA Theorem 3.10 supplies the stated old density/rate restrictions, and its
Figure 8 labels the finite values as extrapolated. EC Table 4 matches our
non-systematic rate-1/5, memory-5, zero-state comparison, including all three
quoted prior values. Appendix A.1 explicitly makes that calculation
conditional on the conjectured extension of Lemma 4.

The introduction had misleadingly presented the asymptotic EC comparison as
a density improvement for one fixed construction. It now distinguishes our
fixed-memory wrapped theorem from the original Theorem 3's logarithmic-memory
nonwrapping theorem. The quoted old restrictions are necessary hypotheses,
not sufficient conditions for its failure expression to vanish; that
expression also depends on the memory-growth constant. Section 5 now says so.
The same-ensemble finite comparison is unchanged.

The manifest's first three Bernoulli EC failure exponents were stale metadata.
They now agree with the table and the output substrings already required by
the replay commands. No certificate inputs or numerical algorithms changed.

## GV/negligibility headline, requested by the author

The title is now *Expander-Based Codes at the Gilbert--Varshamov Bound*.
The sole author is Peter Rindal (also in PDF metadata).

The previous asymptotic statements gave `o(1)` failure at every fixed distance
below GV, not negligible failure while approaching GV. A new corollary in
Section 7 now proves the stronger claim with expected Bernoulli degree
`ln(n)^2` and cutoff `floor(n*(delta_p,GV(k/n)-1/ln(n)))`:

- It covers EA over every fixed finite field and wrapped binary EC with any
  fixed memory. The failure is at most `exp(-c*ln(n)^2)` for some constant
  `c>0` and all sufficiently large `n`.
- Sparse supports use the existing uniform endpoint tails at a fixed
  distance above the limiting GV target. Summing `(sk)^r exp(-b*r*ln(n)^2)`
  is negligible. A fixed intermediate threshold gives exponential decay.
- Dense supports use invertibility and the Bernoulli coordinate point mass
  `(1+s*t^r)/p`. The entropy deficit is `Omega(1/ln(n))` while the mixing
  correction is `exp(-Omega(ln(n)^2))`. This gives
  `exp(-Omega(n/ln(n)))` for the dense contribution.
- The target uses the actual rate `k/n`, avoiding any unstated convergence
  speed for that rate. The rounding gap is explicitly at most an extra `1/n`.
- This does not assert negligible failure at the exact finite GV cutoff.
  Nor does fixed expected degree `C ln(n)` suffice: a specified zero row
  already gives a lower bound `n^-C(1+o(1))` on bad sampling.

Do not extend this corollary to full-field EC with fixed memory. Unlike
wrapped binary feedback, its state can return to zero without another
nonzero input. Its main claims here remain finite certificates. The new
corollary changes neither those certificates nor the implementation.

## Narrow constant-degree probe

See `CONSTANT_DEGREE_PROBE.md` for the full argument and scope. For both
region-stratified regular ensembles, a fixed weight-two message gives a
positive, length-independent lower bound on bad sampling at every positive
constant relative distance. EA needs opposite labels on nearby edge pairs;
wrapped binary EC additionally needs the state to cancel at the second edge.
An explicit length-`m` output pattern has probability at least `2^{-m}` and
forces that cancellation, so no mixing-time approximation is needed.

For full-field EC at fixed field order and memory, a weight-one message has
expected output weight at most `d*(1+m*p^m)`, independently of length. Thus
its relative weight tends to zero in probability. This asymptotic obstruction
can occur only at enormous lengths before the bound becomes informative for
128-bit fields; it does not contradict the finite certificates.

The probe rules out a proposed fixed-parameter, vanishing-failure asymptotic
extension, not an existing manuscript theorem. The main paper and PDF were
left unchanged. Six exact finite-enumeration tests check the proof mechanisms.
The author rejected the "concrete linear-time" framing. The abstract and
introduction now report `O(n log^2 n)` expected field operations for the
negligible-failure GV corollary and `O(n log n)` for logarithmic degree.
Section 2 derives these costs. The finite certificates are described through
their explicit degree/memory parameters, without a linear-time claim.

## Main framing: logarithmic degree, tunable polynomial failure

Theorem `thm:gv-log-degree` now leads the asymptotic framing. For every
fixed field, limiting rate in `(0,1)`, and desired exponent `A > 0`, it
chooses a degree constant `C` independent of length and of the rate
sequence's convergence speed. It covers EA and, over the binary field,
fixed-memory wrapped EC. The cutoff is
`floor(n*(delta_p,GV(k/n)-1/ln(n)))`. Failure is at most `n^-A` for all
sufficiently large lengths, with `O(n log n)` expected field operations.

The proof audit checks the following dependencies and estimates:

1. Fix `delta_bar` above the limiting GV distance and below `(p-1)/p`.
   The sparse constants `K,b,tau` depend on the field, rate, and recursive
   map, not on `C`. Hence `b' = b*(1-tau)` is fixed before choosing `C`.
2. Choose `b'C > A+1`. The sparse union is bounded by the geometric sum
   `K sum_r ((p-1)*n^(1-b'C))^r = o(n^-A)`. Strict inequality absorbs all
   constant prefactors. This also shows `C` can scale linearly with `A+1`.
3. Above `r*rho > tau`, activation has a positive lower bound independent
   of length. A sufficiently small fixed `eta < R/2` makes the intermediate
   counting exponent smaller than the uniform tail exponent.
4. Above support `eta*n`, the Bernoulli point-mass correction is bounded
   by `(p-1)*n^-beta`, with fixed `beta = (p/(p-1))*eta*C > 0`.
   This is `o(1/ln(n))` even for small positive `beta`.
5. The entropy gap at the actual rate `k/n` is at least a positive constant
   times `1/ln(n)`, by the mean value theorem and a uniformly positive
   entropy derivative near the limiting GV value. Thus dense messages
   contribute `exp(-Omega(n/ln(n)))`. No rate-convergence speed is assumed.
6. The dense bound conditions on the independent recursive map and holds
   for each such invertible map. Averaging is therefore valid. The sparse
   and intermediate EC bounds already include convolution randomness.
7. The expected expander edge count is `k*C*ln(n)`. The accumulator or
   fixed-memory convolution adds `O(n)` field operations. These costs are
   for encoding with the stored sparse expander, not a dense setup scan.

Corollary `cor:gv-negligible` keeps the same cutoff but uses expected degree
`ln(n)^2`. The sparse sum becomes `exp(-Omega(ln(n)^2))`; the other two
ranges decay faster. It gives `O(n log^2 n)` expected encoding cost.
A specified zero Bernoulli row still prevents one fixed `C ln(n)` choice
from giving negligible failure in `n`. The corollary strengthens failure,
not the distance target.

The abstract, introduction, construction cost paragraph, conclusion, README,
submission scope, and handoff now use this framing. The finite certificates
and implementation were not changed. All 231 tests pass, and strict manifest
integrity checks pass for 12 claim groups and 18 frozen artifacts. These
checks protect the existing finite results; the analytic review above, not
the numerical tests, justifies the new asymptotic theorem.
