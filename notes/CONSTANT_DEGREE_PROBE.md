# Constant-degree probe: short bursts from small message supports

Date: 2026-09-05. This is a research note, not a new claim in the manuscript.

## Question and scope

Can the current regular ensembles, with constant degree and constant memory,
have a positive relative distance with sampling failure tending to zero as
the length grows?

The answer is no for the ensembles below. Two fixed message coordinates
already give a nonvanishing lower bound on failure for EA and binary wrapped
EC. Full-field EC has a stronger obstruction from one message coordinate.
These are events in the sampled code, not losses from a union bound.

This conclusion does not invalidate the finite-length certificates. Their
degree and memory are constants at the stated length, and their failure
bounds concern that length. The lower bounds here can be extremely small.
Nor is this an impossibility result for every constant-degree expander or
every linear-time code.

Use the definitions in `paper/02-constructions.tex`. Fix a left degree
`d >= 1`, and let `n = d*ell` grow through admissible lengths. There is one
edge per message coordinate in each of the `d` consecutive regions. Sample
either the left-regular ensemble or the two-sided regular ensemble. In the
latter case, fix a right degree `b >= 1` and set `k = b*ell`. Assume `k >= 2`.
Region samplings are independent. Over a fixed field of order `p`, edge
labels are independent and uniform among its `p-1` nonzero elements.

As in the paper, define

\[
 d_{\min}(G):=\min_{x\ne0}\operatorname{wt}(xG).
\]

Fix a target relative distance `0 < delta < 1`. All probabilities below are
over the expander and, for EC, its independent convolution coefficients.

## The expander event

Fix the message `x = e_1 + e_2` before sampling the code. In each region,
let `U` and `V` be the edge positions of its first and second coordinates.
Write

\[
 h:=\lfloor\ell/2\rfloor,\qquad
 w:=\lfloor\delta\ell/2\rfloor.
\]

For a fixed integer `s >= 1`, require

\[
 1\le U\le h,\qquad s\le V-U\le w.
\]

There are exactly `h*(w-s+1)` such ordered coordinate pairs when `w >= s`.
They all lie in the region because `h+w <= ell`.
Under left regularity, each pair has probability `1/ell^2`.
Under two-sided regularity, the two vertices occupy distinct permutation
slots. For any distinct right coordinates `u,v`,

\[
 \Pr[U=u,V=v]
 =\frac{b^2}{b\ell(b\ell-1)}\ge\frac1{\ell^2}.
\]

Thus each region satisfies the placement event with probability at least

\[
 A_\ell(s):=\frac{h(w-s+1)}{\ell^2},
 \qquad \lim_{\ell\to\infty} A_\ell(s)=\frac\delta4.
\]

The event arranges a pair of nonzero inputs separated by at most `w`
positions. The following arguments make the recursive state return to zero
at the second input. Every output outside those short intervals is then zero.

## EA over a fixed finite field

For EA, use `s = 1`. In each region, additionally require the two edge labels
to sum to zero. This has probability `1/(p-1)`, independently of positions and
other regions. Over the binary field, it holds automatically.

Starting from zero, the accumulator outputs the first label at positions
`U,...,V-1`. At `V`, the second label cancels the first. The state remains zero
until the next region's first input. Hence the output weight is

\[
 \operatorname{wt}(xG)=\sum_{j=1}^d(V_j-U_j)\le dw
 \le\delta n/2.
\]

In particular, the bad-distance event occurs for all sufficiently large
lengths. Independence across regions gives the finite lower bound

\[
 \Pr[d_{\min}(G)\le\lfloor\delta n\rfloor]
 \ge \left(\frac{A_\ell(1)}{p-1}\right)^d.
\]

Consequently,

\[
 \liminf_{\ell\to\infty}
 \Pr[d_{\min}(G)\le\lfloor\delta n\rfloor]
 \ge\left(\frac{\delta}{4(p-1)}\right)^d>0.
\]

This proof covers every fixed finite field, not only prime fields.

## Binary wrapped EC with fixed memory

Fix memory `m >= 1` and use the paper's wrapped recurrence

\[
 y_t=u_t+y_{t-m}+\sum_{j=1}^{m-1}b_{t,j}y_{t-j}.
\]

The coefficients `b_{t,j}` are independent fair bits. The state comprises the
last `m` output bits. Call a state active when at least one bit is nonzero.

With zero input, an active state cannot become zero. If one of the most
recent `m-1` bits is nonzero, the next output is a fair bit. Otherwise, the
oldest bit is one, and the next output is forced to one.

We need a lower bound on the chance that a second input cancels the state.
From any active state, the following sequence of `m` zero-input outputs has
probability at least `2^{-m}`:

