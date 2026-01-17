# 1. cloud-ai-lab
Cloud사업담당내 AI 관련 스터디(LLM MCP Agent  LangChain LangGraphy RAG)와 핸즈온을 수행
다음 주제를 중심으로 **공부 + 핸즈온 + 토론 결과**를 누적한다.



## 1) 주요 주제
- LLM 기본 개념 및 활용
- RAG (Retrieval Augmented Generation)
- LangChain / LangGraph
- Agent 설계 패턴
- MCP (Model Context Protocol)
- Cloud 운영 자동화 Capstone



## 2) 사용 방법
1. `0_admin/schedule.md`에서 스터디 일정 확인
2. 각 주제 폴더의 `notes.md`로 개념 학습
3. `labs/`에서 실습 진행
4. 결과는 PR로 공유



# 2. Repo 구조

```

cloud-ai-lab/
├─ README.md
├─ 0_admin/                     # 스터디 운영/관리
│  ├─ schedule.md               # 회차별 주제/발표자
│  ├─ rules.md                  # 스터디 운영 규칙
│  └─ resources.md              # 공통 참고자료
├─ 1_fundamentals/              # LLM 공통 기초
│  ├─ llm_basics.md
│  ├─ prompting_patterns.md
│  ├─ tool_calling.md
│  └─ model_comparison.md
├─ 2_rag/                       # RAG 학습 & 실습
│  ├─ notes.md
│  ├─ labs/
│  │  ├─ lab01_basic_rag/
│  │  └─ lab02_rag_evaluation/
│  └─ datasets/
├─ 3_langchain/                 # LangChain 활용
│  ├─ notes.md
│  └─ labs/
├─ 4_langgraph/                 # LangGraph (Agent Graph)
│  ├─ notes.md
│  └─ labs/
├─ 5_agents/                    # Agent 패턴/구현
│  ├─ concepts.md               # Agent 개념/패턴
│  ├─ safety_and_guardrails.md
│  └─ labs/
│     ├─ single_agent/
│     └─ multi_agent/
├─ 6_mcp/                       # MCP 실습 (차별점 🔥)
│  ├─ overview.md
│  └─ labs/
│     ├─ filesystem/
│     ├─ api/
│     └─ kubernetes/
├─ 7_capstones/                 # 회차/팀별 미니 프로젝트
│  ├─ ops_agent/
│  ├─ rag_report_agent/
│  └─ incident_triage_agent/
├─ tools/                       # 공통 유틸
├─ templates/                   # 문서/실습 템플릿
│  ├─ weekly-notes.md
│  └─ lab-readme.md
└─ CONTRIBUTING.md

```



