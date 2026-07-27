#!/usr/bin/env python3
"""Apply the Courier Prime collection's canonical metadata standard to one face.

This is the single source of truth for how every .ttf in the collection is
named and metrically configured, so screenplay, Sans, and Code all group
correctly and share one predictable line rhythm.

Usage
-----
    harmonize.py <in.ttf> <out.ttf> <Family> <Subfamily> [--ribbi]

    Family     e.g. "Courier Prime", "Courier Prime Code", "Courier Prime Sans"
    Subfamily  e.g. "Regular", "Bold", "Italic", "Bold Italic", "Medium", "SemiBold"
    --ribbi    Pure four-style family (no weights beyond Regular/Bold/Italic/
               Bold Italic): omit the typographic (nameID 16/17) records, which
               are only needed to hold a family together once it exceeds RIBBI.

What it sets
------------
Names (Windows platform 3 + Mac platform 1, kept identical):
  - Typographic family/subfamily (16/17) = Family / Subfamily  [unless --ribbi]
  - Legacy family/subfamily (1/2): RIBBI styles stay in Family; a weight beyond
    RIBBI (Medium, SemiBold, ...) gets its own legacy family "Family Weight" so
    old four-slot apps still see a coherent Regular/Bold/Italic set.
  - Full name (4) and PostScript name (6) follow from Family + Subfamily.

Style bits, derived from Subfamily so they can never disagree with the name:
  - fsSelection REGULAR / BOLD / ITALIC, USE_TYPO_METRICS (on), WWS (unless --ribbi)
  - head.macStyle BOLD / ITALIC

Monospace: post.isFixedPitch = 1 and PANOSE proportion = Monospaced, because
every face is a fixed-pitch Courier derivative.

Vertical metrics — one line rhythm for the whole collection:
  - typo and hhea ascender/descender = 1600 / -700, lineGap 0  (1.123 em).
    This is Courier Prime v3's calibrated value; it clears the tallest accents
    (Latin text ink runs ~1.13-1.17 em) so lines never overlap, and it is just
    tight enough to stay dense. USE_TYPO_METRICS is on so it governs everywhere.
  - usWinAscent/Descent = the actual glyph bounding box (floored to 1900/800),
    so Nerd-icon glyphs — which reach far above text — are never clipped, while
    the clip box does not drive line height (USE_TYPO is on).

gasp {65535: 15}: grayscale + gridfit at every size, for clean Windows GDI /
Emacs-on-Windows antialiasing.
"""
import sys
from fontTools.ttLib import TTFont, newTable

# --- collection-wide constants ---------------------------------------------
# Courier Prime v3.018's own vertical metrics, applied uniformly to every face.
# Every family derives from that 2048-UPM design with the same baseline, so one
# metric set is both consistent and faithful to the original. Uniform typo AND
# uniform win means line height is identical in every renderer, whichever metric
# it reads: typo-aware apps get 1.123 em, legacy/GDI apps (incl. Emacs-on-
# Windows, which ignores USE_TYPO_METRICS and reads usWin) get one shared box.
TYPO_ASC, TYPO_DESC, TYPO_GAP = 1600, -700, 0   # 1.123 em unified line rhythm
WIN_ASC, WIN_DESC = 1900, 800                    # shared clip box (upstream's)
RIBBI = {"Regular", "Bold", "Italic", "Bold Italic"}

# fsSelection / macStyle bit positions
FS_ITALIC, FS_BOLD, FS_REGULAR = 1 << 0, 1 << 5, 1 << 6
FS_USE_TYPO, FS_WWS = 1 << 7, 1 << 8
MAC_BOLD, MAC_ITALIC = 1 << 0, 1 << 1