\[
 1,\underbrace{0,\ldots,0}_{m-1}.
\]

The first output is one with probability at least one half. Each requested
zero has probability one half because the initial one is still among the
most recent `m-1` bits. For `m=1`, the sequence is a forced one, so the same
lower bound remains valid. After this sequence, only the oldest state bit
is one. An input one at the next step cancels it deterministically, leaving
the entire state zero.

Apply the placement event with `s = m+1`. The first input at `U` activates
the state. It stays active until the second input at `V`. The last `m`
zero-input steps before `V` exist because `V-U >= m+1`. Requiring the output
sequence above on those steps makes the state zero at `V` with conditional
probability at least `2^{-m}`. This bound holds for every earlier active state.

On this event, the output in the region is supported within `U,...,V-1` and
has weight at most `w`. Applying the conditional bound successively across
regions gives

\[
 \Pr[d_{\min}(G)\le\lfloor\delta n\rfloor]
 \ge \left(A_\ell(m+1)2^{-m}\right)^d
\]

for all sufficiently large lengths. In particular,

\[
 \liminf_{\ell\to\infty}
 \Pr[d_{\min}(G)\le\lfloor\delta n\rfloor]
 \ge \left(\frac{\delta}{4\,2^m}\right)^d>0.
\]

No independence between the outputs of different messages is asserted or
needed: the proof uses one fixed message. It also needs no limiting Markov
chain calculation. This conservative lower bound does not establish that
failure tends to one.

## Full-field EC: spontaneous loss of state

For this paragraph, use the paper's full-field EC coefficients, independently
uniform in `F_p^m`. Fix `p`, `m`, and `d`. Unlike wrapped binary EC, this
convolution can lose its entire state without a second input.

During zero input, a nonzero state produces zero with probability `1/p`.
The zero state stays zero. Therefore, from any state, the next `m` outputs
are all zero with probability at least `p^{-m}`. Such a block leaves zero
state. If `T` counts zero-input steps until the state first becomes zero,
the conditional block bound implies

\[
 \Pr[T>jm]\le(1-p^{-m})^j,
 \qquad \mathbb E[T]\le mp^m.
\]

Fix `x = e_1`. Its expander output has exactly `d` nonzero inputs. Condition
on their positions and labels. Partition the output into intervals starting
at those inputs and ending just before the next input, or at the code's end.
Each interval has one input step followed by zero-input steps. Fresh future
coefficients give conditional expected output weight at most `1+mp^m` in
each interval, regardless of its starting state or length. Thus

\[
 \mathbb E[\operatorname{wt}(e_1G)]\le d(1+mp^m),
\]

and Markov's inequality yields

\[
 \Pr[d_{\min}(G)>\lfloor\delta n\rfloor]
 \le\frac{d(1+mp^m)}{\lfloor\delta n\rfloor+1}
 \longrightarrow0.
\]

This asymptotic statement keeps the field fixed, even when its order is
`2^128`. The displayed bound becomes useful only at enormous lengths for
that field. It says nothing adverse about our certified practical lengths.
It does not apply to a variant that fixes the oldest feedback coefficient
to a nonzero value.

## Consequence for the paper

The defensible split remains:

- Asymptotic GV distance with `O(n log n)` expected field operations and
  any fixed polynomial failure exponent; a stronger corollary gives
  negligible failure at `O(n log^2 n)` expected cost.
- Concrete finite-length certificates with explicit degree and memory costs,
  including the existing near-GV instances. Do not call this a linear-time
  result: the certificates do not establish an asymptotic code family with
  the same distance and failure guarantees.

Simply lowering the target to another positive constant does not give an
asymptotic vanishing-failure theorem for the fixed-parameter ensembles above.
Two-sided regularity does not remove the exhibited events.

Do not yet claim an asymptotic theorem for a fixed, nonvanishing failure
target such as `2^{-40}`. The EA and wrapped-EC lower bounds alone neither
establish nor rule out that stronger uniform-in-length question at every
target. Nor do these bounds show that growing degree or memory suffices.

Presentation decision after discussion with the author: report expected
encoding cost as `O(n log n)` for logarithmic degree and `O(n log^2 n)` for
the negligible-failure GV corollary. Use the finite degree/memory tables for
concrete costs, without a linear-time claim. A new constant-degree asymptotic
construction is a separate project, not another numerical sweep.

Validation: `scripts/test_constant_degree_probe.py` checks the placement
counts, wrapped-state cancellation, accumulator cancellation, and full-field
reset bound by exact finite enumeration. The arguments above establish the
claims for arbitrary admissible parameters; the tests only check small cases.
The note follows CWC's explicit probability-space and scope requirements.
