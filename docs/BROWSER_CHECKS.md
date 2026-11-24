# Browser checks

## November 19 source revision

In the browser, the home page displayed all six topic member lists. Selecting `(황환철)` opened the supplied profile, and the Multi-Robot Systems link returned to the matching Research section. The automated checker also passed on the root and `/cora` builds with 32 pages, five program details, 34 people, 22 topic assignments and 80 bibliography records.

## Earlier checks on the November draft

Checked at desktop viewport 1363 × 936 and a 390 × 844 mobile iframe viewport.

- Homepage: CORA hero, typography, affiliations, social links and highlights render; retained navigation and main content width visually inspected.
- Papers (updated 5 November 2026): all 79 bibliography entries render. Combining keyword `BiC-MPPI`, year 2024, and type Preprint returns one. A nonsense keyword shows the no-results state. Clear resets all three controls and restores all 79 entries. An older-paper query combining Wiener, 2012 and Journal also returns one. The Google Scholar link exactly matches the user's supplied profile URL.
- Mobile Papers (390 × 844): search, year and type controls fit without horizontal overflow (document width and scroll width both 390 px). `TransformerHyMPC` + 2025 + Conference returns one result with its Oral presentation label and Conference program link readable.
- People: PI portrait links to the detailed profile; profile renders the verified name, department and contact destinations.
- Research: both displayed figures load, with source captions; no desktop horizontal overflow.
- Mobile: collapsed navigation expands, includes all seven links, and navigates to Contact; menu collapses after navigation; Contact has no horizontal overflow.
- Contact/email and external scholarly links are destinations only. No messages, applications or external login submissions were sent during testing.

Automated static validation is recorded separately in VALIDATION.json. GitHub Actions deployment is provided but was not executed against a user GitHub repository in this task.

## People update — 6 November 2026

- Desktop People: 33 supplied entries, four populated groups, supplied portraits and links rendered in the retained CLeAR frame.
- Search `embedded` returned two people; Korean-name query `김지원` returned one alumnus; unmatched query showed the empty state; Clear restored all 33 records.
- SungJun Park profile: portrait, role, email, two education records, research interests and three publications with both source link types rendered correctly.
- Mobile iframe (390 × 844): People and Papers had no horizontal overflow; navigation expanded and reached Papers.
- Mobile Papers combined `BiC-MPPI`, 2024, Preprint returned one of 79 publications.
- All 17 current profiles and 16 alumni names are also checked by `scripts/verify.py`; all source images are preserved byte-for-byte.
- Source fields are from the supplied archive; external email addresses and publication destinations were not contacted or reverified.

## Projects update — 6 November 2026

- Desktop homepage: eight navigation links fit on one line; Projects opens the new page. Homepage includes a project overview link.
- Projects: all five requested sections render with bilingual descriptions, verified metadata, focus items, source links and related-page links.
- Mobile iframe (390 × 844): section shortcuts wrap, titles and metadata remain readable; document client width and scroll width are both 375 px (15 px scrollbar), with no horizontal overflow.
- AX Graduate School shortcut scrolls to the expected section without hiding its title under the fixed navigation.
- Mobile menu expands to all eight links; choosing Projects returns to the page top and collapses the menu.
- Root and GitHub project-prefix builds pass static validation: 27 pages, five projects, 33 people, 17 profiles and 79 publications.

## Research update — 6 November 2026

- Six exact user-specified headings and 22 participant entries were checked against the rendered section-by-section lists, including all three parenthesized names.
- Desktop: two-column numbered jump navigation and bilingual research descriptions render within the retained CLeAR frame.
- Mobile iframe (390 × 844): jump navigation becomes one column; heading, participant and topic text wrap without horizontal overflow (375 px client/scroll width plus 15 px scrollbar).
- Safe Learning for pHRI jump link reaches the expected section; the heading and parenthesized participant names are visible below the fixed header.
- The five previous research anchors remain available. Home and Projects links point to the new topic structure.
