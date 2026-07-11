# Third-party aircraft artwork

The SVG files in this directory (`b738.svg`, `a320.svg`, `a359.svg`,
`heavy_2e.svg`, `airliner.svg`, `jet_swept.svg`, `twin_small.svg`) contain
path data extracted from [tar1090](https://github.com/wiedehopf/tar1090)'s
`html/markers.js` (aircraft icon shapes used for its live ADS-B map), commit
[`c9e2c1b`](https://github.com/wiedehopf/tar1090/blob/c9e2c1b41cafc5fc9639daaa9a786323c529cfed/html/markers.js).
tar1090 itself credits the A320/B737-family shapes to contributor `pimlie`.

tar1090 is licensed under the **GNU General Public License v2.0 or later**;
a copy is included in this directory as `LICENSE`. Under GPL's copyleft
terms, these derived SVG files are therefore also GPLv2-or-later — this is
narrower than the rest of this repository, which carries no such
requirement elsewhere.

Fill colors and enclosing `<svg>`/viewBox wrapper were adapted here to fit
this project's dark theme; the path geometry (the actual aircraft shapes)
is unmodified from the source.
