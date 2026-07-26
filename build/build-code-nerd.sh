#!/usr/bin/env bash
# Rebuild "Courier Prime Code" (Regular, Italic, Bold, Medium) with Nerd icons.
#
# Re-run this when the Nerd Fonts patcher updates (new icon sets / codepoints).
#
# Reproducibility note:
#   - Regular + Italic are built fully from source: the 3T1C .glyphs masters ->
#     fontmake -> ttfautohint -> Nerd Fonts patch (--complete --mono).
#   - Bold + Medium have NO published source. 3T1C never released masters for
#     them (confirmed: only Regular/Italic .glyphs ever existed in the fork's
#     git history). They exist only as 3T1C's pre-patched TTFs, so we re-hint
#     those with ttfautohint. They only pick up new patcher icons when 3T1C
#     re-patches upstream.
#
# Requirements (install if missing — don't work around):
#   - python with: fontmake, glyphsLib, fonttools   (pip install fontmake)
#   - ttfautohint                                    (scoop install ttfautohint)
#   - fontforge                                      (scoop install fontforge)
#   - the Nerd Fonts font-patcher (path below)
set -euo pipefail

# --- tools / paths (override via env) ---
ASSETS="${ASSETS:-$HOME/Drive/OneDrive - MSFT/Assets/fonts/_assets}"
PATCHER="${PATCHER:-$ASSETS/scripts/nerd-font-patcher/font-patcher}"
TTFAUTOHINT="${TTFAUTOHINT:-$HOME/scoop/apps/ttfautohint/current/ttfautohint.exe}"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${WORK:-$HERE/_work}"
OUT="${OUT:-$(cd "$HERE/.." && pwd)}"   # repo root: drops masters next to README
FORK_RAW="https://raw.githubusercontent.com/3T1C/CourierPrimeCode/master"

mkdir -p "$WORK/src" "$WORK/stage"
cd "$WORK"
fetch() { curl -fsSL -o "$2" "$1"; }

echo ">> fetching sources from 3T1C/CourierPrimeCode"
fetch "$FORK_RAW/glyphs/Courier%20Prime%20Code.glyphs"          "src/Courier Prime Code.glyphs"
fetch "$FORK_RAW/glyphs/Courier%20Prime%20Code%20Italic.glyphs" "src/Courier Prime Code Italic.glyphs"
fetch "$FORK_RAW/ttf/nerd-fonts/CourierPrimeCodeNerdFont-Bold.ttf"   "src/fork-Bold.ttf"
fetch "$FORK_RAW/ttf/nerd-fonts/CourierPrimeCodeNerdFont-Medium.ttf" "src/fork-Medium.ttf"

# output filename per weight (Regular is bare; others are suffixed)
outfile() {
  case "$1" in
    Regular) echo "$OUT/Courier Prime Code.ttf" ;;
    *)       echo "$OUT/Courier Prime Code $1.ttf" ;;
  esac
}

# harmonize.py applies the collection metadata standard: canonical family name
# "Courier Prime Code", unified vertical metrics, monospace flags, gasp, and a
# usWin box sized from the patched glyph bounds so Nerd icons are never clipped.
harmonize() { python "$HERE/harmonize.py" "$1" "$(outfile "$2")" "Courier Prime Code" "$2"; }

build_from_source() {  # <glyphs-file> <weight>
  local g="$1" w="$2"
  echo ">> [$w] fontmake -> ttfautohint -> patch (--complete --mono)"
  python -m fontmake -g "$g" -o ttf --output-dir "stage/fm-$w"
  local base; base="$(ls "stage/fm-$w"/*.ttf | head -1)"
  "$TTFAUTOHINT" "$base" "stage/base-$w.ttf"
  rm -rf "stage/patched-$w"; mkdir -p "stage/patched-$w"
  fontforge -script "$PATCHER" --complete --mono --quiet --outputdir "stage/patched-$w" "stage/base-$w.ttf"
  harmonize "$(ls "stage/patched-$w"/*.ttf | head -1)" "$w"
}

rehint_fork() {        # <weight>
  local w="$1"
  echo ">> [$w] re-hint 3T1C pre-patched TTF (no source available)"
  "$TTFAUTOHINT" "src/fork-$w.ttf" "stage/bm-$w.ttf"
  harmonize "stage/bm-$w.ttf" "$w"
}

build_from_source "src/Courier Prime Code.glyphs"        Regular
build_from_source "src/Courier Prime Code Italic.glyphs" Italic
rehint_fork Bold
rehint_fork Medium

echo ">> done -> $OUT"
echo "   Install (Windows, per-user): copy each .ttf into"
echo "   %LOCALAPPDATA%\\Microsoft\\Windows\\Fonts and add an HKCU font-registry"
echo "   entry, or just double-click each in Explorer and click Install."
