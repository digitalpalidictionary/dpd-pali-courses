# Handoff — restyle the website and its icon (GitHub #10; draft, not yet a thread)

Status: **seed only.** No `spec.md` or `plan.md` exists. Nothing in the repo was changed for this except this file and `preview.png`.
Next step: run `/kamma:1-plan` with this file as input. Present the plan inline for approval (do not use a multiple-choice tool for the approval gate).
Written 2026-11-13. Everything under "Facts" and "Prototype" was measured or built on that date; nothing here is from memory.
**Revised 2026-11-14** after owner feedback on the first draft (robe-orange, hue 28): *"The orange is violent! Why not just use a variation of the light and dark palette in dpd-db/identity?"* Sections 3, 4.1, 4.5, 5, 6 and 10 now describe the blue variant. `preview.png` was regenerated from a fresh prototype build of the blue variant.
**Revised 2026-11-15** after owner feedback on the blue variant: *"i need to change the letters in the lable from "dpc" to "dpd" but keep the color. also on the prototipe site dark and light mode when we have dark blue background and the black letters - it is not very readable… not compleatley white since we use that already"*. Decision 1 therefore takes the `dpd` fallback (DPD's own letter paths, deeper disc) and decision 4 is settled: the tab bar moves to `--primary-alt` with pale-blue labels. Sections 3, 3.1, 3.2, 4.1-4.5, 5, 6, 8-10 updated; `preview.png` regenerated.

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

## 3. The idea: "DPD's own palette, one step deeper, same `dpd` logo"

One sentence: **keep DPD's palette exactly (the same light and dark backgrounds, text, grays and green) and move only the primary colour one step deeper, to DPD's own `--primary-alt`; keep DPD's `dpd` letterforms and put them on a deeper disc.**

The source palette is `dpd-db/identity/css/dpd-variables.css` (checked 2026-11-14: byte-identical to our `identity/dpd-variables.css`).

Why this fits the request:

- **Family.** The page backgrounds, text colours and font (Inter) are the same as DPD's. The primary colour is a colour DPD already uses (`#0077cc`, its pressed-button colour), so no new hue enters the family. The logo has the same construction: a disc in the primary colour with three bold lowercase Inter letters.
- **Distinct.** The disc is a deeper, darker blue than DPD's sky blue (`#0077cc` vs `#00b2ff`; luminance ratio 1.96 between the two discs), and its letters are `--light` in both schemes, where DPD's dark logo uses `--dark`. The tab bar is deeper still (`#0052a3`). At 16px both icons are blue discs holding `dpd`; you tell them apart by how dark the disc is and by the letter colour.
- **Calmer and more legible than DPD.** The tab bar's active label is 6.97:1 and its inactive labels 5.21:1 (DPD puts dark text on its brighter bar: 8.0:1). Light-mode links are 5.27:1 (DPD 4.24:1).
- **Cheap and reversible.** One small CSS file, two small assets, a few lines in the yaml generator. No change in `docs/`. The shared DPD files stay byte-identical to upstream, so they can still be re-synced.

Rejected: robe orange at hue 28 (first draft; owner: "violent"). Also rejected: a hue turn to cyan or teal, because the primary becomes neon and its contrast on `--light` falls to 1.2–1.4. Also rejected: muted blue `hsl(198, 60%, 45%)`, which reads as faded DPD rather than a sibling.

### 3.1 Palette

Rule: take `dpd-variables.css` unchanged. Override only the primary pair, and add two link tokens and one tab-label token.

| token | DPD | Courses | hex |
| --- | --- | --- | --- |
| `--light`, `--light-shade`, `--dark`, `--dark-shade` | — | **unchanged** (DPD's) | `#e5f7ff`, `#00121a`, … |
| `--primary` | `hsl(198, 100%, 50%)` | `hsl(205, 100%, 40%)` (= DPD `--primary-alt`) | `#0077cc` |
| `--primary-alt` | `hsl(205, 100%, 40%)` | `hsl(210, 100%, 32%)` | `#0052a3` |
| `--primary-text` | `hsl(205, 79%, 48%)` | **unchanged** | `#1a8bdb` |
| `--link-on-light` (new) | — | `hsl(205, 100%, 35%)` | `#0068b2` |
| `--link-on-dark` (new) | — | `hsl(198, 100%, 50%)` (= DPD `--primary`) | `#00b2ff` |
| `--on-primary-muted` (new) | — | `hsl(205, 65%, 83.3%)` | `#b9d9f0` |

`--primary-alt` is also the tab-bar background, and `--on-primary-muted` is the inactive tab label. In both schemes the active tab is `--light`.

Measured contrast (WCAG):

- `--light` on `--primary-alt` (the tab bar and the active tab): 6.97 (DPD's bar: 8.0, but with dark text on its brighter `#00b2ff`).
- `--on-primary-muted` on `--primary-alt` (inactive tab labels): 5.21.
- `--dark` on `--primary`: 4.10. After this change it is no longer used as text on blue anywhere (it was the inactive label in light mode and the active label in dark mode, and the dark logo's letters).
- `--primary-alt` on `--light`: 7.02 (DPD 4.24).
- `--link-on-light` on `--light`: 5.27. `--link-on-dark` on `--dark`: 8.05. Both pass AA (4.5).

**Why the tab bar has to darken.** On `#0077cc` the only labels that clear AA are the two extremes: pure white (4.66:1) and pure black (4.51:1). `--light` is 4.23:1, `--dark` is 4.10:1, and any pale tint is lower still (`#b9d9f0` is 3.16:1 there). Material also renders inactive links at `opacity: .7`, which drops `--dark` on `#0077cc` to 2.9:1 — worse than the 4.10:1 the earlier draft quoted. Since the owner rejected plain white and `--dark` on blue is the complaint, the bar itself has to move. On `#0052a3` the same pale blue reaches 5.21:1, so moving the bar to `--primary-alt` is what makes a readable, non-white label possible.

The link tokens exist because lessons are full of sutta-reference links, and `--primary` on `--light` alone (4.24) is just under AA.

Leave `--secondary` (green), the grays, the shadows and the `--freq*` tokens as they are.

### 3.2 Logo

- Same viewBox as DPD (`0 0 132.29167 132.29167`), a full disc in `--primary` (`#0077cc`).
- Letters `dpd`, Inter Bold, lowercase, as outline paths — DPD's own three letter paths, taken from `dpd-db/identity/logo/dpd-logo.svg` (no `<text>`, so no font is needed to display it).
- Wordmark ink width = 80.3% of the disc and ink centre at x = 66.146, y = 67.5: it is DPD's own wordmark, so the proportions come for free.
- One file, used in both schemes: letters `#e5f7ff` (`--light`). DPD's dark file inverts the letters to `--dark`; on our deeper disc that is 4.10:1 and is exactly the unreadable lettering the owner rejected. `--light` on `#0077cc` is 4.23:1 and stays legible at 16px. The disc colour, not the letter colour, carries the dark-mode difference.
- Favicon: the same logo as a 96×96 transparent PNG. PNG rather than SVG because older Safari does not show SVG favicons.

The complete logo, ready to save as `identity/assets/courses-logo.svg` (one line, 3215 bytes). The three letter paths are DPD's, with their original group transform:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 132.29167 132.29167"><title>dpd</title><circle cx="66.145835" cy="66.145835" r="66.145835" fill="#0077cc"/><g transform="matrix(0.89266763,0,0,0.89266763,5.5336428,8.0597213)" fill="#e5f7ff"><path d="m 19.218448,85.54734 q -4.682047,0 -8.176619,-2.341024 Q 7.5472575,80.865292 5.6133683,76.658235 3.713407,72.451178 3.713407,66.853078 q 0,-5.530245 1.9338892,-9.703374 1.967817,-4.207057 5.4284608,-6.548081 3.494572,-2.374952 8.074835,-2.374952 2.341024,0 4.308841,0.64463 1.967817,0.610702 3.5285,1.866033 1.560682,1.255332 2.71423,3.189221 h 0.03393 V 34.248385 H 39.71089 V 84.800926 H 29.871803 V 79.30461 h -0.03393 q -1.051765,2.0696 -2.646375,3.494571 -1.560682,1.391043 -3.596355,2.069601 -2.035673,0.678558 -4.376697,0.678558 z m 2.578519,-8.142692 q 2.544591,0 4.410625,-1.289259 1.899961,-1.323187 2.951725,-3.698139 1.051764,-2.374952 1.051764,-5.564172 0,-3.223149 -1.051764,-5.564173 -1.051764,-2.374951 -2.951725,-3.664211 -1.866034,-1.323187 -4.410625,-1.323187 -2.408879,0 -4.207057,1.255331 -1.798178,1.255332 -2.816014,3.596356 -0.983909,2.341023 -0.983909,5.699884 0,3.35886 0.983909,5.733811 1.017836,2.341024 2.816014,3.596356 1.798178,1.221403 4.207057,1.221403 z"/><path d="M 46.801815,98.98278 V 48.973085 h 9.873013 v 4.851687 h 0.101783 q 1.119621,-1.866034 2.680303,-3.087438 1.59461,-1.255331 3.596355,-1.866033 2.035673,-0.64463 4.342769,-0.64463 4.580264,0 8.040908,2.374952 3.494571,2.341024 5.42846,6.548081 1.967818,4.173129 1.967818,9.703374 0,5.5981 -1.93389,9.805157 -1.933889,4.207057 -5.394533,6.548081 -3.460643,2.341024 -8.176619,2.341024 -2.341023,0 -4.342768,-0.678558 -1.967817,-0.678558 -3.5285,-2.035673 -1.526755,-1.357115 -2.544591,-3.392788 H 56.810539 V 98.98278 Z M 64.749663,77.404648 q 2.442808,0 4.207057,-1.221403 1.798178,-1.255332 2.782087,-3.596356 1.017836,-2.374951 1.017836,-5.733811 0,-3.358861 -1.017836,-5.699884 -0.983909,-2.341024 -2.782087,-3.596356 -1.764249,-1.255331 -4.207057,-1.255331 -2.510663,0 -4.444552,1.323187 -1.899961,1.28926 -2.951726,3.664211 -1.017836,2.341024 -1.017836,5.564173 0,3.18922 1.017836,5.564172 1.051765,2.374952 2.951726,3.698139 1.933889,1.289259 4.444552,1.289259 z"/><path d="m 102.2739,85.54734 q -4.682049,0 -8.17662,-2.341024 -3.494572,-2.341024 -5.428461,-6.548081 -1.899962,-4.207057 -1.899962,-9.805157 0,-5.530245 1.93389,-9.703374 1.967817,-4.207057 5.42846,-6.548081 3.494572,-2.374952 8.074833,-2.374952 2.34103,0 4.30884,0.64463 1.96782,0.610702 3.5285,1.866033 1.56069,1.255332 2.71423,3.189221 h 0.0339 v -19.67817 h 9.9748 v 50.552541 h -9.83909 V 79.30461 h -0.0339 q -1.05177,2.0696 -2.64638,3.494571 -1.56068,1.391043 -3.59635,2.069601 -2.03568,0.678558 -4.3767,0.678558 z m 2.57852,-8.142692 q 2.54459,0 4.41062,-1.289259 1.89996,-1.323187 2.95173,-3.698139 1.05176,-2.374952 1.05176,-5.564172 0,-3.223149 -1.05176,-5.564173 -1.05177,-2.374951 -2.95173,-3.664211 -1.86603,-1.323187 -4.41062,-1.323187 -2.40888,0 -4.20706,1.255331 -1.798177,1.255332 -2.816014,3.596356 -0.983908,2.341023 -0.983908,5.699884 0,3.35886 0.983908,5.733811 1.017837,2.341024 2.816014,3.596356 1.79818,1.221403 4.20706,1.221403 z"/></g></svg>
```

If the owner picks other colours, only the two `fill` values change: disc = the new `--primary` hex; letters = the new text hex. The paths stay.

Because there is one file, `theme.logo` covers both schemes and the two `content: url(...)` swap rules are deleted (section 4.4). Nothing in the logo depends on the colour scheme.

## 4. Changes, file by file

Six items. Items 1-5 were built as a prototype (section 5). Item 6 is documentation.

### 4.1 New file `identity/courses-variables.css`

```css
/* DPD Pāḷi Courses palette: the DPD palette (dpd-variables.css) with the primary
   one step deeper: the course primary is DPD's own --primary-alt. Load after dpd-variables.css. */
:root {
  --primary: hsl(205, 100%, 40%);
  --primary-alt: hsl(210, 100%, 32%);
  /* link colours, one per scheme, both above 4.5:1 on their background */
  --link-on-light: hsl(205, 100%, 35%);
  --link-on-dark: hsl(198, 100%, 50%);
  /* inactive tab labels on the --primary-alt tab bar, 5.2:1 */
  --on-primary-muted: hsl(205, 65%, 83.3%);
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

- `identity/assets/courses-logo.svg` — section 3.2 (one file, both schemes).
- `identity/assets/courses-favicon.png` — 96×96 transparent PNG of that logo. Verified way to make it (macOS, Fish; paths are examples, run from the repo root after the SVG exists):

  ```fish
  echo "<body style='margin:0;background:transparent'><img src='identity/assets/courses-logo.svg' width=96 height=96 style='display:block'>" > temp/fav.html
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --default-background-color=00000000 --window-size=96,96 --screenshot=identity/assets/courses-favicon.png "file://"(pwd)"/temp/fav.html"
  ```

  Check with `file identity/assets/courses-favicon.png`; it must say `PNG image data, 96 x 96, 8-bit/color RGBA`. `temp/` is gitignored.

Why `identity/assets/` and not `docs/assets/`: `identity/` is the brand folder ("DPD CSS and JavaScript assets", README line 15); F12 shows it publishes to `assets/`; and it keeps `docs/` untouched (the repo's data-preservation rule concerns `docs/`). `docs/assets/images/` already exists and merges with it without conflict (seen in the prototype build).

### 4.3 `scripts/generate_mkdocs_yaml.py` — the `config` dict (lines ~126-142)

Four edits inside `'theme'` and one in `'extra_css'`:

1. Add `'logo': 'assets/courses-logo.svg',`
2. Add `'favicon': 'assets/courses-favicon.png',`
3. Add `'font': {'text': 'Inter'},` (fixes F7; same setting as DPD)
4. In both palette entries change `'primary': 'brown', 'accent': 'orange'` to `'primary': 'custom', 'accent': 'custom'` (same as DPD; removes the leftover Material brown, F6)
5. `'extra_css': ['dpd.css', 'dpd-variables.css', 'courses-variables.css', 'extra.css'],` — the new file must come **after** `dpd-variables.css`.

Then regenerate: `uv run python scripts/generate_mkdocs_yaml.py`. Do not hand-edit `mkdocs.yaml` (F11).

### 4.4 `identity/extra.css` — delete the logo swaps, retune the tabs

- Delete the two `.md-logo img { content: url("../assets/dpd-logo…"); … }` blocks (lines 58-63 and 153-158). With `theme.logo` set they are dead weight, and left in place they would hotlink DPD's logo (F4). They match nothing today only because `theme.logo` is unset (F2).
- Delete the four scheme-specific tab rules (lines 133-139 and 228-234) and put one block in the global section at the end of the file:

  ```css
  /* Navigation tabs, both schemes: --primary-alt bar, pale-blue inactive labels.
     Material dims inactive links to opacity .7; overridden so the label keeps its
     measured 5.2:1 contrast. */
  .md-tabs {
      background-color: var(--primary-alt);
  }
  .md-tabs__link {
      font-weight: 700;
      font-size: 0.9rem;
      color: var(--on-primary-muted);
      opacity: 1;
  }
  .md-tabs__link:hover,
  .md-tabs__item--active .md-tabs__link {
      color: var(--light);
  }
  ```

The old rules flipped active/inactive text between schemes (dark on blue in light mode, the reverse in dark mode), which is why both modes had an unreadable label. Change nothing else in the file: all other rules use `var(--…)` and follow the new palette automatically (49 `var(--primary|light|dark…)` uses; the only literal colours are black box-shadows).

### 4.5 Tests — new file `tests/test_restyle.py`

Data tests only, each failing for a different reason:

1. `identity/courses-variables.css` defines exactly `--primary`, `--primary-alt`, `--link-on-light`, `--link-on-dark` and `--on-primary-muted` with the section 3.1 values (parse `--name: value;` pairs), and does **not** redefine `--light`, `--light-shade`, `--dark` or `--dark-shade`. Those must keep coming from DPD.
2. Contrast: compute the WCAG ratio from the HSL values in that file; `--link-on-light` on `--light` ≥ 4.5, `--link-on-dark` on `--dark` ≥ 4.5, `--light` on `--primary-alt` ≥ 4.5 (the active tab) and `--on-primary-muted` on `--primary-alt` ≥ 4.5 (the inactive tabs).
3. `identity/assets/courses-logo.svg` parses as XML, has the DPD viewBox, one `<circle>` filled `#0077cc`, exactly three `<path>` letters inside one `<g fill="#e5f7ff">`, and no `<text>`.
4. `identity/extra.css` contains no `dpd-logo` and no `url("../assets/`; `.md-tabs` takes its background from `var(--primary-alt)`; `.md-tabs__link` uses `var(--on-primary-muted)` with `opacity: 1` and never `var(--dark)`.
5. In `scripts/generate_mkdocs_yaml.py`'s output, `courses-variables.css` comes after `dpd-variables.css` in `extra_css`, and `theme.logo` / `theme.favicon` point to files that exist under `identity/`. Read the generated `mkdocs.yaml` with `yaml.safe_load`; do not import the script (it runs at import time and writes the file).

Run only `uv run pytest tests/test_restyle.py -v`. Never run a bare `uv run pytest` (memory rule: it has caused memory blow-ups).

### 4.6 Documentation

- `README.md` line 15 (`identity/` description): mention the course palette override and the logo/favicon in `identity/assets/`.
- `kamma/tech.md` → the assets list near line 40: add `identity/courses-variables.css` and `identity/assets/`, and one sentence with the hue rule from section 3.1 and the instruction "never edit `dpd-variables.css`; it mirrors upstream".
- No script-registry entry is needed unless a regularly-run script is added (none is proposed).

## 5. Prototype (already built twice; proves the plan works)

Rebuilt 2026-11-15 for the `dpd` logo and the tab-bar fix (the previous rebuild was 2026-11-14 for the blue variant). Method: a throwaway copy of `identity/` plus the changes in 4.1-4.4. The config was loaded from the current `mkdocs.yaml` and given the 4.3 edits. `custom_dir`, `docs_dir` and the `hooks` paths were made absolute. The config was split into a light-only and a dark-only palette, so headless Chrome renders each scheme without a toggle. Each was built with `uv run mkdocs build -q -f <scratch>/mkdocs_<mode>.yaml`. The build ran from a scratch copy of `identity/`; the only repo files written were this file and `preview.png`.

`preview.png` (1340×1897) shows: section 1, the DPD logo next to the course logo at 16/24/32/64/120 px on DPD's light and dark backgrounds; section 2, the tab labels before and after; sections 3-4, `/bpc/class_4/1_review/` in light and dark.

Observed:

- The header shows one `#0077cc` disc with `dpd` letters in both schemes (no separate dark file).
- The tab bar renders `#0052a3`; inactive labels `#b9d9f0` (5.21:1), active label `#e5f7ff` (6.97:1), in both schemes. The before/after strip in section 2 shows the old 2.9:1 label next to the new one.
- `rel="icon"` points to `…/assets/courses-favicon.png` on root and nested pages (`assets/…` and `../../../assets/…`).
- `--md-text-font:"Inter"` and `data-md-color-primary="custom"` are in the HTML.
- Page background is DPD's `#e5f7ff` (light) / `#00121a` (dark); links are `#0068b2` (light) / `#00b2ff` (dark).
- Both builds finished with no output under `-q` (no warnings).

Not checked in the prototype: the search box (it does not render from `file://`), mobile width, the nav drawer logo, PDFs.

## 6. Decisions for the owner (ask during planning; recommendation first)

1. **Logo: settled 2026-11-15 — `#0077cc` disc with DPD's own `dpd` letters.** The owner asked for `dpd` and for the disc colour to stay; the inverted-disc option is off the table. The dark-letter variant is dropped (4.10:1 on the deeper disc was exactly the unreadable lettering complained about); one file with `--light` letters serves both schemes.
2. **Primary: `hsl(205, 100%, 40%)` = DPD's `--primary-alt` (recommended).** Rejected: robe orange (owner, 2026-11-14: "violent"); cyan/teal hue turns (neon, 1.2–1.4:1 on light); muted `hsl(198, 60%, 45%)` (reads as faded DPD).
3. **PDFs: leave as they are for now (recommended), or restyle too?** To restyle PDFs, add `"identity/courses-variables.css"` after `dpd-variables.css` in `scripts/generate_pdfs.py` (lines 671-676) and in `tests/test_generate_pdfs.py:195`. Effect: PDF links change from `#00b2ff` to `#0077cc` on white. The `--md-typeset-a-color` rules do nothing in PDFs. Recommended as a separate later step because it changes every released PDF and needs the PDF checks in `kamma/tech.md`.
4. **Tab bar: settled 2026-11-15 — `#0052a3` with `#b9d9f0` inactive / `#e5f7ff` active, the same in both schemes.** The owner rejected "completely white" for the labels; on `#0077cc` the only light colour that passes is white itself (4.66:1) and the only dark one is pure black (4.51:1), so the bar had to darken. Alternative considered and dropped: keep `#0077cc` and accept ~4.2:1 with `--light`.
5. **Layout (F10).** Recommended: no layout change. The request is about look and icon; tabs and the small header are deliberate.

## 7. Verification steps for the thread

1. `uv run python scripts/generate_mkdocs_yaml.py`, then `uv run mkdocs build` — must finish without new warnings. (The usual local route is `./scripts/cl/pali-build-website`; read it before running, it also runs the preprocessing scripts, which may modify files in `docs/`.)
2. `uv run mkdocs serve`, open `http://127.0.0.1:8000`, and check in **both** light and dark mode:
   - home page, `/bpc/class_4/1_review/` (right-aligned reference links), `/bpc/class_6/4_subst/` (paradigm tables), one `bpc_key` page;
   - header logo, tab labels (readable in both modes), tab icon, search box and results panel, footnote pop-up (hover a footnote number), the nav drawer at phone width (logo appears there too).
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
- Use the DPD name and wordmark only as a sibling of the same project. Decision 1 is "keep `dpd`", so `identity/assets/courses-logo.svg` reuses DPD's three letter paths; do not copy DPD's SVG file wholesale — the repo file is rebuilt around a `<circle>` and a `<g fill>` with a new disc colour.

## 9. Files the thread will touch (expected)

- new: `identity/courses-variables.css`, `identity/assets/courses-logo.svg`, `identity/assets/courses-favicon.png`, `tests/test_restyle.py`
- edit: `scripts/generate_mkdocs_yaml.py`, `identity/extra.css` (delete 4 blocks, add 1), `README.md`, `kamma/tech.md`
- only if decision 3 = restyle PDFs: `scripts/generate_pdfs.py`, `tests/test_generate_pdfs.py`

Draft commit message: `Related to #10 restyle website: course palette, dpd logo and favicon`

## 10. Not done / not verified

- Owner rejected the orange draft (2026-11-14) and asked for `dpd` letters plus readable tab labels (2026-11-15). The owner has not yet seen or approved this revision or the new `preview.png`.
- The reading of the owner's comment ("a variation of the light and dark palette") as "keep DPD's palette, deepen only the primary" is an interpretation. Confidence 7/10.
- The 16px tab-icon distinction from DPD (lighter vs darker blue disc, light vs dark letters) was judged only from `preview.png`, not in a real browser tab strip next to DPD.
- The letters are now DPD's own paths, so the earlier "older Inter" mismatch no longer applies. The disc colour is the only difference at large sizes.
- No check of images inside `docs/` for baked-in colours that might clash with the deeper-blue tab bar (less likely now than with orange).
- Mobile layout, search panel and footnote pop-up colours were not looked at in the prototype.
- PDF and DOCX output were not built.
- Whether the DPD project owner wants to be told about the sibling logo: not asked.

## 11. Automatic light/dark mode ("A" toggle) — copied from the study-tools thread

Added 2026-11-16 at the owner's request. Source: `/Users/deva/Documents/sasanarakkha/study-tools/kamma/archive/20261116_website_restyle/` (`plan.md` Phase 5, tasks 5.1 and 5.8; `kamma/tech.md` "Automatic scheme" in that repo). Not yet tried in this repo; the Material version here is 9.7.1 (study-tools used 9.7.6), so re-check the points below.

### 11.1 Requirement

Light/dark mode must follow the browser/OS setting automatically (at least in Safari), and the visitor must always be able to return to "follow the system".

### 11.2 Why the current toggle is not enough

- Our palette already has `media: (prefers-color-scheme: light|dark)` entries, so the OS setting is used on a first visit.
- Material saves the toggle choice in `localStorage` (`__palette`, see `material/templates/partials/javascripts/palette.html`). After one click the saved choice wins over the OS forever, and a 2-state toggle has no way back to "follow the system".
- Fix (Material's own): a third palette entry with `media: "(prefers-color-scheme)"` and no `scheme`, which is the automatic mode, with the `material/brightness-auto` icon (shown as "A").

### 11.3 Change (in `scripts/generate_mkdocs_yaml.py`, the `theme.palette` list; `mkdocs.yaml` is generated, F11)

Add this entry **first** in the list:

```yaml
- media: "(prefers-color-scheme)"
  primary: custom
  accent: custom
  toggle:
    icon: material/brightness-auto
    name: Switch to light mode
```

Then change the dark entry's `toggle.name` to `Switch to system preference`. Leave the light entry unchanged. (`primary: custom` / `accent: custom` is already item 4 of section 4.3; the new entry needs it too, otherwise the body starts as `indigo` until the JS switches it.) In `generate_mkdocs_yaml.py` this is a Python dict, so write the same keys as dict entries.

Behaviour: the toggle cycles auto → light → dark → auto.

### 11.4 Verification (from the study-tools thread)

- `uv run python -c "import yaml;p=yaml.safe_load(open('mkdocs.yaml'))['theme']['palette'];print(len(p),[e['media'] for e in p])"` → `3 ['(prefers-color-scheme)', '(prefers-color-scheme: light)', '(prefers-color-scheme: dark)']`
- After `uv run mkdocs build`: `site/index.html` contains `data-md-color-media="(prefers-color-scheme)"` as the first palette input.
- Headless Chrome, fresh profile: with `--force-dark-mode` the home page body has `data-md-color-scheme="slate"`; without it, `default`.
- Owner check in Safari: the system setting is followed; the toggle cycles auto → light → dark; if an old 2-state choice sticks, clear the site data once (stale `__palette` in `localStorage`).
- Add a test to `tests/test_restyle.py`: the generated palette has three entries, the first with media `(prefers-color-scheme)`, no `scheme`, and icon `material/brightness-auto`.

### 11.5 Settled: same behaviour as the study-tools thread

Owner decision 2026-11-16: use exactly the behaviour described above. "A" (automatic) is the default on a first visit. After that Material remembers the visitor's last choice in `localStorage` (`__palette`), so a refresh keeps the chosen mode. No extra JS that resets to "A" on refresh. (The owner's earlier remark that every refresh goes to "A" was a mistake and is withdrawn.)

### 11.6 Files this adds to section 9

`scripts/generate_mkdocs_yaml.py` (palette entry) and `tests/test_restyle.py` (one more test); also one line in `kamma/tech.md` under the palette note.
