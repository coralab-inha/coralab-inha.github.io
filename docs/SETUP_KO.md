# CORA Lab 홈페이지 편집·배포 안내

## 구성

- Home: CORA 메인 이미지, 소속, 연구 성과와 연구 분야
- About: 연구실 소개와 연구 접근 방법
- Research: 6개 연구 주제, 주제별 참여연구원, 실제 연구 이미지·코드 링크
- Projects: 한일국제공동연구·중견연구·BK21·AX대학원·지역지능화의 목록과 사업별 상세 페이지, 확인된 사업 기간과 연구·교육 내용
- Papers: 80개 서지 항목, 검색·연도·유형 필터
- People: 교수 1명·박사과정 7명·석사과정 9명·동문 17명, 현재 구성원 상세 프로필 17개, 이름·연구 관심사·이메일 검색
- Teaching: 교과목 소개와 공개 코드 자료
- Contact: 이메일, 소속, 진학·공동연구 문의

이 ZIP은 Python으로 빌드하는 독립 소스입니다. 생성된 홈페이지는 `dist/`에 들어 있습니다.

기존 CLeAR 재구현 코드의 글꼴, 본문 폭, 내비게이션과 목록 스타일을 재사용했습니다. CORA 전용 SVG와 연구실 공개 자료를 사용하며, CLeAR 연구실 정보나 인트라넷을 CORA 정보로 남겨두지 않았습니다.

## 로컬에서 실행

압축을 해제한 폴더에서 다음을 실행합니다.

```sh
python3 scripts/build.py
python3 scripts/verify.py dist
python3 -m http.server 8000 --directory dist
```

http://localhost:8000/ 을 엽니다. Windows에서는 `python3` 대신 `py`를 사용할 수 있습니다. 파일을 직접 더블클릭하지 말고 HTTP 서버로 열어 주세요.

## github.io 배포

1. 본인 GitHub 계정 또는 조직에 새 저장소를 만듭니다. 대표 주소는 `<계정명>.github.io`, 프로젝트 사이트는 원하는 저장소명을 사용합니다.
2. 이 패키지의 내용물을 저장소 최상위에 올립니다. `.github/` 폴더도 포함합니다.
3. **Settings → Pages → Build and deployment → Source**에서 **GitHub Actions**를 선택합니다.
4. `main`에 push하거나 **Actions → Deploy CORA Lab to GitHub Pages → Run workflow**를 실행합니다.
5. 완료 후 Pages에서 제공하는 주소를 엽니다.

프로젝트 저장소의 하위 경로는 자동 반영합니다. 계정 정책에 따른 Pages 사용 가능 여부는 GitHub 설정에서 확인합니다. 이 패키지에 특정 사용자의 GitHub 계정이나 원본 CLeAR 저장소로 push하는 명령은 포함하지 않았습니다.

## 내용 수정

`data/verified-facts.json`에서 `pi`, `news`를, `data/publications.json`의 `records`에서 논문 목록을 수정한 뒤 다시 빌드합니다. 논문은 `id`, `title`, `authors`, `year`, `venue`, `type`, `provenance`를 기본으로 사용하고, `doi`, `volume`, `issue`, `pages`, `article`, `preprint`, `code`는 해당할 때 추가합니다. 논문 검색은 화면에 보이는 제목·저자·학술지 내용을 대상으로 합니다. 연도와 유형 필터를 동시에 사용할 수 있습니다. Google Scholar에서 내보낸 목록과 비교하는 방법은 [논문 갱신 절차](PUBLICATIONS_UPDATE.md)를 참조하세요.

연구 분야와 강의 설명은 `data/content.json`, 공통 메뉴와 푸터는 `templates/layout.html`, 보조 스타일은 `assets/cora.css`에서 관리합니다. `dist/`는 매번 생성되므로 직접 수정하지 않습니다.

## 실제 운영 전 보완할 자료

