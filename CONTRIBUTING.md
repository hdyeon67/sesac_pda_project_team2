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

## 파일/문서 네이밍 규칙
- 회의록은 날짜 기준 파일명을 사용합니다.
- 형식: `회의록_YYYYMMDD.md`, 상세 구분이 있으면 `회의록_YYYYMMDD_오전.md`처럼 suffix를 붙입니다.
- 최종 정리본은 `회의록_YYYYMMDD_최종정리.md` 형식을 권장합니다.
- 날짜순 인덱스는 `notebooks/회의록_목록_날짜순.md`를 갱신합니다.

## 노트북 작업 규칙
- 핵심 결과 셀은 제목/설명(마크다운)과 함께 유지
- 원본/개인 데이터(`*.csv`)는 커밋 금지
- 단, `resources/all_steps/`의 결과 CSV는 예외적으로 커밋 가능
- 발표용 결과는 회의록/가이드 문서와 메시지 일관성 유지

## 리소스 관리 규칙
- 분석 산출물 기준 경로는 `resources/all_steps/`를 우선 사용합니다.
- 중복 요약 폴더를 임시로 만들었더라도 최종 병합 시 단일 경로로 정리합니다.
- 발표 전용 산출물은 `resources/gamma_pack_0310/` 같은 별도 폴더로 모아 관리합니다.
