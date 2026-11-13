# Handoff — restyle the website and its icon (GitHub #10; draft, not yet a thread)

Status: **seed only.** No `spec.md` or `plan.md` exists. Nothing in the repo was changed for this except this file.
Next step: run `/kamma:1-plan` with this file as input. Present the plan inline for approval (do not use a multiple-choice tool for the approval gate).
Written 2026-11-13. Everything under "Facts" and "Prototype" was measured or built on that date; nothing here is from memory.

## 1. The request

GitHub issue #10 "restyle website" (label: enhancement), https://github.com/digitalpalidictionary/dpd-pali-courses/issues/10

> Restyle the website with the Claude
> - including restyling of the icon

Owner's comment on the issue:

> The original DPD site is available at https://digitalpalidictionary.github.io. The dpd-pali-course site should resemble it while remaining distinct. Its logo must also be similar yet different, so users can tell them apart in a browser while recognizing a shared family.

Two requirements follow:

1. **Family:** the course site must look like a sibling of the DPD docs site.
2. **Distinct:** a user with both sites open must be able to tell them apart, including by the browser-tab icon.

## 2. Facts about the current state

Read these before planning. Several are surprising.

| # | Fact | How it was checked |
| --- | --- | --- |
| F1 | **The two sites have the same tab icon.** Both serve Material's default `assets/images/favicon.png` (48×48, identical md5 `370ef648…`). Neither sets `theme.favicon`. | `curl` both files, `md5` |
| F2 | **The course site has no logo image.** The header shows Material's default "reader" icon as inline `<svg>`. `theme.logo` is not set in `scripts/generate_mkdocs_yaml.py`. | HTML of the live home page |
| F3 | **The logo rules in `identity/extra.css` are dead code.** Lines 58-63 and 153-158 set `.md-logo img { content: url("../assets/dpd-logo.svg") }`, but there is no `<img>` to match (F2). | same |
| F4 | If F2 were fixed without fixing F3, the `content: url("../assets/…")` rule would take over and **hotlink the DPD logo from the parent site** (`digitalpalidictionary.github.io/assets/dpd-logo.svg`). It would 404 on `mkdocs serve`. No logo file exists anywhere in this repo. | `find` for `*logo*`; URL resolution |
| F5 | `identity/dpd-variables.css` is **byte-identical** to the DPD site's `stylesheets/dpd-variables.css`. The course site therefore uses exactly DPD's colours: hue 198 sky blue. | `diff` |
| F6 | The palette in `generate_mkdocs_yaml.py` says `primary: brown, accent: orange`. `extra.css` overrides almost all of it with the blue variables, but **link colour still comes from Material's brown palette** (`#795548` light, `#c1775c` dark). Result today: blue tab bar with brown links. | screenshot of `/bpc/class_4/1_review/` |
| F7 | **The course site does not load Inter.** DPD sets `theme.font.text: Inter`. The course site sets no font, so Material downloads Roboto, and `identity/dpd.css` line 2 (`body { font-family: "Inter", "Noto Sans Devanagari", sans-serif }`) then overrides it with a font that was never loaded. Visitors without Inter installed get the system sans-serif. | `--md-text-font` in both pages' HTML |
| F8 | The DPD logo is a disc in `--primary` (`#00b2ff`) holding the letters "dpd" in Inter Bold, lowercase, as outlines. Letters are `--light` (`#e5f7ff`) in the light file and `--dark` (`#00121a`) in the dark file. ViewBox `0 0 132.29167 132.29167`. The wordmark's ink is 80.3% of the disc width. | the two SVG files |
| F9 | DPD swaps light/dark logo with CSS `content: url(...)` under `[data-md-color-scheme="default"]` / `["slate"]`. The course `extra.css` copied that mechanism. | DPD `stylesheets/extra.css` |
| F10 | Layout differences that already exist and are the owner's earlier choices: course site has `navigation.tabs` (sticky), a 26px "tiny" header, 1rem body text, no footer. DPD has a normal header, sidebar-only nav, `navigation.footer`. | both configs, `extra.css` |
| F11 | `mkdocs.yaml` is **generated and gitignored**. Every theme setting must be changed in `scripts/generate_mkdocs_yaml.py` (the `config` dict, around lines 126-142). | `.gitignore`, script |
| F12 | Files in `identity/` (the theme `custom_dir`) are copied to the site root. That is why `extra_css: ['dpd.css', …]` works. A file `identity/assets/x.svg` is published as `assets/x.svg`. | prototype build |
| F13 | PDFs use the same CSS: `scripts/generate_pdfs.py` lines 671-676 list `dpd-pdf-fonts.css`, `dpd-variables.css`, `dpd.css`, `extra.css`. `tests/test_generate_pdfs.py:195` repeats that list. In PDFs `dpd.css` line 45 (`a { color: var(--primary) }`) colours links. | source |
| F14 | `scripts/update_css.py` copies each CSS file onto itself (source and target paths are the same in `tools/paths.py`). It is a no-op today. `tests/test_ssg_scripts.py::test_update_css` checks a path (`tools/ssg/stylesheets/`) that no longer exists. Leave both alone; they are out of scope. | source |
| F15 | Versions: mkdocs 1.6.1, mkdocs-material 9.7.1. `fonttools` is already a project dependency. | `uv run python -c …`, `pyproject.toml` |
| F16 | The deploy workflow (`.github/workflows/deploy_site.yaml`) triggers on `docs/**`, `identity/**`, `scripts/**`. A change in `identity/` deploys on push to `main`. | workflow file |

