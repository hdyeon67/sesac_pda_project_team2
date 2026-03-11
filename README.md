# sesac_pda_project_team2

스타티(Startie) 채널 가치 분석 프로젝트 저장소입니다.

## 프로젝트 목표
- 핵심 질문: 어떤 채널에서 들어온 유저가 가장 가치 있는가?
- 목표: 상위 채널 선정 및 예산 재배분 근거 도출

## 주요 분석 파일
- `01_eda.ipynb`: 발표용 EDA 메인 노트북
- `Step5_1_ModelB.ipynb`: 모델B(ROI 제외) 백업 노트북
- `notebooks/`: 회의록 및 정리 문서
- `notebooks/발표대본_0310.md`: 최종 발표 대본(5분 버전)
- `notebooks/질문대응_0310.md`: 슬라이드별 질문 대응(Q1~Q25)
- `resources/all_steps/`: Step 1~9 결과 표/시각화 리소스
- `resources/gamma_pack_0310/`: 최종 발표 산출물(PPT/프롬프트/리소스 목록)
  - 최종 발표본: `resources/gamma_pack_0310/스타티 성장 전략 보고서 최종.pptx`
- `resources/canva/SQLT_PDA_Project.pptx`: 2026-03-10 Canva 편집본 발표 자료
- `scripts/export_all_steps_resources.py`: Step 1~9 리소스 자동 내보내기 스크립트
- `notebooks/발표자료_프롬프트.md`: 발표자료 생성 프롬프트(최신 Step 반영)

## 회의록
- 날짜 기준 파일명: `회의록_YYYYMMDD.md`
- 최신 회의록: `notebooks/회의록_20260311.md`
- 날짜순 인덱스: `notebooks/회의록_목록_날짜순.md`

## 데이터 관리 정책
- 원본 대용량 CSV(`data/` 외 임시/개인 데이터)는 로컬 관리 원칙을 따릅니다.
- `.gitignore`에 `*.csv`가 포함되어 있으며, 신규 CSV는 기본적으로 추적되지 않습니다.
- 단, `resources/all_steps/`의 분석 결과 CSV는 발표/검증 목적상 예외적으로 추적될 수 있습니다.

## 실행 환경
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 협업 규칙
브랜치/커밋/PR 규칙은 `CONTRIBUTING.md`를 참고하세요.
