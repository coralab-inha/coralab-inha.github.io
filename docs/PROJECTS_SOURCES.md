# Projects: content sources and editorial scope

Updated 6 November 2026.

The visible website includes the five categories requested by the lab PI. This is a lab project/program overview, not an award registry. English headings (except the SafeRL-HRC project name) and focus summaries are editorial translations or summaries. Detailed funding amounts, unpublished results and internal project proposals are not included.

| Item | Evidence used | Scope and limitations |
| --- | --- | --- |
| Korea–Japan / SafeRL-HRC | Supplied `coralab-inha.github.io-main.zip`, `_data/projects.yml`; JST SICORP Korea page | Korean title and 2025.10.01–2028.09.30 dates come from supplied source. JST identifies Kwangki Kim, Takamitsu Matsubara, Inha, NAIST, official English title and FY2025–FY2028 program period. |
| NRF Mid-career | Supplied `_data/projects.yml`; user-provided award context | Exact current-source dates 2025.03.01–2028.02.29 replace earlier shorthand 2025–2027. `funding` in the supplied YAML contains dates, not a grant amount. GPU path optimization/trajectory-estimation description follows supplied project content. |
| BK21 FOUR | Inha ECE official program page | ICT-미래자동차 융합 교육연구단; NRF; 2020.09–2027.08 is the overall group period. User request identifies the lab’s participation. CORA focus summaries reflect existing lab research and teaching, not an official work package or an individual funding allocation. |
| AX Graduate School | Inha ECE official selection news, Inha AIX faculty directory | Inha 인공지능혁신대학원 selected in 2026, support through 2031. Official faculty page lists Kim as 교육과정위원장, 로봇AI 융합 도메인; robotics/control/optimization/Physical AI. This is not the separate proposed AX manufacturing/on-device workforce consortium. |
| Regional intelligence | MSIT/IITP official program notice on IRIS | General program purpose only. Lab-specific consortium, region, subproject, PI role and dates remain unconfirmed. A secondary aggregator showed a Kyungnam program; official evidence did not establish a CORA connection. The Inha/Incheon program was also not assumed to be the lab’s exact grant. The 2026 national call link is background, not an assertion of a 2026 award. |

## Primary public sources

- JST: https://www.jst.go.jp/inter/english/program_e/sicorp_e/korea.html
- Inha BK21: https://www.inhaece.co.kr/page/biz02
- Inha AX selection: https://www.inhaece.co.kr/board/view?bd_id=news01&main=1&wr_id=550
- Inha AX faculty: https://aix.inha.ac.kr/about/members/faculty/
- MSIT/IITP regional-intelligence program: https://www.iris.go.kr/contents/retrieveBsnsAncmView.do?ancmId=020254&ancmPrg=ancmPre

These links were retrieved during this update. Funding figures, contact-person private details, participant admissions promises and company-specific internal project plans are omitted.

## Directory and detail pages (19 November 2026)

Edit `data/projects.json` to update the directory and all five detail pages together. `program_label` supplies the English program name. The Korean jump label and the project’s English and Korean titles are separate fields. Keep each `id` stable. The directory uses `/projects/#<id>` for bookmarks and `/projects/<id>/` for the full program page. `metadata`, `focus`, `links` and `related_links` appear on the detail page. Use `scope_ko` for a brief visitor-facing clarification where a description is limited to a national program.
