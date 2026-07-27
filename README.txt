COURIER PRIME FONTS — master set
=================================

This folder holds the master copies of the Courier Prime font families.

Standard format: hinted TrueType (.ttf). Filenames: Title Case with spaces.
TTF is what every upstream source ships natively, and TTF + bytecode/gasp
hinting renders cleanly everywhere — including Emacs-on-Windows (GDI), where
unhinted CFF/OTF looks pixellated.

License: SIL Open Font License 1.1 (OFL) for all families. See
courier-prime+LICENSE.txt.

Credits:
  - Courier Prime (screenplay) — Alan Dague-Greene, for John August /
    Quote-Unquote Apps.
  - Medium / SemiBold weights — M. Babek Aliassa.
  - Code (Nerd icons) — built in this repo (see BUILD).

Font-level change history: courier-prime+FONTLOG.txt.


THREE FAMILIES (14 faces — all hinted TTF)
------------------------------------------
The collection is three separate font families that share the "Courier Prime"
name prefix. They are distinct designs, not weights of one another, so each is
its own family (the same pattern as Source Sans / Serif / Code, or IBM Plex
Sans / Serif / Mono). Within a family, weights beyond Regular/Bold/Italic/Bold
Italic are held together by the typographic family name; see METADATA STANDARD.

Courier Prime — screenplay slab monospace (quoteunquoteapps v3.018):
  Courier Prime Regular.ttf
  Courier Prime Bold.ttf
  Courier Prime Italic.ttf
  Courier Prime Bold Italic.ttf
  Courier Prime Medium.ttf       (community weight, M. Babek Aliassa)
  Courier Prime SemiBold.ttf     (community weight, M. Babek Aliassa)
  -> family "Courier Prime": Regular / Medium / SemiBold / Bold + italics

Courier Prime Sans — v3.020:
  Courier Prime Sans Regular.ttf
  Courier Prime Sans Italic.ttf
  Courier Prime Sans Bold.ttf
  Courier Prime Sans Bold Italic.ttf
  -> family "Courier Prime Sans" (four-style RIBBI)

Courier Prime Code — base v3.0318 + Nerd Fonts 3.4.0 icons
  (single-width "mono"; ~11k glyphs incl. all NF icon sets):
  Courier Prime Code.ttf         (Regular)
  Courier Prime Code Medium.ttf
  Courier Prime Code Bold.ttf
  Courier Prime Code Italic.ttf
  -> family "Courier Prime Code": Regular / Medium / Bold / Italic.
     The short family name (no "Nerd Font Mono" suffix) fits terminals and
     editors that limit the family field. Point them at the family name, not
     the filename.


METADATA STANDARD (build/harmonize.py)
--------------------------------------
Every face is passed through build/harmonize.py, the single source of truth
for the collection's naming and metrics:

  - Family grouping: each family's faces share one typographic family name
    (nameID 16). A weight beyond RIBBI (Medium, SemiBold) also gets its own
    legacy family (nameID 1) so four-slot apps still see a coherent
    Regular/Bold/Italic set. This is why the OS shows exactly three families,
    not five, and why every weight lands under the right one.
  - Monospace: post.isFixedPitch = 1 and PANOSE proportion = Monospaced.
  - One line rhythm across the whole collection: every face carries Courier
    Prime v3.018's own vertical metrics, identical on all 14 — typo and hhea
    ascender/descender = 1600 / -700, lineGap 0 (1.123 em), USE_TYPO_METRICS
    on, and usWinAscent/Descent = 1900 / 800. Uniform typo AND uniform win
    means line height is consistent in every renderer, whichever metric it
    reads: typo-aware apps (browsers, macOS, DirectWrite) get 1.123 em;
    legacy/GDI apps that ignore USE_TYPO_METRICS — including Emacs-on-Windows,
    which takes line height from usWin — get one shared box. So faces mix like
    a single designed family (bold within a paragraph, a code block in prose)
    with no line-height jump. The trade: a few oversized Nerd icons in Code
    Bold/Medium (~0.14%, a 3T1C build quirk in the two weights with no
    rebuildable source), plus the Vietnamese stacked-tone capitals in those
    same weights, reach past the 1900/800 box and are clipped; both already
    break the monospace cell. Normal accents and all other text fit.
  - gasp {65535: 15}: grayscale + gridfit at all sizes for clean GDI output.

Re-apply the standard to any face (e.g. a freshly downloaded vendor TTF):
    python build/harmonize.py <in.ttf> <out.ttf> "<Family>" "<Subfamily>" [--ribbi]
  Use --ribbi for a pure four-style family (Sans) to omit the typographic
  (nameID 16/17) records.


BUILD / UPDATE (Code only)
--------------------------
Screenplay, Sans, Medium and SemiBold are upstream TTFs, harmonized as-is (see
RE-DOWNLOAD). Only Courier Prime Code is built here. Rebuild it when the Nerd
Fonts patcher gains new icons / codepoints:

    bash build/build-code-nerd.sh

Pipeline (build/build-code-nerd.sh + build/harmonize.py):
  - Regular + Italic: 3T1C .glyphs -> fontmake -> ttfautohint -> Nerd Fonts
    patch (--complete --mono). Fully reproducible from source.
  - Bold + Medium: NO published source exists — 3T1C never released masters
    (only Regular/Italic .glyphs are anywhere in the fork's git history).
    They are re-hinted from 3T1C's pre-patched TTFs, so they only gain new
    patcher icons when 3T1C re-patches upstream.
  - harmonize.py then applies the METADATA STANDARD above.

Tools (install if missing — don't work around):
    pip install fontmake glyphsLib fonttools
    scoop install ttfautohint fontforge
    Nerd Fonts font-patcher lives under _assets/scripts/nerd-font-patcher.


SOURCES
-------
  Courier Prime / Sans / Code (upstream):  github.com/quoteunquoteapps
  Medium / SemiBold:                       quoteunquoteapps.com/courierprime
  Code Nerd Font base fork:                github.com/3T1C/CourierPrimeCode
  Nerd Fonts patcher:                      github.com/ryanoasis/nerd-fonts


RE-DOWNLOAD (if a master is ever lost) — native TTF, then harmonize
-------------------------------------------------------------------
  Screenplay (R/B/I/BI), Courier Prime v3.018:
    github.com/quoteunquoteapps/CourierPrime   (fonts/ttf/)
  Medium / SemiBold:
    curl -fsSL -o cp-medium-semibold.zip \
      https://quoteunquoteapps.com/courierprime/downloads/courier-prime-medium-semi-bold.zip
  Sans (R/I/B/BI):     github.com/quoteunquoteapps/CourierPrimeSans   (ttf/)
  Code:                bash build/build-code-nerd.sh   (see BUILD)
  Then run each downloaded TTF through build/harmonize.py (see METADATA
  STANDARD) so its names and metrics match the collection.


LINKS
-----
  Courier Prime — home ("It's Courier, just better"):
    https://quoteunquoteapps.com/courierprime/
  Courier Prime — repo:        https://github.com/quoteunquoteapps/CourierPrime
  Courier Prime Code — repo:   https://github.com/quoteunquoteapps/CourierPrimeCode
  Courier Prime Sans — repo:   https://github.com/quoteunquoteapps/CourierPrimeSans
  Code fork (Mono Nerd icons, Bold/Medium, .glyphs source):
    https://github.com/3T1C/CourierPrimeCode
