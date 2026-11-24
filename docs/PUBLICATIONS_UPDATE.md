# Publications 관리 및 Google Scholar 갱신

편집 원본은 `data/publications.json`입니다. 사이트 빌드는 이 파일로 `dist/publications/index.html`을 생성합니다. Google Scholar 공개 프로필은 Papers 페이지 상단에서 열 수 있습니다.

## 2026년 11월 19일 대조 결과

| 항목 유형 | 건수 |
| --- | ---: |
| 학술지 논문 (Journal) | 43 |
| 학회 논문 및 발표 (Conference) | 29 |
| 프리프린트 (Preprint) | 6 |
| 단행본 장 (Book chapter) | 1 |
| 전문지 기고 (Magazine) | 1 |
| **전체 표시 항목** | **80** |

11월 5일 초안의 79개와 GitHub `main`의 기존 24개를 대조했습니다. 서로 대응하는 23개는 기존 ID를 유지했고, 저장소에만 있던 2021년 건물 HVAC 제어 기고문 한 편을 추가했습니다. 대한전기학회의 발간본에서 제목과 저자 표기, 『전기의 세계』 제70권 제4호, 15–29쪽을 확인했습니다. 홈페이지에는 `Magazine`으로 표시합니다. [대한전기학회 2021년 4월호](https://www.kiee.or.kr/upload/board_files/upfile_210408132323503.pdf) · [저장소의 원래 항목](https://github.com/coralab-inha/coralab-inha.github.io/blob/3efc90a357dffcf18b4ea07809c5ab0f7510ab9f/_papers/2021-kim-decentralized-lq.md)

목록은 2010–2026년 Kwang-Ki Kim과 공동저자들의 성과이며 연구실 설립 이전 연구도 포함합니다. 11월 5일 초안의 출처는 공개 ORCID, 출판사, arXiv, 연구자가 제공한 2026년 6월 CV입니다. CV의 발표·출판 완료 42개 인용을 대조했습니다. 당시 Scholar의 접근 제한(HTTP 429)으로 프로필 전체와의 일치 여부는 확인되지 않았습니다. 80건은 이 사이트의 표시 항목 수입니다. [ORCID](https://orcid.org/0000-0002-0499-7253)

## 다음 갱신 방법

1. **프로필 내보내기.** 연구책임자의 Scholar 프로필에서 항목을 선택한 뒤 **Export**로 CSV 또는 BibTeX를 내려받습니다. 전체 목록은 제목 열 옆 체크박스로 선택할 수 있습니다. 선택 메뉴가 보이지 않으면 프로필 소유 계정에서 진행합니다. 작업 기록에 내보낸 날짜와 범위를 남깁니다. 접근 제한이 다시 발생하면 사용자 제공 내보내기 파일을 사용하거나 대조하지 못한 범위를 기록합니다. [Google Scholar 프로필](https://scholar.google.com/citations?user=BfaXDOAAAAAJ&hl=ko) · [공식 내보내기 안내](https://scholar.google.com/intl/en/scholar/citations.html)
2. **같은 연구 식별.** DOI의 URL 접두사와 공백을 제거하고 대소문자를 통일해 기존 `records`와 대조합니다. DOI가 없으면 제목, 저자 순서, 연도, 학술지 또는 학회명을 함께 확인합니다. 온라인 공개와 권호 발간 연도가 다르면 권호 연도를 `year`로 쓰고 온라인 연도를 `online_year`에 남깁니다. Scholar에서 누락된 기존 항목은 출처를 다시 확인한 후 처리합니다.
3. **메타데이터 반영.** 기존 항목은 `id`를 유지해 개별 링크가 계속 작동하도록 합니다. 새 항목에는 고유한 `id`, `title`, `authors`, `authors_list`, 숫자 `year`, `venue`, `type`, `status`를 입력합니다. 공식 DOI는 접두사 없는 `doi`에, 원문 또는 프로그램 URL은 `url`에 기록합니다. 발표만 확인되면 `status: Presented`와 근거에 맞는 `presentation_type`을 씁니다. 원문 링크나 DOI를 확인하지 못했으면 비워 둡니다. 각 항목의 `provenance`에 근거 URL을, `verified_date`에 확인일을 남깁니다.
4. **버전과 상태 검토.** 공식 DOI 연결 또는 저자·출판사의 명시적 연결을 확인한 프리프린트는 출판 항목의 `preprint`로 보존합니다. 별도 연구인지 결정하기 어려우면 관련성을 기록하고 다음 대조 때 재검토합니다. 공개 프리프린트, 출판 논문, 학회 발표의 상태를 구분합니다. 인용 지표는 Scholar 프로필에서 확인할 수 있습니다.
5. **수량과 출처 갱신.** `metadata.updated_date`, `displayed_count`, `displayed_types`를 갱신합니다. `verified_date`는 11월 5일 기존 자료 수집일입니다. 일부 항목만 손본 경우 기존 수집일은 유지합니다. Scholar 전체 대조를 마쳤을 때는 `metadata.scholar_access`에 확인일·범위·미해결 항목을 기록합니다.
6. **빌드 검증.** 압축을 푼 프로젝트 최상위에서 아래 명령을 실행합니다. 검증기는 JSON과 생성된 HTML의 항목 수, ID, 유형과 표시 필드, 중복 DOI 및 제목·연도, 정적 링크 연결을 검사합니다. 브라우저에서 새 제목을 검색하고 연도·유형 필터, DOI 또는 원문 링크도 확인합니다.

```bash
python3 scripts/build.py
python3 scripts/verify.py dist
python3 -m http.server 8000 --directory dist
```

브라우저에서 `http://localhost:8000/publications/`을 엽니다. 수정할 때는 `data/publications.json`에 반영한 뒤 빌드를 다시 실행합니다.

## 11월 5일 대조에 사용한 기존 기준

- Prefer final publisher titles, author lists, volume/issue/pages and DOI over shortened CV wording.
- Prefer the issue publication year when a journal has both early online and print dates. This corrects three older journal rows to 2017 or 2014 and retains their online-year metadata.
- A separate CV inconsistency lists *Modification of Crystal Shape through Deep Temperature Cycling* as 2013; the publisher's volume 53, issue 13 record gives 2014, which is retained.
- The conic-constraint IPDDP article uses the publisher's 2022 year rather than the CV's 2023 entry.
- Four public preprint versions are grouped with their journal articles: one source-declared arXiv/journal DOI relationship and three existing verified lab links corroborated by matching primary-source content. Preprint links remain available on the journal rows.
- Two ICCAS2025 CV entries are listed as **oral presentations**, without invented DOI or proceedings-page claims. The official TransformerHyMPC program includes Minwoo Gwon, omitted in the CV; the program's three-author list is used.
- Other preprints remain separate where the source evidence does not establish a final publication relationship. The displayed count is a bibliography-entry count, not a claimed Google Scholar unique-paper total.

Per-record provenance, CV entry mapping, grouped version evidence and year decisions are retained in `data/publications.json`.
