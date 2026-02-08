# Deployment Guide - 배포 가이드

## 배포 순서

### Phase 1: 인프라 구성
1. Kubernetes 클러스터 준비
2. OpenSearch 클러스터 배포
3. OpenSearch Dashboards 배포

### Phase 2: 이벤트 수집 파이프라인
4. Azure Event Hub + Logstash 구성
5. AWS EventBridge + Lambda 구성
6. 이벤트 정규화 및 인덱스 생성

### Phase 3: Controller Application
7. 탐지 룰 ConfigMap 배포
8. Controller App 배포
9. 알림 채널 연동 테스트 (Mattermost, Email)

### Phase 4: 운영 안정화
10. 대시보드 구성
11. 모니터링 (Prometheus + Grafana) 연동
12. ILM 정책 적용

## 환경별 배포

| 환경 | 용도 | OpenSearch 노드 | Controller 레플리카 |
|------|------|-----------------|-------------------|
| dev | 개발/테스트 | 1 (single) | 1 |
| staging | 스테이징 | 3 (cluster) | 1 |
| prod | 운영 | 5+ (cluster) | 2+ |

## Helm Values 오버라이드

```bash
# dev
helm install opensearch opensearch/opensearch -f values-dev.yaml

# prod
helm install opensearch opensearch/opensearch -f values-prod.yaml
```

## 헬스체크

배포 후 확인 사항:

```bash
# OpenSearch 클러스터 상태
curl -k https://opensearch:9200/_cluster/health

# 인덱스 목록
curl -k https://opensearch:9200/_cat/indices

# Controller App 상태
kubectl logs -f deployment/controller-app -n cloud-event-ops
```
