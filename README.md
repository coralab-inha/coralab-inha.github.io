# CORA Lab — CLeAR-based homepage

Computational Robotics and Autonomy Lab, Inha University.

This site adapts the previously reproduced CLeAR website into CORA's homepage. It retains the reference's 800px desktop container, Open Sans typography, white background, Bootstrap navigation, portrait layout, bibliography style, and pale-blue news panel. Original CLeAR content and service destinations have been replaced with CORA content.

## Local preview

```sh
python3 scripts/build.py
python3 scripts/verify.py dist
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. On Windows use `py` instead of `python3`. Python 3 standard libraries are sufficient; no Ruby, Jekyll, npm or dependency installation is required.

## GitHub Pages

Upload the package contents to your own repository, including `.github/`. Select **Settings → Pages → Source → GitHub Actions**, then push to `main` or manually run **Deploy CORA Lab to GitHub Pages**. The workflow supports both account sites and project subpaths.

See [한국어 편집·배포 안내](docs/SETUP_KO.md).

## Editing

- `data/verified-facts.json`: lab details, PI, homepage highlights and their source URLs.
- `data/publications.json`: current Papers catalog, source provenance, CV reconciliation and version grouping.
- `data/projects.json`: five research and education programs, dates, descriptions and source notes.
- `scripts/render_projects.py`: Projects directory and individual program pages.
- `data/people.json`: supplied roster, categories, education, research interests and selected publications.
- `assets/people/`: supplied member portraits.
- `scripts/render_people.py`: People directory and profile rendering.
- `data/content.json`: research descriptions, teaching topics and open-source links.
- `templates/layout.html`: shared navigation and page frame.
- `scripts/build.py`: page rendering and path handling.
- `assets/style.css`: original template CSS, retained unchanged.
- `assets/cora.css`: small CORA-specific additions.
- `assets/`: CORA artwork, public faculty portrait and research figures.

Research lists six topics and 22 participant assignments on both the homepage and the Research page. Names link to their supplied profiles when available. Each linked profile also lists its research topic.

People includes the 33 supplied records and the requested alumni entry for 정민찬, for 34 directory entries. Seventeen current members have individual profiles. The 17 alumni appear by name.

Papers lists 80 bibliography entries spanning 2010–2026, including the 79 November draft records and the 2021 HVAC magazine article retained from the previous lab bibliography. The [Google Scholar refresh guide](docs/PUBLICATIONS_UPDATE.md) covers export, version matching and verification. A complete comparison with the current Scholar profile is still pending.

Original MIT template license and third-party dependency notices are retained. See [content sources](docs/CONTENT_SOURCES.md) and `vendor/licenses/`.

The Projects page covers Korea–Japan collaboration (SafeRL-HRC), NRF Mid-career research, BK21 FOUR, the AX Graduate School and regional intelligence talent development. See `docs/PROJECTS_SOURCES.md` for verification and editorial limits.
