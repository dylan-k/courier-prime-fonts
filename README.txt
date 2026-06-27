COURIER PRIME FONTS — master set
=================================

This folder holds the master copies of the Courier Prime font families.

Standard format: OpenType (.otf). Filenames: Title Case with spaces.

EXCEPTION: the Code Nerd Font Mono family ships as hinted TrueType (.ttf) —
TTF + bytecode/gasp hinting renders cleanly under Emacs-on-Windows (GDI),
where unhinted CFF/OTF looks pixellated. 

License: SIL Open Font License 1.1 (OFL) for all families.


CONTENTS (14 faces — 10 OTF + 4 TTF)
---------------------------------------------
Courier Prime (screenplay) — v1.203/1.202, native OTF:
  Courier Prime Regular.otf
  Courier Prime Bold.otf
  Courier Prime Italic.otf
  Courier Prime Bold Italic.otf

Courier Prime community weights — v1.202, by M. Babek Aliassa:
  Courier Prime Medium.otf
  Courier Prime SemiBold.otf

Courier Prime Sans — v3.020:
  Courier Prime Sans Regular.otf
  Courier Prime Sans Italic.otf
  Courier Prime Sans Bold.otf
  Courier Prime Sans Bold Italic.otf

Courier Prime Code Nerd Font Mono — base v3.0318 + Nerd Fonts 3.4.0 icons
  (hinted TTF; single-width "mono"; ~11k glyphs incl. all NF icon sets):
  Courier Prime Code Nerd Font Mono.ttf         (Regular)
  Courier Prime Code Nerd Font Mono Medium.ttf
  Courier Prime Code Nerd Font Mono Bold.ttf
  Courier Prime Code Nerd Font Mono Italic.ttf
  -> Internal font family name is "Courier Prime Code Nerd Font Mono"
     (Medium is its own family "...Mono Medium"). PostScript names stay
     space-free ("CourierPrimeCodeNerdFontMono-*").
     Set terminals/editors to the family name (not the filename).


CHANGELOG
---------
2026-06-27

  Rebuilt the Code Nerd Font Mono family as hinted TTF + renamed it.
    - Problem: the OTF (CFF) build looked pixellated / "ugly" in Emacs on
      Windows. Cause = Emacs rasterizes via GDI, which renders unhinted CFF
      outlines poorly; terminals (DirectWrite) were unaffected. The OTFs
      also carried zero hinting tables.
    - Also: glyphs looked too small in the terminal. Cause = the Nerd patch
      inflated typo/hhea vertical metrics to 1797/-839 (em unchanged), so
      the line box grew and letters sat small in the cell.
    - Fix: fontforge CFF->quadratic (glyf) for all 4 weights; added
      gasp {65535:15} (smooth+gridfit at all sizes); restored typo/hhea to
      1421/-643 (win kept 1797/839 for icon clipping). Outlines, glyph set
      (mono, all NF icons), and weights are otherwise unchanged from the
      2026-06-25 OTF build. Per-glyph TT instructions were NOT added
      (autoInstr on ~11k glyphs is impractical; gasp grayscale carries it —
      revisit with ttfautohint if small sizes look soft).
    - Renamed family "CourierPrimeCode Nerd Font Mono" ->
      "Courier Prime Code Nerd Font Mono" to match the sibling families
      (Courier Prime, Courier Prime Sans). Emacs config updated to match.

2026-06-25

  Built one consolidated Courier Prime Code Nerd Font:
    - Base: the 3T1C/CourierPrimeCode fork, chosen after comparing every
      upstream fork by commits-ahead and inspecting the actual files (not
      star count). It carries the upstream v3.0318 outlines PLUS genuine
      Bold + Medium weights and Vietnamese glyphs the original never had.
    - Regular/Medium/Bold come from that fork (already patched with
      Nerd Fonts 3.4.0 — single-width "mono", current v3 icon codepoints,
      ~10,400 icons per face).
    - Italic was patched locally: upstream Courier Prime Code Italic
      v3.0318 + Nerd Fonts 3.4.0 (--complete --mono) via fontforge
      font-patcher, so the family is complete with a true italic.
    - All four normalized to one family: "CourierPrimeCode Nerd Font Mono".

  Standardized the whole Courier Prime collection:
    - Format: TTF-only families converted to OTF with
      fontforge (quadratic -> cubic). No native OTF exists for
      Medium/SemiBold/Sans at ANY source (upstream, all forks, fontain.org,
      Google Fonts, Adobe) — local conversion was the only path to OTF.
    - Filenames: Title Case with spaces.
    - Screenplay R/I/B/BI kept as-is. The on-disk OTFs (fontain.org re-cut,
      Mar 2025) are the ONLY native-OTF distribution and have broader
      coverage (397-398 codepoints) than the canonical v3.018 TTFs (383).
      The "v1.20x vs v3.018" gap is a FALSE signal: these are two
      separately-versioned re-cuts, not sequential releases.
    - Medium/SemiBold verified byte-identical (sha256) to the canonical
      quoteunquoteapps.com download, then converted to OTF.
    - Sans v3.020 (the only version that exists anywhere) converted to OTF.

  Removed (moved to _superseded/, recoverable):
    - Old variable-width Code Nerd Font build (Mar 2025, Regular+Italic
      only): "CourierPrimeCode Nerd Font.otf/.ttf" + Italic.
    - Orphan partial patch: "CourierPrimeSans NF Bold Italic.ttf"
      (1 of 4 styles) — dropped in favor of the Code Nerd Font.
    - Unpatched base: "Courier Prime Code.ttf" / "Italic.ttf" — the italic
      and regular now live (as a superset) inside the Code Nerd Font Mono.
    - All source TTFs, replaced by their OTF conversions.


SOURCES
-------
  Courier Prime / Sans / Code (upstream):  github.com/quoteunquoteapps
  Screenplay OTF re-cut:                   fontain.org/courier-prime
  Medium / SemiBold:                       quoteunquoteapps.com/courierprime
  Code Nerd Font base fork:                github.com/3T1C/CourierPrimeCode
  Nerd Fonts patcher (3.4.0):              github.com/ryanoasis/nerd-fonts


LINKS (merged from the old .url / .webloc bookmark files)
---------------------------------------------------------
  Courier Prime — home ("It's Courier, just better"):
    https://quoteunquoteapps.com/courierprime/
  Courier Prime — repo:        https://github.com/quoteunquoteapps/CourierPrime
  Courier Prime Code — repo:   https://github.com/quoteunquoteapps/CourierPrimeCode
  Courier Prime Sans — repo:   https://github.com/quoteunquoteapps/CourierPrimeSans
  Courier Prime Code — fork (Mono Nerd icons, Bold/Medium, .glyphs source):
    https://github.com/3T1C/CourierPrimeCode
  Screenplay OTF re-cut (updated .otf version):
    https://fontain.org/courier-prime/


RE-DOWNLOAD (if a master is ever lost)
--------------------------------------
  Medium / SemiBold:
    curl -fsSL -o cp-medium-semibold.zip \
      https://quoteunquoteapps.com/courierprime/downloads/courier-prime-medium-semi-bold.zip
  Sans (TTF master, then convert):
    curl -fsSL -o cp-sans.zip \
      https://quoteunquoteapps.com/courierprime/downloads/courier-prime-sans.zip
