# Data Flow

## 이벤트 수집 흐름

### Azure 이벤트 흐름
```
Azure Activity Log
  → Diagnostic Settings
    → Event Hub
      → Logstash (Azure Event Hub Input)
        → OpenSearch (Bulk Index)
```

### AWS 이벤트 흐름
```
AWS CloudTrail / EventBridge
  → EventBridge Rule
    → Lambda Function
      → OpenSearch (Bulk API)
```

## 이벤트 정규화 스키마

```json
{
  "timestamp": "ISO8601",
  "cloud_provider": "azure | aws",
  "event_source": "string",
  "event_type": "string",
  "severity": "critical | high | medium | low | info",
  "resource_id": "string",
  "resource_type": "string",
  "region": "string",
  "subscription_id": "string (azure) | account_id (aws)",
  "actor": "string",
  "action": "string",
  "status": "success | failure",
  "raw_event": {},
  "tags": []
}
```

## 알림 발송 흐름

```
OpenSearch Index
  → Controller App (Polling / Alerting Plugin)
    → Detection Rule 매칭
      → [매칭됨] → RAG 판단 보조 (선택적)
        → Alert Routing (P0/P1/P2)
          → Mattermost / Email / SMS
      → [매칭안됨] → 로그 기록
```

## 데이터 보관 흐름

```
Hot (0~7일) → Warm (7~30일) → Cold (30~90일) → Delete (90일+)
```
