# Prompt Analysis

## 프로젝트 개요

Azure/AWS 클라우드 이벤트를 OpenSearch로 수집하고,
운영자가 반드시 알아야 하는 이벤트 발생 시 Alert을 전송하는 시스템 구축.

## 핵심 요구사항 분석

### 1. 이벤트 수집
- Azure Event Grid / Activity Log → OpenSearch 인제스트
- AWS CloudTrail / EventBridge → OpenSearch 인제스트

### 2. 이상징후 탐지
- OpenSearch에 수집된 이벤트 실시간 감시
- 사전 정의된 룰 기반 탐지
- RAG 기반 판단 보조

### 3. 알림 발송
- 이메일, SMS, Slack/Mattermost 등 다채널 알림
- 우선순위(P0/P1/P2)에 따른 에스컬레이션

### 4. 운영
- 데이터 라이프사이클 관리
- 보안 설정 (인증/권한)
- 배포 및 스케일링 전략
