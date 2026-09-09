# Stress test for uncertified rate-one-half wrapped-EC profiles

## Certified control

The current binary boundary profile has

```text
k = 2^20
n = 2^21
L = 230741
delta = L/n = 0.11002588272094727
C = 2.85
p = C ln(n)/n
wrapping memory = 13
```

The Bernoulli expander therefore has expected row weight
`pn = C ln(n) = 41.4848587565`.

This profile is not aggressive: the existing Arb certificate bounds the
probability that the sampled code has
a nonzero word of weight at most `L` by `5.971032143e-7`.  Its three pieces are

| message range | certified contribution |
|---|---:|
| exact, `1 <= r <= 32` | `2.574039056e-7` |
| intermediate | `1.589442947e-10` |
| dense | `3.395403644e-7` |

The exact piece is almost entirely the weight-one term:

| message weight `r` | certified first-moment term | bits |
|---:|---:|---:|
| 1 | `2.574039031e-7` | 21.8895 |
| 2 | `2.481382357e-15` | 48.5178 |
| 3 | `1.290730873e-23` | 76.0362 |

This certified profile is a negative control for the search harness.  A search
over small message supports should first test individual rows.  Pair and triple
searches are useful controls, but the ensemble bound predicts that they are much
less dangerous.  The dense contribution is an aggregate upper bound.  It does
not identify a structured witness.

## Uncertified targets

The first genuinely aggressive target is the published fixed-row wrapping
profile

```text
k = 2^20
n = 2^21
exact expander row weight = 5
wrapping memory = 25
```

The Expand--Convolute paper recommended this profile from empirical evidence,
not from a minimum-distance proof.  It reported a smallest found relative
weight near `0.1`.  The stress test should also sweep memory below `25`,
including the published `w=5, m=9` experiment whose smallest found relative
weight was near `0.03`.

The archived `ExConvCodeOld` implementation is the reference implementation
for this target.  It is systematic by default and applies one convolution pass.
Each expander row samples five coordinates uniformly with replacement; repeated
coordinates cancel over `F_2`.  It does not use the newer stratified expander.

Consequently, the implementation's nominal row weight `5` is not an exact row
weight.  For an expander domain of size `q`, one row has effective weight three
with probability

```text
(60 binom(q,3) + 240 binom(q,4)) / q^5.
```

At `q=2^20`, this probability is `9.536697689e-6`.  Among `2^20` rows, the
expected number of effective weight-three rows is `9.9999523`, and the
independent-row model gives probability `0.9999546` of at least one.  Effective
weight-one rows have expected count only `1.43051e-5`.  An exhaustive generator
row sweep can therefore find the effective weight-three family.  The resulting
codeword weight still depends on the sampled convolution and must be measured;
the collision count alone is not a codeword-weight bound.

The support of a collapsed weight-three row is uniform among three-subsets of
the parity block.  If there are approximately ten such rows, the median latest
starting support leaves a suffix fraction `a` determined by

```text
10 a^3 = ln 2,
```

or `a = 0.41078`.  A live wrapping convolution has output density close to one
half in that suffix.  Since the systematic code has length `2k`, this predicts
a best generator-row relative weight near `a/4 = 0.10269`.  This is a
findability heuristic, not a distance proof.

The collision finder in `scripts/ec_collision_finder.py` tests this mechanism
in linear expander time and bit-slices all retained rows through the same
convolution.  A 16-seed ensemble-level sweep at `k=2^20`, `w=5`, and `m=25`
found `8.5` collapsed rows per code on average.  The mean best relative weight
was `0.1057841`, and the best sample had relative weight `0.03628016`.  The
results are stored in
`results/ec_collision_k20_w5_m25_seeds1_16.json`.  They use NumPy's PCG64 and
therefore sample the paper ensemble without replaying libOTe's AES-based PRNG.

This experiment explains why the newer fixed-region edges matter.  A single
duplicate pair in the old with-replacement sampler occurs with probability
Theta(`1/k`) per row and leaves an effective weight-three row.  Four edges in
disjoint fixed regions remove that first-order cancellation mechanism without
the cost of sampling every edge globally without replacement.  Collisions
involving the remaining uniform edges are still possible, but reaching
effective weight three then requires multiple coincidences and has much lower
probability.

## Paper-like exact-row target

The primary attack target removes the sampler collision.  Let `B` have `k`
rows, each sampled independently as a uniform five-subset of `[k]`.  Let `C`
be one zero-initial wrapping convolution pass of memory `25`.  The systematic
rate-one-half generator is

```text
[I | B C].
```

This ensemble has a separate boundary mechanism.  For a suffix `D_s` of `s`
parity coordinates, a fixed expander row lies in `D_s` with probability

```text
binom(s,5) / binom(k,5).
```

