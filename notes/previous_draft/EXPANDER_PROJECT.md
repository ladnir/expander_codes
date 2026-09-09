# Enumerator proofs for expander-based codes

## Objective

Replace the loose Markov-chain bounds for Expand--Accumulate (EA) and
Expand--Convolute (EC) with exact ensemble enumerators.  Use the resulting
first moments to improve finite parameters and, where possible, the asymptotic
rate--distance theorem.

The primary sources are:

- Boyle et al., *Correlated Pseudorandomness from Expand-Accumulate Codes*,
  IACR ePrint 2022/1014.
- Raghuraman, Rindal, and Tanguy, *Expand-Convolute Codes for Pseudorandom
  Correlation Generators from LPN*, IACR ePrint 2023/882.

## Exact binary proof stack

The binary argument now has five layers.

1. For a message of weight `r`, a Bernoulli expander produces independent
   bits with parameter

   ```text
   q_r = (1-(1-2p)^r)/2.
   ```

   `Expander.tex` gives its exact input--output enumerator.  It also gives
   normalized formulas for fixed column degree and fixed row weight.

2. Column-exchangeability makes the expander output uniform within each
   Hamming slice.  This proves an exact serial-composition identity without
   inserting an interleaver.

3. For EA, compose the expander enumerator with the exact accumulator
   input--output enumerator.

4. For EA, symmetrize the exact two-state weight-generating matrix and extract
   its Perron eigenvalue.  `EAProof.tex` proves that, for rate `R`, relative
   distance `delta`, and Bernoulli density `p=C log(n)/n`, linear distance holds
   when

   ```text
   C (1 - 2 sqrt(delta (1-delta))) > 1
   h(delta) < (1-R) log(2).
   ```

   The first condition is the sparse-message threshold.  The second is the
   binary Gilbert--Varshamov condition and is forced by linear-weight messages.
   The published Markov proof instead requires
   `C > 1/(1/2-delta)^2` and a strictly weaker rate--distance condition.  At
   `delta=0.05`, the density threshold falls from `4.938` to `1.773`; for
   `n=5*2^20`, that is an expected-row-weight threshold of `76.41` versus
   `27.43`.  These are asymptotic thresholds, not finite-security claims.

5. For EC, use the `(m+1)`-state transfer matrices in `nonWrapping.tex` and
   `wrapping.tex`. The state is the number of trailing zero outputs, capped at
   the memory `m`. Wrapping changes only state `m-1`: input zero produces one
   and returns to state zero, while input one produces zero and enters the
   all-zero state. This is the exact chain from the construction, not the
   reversible comparison chain used in the published proof.

For either construction, summing the expected number of low-weight images of
nonzero messages and applying Markov's inequality gives the distance-failure
bound.

## Certified finite parameters

`scripts/expander_bounds.py` evaluates a one-variable Chernoff extraction from
the exact transfer matrix.  At the EA parameters

```text
k = 2^20, n = 5k, target relative distance = 0.05,
```

the scan gives the following largest sampled first-moment terms:

| expected row weight | message weight | log2 term |
|---:|---:|---:|
| 36 | 1 | -9.0748 |
| 50 | 1 | -20.4686 |
| 78 | 1 | -43.2566 |

For row weight 50, the sampled weights `r>=2` begin at `-42.1608` bits and
decrease rapidly.  This is strong evidence that an enumerator proof can replace
the published row weight 78 by approximately 50 at the same nominal 20-bit
failure target.

The complete verifier gives the following table at rate `1/5`, relative
distance `0.05`, and failure target `2^-20`.

| message length | expected row weight | certified failure bound | certified bits |
|---:|---:|---:|---:|
| `2^20` | 50 | `6.891818499e-7` | 20.468611 |
| `2^25` | 56 | `7.475946766e-7` | 20.351240 |
| `2^30` | 62 | `8.107513660e-7` | 20.234237 |

