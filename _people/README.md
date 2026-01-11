# 구성원(People) 관리

이 디렉토리는 연구실 구성원들의 프로필 정보를 포함하고 있습니다. 각 파일은 한 명의 구성원을 나타냅니다.

## 새로운 구성원 추가 방법

1. 이 디렉토리에 새로운 마크다운 파일을 생성합니다: `영문이름.md` (예: `daehun.md`, `chris_mccomb.md`).
2. 아래 템플릿을 복사하여 붙여넣으세요:

```yaml
---
layout: profile
title: "이름 (Name)" # 이름
category: phd # 예: professor, phd, ms, undergrad, alumni (5가지 중 한개 필수)
role: "역할 (e.g., Ph.D. Student)" # 예: Ph.D. Student, M.S. Student, Undergraduate Student, Alumni (박사나 석사 안에도 석사 연구원, 포닥.. 등 여러가지로 등록될 수 있기 때문에 존재. 화면에 나타나는 부분) 
email: "usuario@example.com" # 이메일
image: "/assets/img/people/sample_m.png" # 프로필 이미지 경로, 경로에 실제로 프로필 이미지가 있어야함.
education:
  - degree: "학위 (e.g., Ph.D. in Design)"
    institution: "학교 (e.g., Penn State University)"
    year: "기간 (e.g., 2023 - Present)"
research_interests:
  - 관심 분야 1
  - 관심 분야 2
selected_publications:
  - authors: "저자 목록"
    title: "논문 제목"
    journal: "저널 또는 학회명"
    link: "#" # 논문 링크
---
```

## 필드 설명

- **layout**: 항상 `profile`로 설정합니다.
- **title**: 구성원의 이름입니다.
- **category**: 구성원 카테고리. 사이트에서 그룹화에 사용됩니다 (`professor`, `phd`, `ms`, `undergrad`, `alumni` 등).
- **role**: 표시될 직함입니다.
- **email**: 연락처 이메일입니다.
- **image**: 프로필 이미지의 경로입니다.
- **education**: 학력 정보 리스트입니다. `degree`(학위), `institution`(기관), `year`(기간)을 포함합니다.
- **research_interests**: 연구 관심사 목록입니다.
- **selected_publications**: 주요 실적 또는 선택된 논문 목록입니다.
