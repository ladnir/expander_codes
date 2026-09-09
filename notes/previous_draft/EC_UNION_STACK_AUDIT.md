# EC union-stack audit

## Question

Does the one-pass prime-field Expand--Convolute analysis miss an
intermediate-shell denominator analogous to the repeat--accumulate and
block--accumulate composition bounds?

## Conclusion

No additional uniform permutation should be inserted or removed.  The
construction's independent regional permutations already randomize the
expanded support conditionally on its regional profile.  Writing this as an
explicit expander-enumerator/convolution-enumerator composition is an exact
refactorization of the fixed-projective-line first moment; it does not create
a new denominator.

Applying the projective cap only after that complete fixed-line composition is
far weaker than the existing constraint trace.  At the certified parameters

```
p = 2^127 - 1, d/q = 28/14, m = 3,
n = 2,097,144, k = 1,048,572, L = 1,032,062,
```

the coarse shell stack at message support 128 has log2 bound `1843.8264` and
its projective cap is saturated.  The existing placement-conditioned
constraint trace at the same support has log2 bound `-284.3091`.  The cap must
therefore remain inside the trace/placement sum.

## Conditional placement cap

For a fixed regional placement one can validly cap the sum over all compatible
low-weight convolution traces at one before averaging the placement.  The
small exhaustive diagnostic in `scripts/ec_placement_cap_experiment.py`
measures this possible improvement.

The gain is zero at sparse support in the tested instances.  It becomes
visible only toward dense support (for example, about 0.41 bits at support
6 of 8 and 6.68 bits at full support in one toy instance).  The finite proof
already switches to a separate dense/full-support bound there.  This cap is
therefore unlikely to change the minimum certified degree.

## Singleton refinement

The current regional EC trace does lose genuine regular-expander information.
It combines every group hit by at least one supported message coordinate into
one occupied case.  Over nonzero edge labels, a group hit exactly once cannot
cancel to zero.  Only a group hit at least twice can cancel.

Let `Q_0`, `Q_1`, and `Q_ge2` denote the empty, singleton, and collision
coordinate transfers.  At convolution state zero, `Q_1` has only the nonzero
transition.  The refined regional polynomial is

```
Q_0 + q X Q_1 + ((1+X)^q - 1 - q X) Q_ge2.
```

This refinement is theorem-level: it follows directly from a nonzero message
symbol times a nonzero edge label being nonzero.  The diagnostic implements
both normalized exact coefficients and the positive coefficient saddle.

Measured improvements:

| Parameters | Support band | Old log2 bound | Singleton-refined log2 bound |
|---|---:|---:|---:|
| d=26, m=3 | r=128 exact | 1.60770 | 1.18185 |
| d=28, m=3 | r=193..256 saddle | -28.64865 | -30.28319 |

The refinement is real but does not make degree 26, memory 3 certify the GV
cutoff with a 20-bit margin.

## Memory-four degree-26 candidate

Increasing the convolution memory from three to four has a much larger effect.
For degree 26 and the exact floored p-ary GV cutoff,

```
n = 2,097,134, k = 1,048,567, L = 1,032,057,
```

the singleton-refined exact terms sampled so far are safely negative:

| Support | Diagnostic log2 bound |
|---:|---:|
| 128 | about -175.4 |
| 224 | about -260.7 |

However, the current per-region positive coefficient saddle is extremely
loose in this range.  It gives `+378.27` for block 193..256 and `+308.16` for
block 401..800, then becomes safely negative (`-1526.20`) for block 801..1600.
This is hundreds of bits of coefficient-extraction slack, not evidence of bad
codes.

## Next proof target

The most promising route to a degree-26, memory-4 certificate is to retain
normalized exact regional coefficients through support 800, or to prove a
sharper coefficient bound that recovers the local point-mass factor lost by
the current saddle.  This is the same kind of support-range separation that
the recent large-field repeat--accumulate/block--accumulate proofs exploit.
It is more promising than adding another convolution shell union bound.

## Closed degree-26, memory-4 certificate

The truncated Arb polynomial-matrix verifier removes the coefficient-saddle
slack while keeping outward-rounded arithmetic.  It evaluates the
singleton-refined regional numerator through support 800, then uses the
positive saddle from support 801 onward.

At the exact floored p-ary GV cutoff it certifies

```
d/q = 26/13, m = 4,
n = 2,097,134, k = 1,048,567, L = 1,032,057,
Pr[d_min <= L] <= 3.052485e-22 < 2^-71.4724.
```

Thus degree 26, memory 4 exceeds the requested 20-bit margin by more than 51
bits.  The largest contribution is the exact band 97..128.  The next frontier
is degree 24: memory 5 fails near support 160, while preliminary exact
diagnostics indicate that memory 6 may work.

## Memory--degree frontier

The current rate-half, floored-GV frontier through memory 21 is approximately

| Convolution memory | Smallest left degree | Status |
|---:|---:|---|
| 1 | 38 | diagnostic |
| 2 | 30 | diagnostic, marginal 20-bit margin |
| 3 | 28 | certified |
| 4 | 26 | certified |
| 6 | 24 | diagnostic |
| 12 | 22 | diagnostic |

Degree 20 is not reached by memory 21 with the present trace: at memory 21,
support 512 still has exact structural log2 bound about `+131.90`.  The rough
work proxy `d+m` is minimized at the middle of the observed frontier:
degree/memory `26/4` and `24/6` both cost 30, whereas `22/12` costs 34.
Thus increasing memory remains valuable, but returns diminish sharply after
memory six at this block length.
