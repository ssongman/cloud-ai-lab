# Data Life Cycle - 데이터 라이프사이클 관리

## 인덱스 라이프사이클 정책

### 단계 정의

```
Hot (0~7일) → Warm (7~30일) → Cold (30~90일) → Delete (90일+)
```

| 단계 | 기간 | 스토리지 | 레플리카 | 용도 |
|------|------|----------|----------|------|
| **Hot** | 0~7일 | SSD | 1 | 실시간 검색/분석 |
| **Warm** | 7~30일 | HDD | 1 | 과거 조회 |
| **Cold** | 30~90일 | 저비용 | 0 | 감사/컴플라이언스 |
| **Delete** | 90일+ | - | - | 삭제 |

### ISM(Index State Management) 정책

```json
{
  "policy": {
    "policy_id": "cloud-events-lifecycle",
    "description": "Cloud events index lifecycle policy",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [
          {
            "rollover": {
              "min_index_age": "1d",
              "min_primary_shard_size": "30gb"
            }
          }
        ],
        "transitions": [
          {
            "state_name": "warm",
            "conditions": {
              "min_index_age": "7d"
            }
          }
        ]
      },
      {
        "name": "warm",
        "actions": [
          {
            "replica_count": {
              "number_of_replicas": 1
            }
          },
          {
            "force_merge": {
              "max_num_segments": 1
            }
          }
        ],
        "transitions": [
          {
            "state_name": "cold",
            "conditions": {
              "min_index_age": "30d"
            }
          }
        ]
      },
      {
        "name": "cold",
        "actions": [
          {
            "replica_count": {
              "number_of_replicas": 0
            }
          }
        ],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "90d"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "delete": {}
          }
        ]
      }
    ],
    "ism_template": [
      {
        "index_patterns": ["cloud-events-*"],
        "priority": 100
      }
    ]
  }
}
```

### ISM 정책 적용

```bash
# ISM 정책 생성
curl -X PUT "https://opensearch:9200/_plugins/_ism/policies/cloud-events-lifecycle" \
  -H 'Content-Type: application/json' \
  -d @ism-policy.json

# 기존 인덱스에 정책 적용
curl -X POST "https://opensearch:9200/_plugins/_ism/add/cloud-events-*" \
  -H 'Content-Type: application/json' \
  -d '{"policy_id": "cloud-events-lifecycle"}'
```

## 인덱스 템플릿

```json
{
  "index_patterns": ["cloud-events-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "cloud-events-lifecycle",
      "index.lifecycle.rollover_alias": "cloud-events"
    }
  }
}
```

## 데이터 보관 정책 요약

| 데이터 유형 | 보관 기간 | 비고 |
|-------------|-----------|------|
| 클라우드 이벤트 | 90일 | ISM 자동 삭제 |
| 알림 이력 | 1년 | 감사 목적 |
| 스냅샷 | 30일 | S3 백업 |
| 탐지 룰 변경 이력 | 영구 | Git 관리 |