The convolution matrix is upper triangular.  It therefore maps every vector
supported in `D_s` to another vector supported in `D_s`.  If row `i` lies in
the suffix, the message basis vector `e_i` produces a systematic codeword of
weight at most `1+s`.  This bound holds for every realization of the
convolution.

More generally, for constant row weight `w`, set

```text
s = ceil(c k^(1-1/w)).
```

The expected number of rows in `D_s` tends to `c^w`.  The probability of at
least one such row tends to `1-exp(-c^w)`.  Taking
`c=(log k)^(1/w)` makes the failure probability polynomially small and gives
an efficiently findable codeword of relative weight

```text
O((log(k)/k)^(1/w)).
```

The finder only scans the first coordinate of every sorted row.  Its expander
work is `O(kw)`.  This attack uses exact rows sampled without replacement; it
does not use duplicate-edge cancellation.

At `k=2^20`, `w=5`, and `s=k/16`, the expected number of suffix rows is
`0.999857`.  The probability of at least one is `0.632068`.  Seed `1` of the
ensemble sampler contains the row

```text
1005910, 1011372, 1037456, 1039829, 1042887.
```

All five coordinates are in the final sixteenth.  The deterministic suffix
bound gives relative weight at most `0.0312505`.  Exact convolution evaluation
gives message weight `1`, parity weight `21343`, and relative codeword weight
`0.0101776123`.  The receipt is
`results/ec_region_k20_w5_m25_r16_seed1.json`.

The scope is the zero-initial upper-triangular construction.  A construction
that prepends a random initial-state map, or forces one edge into every one of
five separated regions, does not satisfy the suffix-row premise.

These profiles are the positive targets: the objective is to improve the known
low-weight constructions or find a different mechanism.  Any profile that later
receives a complete certificate moves into the control set.

The current libOTe profile is different from both published targets.  The
configuration called `ExConv7x24` uses expander weight `7`.  Its 24 random
feedback taps and one fixed wrapping tap give convolution memory `25`.  The
expander places four edges in four fixed coordinate regions and places three
edges uniformly.  The systematic implementation also applies two independently
seeded convolution passes.  Parameter selection assigns this construction
pseudo-distance `0.15`.
That value is an aggressive assumption, not a proved distance or a stored
low-weight witness.

## What the existing software can find

The current `ExConvChecker` implements two searches.

1. Its default search exhaustively evaluates all generator rows.  The finder is
   polynomial-time and practical through bit slicing.  It returns the minimum
   weight but does not retain the message index, codeword, seed, or a witness
   digest.
2. Its `x2` search evaluates all sums of two generator rows.  It first stores the
   compressed generator matrix and then performs a quadratic scan.  At
   `k=2^20`, this method requires about 256 GiB for the generator matrix and
   approximately `2^40` pair comparisons.  It is not a feasible full-size
   attack.

The EC checker does not implement the region-signature attack from Section 4.2
of the paper.  The related `EAChecker` implements approximate signature hashing
for the accumulator construction, but that code does not enforce or solve the
larger convolution boundary state.

The reproducible evidence presently supports only the following claims.

| construction | search evidence | reported relative weight |
|---|---|---:|
| published `w=5, m=9` | empirical search reported in the EC paper | `0.03` |
| published `w=5, m=25` | empirical search reported in the EC paper | `0.1` |
| current libOTe `w=7, m=25`, two pass | configured pseudo-distance assumption | `0.15` |

The first two rows are paper-level empirical claims.  The repository does not
currently contain the sampled seed, message support, and codeword digest needed
to replay either witness.  The third row is not a witness claim.  Therefore, we
do not yet have a reproducible upper bound below `0.15n` for the exact deployed
construction.

## Relation of the certified control to the region-signature attack

Section 4.2 of the Expand--Convolute paper partitions the `n` expander
coordinates into `beta` regions.  It groups rows by the regions hit by their
expander edges.  Enough rows in one group give a nonzero assignment that
returns all convolution states to zero at the region boundaries.

For row weight `w` and convolution memory `m`, the deterministic argument asks
for more than `mw` rows in one signature class.  Its coarse pigeonhole
condition is

```text
k / beta^w > mw.
```

At `k=2^20`, `w=41`, and `m=13`, this condition requires
`beta < 1.2033`.  No nontrivial integer partition qualifies.  Moreover, a
union of `w` equal regions has relative length at most `w/beta`.  Reaching the
target distance would require approximately `beta >= w/delta = 372.64`.
Even after treating each signature as an unordered multiset, the number of
signatures at `beta=373` is approximately `2^188.81`, compared with only
`2^20` expander rows.

This calculation does not prove that the code resists structured searches.  It
shows that the original exact-signature collision is the wrong search space for
this parameter set.

## Exact-row hardening of the certified control

The implementation can sample every expander row with a fixed weight near the
Bernoulli mean.  A floating-point Chernoff diagnostic for exact row weight `41`
and memory `13` gives the following estimates for the first eight message
weights:

| `r` | first-moment log2 bound | dominant expander shell |
|---:|---:|---:|
| 1 | -58.074116 | 41 |
| 2 | -125.590422 | 82 |
| 3 | -193.956080 | 123 |
| 4 | -262.813764 | 164 |
| 5 | -332.021790 | 205 |
| 6 | -401.501158 | 246 |
| 7 | -471.200919 | 287 |
| 8 | -541.085329 | 328 |

Fixing the row weight removes the Bernoulli ensemble's dominant light-row
mechanism.  The weight-one bound improves from `2^-21.8895` to `2^-58.0741`,
while the expander cost decreases slightly from mean weight `41.485` to weight
`41`.  This diagnostic does not yet certify all message weights.  The full
exact-row Arb run remains open.

## Stronger witness searches

### 1. Exact row sweep

For each message basis vector `e_j`, compute `e_j B C` and record its weight,
first active expander coordinate, number of active convolution episodes, and
longest zero interval.  This search directly targets the dominant Bernoulli
term.  For the exact-row ensemble, it tests whether an implementation detail
creates a row distribution that differs from the mathematical model.

### 2. Rank-based interval search

Choose an output support candidate `D`, preferably a union of short intervals,
and a candidate message set `S`.  A nonzero message supported in `S` produces
a codeword supported in `D` exactly when

```text
rank((B C)[S, complement(D)]) < |S|.
```

Testing this rank condition uses the actual convolution equations.  It can find
dependencies that the old boundary-state pigeonhole argument misses.  Search
over unequal intervals, adaptive interval splits, and rows with unusually many
neighbors near `D`.

### 3. Soft-support subset search

The original experiment admitted signatures that differed by one neighboring
region.  A stronger search should not classify an outside edge as an immediate
failure.  Instead, it should score the exact extra output weight caused by that
edge.  Beam search or meet-in-the-middle can combine rows while retaining the
best partial assignments according to

```text
(current output weight, boundary state, uncovered expander edges).
```

This search interpolates between exact signature collisions and unrestricted
low-weight-codeword search.

For the current `ExConv7x24` expander, hash the four stratified edges first and
treat the three uniform edges as soft support.  If each stratified coordinate
region is divided into eight bins, there are `8^4 = 4096` signatures and about
`2^20/8^4 = 256` rows per signature on average.  This is large enough to solve
hundreds of linear boundary equations.  The search must still pay for the three
uniform edges and the second convolution pass; ignoring either effect would not
produce a valid witness.

### 4. Output-domain shortening search

For any candidate output `y`, define `z = y C^-1`.  The inverse recurrence is
local: each nonzero coordinate of `y` affects only a memory-13 neighborhood in
`z`.  A codeword supported in `D` exists exactly when some nonzero `y_D`
satisfies

```text
y_D C^-1 in RowSpace(B).
```

For a parity-check matrix `H_B` of the expander row space, this becomes a rank
test on `((C^-1)[D, *]) H_B^T`.  Interval supports make the inverse images
sparse and give a structured family of shortening tests.

### 5. Generic-search control

At reduced lengths, compare the structured searches against exact minimum
distance or an information-set-decoding baseline.  Record both the lightest
word and the message weight that produces it.  Small-length results are a
calibration tool, not evidence for asymptotic distance.

### 6. Planted-witness control

Sample a valid-looking expander with a hidden interval collision or rank defect.
Every search implementation must recover the planted word at the expected
cost.  A negative result on unplanted samples is not meaningful until this
control succeeds.

### 7. Findability enumerator

Define `Z_L` as the number of generator rows whose codeword weight is at most
`L`.  The existing distance enumerator gives an upper bound on `E[Z_L]`, but a
finder needs a lower bound on `Pr[Z_L > 0]` or a reproducible empirical
estimate.  For the deployed two-pass convolution, an exact single-row transfer
process can track both convolution states.  Its reduced state space has at most
`(m+1)^2` states before adding the small exact-row counter.

The marginal row calculation predicts the threshold found by an exhaustive row
sweep.  A second-moment calculation for two independently sampled expander rows
under the shared convolution would convert that prediction into a lower bound
on finder success through Paley--Zygmund.  The shared convolution randomness
must remain explicit; treating the `k` generator-row events as unconditionally
independent is not justified.

## Recommended order

1. Measure the suffix-row attack across independent exact-row samples and
   compare it with its exact order statistic.
2. Run the boundary-nullspace search after excluding terminal suffix buckets.
   This isolates the multi-row mechanism from the single-row boundary effect.
3. Add shifted and unequal partitions, followed by soft-support buckets.
4. Repeat the experiment with a random initial-state map.
5. Treat the five-region expander as a later countermeasure, not as the attack
   target.

The primary target is now the single-pass, systematic, exact-weight-five paper
ensemble.  The old with-replacement implementation is a diagnostic control.
The newer two-pass construction remains a later hardening comparison.