Each certificate evaluates weights 1 through 128 with the exact generating
matrix. It covers the remaining weights with monotone spectral blocks and uses
outward-rounded Arb ball arithmetic throughout. The weight-one contribution
dominates all three certificates. The adjacent row weights 49, 55, and 61 give
bounds above `2^-20` under the same certificate.

The exact-row ensemble now has a separate all-weight certificate. Small
message weights use a positive hypergeometric shell recurrence, intermediate
weights use the Bernoulli bound conditioned on each selected row having the
prescribed weight, and weights from `k/8` onward use a Fourier/L2 estimate.

| message length | exact row weight | certified failure bound | certified bits |
|---:|---:|---:|---:|
| `2^20` | 31 | `3.321605945e-7` | 21.521615 |
| `2^25` | 35 | `2.548539646e-7` | 21.903825 |
| `2^30` | 39 | `2.796467641e-7` | 21.769891 |

These rows save 19, 21, and 23 nonzero entries per expander row relative to
the certified Bernoulli table. `scripts/exact_row_certificate.py` verifies all
three cases with outward-rounded Arb arithmetic; its optimizer only selects
fixed decimal Chernoff markers.

The region-stratified left-regular EA proof is also complete. It uses exact
regional transfer matrices for small messages, a Poissonized spectral bound
for intermediate messages, and the regional Fourier point-mass bound for dense
messages.

| rate | `k` | regions / row weight | region length | cutoff | failure bound | bits |
|---:|---:|---:|---:|---:|---:|---:|
| `1/5` | `1048544` | 31 | `169120` | `262136` | `3.108423898e-7` | 21.617313 |
| `1/2` | `1048576` | 64 | `32768` | `230718` | `8.982345581e-7` | 20.086404 |

At rate `1/5`, regular degree `31` only matches the certified global exact-row
weight `31`; it does not improve sparsity. At rate `1/2`, a Bernoulli EA
certificate at the same length and cutoff needs expected row weight `75` and
gives `20.222410` bits. Regular degree `64` saves `14.67%` of the expansion
edges. This gain is smaller than for wrapped EC because an even-weight message
has even parity in every region and returns the accumulator to state zero at
every regional boundary. Message weight two dominates both regular EA
certificates.

For comparison, the `C=3` row of Figure 8 in the EA paper uses expected row
weights 46.42, 56.81, and 67.21. Its extrapolated failure bounds at distance
`0.05` are `0.0157`, `0.00794`, and `0.00402`. The new table gives a uniform
certified `2^-20` bound. At the two larger lengths, it also uses lower row
weights.

For wrapped EC, `wrapping.tex` now proves both the exact bivariate convolution
enumerator and its Bernoulli-expander first moment. It also gives the exact-row
composition

```text
sum_r binom(k,r) sum_u rho[r,u] Q_wConv(u,L),
```

where `rho` is the positive hypergeometric shell recurrence and `Q_wConv` is a
fixed-input-weight convolution tail. The two-marker transfer bound evaluates
`Q_wConv` without the old termination/near-termination case split.
The recurrence agrees with Appendix A.1 of the EC paper: its fixed last state
tap is the oldest output bit `y[i-sigma]` under chronological indexing.

At `k=2^20`, `n=5k`, relative distance `0.05`, and memory `21`, the initial
floating-point diagnostic gave the following low-message-weight terms for an
exact row weight of `15`:

| message weight | dominant intermediate shell | log2 first-moment term |
|---:|---:|---:|
| 1 | 15 | -21.1441 |
| 2 | 30 | -50.4911 |
| 3 | 45 | -81.0189 |
| 8 | 120 | -240.5495 |

Row weight `14` has a `-17.9677`-bit weight-one upper bound, so the diagnostic
first selects row weight `15`. The all-weight Arb verifier certifies:

| message length | memory | exact row weight | certified failure bound | certified bits |
|---:|---:|---:|---:|---:|
| `2^20` | 21 | 15 | `5.160307473e-7` | 20.886039 |
| `2^25` | 21 | 17 | `4.259825504e-7` | 21.162702 |
| `2^30` | 21 | 20 | `4.830790936e-8` | 24.303165 |

