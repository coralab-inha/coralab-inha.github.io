# 웹사이트 관리 가이드 (User Manual)

이 문서는 웹사이트의 주요 콘텐츠(Home, People, Project, Publication)를 관리하는 방법을 설명합니다.
모든 데이터는 Markdown (`.md`) 파일과 YAML (`.yml`) 파일로 관리됩니다.

## 1. 폴더 구조 (Folder Structure)

주요 데이터가 위치한 폴더 구조는 다음과 같습니다.

```
root/
├── _data/                 
│   └── home.yml           # Home 페이지의 텍스트 및 설정 관리
├── _people/               # 연구실 구성원 (People) 개별 파일 위치
├── _projects/             # 프로젝트 (Project) 개별 파일 위치
├── _papers/               # 논문 및 출판물 (Publication) 개별 파일 위치
└── assets/
    └── img/               # 이미지 파일 저장 위치
```

---

## 2. Home 페이지 관리

Home 페이지의 메인 섹션(Hero, Research Areas, Application Domains)은 `_data/home.yml` 파일에서 수정할 수 있습니다.

**파일 위치:** `_data/home.yml`

### 주요항목 설명

*   **hero**: 최상단 메인 배너 영역
    *   `title`: 큰 제목 (예: THE DESIGN RESEARCH COLLECTIVE)
    *   `background_image`: 배경 이미지 경로 (예: `/assets/img/background.png`)
    *   `buttons`: 버튼 목록 (Meet Our Team, Join Our Team 등)
*   **research_areas**: 연구 분야 섹션
    *   `items`: 각 연구 분야 카드 목록 (제목, 이미지, 설명)
*   **application_domains**: 적용 분야 섹션
    *   `items`: 각 적용 분야 카드 목록

**예시 (`_data/home.yml`):**

```yaml
hero:
  title: "연구실 이름 또는 슬로건"
  background_image: "/assets/img/main-bg.jpg" # assets/img 폴더 내 이미지

research_areas:
  title: "RESEARCH AREAS"
  items:
    - title: "Robotics"
      image: "/assets/img/robot.png"
      description: "로봇 연구에 대한 설명..."
```

---

## 3. People (구성원) 관리

새로운 구성원을 추가하거나 정보를 수정하려면 `_people` 폴더 내의 Markdown 파일을 편집합니다.

**파일 위치:** `_people/영문이름.md` (예: `_people/hong_gildong.md`)

### 파일 작성 규칙

새 파일을 생성할 때 아래 형식을 복사해서 사용하세요.

```markdown
---
layout: profile
title: "Hong Gildong"        # 이름 (필수)
category: phd                # 역할 분류 (phd, ms, undergrad, pic, alumni 등)
role: "Ph.D. Student"        # 직함 표시
email: "hong@example.com"    # 이메일
image: "/assets/img/prof_pic.jpg" # 프로필 사진 경로
education:                   # 학력 (선택 사항)
  - degree: "Ph.D. in CS"
    institution: "University Name"
    year: "in progress"
research_interests:          # 연구 분야 (선택 사항)
  - Robotics
  - AI
---
```

*   **파일명**: 공백 없이 소문자와 언더바(`_`)를 사용하세요. (예: `kim_cheolsu.md`)
*   **category**: 웹사이트에서 탭이나 그룹을 나누는 기준이 됩니다.

---

## 4. Project (연구 과제) 관리

프로젝트를 추가하려면 `_projects` 폴더에 Markdown 파일을 생성합니다.

**파일 위치:** `_projects/프로젝트명.md`

### 파일 작성 규칙

```markdown
---
layout: project
title: "Autonomous Navigation"    # 프로젝트 제목
description: "Vision-LiDAR fusion..." # 짧은 설명
img: /assets/img/projects/nav.png # 썸네일 이미지
importance: 1                     # 정렬 순서 (숫자가 작을수록 먼저 표시됨)
category: Research Projects       # 카테고리
funding: "NRF (2024–2026)"        # 연구비 지원 기관 (선택)
---
```

---

## 5. Publication (논문) 관리

논문을 추가하려면 `_papers` 폴더에 Markdown 파일을 생성합니다.

**파일 위치:** `_papers/연도-저자-키워드.md` (예: `2024-kim-autonomous.md`)

### 파일 작성 규칙

```markdown
---
layout: paper
title: "Deep Reinforcement Learning for Autonomous Parking" # 논문 제목
authors: "Kim, D.H. and Lee, M.J." # 저자 목록 (이름 구분은 'and' 사용)
year: 2024                         # 출판 연도
journal: "ICRA"                    # 학회 또는 저널명
pdf: paper.pdf                     # PDF 파일 경로 (assets/pdf/ 폴더 등에 위치)
image: /assets/img/paper_thumb.png # 논문 썸네일 이미지
category: article                  # 분류 (article 등)
---
```
