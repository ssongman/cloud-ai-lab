# Solution - 인프라 구성 가이드

## 개요

이 디렉토리는 Cloud Event Ops 시스템의 인프라 구성 요소 설치 및 설정 가이드를 포함합니다.

## 구성 요소

| 디렉토리 | 설명 |
|-----------|------|
| `opensearch/` | OpenSearch 클러스터 설치 (Kubernetes Helm) |
| `opensearch-dashboards/` | OpenSearch Dashboards 설치 (시각화) |
| `mattermost/` | Mattermost 알림 채널 설정 |

## 설치 순서

1. **OpenSearch 클러스터** 설치 → `opensearch/install.md`
2. **OpenSearch Dashboards** 설치 → `opensearch-dashboards/install.md`
3. **Mattermost Webhook** 설정 → `mattermost/setup.md`

## 사전 요구사항

- Kubernetes 클러스터 (v1.25+)
- Helm v3
- kubectl 구성 완료
- 충분한 리소스 (최소 8GB RAM, 4 CPU)