The exact small-weight limits are `59`, `240`, and `529`. The verifier then
uses `51`, `86`, and `119` uniform conditioned-Bernoulli transfer blocks,
followed by the invertibility/L2 bound from `k/4` onward. Memory `25` improves
the weight-one diagnostic by less than `0.002` bits in the tested cases, so the
certified table retains memory `21`.

By comparison, the completed exact-row EA certificates need row weights `31`,
`35`, and `39` at the same lengths, rate, distance, and failure target. The
present certificate does not close the adjacent lower EC row weights; this is
a limitation of the bound, not an impossibility result.

The asymptotic Bernoulli theorem is also closed. For fixed wrapping memory
`sigma` and relative distance `delta`, its sparse exponent is

```text
I_w(sigma,delta)
  = (sqrt(1 - 2 delta + 2^(1-sigma) delta)
     - sqrt(2^(1-sigma) delta))^2.
```

If `p_n = C ln(n)/n`, the sparse condition is `C I_w > 1`. The dense condition
is the binary Gilbert--Varshamov bound `h(delta) < (1-R) ln 2`. At memory `21`
and distance `0.05`, the new density threshold is `C > 1.111623`, and the rate
can be any `R < 0.7136`.

Theorem 3 of the original EC paper treats the nonwrapping construction with
memory proportional to `log n`. At distance `0.05`, its displayed conditions
require `C > 10.4344` and `R < 0.1278`. Its fixed-memory wrapping calculation
uses a comparison with the nonwrapping chain and explicitly invokes the
conjectural small-memory extension of Lemma 4. The new transfer proof is direct
and unconditional for every fixed positive memory.

Holding the original Table 4 ensemble fixed gives a direct finite comparison.
Here `k=2^20`, `n=5k`, the convolution has memory `5` and zero initial state,
and the Bernoulli expander has expected row weight `C ln n`.

| `C` | expected row weight | original Table 4 | certified exact transfer | gain |
|---:|---:|---:|---:|---:|
| 3.0 | 46.4171 | `2.26e-7` | `2.187816572e-10` | 10.01 bits |
| 2.5 | 38.6810 | `1.72e-5` | `9.485867880e-8` | 7.50 bits |
| 2.3 | 35.5865 | `1.73e-4` | `1.124903039e-6` | 7.26 bits |

This comparison changes only the analysis. The original Table 4 calculation
explicitly assumes its conjectural extension of Lemma 4. The exact-transfer
column is an unconditional all-weight Arb certificate. Tables 5 and 6 use a
stationary initial state and therefore describe a different boundary ensemble.

The finite GV comparison is now closed for the binary Bernoulli ensemble at
`k=2^20` and rate `1/5`. The binary GV distance is
`0.2430038538089538`. A certified practical point uses `C=5`, expected
expander row weight `77.3619`, and convolutional memory `9`. With integer
cutoff `1274032`, it certifies relative distance `0.2430023193` and failure
probability at most `3.819697244e-7` (`21.320038` bits). This is `99.99937%`
of the binary GV distance and only `8.0451` output-weight units below it. The
same ensemble gives `29.140327` bits at cutoff `1272015`.

Rate `1/2` is also closed at `k=2^20`. Its binary GV distance is
`0.11002786443829`. The common certified cutoff `230741` gives relative
distance `0.11002588272094727`, or `99.99820%` of GV. Four certified Pareto
profiles are available:

| `C` | expected row weight | memory | failure bound | bits |
|---:|---:|---:|---:|---:|
| 3.15 | 45.8517 | 5 | `7.637727109e-7` | 20.320353 |
| 3 | 43.6683 | 7 | `5.278295360e-7` | 20.853424 |
| 2.9 | 42.2127 | 9 | `5.560776634e-7` | 20.778210 |
| 2.85 | 41.4849 | 13 | `5.971032143e-7` | 20.675516 |

