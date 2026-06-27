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
  - Code Nerd Font Mono — built in this repo (see BUILD).

Font-level change history: courier-prime+FONTLOG.txt.


CONTENTS (14 faces — all hinted TTF)
---------------------------------------------
Courier Prime (screenplay) — fontain.org TTF re-cut:
  Courier Prime Regular.ttf
  Courier Prime Bold.ttf
  Courier Prime Italic.ttf
  Courier Prime Bold Italic.ttf

Courier Prime community weights — by M. Babek Aliassa
  (family "Courier Prime", weights Medium / SemiBold):
  Courier Prime Medium.ttf
  Courier Prime SemiBold.ttf

Courier Prime Sans — v3.020:
  Courier Prime Sans Regular.ttf
  Courier Prime Sans Italic.ttf
  Courier Prime Sans Bold.ttf
  Courier Prime Sans Bold Italic.ttf

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


BUILD / UPDATE (Code Nerd Font Mono only)
-----------------------------------------
Screenplay, Sans, Medium and SemiBold are upstream TTFs used as-is (see
RE-DOWNLOAD). Only the Code Nerd Font Mono family is built here. Rebuild it
when the Nerd Fonts patcher gains new icons / codepoints:

    bash build/build-code-nerd.sh

Pipeline (build/build-code-nerd.sh + build/postprocess.py):
  - Regular + Italic: 3T1C .glyphs -> fontmake -> ttfautohint -> Nerd Fonts
    patch (--complete --mono). Fully reproducible from source.
  - Bold + Medium: NO published source exists — 3T1C never released masters
    (only Regular/Italic .glyphs are anywhere in the fork's git history).
    They are re-hinted from 3T1C's pre-patched TTFs, so they only gain new
    patcher icons when 3T1C re-patches upstream.
  - postprocess.py restores vertical metrics (typo/hhea 1421/-643; usWin
    1797/839 kept tall so icons aren't clipped), sets gasp {65535:15}
    (smooth+gridfit at all sizes), and applies the canonical family name.

Tools (install if missing — don't work around):
    pip install fontmake glyphsLib fonttools
    scoop install ttfautohint fontforge
    Nerd Fonts font-patcher lives under _assets/scripts/nerd-font-patcher.


SOURCES
-------
  Courier Prime / Sans / Code (upstream):  github.com/quoteunquoteapps
  Screenplay TTF re-cut:                   fontain.org/courier-prime
  Medium / SemiBold:                       quoteunquoteapps.com/courierprime
  Code Nerd Font base fork:                github.com/3T1C/CourierPrimeCode
  Nerd Fonts patcher:                      github.com/ryanoasis/nerd-fonts


LINKS (merged from the old .url / .webloc bookmark files)
---------------------------------------------------------
  Courier Prime — home ("It's Courier, just better"):
    https://quoteunquoteapps.com/courierprime/
  Courier Prime — repo:        https://github.com/quoteunquoteapps/CourierPrime
  Courier Prime Code — repo:   https://github.com/quoteunquoteapps/CourierPrimeCode
  Courier Prime Sans — repo:   https://github.com/quoteunquoteapps/CourierPrimeSans
  Courier Prime Code — fork (Mono Nerd icons, Bold/Medium, .glyphs source):
    https://github.com/3T1C/CourierPrimeCode
  Screenplay re-cut (TTF / OTF / UFO downloads):
    https://fontain.org/courier-prime/


RE-DOWNLOAD (if a master is ever lost) — all native TTF
-------------------------------------------------------
  Screenplay (R/B/I/BI):
    curl -fsSL -o cp.ttf.zip \
      https://fontain.org/courier-prime/export/ttf/courier-prime.ttf.zip
  Medium / SemiBold:
    curl -fsSL -o cp-medium-semibold.zip \
      https://quoteunquoteapps.com/courierprime/downloads/courier-prime-medium-semi-bold.zip
  Sans (R/I/B/BI):     github.com/quoteunquoteapps/CourierPrimeSans  (ttf/)
  Code Nerd Font Mono: bash build/build-code-nerd.sh  (see BUILD)