def plan_names(family, sub):
    """Resolve every name-table value from Family + Subfamily."""
    if sub in RIBBI:
        leg_fam, leg_sub = family, sub
    else:
        # A weight beyond RIBBI becomes its own legacy family so four-slot
        # apps see "Family Weight" / Regular instead of a fifth style they
        # cannot represent.
        weight = sub.replace(" Italic", "").strip()
        leg_fam = f"{family} {weight}"
        leg_sub = "Italic" if "Italic" in sub else "Regular"
    # Style bits describe the face's role within its legacy RIBBI family, so
    # derive them from leg_sub (always one of the four RIBBI values). Deriving
    # from the typographic subfamily would misread "SemiBold" as bold.
    bold = "Bold" in leg_sub
    italic = "Italic" in leg_sub
    full = family if sub == "Regular" else f"{family} {sub}"
    ps = f"{family.replace(' ', '')}-{sub.replace(' ', '')}"
    return dict(leg_fam=leg_fam, leg_sub=leg_sub, full=full, ps=ps,
                typo_fam=family, typo_sub=sub,
                bold=bold, italic=italic,
                regular=(leg_sub == "Regular"))


def main(inp, out, family, sub, ribbi=False):
    n = plan_names(family, sub)
    f = TTFont(inp)
    name, os2, hhea, head, post = f["name"], f["OS/2"], f["hhea"], f["head"], f["post"]

    # fsSelection USE_TYPO_METRICS/WWS (bits 7/8) are only honoured from OS/2
    # version 4 up. Versions 2-4 share a binary layout, so the bump is safe.
    if os2.version < 4:
        os2.version = 4

    def setn(nid, val):
        name.setName(val, nid, 3, 1, 0x409)   # Windows
        name.setName(val, nid, 1, 0, 0)        # Mac

    setn(1, n["leg_fam"]); setn(2, n["leg_sub"])
    setn(4, n["full"]);    setn(6, n["ps"])
    if ribbi:
        for nid in (16, 17):
            name.removeNames(nameID=nid)
    else:
        setn(16, n["typo_fam"]); setn(17, n["typo_sub"])

    # Style bits, rebuilt from scratch so they always match the names.
    fs = FS_USE_TYPO
    if not ribbi:
        fs |= FS_WWS
    if n["regular"]:
        fs |= FS_REGULAR
    if n["bold"]:
        fs |= FS_BOLD
    if n["italic"]:
        fs |= FS_ITALIC
    os2.fsSelection = fs
    head.macStyle = (MAC_BOLD if n["bold"] else 0) | (MAC_ITALIC if n["italic"] else 0)

    # Monospace signals.
    post.isFixedPitch = 1
    if hasattr(os2, "panose"):
        os2.panose.bProportion = 9   # PANOSE Latin-text proportion: Monospaced

    # Unified vertical metrics — identical on every face (see constants). A few
    # oversized Nerd icons in Code Bold/Medium (~0.14%, a 3T1C build quirk in
    # the weights that have no rebuildable source) reach past this box and are
    # clipped; they break the monospace cell regardless.
    os2.sTypoAscender, os2.sTypoDescender, os2.sTypoLineGap = TYPO_ASC, TYPO_DESC, TYPO_GAP
    hhea.ascent, hhea.descent, hhea.lineGap = TYPO_ASC, TYPO_DESC, TYPO_GAP
    os2.usWinAscent, os2.usWinDescent = WIN_ASC, WIN_DESC
    head.lowestRecPPEM = 8

    # Smooth GDI rendering at all sizes.
    if "gasp" not in f:
        g = newTable("gasp"); g.version = 1; g.gaspRange = {}; f["gasp"] = g
    f["gasp"].version = 1
    f["gasp"].gaspRange = {65535: 15}

    f.save(out)
    print(f"harmonized: {n['full']:28}  legacy={n['leg_fam']}/{n['leg_sub']}  "
          f"win={os2.usWinAscent}/{os2.usWinDescent}")


if __name__ == "__main__":
    a = sys.argv[1:]
    ribbi = "--ribbi" in a
    a = [x for x in a if x != "--ribbi"]
    main(a[0], a[1], a[2], a[3], ribbi=ribbi)
