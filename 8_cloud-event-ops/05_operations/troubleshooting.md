# Troubleshooting - 문제 해결 가이드

## OpenSearch 관련

### 클러스터 상태가 Red

**증상**: `_cluster/health` → `status: red`

**원인**: 일부 Primary 샤드가 할당되지 않음

**조치**:
```bash
# 미할당 샤드 확인
curl -X GET "https://opensearch:9200/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason"

# 클러스터 할당 설명
curl -X GET "https://opensearch:9200/_cluster/allocation/explain"

# 디스크 공간 확인
curl -X GET "https://opensearch:9200/_cat/nodes?v&h=name,disk.used_percent"
```

### 클러스터 상태가 Yellow

**증상**: `_cluster/health` → `status: yellow`

**원인**: Replica 샤드가 할당되지 않음 (노드 부족)

**조치**: Data Node 추가 또는 레플리카 수 조정

### 인덱싱 성능 저하

**조치**:
```bash
# Bulk Queue 확인
curl -X GET "https://opensearch:9200/_cat/thread_pool/bulk?v"

# 노드 리소스 확인
curl -X GET "https://opensearch:9200/_cat/nodes?v&h=name,cpu,heap.percent,disk.used_percent"
```

## Controller Application 관련

### 이벤트 감지 지연

**증상**: 이벤트 인덱싱 후 알림까지 지연 증가

**조치**:
1. Controller Pod 로그 확인
   ```bash
   kubectl logs -f deployment/controller-app -n cloud-event-ops
   ```
2. OpenSearch 쿼리 성능 확인
3. 폴링 주기 조정

### 알림 발송 실패

**증상**: 이벤트 탐지는 되지만 알림이 도착하지 않음

**조치**:
1. Mattermost Webhook URL 유효성 확인
   ```bash
   curl -X POST <WEBHOOK_URL> -d '{"text": "test"}'
   ```
2. SMTP 설정 확인
3. 네트워크 정책 (NetworkPolicy) 확인

### 중복 알림 발생

**증상**: 동일 이벤트에 대해 알림이 반복 발송

**조치**:
1. Dedup 설정 확인 (`suppression-dedup.md`)
2. Controller 다중 인스턴스 간 리더 선출 확인
3. 쿨다운 시간 조정

## 이벤트 수집 관련

### Azure 이벤트 수집 중단

**조치**:
1. Event Hub 상태 확인 (Azure Portal)
2. Logstash Pod 상태 확인
   ```bash
   kubectl logs -f deployment/logstash -n opensearch
   ```
3. Event Hub Consumer Group 오프셋 확인

### AWS 이벤트 수집 중단

**조치**:
1. EventBridge Rule 상태 확인 (AWS Console)
2. Lambda 함수 로그 확인 (CloudWatch)
3. Lambda → OpenSearch 네트워크 연결 확인

## 공통 점검 항목

| 점검 항목 | 명령 | 기대값 |
|-----------|------|--------|
| OpenSearch 상태 | `curl opensearch:9200/_cluster/health` | `green` |
| Pod 상태 | `kubectl get pods -n opensearch` | `Running` |
| 디스크 사용률 | `_cat/nodes?h=disk.used_percent` | < 75% |
| JVM Heap | `_cat/nodes?h=heap.percent` | < 85% |
| 인덱스 수 | `_cat/indices?h=index` | 예상 범위 내 |
