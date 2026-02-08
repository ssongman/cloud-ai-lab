# Architecture Overview

## 시스템 개요

Cloud Event Ops는 Azure/AWS 클라우드 환경에서 발생하는 이벤트를
실시간으로 수집·분석·알림하는 운영 자동화 플랫폼입니다.

## 주요 구성 요소

| 구성 요소 | 역할 | 기술 |
|-----------|------|------|
| OpenSearch Cluster | 이벤트 저장·검색·분석 | OpenSearch 2.x on K8s |
| OpenSearch Dashboards | 시각화·대시보드 | OpenSearch Dashboards |
| Event Ingestion | 클라우드 이벤트 수집 | Azure EventHub / AWS EventBridge → Logstash/FluentBit |
| Controller App | 이상징후 탐지·판단 | Python/Go |
| Alert System | 알림 발송 | Mattermost Webhook / Email / SMS |
| RAG Knowledge Base | 판단 보조 지식베이스 | Vector DB + LLM |

## 환경

- **런타임**: Kubernetes (EKS / AKS / On-prem)
- **모니터링**: Prometheus + Grafana
- **CI/CD**: GitHub Actions / ArgoCD
