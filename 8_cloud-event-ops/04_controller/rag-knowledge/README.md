# RAG Knowledge Base

## 개요

Controller Application이 이벤트 판단 시 참조하는 RAG(Retrieval-Augmented Generation) 지식베이스입니다.

## 디렉토리 구조

```
rag-knowledge/
├── README.md            # 본 문서
├── criteria/            # "전달 여부" 판단 기준 문서
├── playbooks/           # 이벤트별 대응 절차 (운영자 전달용)
└── examples/            # 샘플 이벤트/라벨링 예시 (정답셋)
```

## 범위

- 클라우드 이벤트의 **운영자 전달 여부**를 판단하기 위한 근거 문서
- 탐지된 이벤트에 대한 **대응 절차(Playbook)** 제공
- 판단 정확도 검증을 위한 **라벨링 예시** 데이터

## 문서 포맷 규칙

### 판단 기준 문서 (criteria/)
- Markdown 형식
- 이벤트 유형별 판단 기준 기술
- 정상/비정상 구분 기준 명시

### 대응 플레이북 (playbooks/)
- Markdown 형식
- 단계별 대응 절차
- 담당자/채널 정보 포함

### 예시 데이터 (examples/)
- JSON 형식
- 실제 이벤트 + 기대 라벨(P0/P1/P2/무시) 쌍
- RAG 정확도 평가용

## 업데이트 방식

1. 운영팀이 새로운 판단 기준/플레이북 작성
2. Git PR로 리뷰 후 머지
3. Controller App 재시작 시 자동 로딩 (또는 Hot Reload)
