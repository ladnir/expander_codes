# Standalone repository migration

Date: 2026-09-09.

Canonical repository: <https://github.com/ladnir/expander_codes>.

The working project was copied from the `expander_codes/` directory of
`ladnir/permute_conv` into the root of this repository. This is a file import,
not a Git history rewrite. The source checkout was based on commit
`63acf54f` and contained additional uncommitted paper, verifier, test, and
audit changes; those working files are included here.

The import includes 185 source/data/documentation files, including the new
core audit, constant-degree probe, and their tests. Each imported file was
checked byte-for-byte against its source before the standalone README and
ignore rules were adjusted. The latest paper PDF is also included under
`output/pdf/` and includes the author's ChatGPT-assistance footnote.

The source copy has not been deleted or modified by this migration. The
original permute-convolute paper and SPIN work remain in `permute_conv`.
The libOTe implementation remains in its own repository/worktree; it is not
part of this import.

Generated LaTeX intermediates, Python bytecode, numerical caches, and scratch
work are not imported. Frozen certificates, recorded result files, active
research notes, and the previous draft sources are included.

Run the commands in `SUBMISSION.md` from this repository's root. Older
handoffs retain historical absolute paths and `expander_codes/` prefixes;
their mathematical context remains useful, but new work should use this
standalone repository. No verifier paths or certificate digests were changed.

Local clone: `C:/Users/peter/repo/expander_codes`.

## Standalone verification

- All 231 unit tests pass from the new repository root.
- Strict manifest checks pass for 12 claim groups and 18 frozen artifacts.
- A clean LaTeX build produces the 51-page paper without unresolved
  references or overfull/underfull boxes.
- Extracted text from every rebuilt PDF page matches the imported PDF;
  the first page and assistance footnote were also visually checked.

The published PDF is the byte-for-byte copy of the last reviewed source
PDF. The clean build is a reproducibility check, not a manuscript revision.