The rate-`1/2` verifier uses exact transfer through weight `32`. The uniform
transfer regime ends between weights `26362` and `28045`, depending on `C`.
Point-mass blocks cover all remaining weights. This regime split avoids the
loose intermediate transfer relaxation.

A region-stratified left-regular profile is now certified at essentially the
same rate and length. Each row has one nonzero entry in each of `28` regions,
so its row weight is exactly `28`; a SPIN-style block-to-region transpose can
implement this layout. The proof retains the convolution state between
regions. Small messages use exact normalized regional slice matrices,
intermediate messages use a Poissonized transfer comparison whose conditioning
cost is only polynomial in the message weight, and dense messages use a
Fourier point-mass bound for the regional unit-vector walk.

| `k` | `n` | exact row weight / regions | memory | cutoff | GV ratio | failure bound | bits |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `1048572` | `2097144` | 28 | 9 | `230730` | `99.993813%` | `2.036626439e-7` | 22.227315 |

The comparable Bernoulli memory-`9` row has expected weight `42.2127` and
cutoff `230741`. Thus regional left regularity reduces expander row weight by
`33.67%` at a distance cost of `11` output-weight units. Degree `5` is not a
near-GV profile: at message weight about `0.4k`, its regional parity density is
only about `0.432`, and the sampled first moment is exponentially large. The
dense mixing expression

```text
d + n log2(1 + exp(-d/2))
```

selects degrees near `28` at this block length. Constant degree can still give
a positive distance, but approaching GV as the length grows requires growing
left degree.

The finite verifier now partitions message weights from `k/4` onward into ten
dense blocks. Each block combines its minimum activation probability with an
outward-rounded Hamming-ball bound. This removes the large counting loss from
using all `2^k` messages at the activation probability for weight `k/4`.

## Field choice

Binary should be the first complete theorem.  It already addresses both prior
papers and avoids mixing two distinct large-field models.

The labeled prime-field EA extension is now proved. Sample every nonzero
expander entry independently and uniformly from `F_p^*`. This edge-label model
is the direct support-randomizing analogue of the monomial weighters in the
generalized BAA construction. It is not equivalent to placing one random
diagonal after an addition-only expander: a post-expander scalar does not
change whether a coordinate sum vanishes.

For a support-`r` message in the Bernoulli ensemble, every expanded coordinate
is zero or uniform nonzero with

```text
q_p(r) = (p-1)/p * (1 - (1 - p theta/(p-1))^r).
```

The accumulator lumps exactly to zero/nonzero states. Counting projective
message lines gives `binom(k,r)(p-1)^(r-1)`, avoiding the redundant scalar
factor. `PrimeFieldEA.tex` proves the exact finite first moment and the
asymptotic theorem. For fixed `p`, density `theta=C ln(n)/n` reaches every
distance below the `p`-ary GV bound when

```text
C * (sqrt(1-delta) - sqrt(delta/(p-1)))^2 > 1.
```

At rate `1/2`, the limiting `C` threshold at GV is `2.67272` for `p=2`,
`2.48437` for `p=3`, `2.29681` for `p=5`, `2.19795` for `p=7`, and `2.00832`
for `p=17`. These are asymptotic thresholds, not finite `2^-20` certificates.
The reproducible calculation is `scripts/prime_field_ea_diagnostic.py`.

The fixed-field quantifier matters. The projective message count contributes
`(r-1) ln(p-1)`. This disappears into constants for fixed `p`, but it is large
at `n around 2^20` when `p` is a 128-bit prime. If `ln(p)/ln(n)` approaches
`alpha`, the sparse word-counting proof needs roughly
`C I_{p,delta} > 1+alpha`, not merely `>1`. Thus the theorem presently favors
small primes; a cryptographic-size field needs either a much larger degree or
a support/rank argument that controls projective clustering, as in generalized
BAA.

