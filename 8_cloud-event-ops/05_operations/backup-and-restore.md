# Backup & Restore - 백업 및 복구

## 백업 전략

### OpenSearch 스냅샷

#### 스냅샷 리포지토리 등록

```bash
curl -X PUT "https://opensearch:9200/_snapshot/backup_repo" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "s3",
    "settings": {
      "bucket": "opensearch-backup",
      "region": "ap-northeast-2",
      "base_path": "snapshots"
    }
  }'
```

#### 스냅샷 생성 (수동)

```bash
curl -X PUT "https://opensearch:9200/_snapshot/backup_repo/snapshot_$(date +%Y%m%d)" \
  -H 'Content-Type: application/json' \
  -d '{
    "indices": "cloud-events-*",
    "ignore_unavailable": true,
    "include_global_state": false
  }'
```

#### 자동 스냅샷 (ISM 정책)

```json
{
  "policy": {
    "description": "Daily snapshot policy",
    "creation": {
      "schedule": {
        "cron": {
          "expression": "0 2 * * *",
          "timezone": "Asia/Seoul"
        }
      }
    },
    "snapshot_config": {
      "indices": {
        "all_indices": false,
        "pattern": "cloud-events-*"
      },
      "repository": "backup_repo"
    },
    "deletion": {
      "schedule": {
        "cron": {
          "expression": "0 3 * * *",
          "timezone": "Asia/Seoul"
        }
      },
      "condition": {
        "max_age": "30d",
        "max_count": 30
      }
    }
  }
}
```

## 복구 절차

### 인덱스 복구

```bash
# 스냅샷 목록 확인
curl -X GET "https://opensearch:9200/_snapshot/backup_repo/_all"

# 특정 스냅샷에서 복구
curl -X POST "https://opensearch:9200/_snapshot/backup_repo/snapshot_20250101/_restore" \
  -H 'Content-Type: application/json' \
  -d '{
    "indices": "cloud-events-2025.01.*",
    "ignore_unavailable": true
  }'
```

### 복구 확인

```bash
curl -X GET "https://opensearch:9200/_recovery?active_only=true"
```

## 백업 주기

| 대상 | 주기 | 보관 기간 |
|------|------|-----------|
| OpenSearch 인덱스 스냅샷 | 매일 02:00 KST | 30일 |
| Controller App 설정 | Git 기반 (변경 시) | 영구 |
| 탐지 룰 | Git 기반 (변경 시) | 영구 |
