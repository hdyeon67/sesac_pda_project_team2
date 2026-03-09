# sesac_pda_project_team2

스타티(Startie) 채널 가치 분석 프로젝트 저장소입니다.

## 프로젝트 목표
- 핵심 질문: 어떤 채널에서 들어온 유저가 가장 가치 있는가?
- 목표: 상위 채널 선정 및 예산 재배분 근거 도출

## 주요 분석 파일
- `01_eda.ipynb`: 발표용 EDA 메인 노트북
- `Channel_Value_Analysis.ipynb`: 채널 가치 분석 기준 노트북
- `notebooks/`: 회의록 및 정리 문서

## 데이터 관리 정책
- CSV 데이터 파일은 **로컬에서만 관리**합니다.
- `.gitignore`에 `*.csv`가 포함되어 있어 원격 저장소에 업로드되지 않습니다.

## 실행 환경
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 협업 규칙
브랜치/커밋/PR 규칙은 `CONTRIBUTING.md`를 참고하세요.
