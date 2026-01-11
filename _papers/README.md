# 논문(Publications) 관리

이 디렉토리는 논문(Publication)들의 메타데이터를 포함하고 있습니다. 각 파일은 하나의 논문을 나타냅니다.

## 새로운 논문 추가 방법

1. 이 디렉토리에 새로운 마크다운 파일을 생성합니다: `YYYY-저자-키워드.md` (예: `2025-kim-robotd.md`).
2. 아래 템플릿을 복사하여 붙여넣으세요:

```yaml
---
layout: paper
title: "논문 제목"
authors: "저자1, 저자2"
year: 2025
journal: "저널 또는 학회명"
image: /assets/img/publication_preview/example.png # 선택사항 (프리뷰 이미지 경로)
pdf: example.pdf # 선택사항 (PDF 파일 파일명 또는 경로)
url: https://example.com # 선택사항 (논문 공식 링크)
code: https://github.com/example/code # 선택사항 (코드 저장소 링크)
highlight: false # "Group Highlights" 섹션에 표시하려면 true로 설정
category: article # article, book, inproceedings 등
---
```

## 필드 설명

- **layout**: 항상 `paper`로 설정합니다.
- **title**: 논문의 전체 제목입니다.
- **authors**: 저자 목록입니다.
- **year**: 출판 연도 (YYYY).
- **journal**: 저널명, 학회명 또는 출판사명입니다.
- **image**: 프리뷰 이미지 경로입니다. (프로젝트 루트 기준, Group Highlights 섹션에서 사용).
- **pdf**: PDF 파일의 경로 또는 파일명입니다.
- **url**: 논문의 공식 웹페이지 링크입니다.
- **code**: 소스 코드 저장소 링크입니다.
- **highlight**: 중요한 논문이라 "Group Highlight" 섹션에 표시하고 싶다면 `true`로 설정하세요.
- **category**: `article`, `book`, `inproceedings` 등. 필터링이 활성화된 경우 사용됩니다.
