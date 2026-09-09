# Projective union bounds for labeled prime-field EA

## Outcome

The recent large-field RAA repair does transfer to labeled Expand--Accumulate.
The correct witness is not a field-valued message. It is a pair consisting of
a message support and a proposed output support. Conditional on those two
sets and on the unlabeled expander incidence, all message values are grouped
into one projective family.

The field penalty depends on a rank statistic. Let the message support have
size `r`, and let `c` be the number of zero-terminated accumulator gaps hit by
an edge leaving that support. The conditional probability that some message
on the support produces an output in the proposed container is at most

```text
min(1, (p-1)^(r-1-c)).
```

The first `r-1` independent zero equations can therefore be absorbed by the
projective message degrees of freedom. Every additional hit-gap equation costs
a factor `1/(p-1)`.

## Relation to the RAA argument

Khabbazian's large-field RAA proof fixes support geometry and cancellation
locations before union-bounding the projective message family. A prescribed
zero return fixes a fresh random scalar, so only cancellations beyond the
projective dimension contribute field decay. Akhiani--Zhang use the same
large-field separation between support geometry and field assignments.

The EA version must account for expander collisions. A collision does not
invalidate the argument. It lowers the equation rank: all edges ending in the
same zero-terminated gap give scalar multiples of the same suffix equation.
Thus the hit-gap count is the exact rank, rather than a heuristic count of
active edges or zero outputs.

## Probability space and witness

Fix an unlabeled incidence pattern `Gamma`, a message support `S`, and an
output container `U`. Let `W` be the complement of `U`, listed as
`w_1 < ... < w_m`. The `a`-th zero-terminated gap is

```text
I_a = {w_(a-1)+1, ..., w_a},  with w_0 = 0.
```

The trailing positions after `w_m` impose no equation. Define

```text
c_Gamma(S,U) = number of gaps I_a hit by an edge from S.
```

For a fixed nonzero message on `S`, the equation that the accumulator output
vanishes at `w_a` is linear in the independent nonzero edge labels. An edge in
`I_a` has the suffix column that begins at equation `a`. Distinct suffix
columns are independent over every field. The equation rank is therefore
exactly `c_Gamma(S,U)`.

A rank-`c` homogeneous system in `M` variables has at most `(p-1)^(M-c)`
solutions in the nonzero torus. One projective message consequently succeeds
with probability at most `(p-1)^(-c)`. Union-bounding the `(p-1)^(r-1)` lines
on `S` and capping at one proves the displayed bound.

## Bernoulli incidence enumerator

For Bernoulli edge density `theta`, put `m=n-L` and

```text
a_r = (1-theta)^r,
F_r(z,v) = v/(1-z) + (1-v) a_r/(1-a_r z).
```

For one zero-terminated gap containing `u` output-container positions, the gap
length is `u+1`. It is missed by every edge from `S` with probability
`a_r^(u+1)`. The variable `z` records `u`, and `v` records whether the gap is
hit. The factor `1/(1-z)` records the trailing part of the output container.

The resulting finite bound is

```text
sum_r binom(k,r) sum_c
  [z^L v^c] F_r(z,v)^(n-L)/(1-z)
  min(1,(p-1)^(r-1-c)).
```

This enumerator sums message supports and output containers. It does not sum
field-valued messages or accumulator traces separately. It is rigorous, but
it relaxes the requirement that the coordinates inside the output container
are nonzero.

A saddle diagnostic shows that this relaxation is unusable by itself. At a
127-bit prime, rate `1/2`, length near `2^21`, Bernoulli degree `100`, and
`99.5%` of q-ary GV, even the support-one term is about `2^2,096,332`. A
degree-100 row changes the accumulator state at only about 100 locations, but
the relaxed coefficient counts essentially arbitrary half-weight containers.
This is the precise role of the RAA placement enumerator: it counts only
zero/nonzero traces compatible with the active positions.

## Exact Bernoulli trace placement

The compatible trace count again has two states. For a support of size `r`,
let

```text
u_r = 1 - (1-theta)^r
```

be the probability that an expanded coordinate receives at least one active
edge. With `z` marking nonzero output coordinates and `v` marking occupied
coordinates whose new accumulator state is zero, the transfer is

```text
K_u(z,v) = [[1-u+u v, u z],
            [u v,       z]].
```

An unoccupied coordinate preserves the accumulator state. At an occupied
coordinate, the trace selects the new state. If the trace has `a` occupied
coordinates whose new state is zero, the associated prefix equations have
rank `a`. Consecutive equations isolate nonempty groups of fresh edge labels.

The exact trace-placement bound is

```text
sum_r binom(k,r) sum_{h<=L,a}
  [z^h v^a] e0^T K_(u_r)(z,v)^n 1
  min(1,(p-1)^(r-1-a)).
```

For numerical work, split at `a=r`. The `a<=r-1` branch uses a lower-tail
marker. The `a>=r` branch uses a second marker constrained to
`v >= 1/(p-1)`. This prevents low-rank traces from reintroducing the full
projective factor.

The implementation carries `(1-theta)^r` directly. Computing
`1-(1-theta)^r` first can round to one and delete the tiny empty-coordinate
mass that controls dense supports.

## Regular incidence