That support/rank repair is now explicit. For a fixed message support `S`,
unlabeled expander incidence, and proposed output container `U`, let `c` be the
number of zero-terminated accumulator gaps hit by an edge leaving `S`.
Conditional on the incidence, the probability over nonzero edge labels that
some projective message on `S` lands in `U` is at most

```text
min(1, (p-1)^(|S|-1-c)).
```

The hit-gap statistic is the exact rank of the accumulator zero equations in
the edge labels. Expander collisions are included: multiple edges in the same
gap contribute only one rank unit. For Bernoulli incidence, the complete sum
over output containers has the bivariate gap enumerator recorded in
`PrimeFieldEA.tex` and `FP_PROJECTIVE_UNION.md`. This is the direct analogue of
the recent large-field RAA surplus-cancellation argument.

The coarse support-grouped cap has also been added to the finite regular
diagnostic. It leaves the `p=3` and `p=5` candidate terms unchanged, because
those per-support projective unions were already below one. For the 127-bit
Mersenne prime, rate `1/2`, length near `2^21`, degree `100`, and `99.5%` of
the q-ary GV distance, the cap activates at middle weights and leaves a term
near `2^1048540`. Thus the cap alone does not justify a cryptographic-size
field. The hit-gap/rank enumerator, which assigns field decay to surplus zero
equations before summing output containers, is required.

The first Bernoulli saddle test also shows that the relaxed output-container
sum is not sufficient. At degree `100` its support-one term is about
`2^2096332`: it counts arbitrary half-weight containers even though a sparse
row can change accumulator state at only about 100 locations. The RAA method
must be transferred in full by combining exact zero/nonzero trace placement
with the surplus-rank factor. For dense message weights, a fixed-output-support
rank-deficiency bound that groups all message supports is the likely second
branch.

The exact Bernoulli trace transfer now supplies the missing placement factor.
For support size `r`, an expanded coordinate is occupied with probability
`u_r=1-(1-theta)^r`. A two-state matrix marks both nonzero accumulator output
and occupied coordinates that return the state to zero. If a trace has `a`
such returns, its projective penalty is
`min(1,(p-1)^(r-1-a))`. This is the full RAA-style separation of trace
placement and surplus cancellation.

At `p=2^127-1`, `n=2,097,100`, and rate `1/2`, broad floating-point scans give
two candidates:

```text
99.5% of q-GV: degree 143, cutoff 1,026,880, worst sampled term -78.1186 bits
floored q-GV: degree 194, cutoff 1,032,040, worst sampled term -73.2977 bits
```

The q-ary GV root is `0.492127392425`; the floored cutoff has relative distance
`0.492127223308`. These scans are not interval certificates. Dense supports
are numerically delicate because the empty-coordinate probability can be much
smaller than machine epsilon. The diagnostic therefore carries
`(1-theta)^r` instead of subtracting it from one.

The regular projective trace analogue is now complete as an exact theorem.
Within a region, the occupancy-size birth/hold chain is mixed with the uniform
occupied-set trace transfer; multiplying the resulting two-state regional
matrices carries the accumulator state across boundaries. Two rigorous
comparisons cover the large-support range. A free coefficient saddle improves
regional Poissonization by optimizing its mean jointly with the trace markers.
A conditioning-free dense bound follows from
`Pr[E empty] <= (1-1/ell)^(r|E|)`.

For `p=2^127-1` at rate `1/2`, broad floating diagnostics give:

```text
99.5% q-GV: d=143, ell=14666, n=2097238, L=1026947, worst -300.7780 bits
floor(q-GV)-1: d=193, ell=10866, n=2097138, L=1032058, worst -98.2633 bits
```

The exact transfer is used through message weight five. These are not yet
interval certificates. Regularity drives the sparse-support terms far below
their Bernoulli counterparts, but it does not lower the large-field degree:
the dense full-support term is the effective obstruction.

