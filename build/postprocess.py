#!/usr/bin/env python3
"""Post-process a patched Courier Prime Code Nerd Font Mono face.

Applies the two corrections the raw Nerd-Fonts patch needs, plus canonical
naming:

  1. Vertical metrics: the patcher inflates typo/hhea ascender+descender to
     make room for tall icons, which makes normal text look small in the cell.
     Restore them to Courier Prime's native 1421/-643; keep usWin* tall
     (1797/839) so icon glyphs are not clipped.
  2. gasp {65535: 15}: grayscale + gridfit at all sizes, so Windows GDI
     (and thus Emacs-on-Windows) antialiases cleanly.
  3. Names: family "Courier Prime Code Nerd Font Mono" (Medium is its own
     family "... Medium"); PostScript names stay space-free.

Usage: postprocess.py <in.ttf> <out.ttf> <Regular|Bold|Italic|Medium>
"""
import sys
from fontTools.ttLib import TTFont, newTable

FAM = "Courier Prime Code Nerd Font Mono"
# weight -> (family, subfamily, full name, PostScript name)
NAMES = {
    "Regular": (FAM,           "Regular", FAM,           "CourierPrimeCodeNerdFontMono-Regular"),
    "Bold":    (FAM,           "Bold",    FAM + " Bold", "CourierPrimeCodeNerdFontMono-Bold"),
    "Italic":  (FAM,           "Italic",  FAM + " Italic", "CourierPrimeCodeNerdFontMono-Italic"),
    "Medium":  (FAM + " Medium", "Regular", FAM + " Medium", "CourierPrimeCodeNerdFontMono-Medium"),
}
TYPO_ASC, TYPO_DESC = 1421, -643   # native Courier Prime line metrics
WIN_ASC, WIN_DESC   = 1797, 839    # clipping box (keep tall for icons)


def main(inp, out, weight):
    fam, sub, full, ps = NAMES[weight]
    f = TTFont(inp)
    nm = f["name"]

    def setn(i, v):
        nm.setName(v, i, 3, 1, 0x409)  # Windows
        nm.setName(v, i, 1, 0, 0)      # Mac

    setn(1, fam); setn(2, sub); setn(4, full); setn(6, ps)
    setn(16, fam); setn(17, sub)

    os2, hhea, head = f["OS/2"], f["hhea"], f["head"]
    hhea.ascent, hhea.descent, hhea.lineGap = TYPO_ASC, TYPO_DESC, 0
    os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = TYPO_ASC, TYPO_DESC, 0
    os2.usWinAscent, os2.usWinDescent = WIN_ASC, WIN_DESC
    os2.fsSelection &= ~(1 << 7)       # USE_TYPO_METRICS off
    head.lowestRecPPEM = 8

    if "gasp" not in f:
        g = newTable("gasp"); g.version = 1; g.gaspRange = {}; f["gasp"] = g
    f["gasp"].version = 1
    f["gasp"].gaspRange = {65535: 15}

    f.save(out)
    print(f"postprocessed {weight}: {full}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