The conditional surplus-cancellation lemma applies unchanged to the
region-stratified left-regular expander. Only the incidence average changes.
In a region of length `ell`, let `omega[r,u]` be the occupancy-size law after
`r` uniform endpoint draws. Conditional on size `u`, the occupied set is a
uniform `u`-subset. With

```text
Q0(z)   = [[1,0],[0,z]]
Q1(z,v) = [[v,z],[v,z]],
```

the exact regional trace transfer is

```text
S[ell,u] = binom(ell,u)^(-1) [X^u] (Q0 + X Q1)^ell
R[ell,r] = sum_u omega[r,u] S[ell,u].
```

The global theorem replaces `K_u^n` in the Bernoulli coefficient bound by
`R[ell,r]^d`. The two-state product already carries the accumulator state
across region boundaries, so no additional gap state is needed.

Three branches make the bound computable. Small supports use the exact
regional transfer. Intermediate supports use the endpoint exponential
generating function

```text
R[ell,r] = r!/ell^r [t^r] (Q0 + (exp(t)-1) Q1)^ell.
```

A free positive saddle for `[t^r]` is optimized jointly with the output and
zero-return markers. Choosing `t=r/ell` recovers ordinary Poissonization and
its conditioning factor, so the free saddle is never weaker. For dense
supports, every prescribed empty set `E` satisfies

```text
Pr[E is empty] <= (1-1/ell)^(r |E|).
```

Thus `D = (1-1/ell)^r Q0 + Q1` gives a conditioning-free, coefficientwise
trace bound. This dense matrix is deliberately unnormalized.

At `p=2^127-1` and rate `1/2`, the combined floating-point scan gives degree
`143` at `99.5%` of q-GV and degree `193` one output symbol below the floored
q-GV cutoff. The respective largest sampled terms are `-300.7780` and
`-98.2633` bits. Regularity makes sparse supports dramatically safer (the
degree-143 support-one term is below `2^-4860`) but does not improve the degree
over Bernoulli incidence: dense full support controls the frontier.

The fixed-mean Poisson loss was real proof slack: freeing its coefficient
saddle improves the controlling degree-143 term by about `241` bits. It does
not explain the degree frontier. At degree `193` and the floored q-GV cutoff,
the tightened dense term is `+28.7819` bits. The exact singleton empty-set
probability saves only `0.7246` bit, while exact output-shell extraction should
save about `10.83` bits. Removing empty coordinates altogether would save
about `162.8` bits.

This points to two-sided regular incidence. If each region is a random
partition of the `k` input rows among `ell` output coordinates, with exactly
`q=k/ell=d/2` rows per output coordinate, then the exact regional transfer is

```text
binom(k,r)^(-1) [X^r]
  (Q0 + ((1+X)^q-1) Q1)^ell.
```

Every coordinate is occupied at full message support. This model removes the
observed dense obstruction rather than trying to bound it more sharply. The
finite certificate at the floored q-GV cutoff has left degree `30`, right
degree `15`, `ell=69,905`, `n=2,097,150`, `k=1,048,575`, and `L=1,032,064`.
It proves

```text
Pr[d_min <= L] < 9.499e-10 < 2^-29.97.
```

The verifier uses exact regional extraction for supports `1` through `64`, 12
convex support blocks for supports `65` through `k-1`, and a direct
full-support check. The respective 192-bit Arb bounds are `7.319e-30`,
`9.499e-10`, and `1.036e-75`. Floating-point optimization only supplies fixed
positive coefficient markers; all inequalities are re-evaluated with outward
rounding. The certificate is
`results/prime_field_biregular_ea_p127_rate_half_d30_gv.json` and the verifier
is `scripts/prime_field_biregular_ea_certificate.py`.

## What the coarse cap shows

The simpler support-grouped bound

```text
sum_r binom(k,r) min(1,(p-1)^(r-1) tau_r)
```

is already strictly stronger than the word-by-word first moment. It leaves the
small-field `p=3` and `p=5` candidates unchanged because their relevant
projective families are already below the cap. At a 127-bit prime, rate `1/2`,
length near `2^21`, and regular degree `100`, the cap activates at middle
message weights and leaves a term of about `2^1,048,540`. This demonstrates
that support grouping alone is insufficient.

The hit-gap bound is the algebraic half of the substantive repair. At large
`p`, every witness with `c >= r` receives field decay. Only incidence patterns
with fewer than `r` hit zero-gaps remain coefficient-independent. The other
half is the exact trace-placement count.

The combined Bernoulli diagnostic is now implemented. For `p=2^127-1`,
`n=2,097,100`, and rate `1/2`, it gives:

| target | cutoff | degree | largest sampled log2 term | support |
|---|---:|---:|---:|---:|
| `99.5%` of q-ary GV | `1,026,880` | `143` | `-78.1186` | `1` |
| floored q-ary GV | `1,032,040` | `194` | `-73.2977` | `k` |

These are broad floating-point support grids, not interval certificates. The
ordinary per-line enumerator remains stronger for the tested small fields. A
final verifier should take the smaller bound at every message weight.

For dense message supports, the stronger alternative is to fix one output
support `U` and study

```text
rank((B A)[:, complement(U)]) < k.
```

This groups all message supports and all projective assignments. Its generic
rank is a matching problem from message rows through expander endpoints to the
accumulator gap classes. A useful finite-field bound must exploit rank surplus;
a single-minor Schwartz--Zippel bound of order `k/p` is not sufficient.