A slack audit separates two effects. Optimizing the endpoint coefficient
saddle improves the degree-143 controlling term from `-59.8033` to
`-300.7780` bits, so the generic Poisson conditioning factor was quite loose.
At degree `193` and the floored q-GV cutoff, however, the tightened dense term
is still `+28.7819` bits. Replacing `exp(-r/ell)` by the exact singleton-empty
probability recovers only `0.7246` bit. Exact output-weight extraction is
expected to recover about `10.83` further bits. By contrast, setting the
empty-coordinate probability to zero changes the Chernoff term from
`+28.7819` to about `-134.05` bits. Thus rare empty output coordinates, rather
than the remaining elementary relaxations, account for most of this endpoint.

This identifies a stronger regular design. In every region, randomly permute
the `k` input rows into `ell` output groups of size `q=k/ell=d/2`. The graph is
then regular on both sides. For a fixed support of size `r`, its exact regional
trace transfer is

```text
binom(k,r)^(-1) [X^r]
  (Q0 + ((1+X)^q-1) Q1)^ell.
```

At full support every output coordinate is occupied, so this ensemble removes
the dense obstruction exactly. A free positive coefficient saddle, combined
with exact low-support extraction and convex support blocks, gives a finite
certificate at the floored q-GV cutoff:

```text
d=30, right degree q=15, ell=69905, n=2097150, L=1032064
Pr[d_min <= L] < 9.499e-10 < 2^-29.97
```

The verifier evaluates supports `1` through `64` exactly, covers supports `65`
through `k-1` with 12 outward-rounded convex block bounds, and checks full
support directly. At 192-bit Arb precision, these three contributions are less
than `7.319e-30`, `9.499e-10`, and `1.036e-75`. The floating-point optimizer
only selects fixed positive markers; it is outside the trusted base. Reproduce
the result from the repository root with:

```text
python enumerator_paper/scripts/prime_field_biregular_ea_certificate.py verify enumerator_paper/results/prime_field_biregular_ea_p127_rate_half_d30_gv.json
```

Degree `28` has negative selected exact terms but a positive transition saddle,
so it still needs a sharper handoff bound.

The labeled region-stratified regular formulas are also exact. Their shell
chain has birth, hold, and death probabilities; the hold transition is new for
odd `p`. Monomial symmetry makes every conditional regional shell uniform.
The exact two-state regional accumulator transfer, Poisson comparison, and a
dense Fourier point-mass bound are recorded in `Expander.tex` and
`PrimeFieldEA.tex`. Unlike binary regular EA, an even-support message does not
force zero sum, or an accumulator reset, at every regional boundary. For a
support-two message, a regional reset costs one scalar label equation and has
probability `1/(p-1)` instead of probability one. This removes the binary
weight-two obstruction that dominated the rate-`1/2` regular certificate.

`scripts/prime_field_regular_ea_diagnostic.py` gives two strong rate-`1/2`,
length-`2^21` candidates at `99.5%` of the relevant q-ary GV distance:

```text
p=3: d=44, ell=47662, n=2097128, L=332739, L/n=0.1586641
p=5: d=34, ell=61680, n=2097120, L=437916, L/n=0.2088178
```

The ternary scan uses exact regional terms through support 24; its largest
such term is the support-two term at `-23.4066` bits, and its sampled
Poisson/dense terms are smaller. The quinary scan uses exact terms through
support 48; its support-two term is `-24.1188` bits, with smaller sampled
Poisson/dense terms. These are floating diagnostics, not complete interval
certificates. Compared with certified binary degree `64`, they suggest edge
reductions of `31.25%` and `46.875%`.

The labeled strategy now extends to nonwrapping EC through a fresh-constraint
trace. At each output position, the construction samples a fresh feedback
vector uniformly from `F_p^m`; sampling from the full field permits the
`m+1` trailing-zero-state lumping. A zero from an active convolution state
marks an equation in the fresh feedback vector. A zero occupied symbol in the
zero state marks an equation in fresh edge labels. Applying the projective
cap only after counting both kinds of equations avoids interchanging an
average over convolution randomness with a union over messages. The theorem
and finite certificate are in `PrimeFieldEA.tex`.

