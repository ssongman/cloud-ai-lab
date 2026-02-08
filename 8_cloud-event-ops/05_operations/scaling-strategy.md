# Scaling Strategy - 확장 전략

## OpenSearch 클러스터 확장

### 수평 확장 (Scale-Out)

| 구성 | Data Node | Master Node | 일일 이벤트 처리량 |
|------|-----------|-------------|------------------|
| Small | 2 | 3 | ~100만 |
| Medium | 4 | 3 | ~500만 |
| Large | 8+ | 3 | ~2000만+ |

### Data Node 추가

```bash
helm upgrade opensearch opensearch/opensearch \
  --namespace opensearch \
  --set replicas=4 \
  --set persistence.size=100Gi
```

### 샤드 전략

| 인덱스 패턴 | Primary Shards | Replica Shards | 롤오버 주기 |
|-------------|----------------|----------------|------------|
| `cloud-events-*` | 3 | 1 | 일간 |
| `alert-history-*` | 1 | 1 | 월간 |

## Controller Application 확장

### 수평 확장

```bash
kubectl scale deployment controller-app --replicas=3 -n cloud-event-ops
```

### 이벤트 파티셔닝

- 다중 인스턴스 배포 시 이벤트 처리 중복 방지
- 리더 선출 기반 또는 파티션 기반 분배
- OpenSearch Scroll/PIT API 활용

## 알림 시스템 확장

### 비동기 알림 큐

이벤트 볼륨이 증가할 경우 알림 발송을 큐 기반으로 전환:

```
Controller → Message Queue (Redis/RabbitMQ) → Alert Worker(s)
```

## 모니터링 지표

| 지표 | 임계값 | 액션 |
|------|--------|------|
| OpenSearch CPU > 80% | 5분 지속 | Data Node 추가 |
| OpenSearch Disk > 75% | - | ILM 정책 조정 또는 노드 추가 |
| 이벤트 처리 지연 > 5분 | - | Controller 레플리카 추가 |
| 알림 발송 실패율 > 5% | - | 알림 채널 점검 |