첨부 소스의 구성원 33명과 사용자 요청으로 추가한 동문 1명을 반영했습니다. 원문에 없는 졸업연도·진로·학력은 추가하지 않았습니다. 이름의 영문 표기와 학위 기간은 제공된 값을 유지했습니다. 첨부에 비어 있는 포닥·학부생 그룹은 화면에 노출하지 않습니다. 정확한 연구실 호실은 공개 디렉터리 간 정보가 달라 제외했습니다. 강의별 비공개 자료는 공개 홈페이지에 복사하지 않았습니다.

연구 분야의 문장은 연구실용 소개 초안이며, 근거는 논문·공개 저장소 및 기존에 제공한 연구·교육 맥락입니다. 학과·직위와 공식 영문 표기는 `verified-facts.json`의 출처를 기준으로 작성했습니다.

## People 수정

`data/people.json`의 `people` 배열에서 한 명씩 관리합니다.

- `id`: 개인 페이지 주소에 사용합니다. 주소를 유지하려면 기존 id를 바꾸지 마세요.
- `title`: 첨부 원문의 이름. `display_name`이 있으면 화면 이름으로 우선 사용합니다.
- `category`: `professor`, `postdoc`, `phd`, `ms`, `undergrad`, `alumni` 중 하나.
- `role`, `email`, `image`: 과정/직함, 이메일, `/assets/people/파일명` 사진 경로.
- `education`, `research_interests`, `selected_publications`: 제공 가능한 항목만 입력합니다. 빈 배열은 화면에 표시하지 않습니다.
- 논문 `paper`와 `link`는 각각 Paper와 Project 링크로 표시됩니다.

이미지는 `assets/people/`에 넣고 `python3 scripts/build.py`로 다시 빌드하세요. 홈의 박사·석사 인원과 People 그룹별 인원은 JSON에서 자동 계산됩니다. 동문은 이름 목록으로 표시되며, 이름·이메일·관심사 검색은 JavaScript가 작동할 때 사용할 수 있습니다. JavaScript가 없어도 전체 목록과 상세 페이지 링크를 읽을 수 있습니다.

## Projects 수정

`data/projects.json`의 `projects` 배열에서 각 항목을 관리합니다.

- `id`는 목록의 바로가기 주소(`/projects/#id`)와 상세 주소(`/projects/id/`)에 함께 사용합니다. `short_label`은 목록 상단에, `program_label`은 사업명에 표시됩니다.
- `title_en`, `title_ko`, `overview_en`, `overview_ko`에서 영문·국문 이름과 소개를 수정합니다.
- `metadata`에는 확인된 기간·사업명·기관 등을 `label`, `value` 쌍으로 입력합니다. `focus`는 연구·교육 내용입니다.
- `links`는 공식 외부 안내, `related_links`는 연구실 내부 페이지를 연결합니다. 내부 경로는 `/research/#planning-control-cavs`처럼 입력하면 GitHub Pages 하위 경로가 자동 적용됩니다.
- `sources`, `editorial_note`는 편집·검토용으로 화면에 표시되지 않습니다. 확인되지 않은 기간·사업번호·책임자 정보를 임의로 추가하지 마세요.

지역지능화는 현재 일반 사업 개요입니다. 해당 연구실의 정확한 세부과제명·주관기관·참여기간이 확인되면 그 정보를 추가할 수 있습니다.

## Research 수정

`data/content.json`의 `research` 배열에서 6개 연구 주제를 관리합니다.

- `title`, `short`, `body`, `body_ko`: 영문 제목, 홈 소개, 영문·국문 상세 소개.
- `participants`: 참여연구원 이름을 순서대로 입력합니다. 괄호 표기는 사용자가 제공한 그대로 표시하며, 역할이나 참여 상태를 임의로 해석하지 않습니다.
- `topics`: 주요 연구 키워드. `links`와 이미지 출처는 관련 공개 연구 자료입니다.
- `id`: 주제별 바로가기 주소. `aliases`는 이전 주소와의 호환성을 위한 항목입니다.

Research의 참여연구원 추가가 People의 과정·직함·프로필 생성을 자동으로 의미하지는 않습니다. People 정보는 별도로 확인된 자료로 관리합니다.
