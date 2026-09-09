# Submission package

This directory is the venue-independent submission package for
*Expander-Based Codes at the Gilbert--Varshamov Bound*.

## Contents

- `paper/` contains the complete LaTeX source and bibliography.
- `scripts/` contains the numerical verifiers and their unit tests.
- `results/` and `scripts/certificates/` contain the frozen certificate inputs.
- `certificate_manifest.json` maps each finite claim to its verifier and pins
  the verifier-source and certificate digests.
- `requirements.txt` pins the tested Python dependencies.

## Reproduce

From `expander_codes/`, run:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s scripts -p "test_*.py"
python scripts/verify_manifest.py --strict-versions --list
python scripts/verify_manifest.py --run headline
```

The manifest driver runs certificate processes serially.  The degree-6/3
binary certificate is intentionally in the `slow` group and requires much
more time and memory than the other headline checks.  Use `--run all` to replay
every rigorous finite claim.

Build the paper from `paper/` with:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Scope

The main asymptotic theorem approaches GV with `O(n log n)` expected field
operations and tunable polynomial sampling failure. A corollary gives
negligible failure at `O(n log^2 n)` expected cost. Both cover EA over fixed
finite fields and fixed-memory wrapped binary EC. Full-field EC is covered
by the separate finite certificates, not these asymptotic results.

The paper proves minimum-distance statements for sampled code ensembles.  It
does not claim an efficient decoder, a deterministic construction, or a full
Silent OT or Silent VOLE security theorem.  The protocol-level sampling term
is isolated in Proposition 9.1.  The implementation's structured streaming
field encoder is discussed as a heuristic and is not identified with the
independently labeled proof ensemble.

Independent review is still in progress; see
`notes/CORE_RESULTS_AUDIT_ASTRA.md` for the checked claims and remaining work.
In particular, do not equate a successful build or manifest check with a
completed proof audit. Venue-specific work also remains: apply the requested
class file and page limit, supply author metadata, and complete the venue forms.
