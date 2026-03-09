# Contributing Guide

## 브랜치 전략
- `main`: 배포/기준 브랜치
- 작업 브랜치: `feature/<주제>`, `fix/<주제>`, `docs/<주제>`

예시:
- `feature/step8-integration`
- `docs/meeting-note-0309`

## 커밋 컨벤션
형식:
```text
<type>: <summary>
```

권장 type:
- `feat`: 기능/분석 로직 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `refactor`: 구조 개선
- `chore`: 설정/잡무

예시:
- `feat: add step 8-1 integrated scoring`
- `docs: add meeting notes for 0307`

## 작업 절차
1. 최신 `main` 기준으로 브랜치 생성
2. 작업 후 변경사항 확인 (`git status`)
3. 단위별 커밋
4. 원격 브랜치 푸시 및 PR 생성
5. 리뷰 후 `main` 반영

## 노트북 작업 규칙
- 핵심 결과 셀은 제목/설명(마크다운)과 함께 유지
- 대용량 데이터(`*.csv`)는 커밋 금지
- 발표용 결과는 회의록/가이드 문서와 메시지 일관성 유지
