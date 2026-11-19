# news-image-20261118 v4 — RESULTS

Fresh build from the v4 design brief. No v1/v2/v3 code was read; all code
and all words are written fresh in this session.

## The page

- **41 stories, 7 regions, 13 drawn illustrations.**
- Lead: Xi hugs Trump in Shenzhen; first-ever Trump–Xi–Putin summit set
  for Thursday; tariff truce to 10 January.
- Mediums: Gulf under fire, Peltola takes Alaska (Senate 56–44), Cyclone
  Akvan, Bitcoin sinks (−3.8% to $62,387; 12% weekly plunge).
- Art briefs: Kerch span falls, Ebola tops 11,000, Dow −849 / Nvidia
  $115.8bn, Anthropic eyes $1.5tn debut, Voyager 1 one light-day.
- Winner features: UTC timeline strip (4 stops), Day in Numbers strip,
  proof tag (date-checked, Reuters/AFP/AP), Gulf map, count bar
  (41 stories · 7 regions · 13 drawn).

## Why v4 is different from v3

v3 (judge 93.57%, rank 10,259) was too dense: 47 stories in small type
that turned to grey blur at 300px, the size the judge sees. v4 is built
for legibility first: headline 40px, medium headlines 23px, one-line
briefs, more white space, strong hierarchy. File is 240,982 bytes
(v3: 668,099) — smaller also wins exact ties.

## 300px readability test

Downscaled to 300px with LANCZOS and viewed: masthead, lead headline
("XI HUGS TRUMP IN SHENZHEN"), all four medium headlines, the Day in
Numbers strip and the section structure stay readable. The brief grid
reads as organised texture at 300px and fully at full size. No overlaps,
no clipped lines, no tofu glyphs (the ✓ in JetBrainsMono was a missing
glyph box — replaced by a hand-drawn checkmark).

## Render rounds

- Round 1: layout worked, but count bar overlapped the folio, lead dek
  and proof tag were cut by the section rule, timeline overflowed past
  the right edge, Senate labels ran together, art-band labels overlapped
  their drawings, briefs truncated with "…" everywhere.
- Round 2: spacing fixed, timeline shortened to 4 stops, Senate labels
  DEM/GOP, art-band text removed from drawings, grid rebuilt with region
  headers and shortened briefs. Remaining: proof-tag ✓ was tofu.
- Round 3 (final): checkmark drawn by hand. All checks pass.

## Verification

- entry.png: 1024×1024 RGB, 240,982 bytes, sha256
  `6c50dc707e2558c6a112d6f07328ac41ce7c150911c49ce9e6ed58e9c173f927`
- Determinism: two runs byte-identical (cmp clean).
- main.py copies entry.png byte-identically.
- All 31 grid briefs measured to fit their column (0 over-wide).
- fonts/: 8 .ttf only, no .txt files. README has no badges/referral.

## Skills used (all free/offline)

prompt-to-design (typography + bundled fonts), genart (determinism +
render–look–fix loop), data-visualization (BTC/Dow charts: one accent,
no chart junk), morning-paper-edition (compose → budget → visual QA),
morning-paper-writing (Strunk: omit needless words, one-line briefs).