DPD contrast numbers, for comparison with the proposal (WCAG ratio): `--primary` on `--light` 2.17; `--primary` on `--dark` 8.00; `--primary-alt` on `--light` 4.23. Current brown links: 5.95 (light), 5.50 (dark).

## 3. The idea: "same mould, robe-orange hue, dpc"

One sentence: **keep DPD's design system exactly and change one parameter, the hue, from sky blue to robe orange; and build the logo the same way as DPD's, with the letters `dpc`.**

Why this fits the request:

- **Family.** DPD's whole palette is one hue (198) at fixed saturation and lightness steps. Rotating only the hue keeps every lightness and saturation relationship, so the two sites read as two colourways of one design. The font becomes the same (Inter). The logo is the same construction: a disc in the primary colour with three bold lowercase Inter letters.
- **Distinct.** Orange is close to the complement of sky blue, so the two tab icons cannot be confused, also for most colour-blind users. The letters differ too: `dpd` (Digital Pāḷi Dictionary) becomes `dpc` (**D**PD **P**āḷi **C**ourses, the site's own name).
- **Not arbitrary.** Orange is the colour of the robe. The config already asks for `brown`/`orange`, and the links are already brown-orange (F6). The restyle finishes a direction the site half has.
- **Cheap and reversible.** One small CSS file, three small assets, a few lines in the yaml generator. No change in `docs/`. The shared DPD files stay byte-identical to upstream, so they can still be re-synced.

### 3.1 Palette

Rule: take `dpd-variables.css`; replace hue 198 with **28** and hue 205 with **21**; keep saturation and lightness. (DPD's alternate colour is 7 degrees deeper into blue; ours is 7 degrees deeper into red.)

| token | DPD | Courses | hex |
| --- | --- | --- | --- |
| `--light` | `hsl(198, 100%, 95%)` | `hsl(28, 100%, 95%)` | `#fff1e5` |
| `--light-shade` | `hsl(198, 100%, 93%)` | `hsl(28, 100%, 93%)` | `#ffecdb` |
| `--dark` | `hsl(198, 100%, 5%)` | `hsl(28, 100%, 5%)` | `#1a0c00` |
| `--dark-shade` | `hsl(198, 100%, 7%)` | `hsl(28, 100%, 7%)` | `#241100` |
| `--primary` | `hsl(198, 100%, 50%)` | `hsl(28, 100%, 50%)` | `#ff7700` |
| `--primary-alt` | `hsl(205, 100%, 40%)` | `hsl(21, 100%, 40%)` | `#cc4700` |
| `--primary-text` | `hsl(205, 79%, 48%)` | `hsl(21, 79%, 48%)` | — |
| `--link-on-light` (new) | — | `hsl(21, 100%, 33%)` | `#a83b00` |
| `--link-on-dark` (new) | — | `hsl(28, 100%, 60%)` | `#ff9233` |

Measured contrast for hue 28: `--primary` on `--light` 2.40 (DPD 2.17); `--primary` on `--dark` 7.20 (DPD 8.00); `--primary-alt` on `--light` 4.24 (DPD 4.23). So hue 28 reproduces DPD's contrast structure almost exactly. Hues 35 and 42 were also tried: they look more yellow and drop to 2.02 and 1.69 on light, so 28 is the recommendation.

The two link tokens are new because lessons are full of sutta-reference links, and a link in `--primary` on `--light` would be 2.40:1. `--link-on-light` gives 5.76:1 and `--link-on-dark` gives 8.58:1. Both pass WCAG AA (4.5).

Leave `--secondary` (green), the grays, the shadows and the `--freq*` tokens as they are.

### 3.2 Logo

- Same viewBox as DPD (`0 0 132.29167 132.29167`), a full disc in `--primary` (`#ff7700`).
- Letters `dpc`, Inter Bold, lowercase, as outline paths (no `<text>`, so no font is needed to display it).
- Wordmark ink width = 80.3% of the disc, the same proportion as DPD. Ink centre at x = 66.146 (the disc centre), y = 67.5 (same as DPD).
- Light file: letters `#fff1e5` (`--light`). Dark file: letters `#1a0c00` (`--dark`). The disc is the same in both. This mirrors F8.
- Favicon: the light logo as a 96×96 transparent PNG. PNG rather than SVG because older Safari does not show SVG favicons.

The complete light logo, ready to save as `identity/assets/dpc-logo.svg` (one line, 2562 bytes). It was generated from Inter Bold 4.001 with fontTools; the three letters are one path:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 132.29167 132.29167"><title>dpc</title><circle cx="66.145835" cy="66.145835" r="66.145835" fill="#ff7700"/><path fill="#fff1e5" d="M26.353 83.751Q22.606 83.751 19.575 81.804Q16.544 79.856 14.788 76.094Q13.031 72.331 13.031 66.885Q13.031 61.293 14.846 57.545Q16.662 53.797 19.677 51.923Q22.693 50.049 26.324 50.049Q29.106 50.049 30.95 50.986Q32.795 51.923 33.937 53.299Q35.079 54.675 35.635 55.963H35.928V39.566H44.712V83.194H36.075V77.953H35.635Q35.05 79.271 33.893 80.603Q32.737 81.935 30.892 82.843Q29.047 83.751 26.353 83.751ZM29.077 76.694Q31.302 76.694 32.883 75.464Q34.464 74.235 35.284 72.024Q36.104 69.813 36.104 66.856Q36.104 63.869 35.299 61.688Q34.493 59.506 32.912 58.291Q31.331 57.076 29.077 57.076Q26.763 57.076 25.197 58.335Q23.63 59.594 22.84 61.79Q22.049 63.986 22.049 66.856Q22.049 69.725 22.854 71.951Q23.66 74.176 25.226 75.435Q26.793 76.694 29.077 76.694ZM52.208 95.434V50.459H60.846V55.963H61.256Q61.871 54.675 62.998 53.299Q64.125 51.923 65.97 50.986Q67.815 50.049 70.596 50.049Q74.227 50.049 77.243 51.923Q80.259 53.797 82.06 57.545Q83.861 61.293 83.861 66.885Q83.861 72.331 82.104 76.094Q80.347 79.856 77.331 81.804Q74.315 83.751 70.538 83.751Q67.873 83.751 66.029 82.843Q64.184 81.935 63.027 80.603Q61.871 79.271 61.256 77.953H60.992V95.434ZM67.844 76.694Q70.128 76.694 71.695 75.435Q73.261 74.176 74.066 71.951Q74.871 69.725 74.871 66.856Q74.871 63.986 74.066 61.79Q73.261 59.594 71.709 58.335Q70.157 57.076 67.844 57.076Q65.59 57.076 64.008 58.291Q62.427 59.506 61.607 61.688Q60.787 63.869 60.787 66.856Q60.787 69.813 61.622 72.024Q62.456 74.235 64.038 75.464Q65.619 76.694 67.844 76.694ZM104.65 83.839Q99.701 83.839 96.115 81.716Q92.528 79.593 90.581 75.801Q88.633 72.009 88.633 66.973Q88.633 61.878 90.581 58.086Q92.528 54.294 96.115 52.172Q99.701 50.049 104.65 50.049Q107.549 50.049 110.008 50.81Q112.468 51.571 114.371 52.977Q116.274 54.382 117.504 56.403Q118.734 58.423 119.202 60.941L111.033 62.464Q110.77 61.175 110.213 60.165Q109.657 59.155 108.866 58.438Q108.076 57.72 107.036 57.34Q105.997 56.959 104.738 56.959Q102.395 56.959 100.799 58.218Q99.204 59.477 98.398 61.732Q97.593 63.986 97.593 66.944Q97.593 69.842 98.398 72.097Q99.204 74.352 100.799 75.64Q102.395 76.928 104.738 76.928Q105.997 76.928 107.051 76.533Q108.105 76.138 108.925 75.391Q109.745 74.644 110.301 73.59Q110.857 72.536 111.092 71.219L119.261 72.712Q118.792 75.318 117.563 77.353Q116.333 79.388 114.43 80.852Q112.526 82.316 110.052 83.077Q107.578 83.839 104.65 83.839Z"/></svg>
```

`identity/assets/dpc-logo-dark.svg` is the same file with the single string `fill="#fff1e5"` replaced by `fill="#1a0c00"`. Nothing else differs (checked with `diff`).

If the owner picks another hue, only the `fill` values change: disc = the new `--primary` hex; letters = the new `--light` / `--dark` hex. The path stays.

## 4. Changes, file by file

Six items. Items 1-5 were built as a prototype (section 5). Item 6 is documentation.

### 4.1 New file `identity/courses-variables.css`

```css
/* DPD Pāḷi Courses palette: the DPD palette (dpd-variables.css) with the hue
   turned from sky blue (198/205) to robe orange (28/21). Load after dpd-variables.css. */
:root {
  --light: hsl(28, 100%, 95%);
  --light-shade: hsl(28, 100%, 93%);
  --dark: hsl(28, 100%, 5%);
  --dark-shade: hsl(28, 100%, 7%);
  --primary: hsl(28, 100%, 50%);
  --primary-alt: hsl(21, 100%, 40%);
  --primary-text: hsl(21, 79%, 48%);
  /* link colours, one per scheme, both above 4.5:1 on their background */
  --link-on-light: hsl(21, 100%, 33%);
  --link-on-dark: hsl(28, 100%, 60%);
}
body[data-md-color-scheme="default"] {
  --md-typeset-a-color: var(--link-on-light);
}
body[data-md-color-scheme="slate"] {
  --md-typeset-a-color: var(--link-on-dark);
}
```

Do **not** edit `identity/dpd-variables.css` or `identity/dpd.css`. They stay identical to upstream DPD; the override file is the only place the course colours live. The `body[...]` prefix is deliberate: it out-ranks Material's own `[data-md-color-scheme=…]` rule that sets `--md-typeset-a-color`.

### 4.2 New assets in a new folder `identity/assets/`

- `identity/assets/dpc-logo.svg` — section 3.2.
- `identity/assets/dpc-logo-dark.svg` — section 3.2.
- `identity/assets/dpc-favicon.png` — 96×96 transparent PNG of the light logo. Verified way to make it (macOS, Fish; paths are examples, run from the repo root after the SVG exists):

  ```fish
  echo "<body style='margin:0;background:transparent'><img src='identity/assets/dpc-logo.svg' width=96 height=96 style='display:block'>" > temp/fav.html
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --default-background-color=00000000 --window-size=96,96 --screenshot=identity/assets/dpc-favicon.png "file://"(pwd)"/temp/fav.html"
  ```

  Check with `file identity/assets/dpc-favicon.png`; it must say `PNG image data, 96 x 96, 8-bit/color RGBA`. `temp/` is gitignored.

Why `identity/assets/` and not `docs/assets/`: `identity/` is the brand folder ("DPD CSS and JavaScript assets", README line 15); F12 shows it publishes to `assets/`; and it keeps `docs/` untouched (the repo's data-preservation rule concerns `docs/`). `docs/assets/images/` already exists and merges with it without conflict (seen in the prototype build).

### 4.3 `scripts/generate_mkdocs_yaml.py` — the `config` dict (lines ~126-142)

Four edits inside `'theme'` and one in `'extra_css'`:

1. Add `'logo': 'assets/dpc-logo.svg',`
2. Add `'favicon': 'assets/dpc-favicon.png',`
3. Add `'font': {'text': 'Inter'},` (fixes F7; same setting as DPD)
4. In both palette entries change `'primary': 'brown', 'accent': 'orange'` to `'primary': 'custom', 'accent': 'custom'` (same as DPD; removes the leftover Material brown, F6)
5. `'extra_css': ['dpd.css', 'dpd-variables.css', 'courses-variables.css', 'extra.css'],` — the new file must come **after** `dpd-variables.css`.

Then regenerate: `uv run python scripts/generate_mkdocs_yaml.py`. Do not hand-edit `mkdocs.yaml` (F11).

### 4.4 `identity/extra.css` — two lines

- line 59: `content: url("../assets/dpd-logo.svg");` → `content: url("assets/dpc-logo.svg");`
- line 154: `content: url("../assets/dpd-logo-dark.svg");` → `content: url("assets/dpc-logo-dark.svg");`

The URL is relative to `extra.css`, which sits at the site root, so there is no `../`. This is what swaps the logo in dark mode (F9) and removes the hotlink trap (F4). Change nothing else in the file: all other rules use `var(--…)` and follow the new palette automatically (49 `var(--primary|light|dark…)` uses; the only literal colours are black box-shadows).

### 4.5 Tests — new file `tests/test_restyle.py`

Data tests only, each failing for a different reason:

1. `identity/courses-variables.css` defines every token in section 3.1's "Courses" column (parse `--name: value;` pairs).
2. Contrast: compute the WCAG ratio from the HSL values in that file; `--link-on-light` on `--light` ≥ 4.5 and `--link-on-dark` on `--dark` ≥ 4.5.
3. Both logo SVGs parse as XML, have the DPD viewBox, and their `<path d>` strings are equal (only the fill differs).
4. `identity/extra.css` contains no `dpd-logo` and no `url("../assets/`.
5. In `scripts/generate_mkdocs_yaml.py`'s output, `courses-variables.css` comes after `dpd-variables.css` in `extra_css`, and `theme.logo` / `theme.favicon` point to files that exist under `identity/`. Read the generated `mkdocs.yaml` with `yaml.safe_load`; do not import the script (it runs at import time and writes the file).

Run only `uv run pytest tests/test_restyle.py -v`. Never run a bare `uv run pytest` (memory rule: it has caused memory blow-ups).

### 4.6 Documentation

- `README.md` line 15 (`identity/` description): mention the course palette override and the logo/favicon in `identity/assets/`.
- `kamma/tech.md` → the assets list near line 40: add `identity/courses-variables.css` and `identity/assets/`, and one sentence with the hue rule from section 3.1 and the instruction "never edit `dpd-variables.css`; it mirrors upstream".
- No script-registry entry is needed unless a regularly-run script is added (none is proposed).

## 5. Prototype (already built once; proves the plan works)

A throwaway copy of `identity/` plus the changes in 4.1-4.4 was built with `uv run mkdocs build -f <scratch>/mkdocs.yaml` into a scratch folder. The repo was not touched (`git status` stayed clean). The scratch folder is session-temporary and will be gone; rebuild it if a preview is needed.

Observed in the built site and in headless-Chrome screenshots of `/bpc/class_4/1_review/` (light and dark):

- The header shows the orange `dpc` disc; dark mode shows the dark-letter variant.
- `<link rel="icon" href="…/assets/dpc-favicon.png">` is present on root and nested pages.
- `--md-text-font:"Inter"` and `data-md-color-primary="custom"` are in the HTML.
- Page background is cream `#fff1e5` (light) / warm near-black `#1a0c00` (dark); the tab bar is orange; links are dark orange (light) / light orange (dark).
- The build succeeded with no new warnings.

Not checked in the prototype: the search box (it does not render from `file://`), mobile width, the nav drawer logo, PDFs.

## 6. Decisions for the owner (ask during planning; recommendation first)

1. **Letters: `dpc` (recommended) or keep `dpd`?** `dpc` = the site's initials, and it differs from DPD in shape as well as colour. Keeping `dpd` and changing only the colour is the fallback; then only the two `fill` values in DPD's own SVGs change.
2. **Hue: 28 robe orange (recommended).** Alternatives measured: 35 and 42 (yellower, weaker contrast). Another candidate with a family argument is DPD's own `--secondary` green (hue 158), but green on a light green page gave link contrast under 3.6 even at 30% lightness, and blue/green tab icons are harder to tell apart.
3. **PDFs: leave blue for now (recommended), or restyle too?** To restyle PDFs, add `"identity/courses-variables.css"` after `dpd-variables.css` in `scripts/generate_pdfs.py` (lines 671-676) and in `tests/test_generate_pdfs.py:195`. Effect: PDF links change from `#00b2ff` to `#ff7700` on white. The `--md-typeset-a-color` rules do nothing in PDFs. Recommended as a separate later step because it changes every released PDF and needs the PDF checks in `kamma/tech.md`.
4. **Tab bar.** It stays a full-saturation band, now orange. The active tab's text is `--light` on `--primary` (2.40:1; today 2.17:1 on blue). Recommended: leave as is in this thread, since it is inherited behaviour; note it as a possible follow-up.
5. **Layout (F10).** Recommended: no layout change. The request is about look and icon; tabs and the small header are deliberate.

## 7. Verification steps for the thread

1. `uv run python scripts/generate_mkdocs_yaml.py`, then `uv run mkdocs build` — must finish without new warnings. (The usual local route is `./scripts/cl/pali-build-website`; read it before running, it also runs the preprocessing scripts, which may modify files in `docs/`.)
2. `uv run mkdocs serve`, open `http://127.0.0.1:8000`, and check in **both** light and dark mode:
   - home page, `/bpc/class_4/1_review/` (right-aligned reference links), `/bpc/class_6/4_subst/` (paradigm tables), one `bpc_key` page;
   - header logo, tab icon, search box and results panel, footnote pop-up (hover a footnote number), the nav drawer at phone width (logo appears there too).
3. Open the DPD site in the next tab and confirm the two tab icons are clearly different.
4. Python validation for every changed or new `.py` file (CLAUDE.md, mandatory): `uv run ruff check --fix <file>`, `uv run ruff format <file>`, `uv run pyright <file>`, `uv run --with pyrefly pyrefly check --min-severity warn <file>`, `uv run pytest tests/test_restyle.py -v`.
5. `git status` must show no change under `docs/`. If step 1 used the preprocessing scripts and they touched `docs/`, report it to the owner; do not revert on your own.
6. Ask the owner to look at the result in a real browser. Colour and logo approval is a human judgement.

## 8. Constraints to carry into the spec

- **No change in `docs/`.** This thread should not need one.
- Clean-markdown rule: no styling goes into `.md` files; everything is CSS, config or assets.
- Do not edit `identity/dpd-variables.css` or `identity/dpd.css`.
- Do not touch `scripts/update_css.py`, `tools/paths.py` or `test_update_css` (F14).
- Hindi (`docs/bpc_hi*`) is unaffected and stays unpublished.
- Do not commit, push or deploy. The owner commits. A push to `main` deploys the site (F16), so the owner should see a local build first.
- `kamma/threads/20261113_br_markup/` belongs to another thread; leave it alone.
- Use the DPD name and logo construction only as a sibling of the same project; do not copy DPD's logo file into this repo unless decision 1 goes to "keep `dpd`".

## 9. Files the thread will touch (expected)

- new: `identity/courses-variables.css`, `identity/assets/dpc-logo.svg`, `identity/assets/dpc-logo-dark.svg`, `identity/assets/dpc-favicon.png`, `tests/test_restyle.py`
- edit: `scripts/generate_mkdocs_yaml.py`, `identity/extra.css` (2 lines), `README.md`, `kamma/tech.md`
- only if decision 3 = restyle PDFs: `scripts/generate_pdfs.py`, `tests/test_generate_pdfs.py`

Draft commit message: `Related to #10 restyle website: course palette, dpc logo and favicon`

## 10. Not done / not verified

- Owner has not seen or approved the hue, the letters or any screenshot.
- The DPD logo was drawn with an older Inter than the 4.001 used for `dpc` (letter proportions differ by a few percent). Not visible at header or tab size; say so if the owner compares them enlarged.
- No check of images inside `docs/` for baked-in blue that might clash with the orange page.
- Mobile layout, search panel and footnote pop-up colours were not looked at in the prototype.
- PDF and DOCX output were not built.
- Whether the DPD project owner wants to be told about the sibling logo: not asked.