Audit note: the earlier degree-`18`, memory-`1` and degree-`24`, memory-`1`
files applied the projective cap after averaging the active-state convolution
probability. Different projective messages generally impose different
feedback equations, so that interchange is not justified. Those certificates
have been withdrawn. The replacement trace counts each fresh equation before
the projective union and is independently checked on an exhaustive ternary
toy instance.

The rate-`1/2` finite result is closed at the exact floored `p`-ary GV cutoff:

| `p` | `k` | `n` | left/right degree | memory | cutoff | failure bound | bits |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `2^127-1` | `1048572` | `2097144` | `28/14` | `3` | `1032062` | `4.752556241e-9` | `27.648649` |

The union bound is partitioned by support rather than charging every support
the same relaxation. Eight exact bands cover `1..192`, 32 convex blocks cover
`193..k-1`, and full support is evaluated directly. The exact bands sum to
`1.987563e-22`; the block `[193,256]` dominates the result. The certificate
and result are
`results/prime_field_biregular_ec_p127_rate_half_d28_m3_gv.json` and the
corresponding `_result.json` file. Verification uses 256-bit Arb arithmetic.
The current degree-`26`, memory-`3` exact saddle is positive at support `128`
(`+1.607` bits). This does not rule out degree `26`; it means the present
constraint-trace relaxation does not close it. Degree `28` is the smallest
degree presently certified.

The addition-only large-field extension is different.  If every nonzero
matrix entry remains `1`, the image distribution depends on the complete
message-symbol composition, not only its support.  The composition and
information-projection machinery in `C:\Users\peter\repo\gen-BAA\field-universality`
is the correct starting point for that model.  It should be treated as a
second theorem rather than hidden inside the labeled extension.

## Current target and deferred work

The binary Bernoulli and exact-row EA targets are closed. The labeled
prime-field, two-sided regular rate-`1/2` EA target is also closed at the
floored q-ary GV cutoff for degree `30`, with ensemble failure probability
below `2^-29.97`. The corresponding nonwrapping prime-field EC target is
closed at the same rate and exact floored GV cutoff for degree `28` and
memory `3`, with failure below `2^-27.64`. `EAProof.tex`
contains the asymptotic Bernoulli theorem and certified finite bounds for both
ensembles at all three published message lengths. It now also contains
region-stratified left-regular certificates at rates `1/5` and `1/2`.

The binary finite-length and Bernoulli-asymptotic EA and wrapped-EC targets are
closed. The same-ensemble comparison with the original EC paper is closed.
The rate-`1/5` and rate-`1/2` finite GV frontiers are also closed; the latter
includes four Bernoulli row-weight/memory Pareto profiles and one certified
region-stratified left-regular profile.

1. Compare encoder cost, rather than only row weight and convolutional memory,
   along the certified frontier.
2. Check whether a sharper finite Hamming-ball estimate closes any of the
   remaining eight output-weight units without increasing `C`.
3. Keep the zero-state and stationary-boundary ensembles separate.
4. Build a finite rate-`1/2` labeled-regular EA certificate for `p=3,5,7` and
   compare its degree with the binary degree `64` certificate.
5. Decide whether reducing the `2^30` EC row weight below `20` justifies a more
   scalable small-weight verifier.
6. Treat an addition-only large-field result as a separate composition theorem
   using the machinery in `gen-BAA`.
7. Extend the labeled prime-field transfer and support-band certificate to
   wrapping EC.
8. Strengthen the degree-`30` two-sided regular certificate to a conventional
   `2^-128` ensemble failure target, either by extending exact extraction past
   support `64` or by certifying degree `32`.
9. Determine whether a sharper exact-to-saddle handoff can close degree `28`.
10. Decide whether the quadratic exact-prefix cost needed to push the
    prime-field EC degree from `18` to `16` is worthwhile; the current generic
    saddle becomes effective only near support `1600` at degree `16`.
