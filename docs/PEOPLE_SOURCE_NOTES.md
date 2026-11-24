# People data source and editorial notes

## Source

Imported from the user-supplied `coralab-inha.github.io-main.zip`, using `_data/people.yml` and the YAML front matter in `_people/*.md`. Profile images were copied byte-for-byte from `assets/img/people/`. No roster facts were inferred from filenames, outside sources, or previous discussions.

`data/people.json` retains source values and filename order. It includes the original category definitions, metadata, header, and every profile field. The only changed source field is `image`, relocated to `/assets/people/<original-filename>`; `source_image` records its original value. Added `source_filename` records the source file and `id` removes each numeric filename prefix. The professor's ID remains `kwangki-kim` for compatibility with the existing site; his original title `KwangKi Kim` is preserved, and `display_name: Kwang-Ki K. Kim` supports the existing public spelling.

## Original roster (33 records)

- Professor: 1
- Ph.D. Students: 7
- M.S. Students: 9
- Alumni: 16
- Total: 33

The source defines Postdoctoral Researchers and Undergraduate Students categories but contains no profiles in those categories. Do not imply that a missing category has members.

All 17 current members have a supplied individual photo; all 16 alumni reference the shared `default.png`. The source People page renders alumni as a name list. Photos vary in resolution (as low as 80 × 107 pixels); avoid large display sizes or invented replacement images.

## Updated roster and research links

The current archive contains 34 People records. 정민찬 is the seventeenth alumnus, added by name at the lab's request. The 17 current-member profiles retain the original portraits.

The six research topics and their 22 participant labels are maintained in `data/content.json`. The `research_name_ko` field in `data/people.json` connects 16 of these names to existing profiles. The builder uses that field to create links in both directions and support People searches in Korean or by topic. Original English profile titles and supplied research interests are retained.

조명근, 오창석, 이도윤, 김화랑, 배재영, and 정성운 appear as names under their assigned topics. The archive supplies no individual profile or degree information for these six participants. The original parentheses around 황환철, 노경곤, and 김여호수아 are retained in the assignments.

## Preserve and verify

1. Display each original `title`, not a name reconstructed from `id` or `source_filename`. Examples include Yeohosua Kim (`02_joshua-kim.md`), SungGin Noh (`03_sung-jin-noh.md`), SeonWoo Shin (`05_sun-woo-shin.md`), GeonWoo Kim (`06_gun-woo-kim.md`), JeongUk Kim (`07_jung-wook-kim.md`), and JeongHun Youn (`08_jung-hoon-yoon.md`).
2. JeongUk Kim's bachelor-degree text is exactly `B.S. in Naval architecture occean Engineering & Electrical Engineering` in the source. It is preserved in JSON; `occean` appears to be a spelling error and can be confirmed before editorial correction.
3. Only SungJun Park, SeonWoo Shin, JeongUk Kim, JeongHun Youn, and SangHo Jeon have education details. Other empty education arrays must not be replaced with inferred degrees or dates.
4. Only SungJun Park has selected publications (three). Preserve both `paper` and `link` when present: they point to different destinations. Imported publication details are user-supplied metadata, not newly verified bibliographic records.
5. `Robotics Team` and `xEV Team` are source research-interest entries. The other members' team membership is unspecified; do not infer it from research topics.
6. The professor's source profile has empty education, research-interest, and selected-publication arrays. Existing verified professor biography can remain in its separate template. Do not mistake empty arrays for a request to erase that biography.
7. Alumni have no supplied email, education, research, graduation year, employment, or personal website. Preserve their names without inventing additional details.
8. Records use `role`, while the original profile template reads `position` only. Render `position` or fall back to `role` to avoid dropping the role. Hide empty sections by checking array length.
9. The source includes two alumni filenames beginning `09_`; these are distinct people (이광재 and 이원형), not duplicates.
10. This roster reflects the attached archive. No independent check of present enrollment or graduation status was performed.

## Maintenance

Edit `data/people.json` and retain the original identity for existing profiles. When adding a supplied profile for a research participant, set `research_name_ko` to the exact Korean name used in the assignment, without parentheses. Maintain the original display spelling, including parentheses, in the topic's `participants` list. Add new image files to `assets/people/`, then run the site's build and verification commands documented in the main README. Empty categories should stay hidden in the rendered page.
