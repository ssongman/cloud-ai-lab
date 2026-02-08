# Suppression & Deduplication - 억제 및 중복 제거 정책

## 중복 제거 (Deduplication)

### 중복 판단 기준

동일 이벤트로 판단하는 조건:

```yaml
dedup_key:
  - cloud_provider     # 클라우드 제공자
  - event_type         # 이벤트 타입
  - resource_id        # 대상 리소스
  - actor              # 수행자
```

위 4개 필드가 모두 동일하면 중복으로 판단합니다.

### 중복 윈도우

| 우선순위 | 중복 윈도우 | 설명 |
|----------|-------------|------|
| P0 | 30분 | 동일 이벤트 30분 내 재발생 시 억제 |
| P1 | 1시간 | 동일 이벤트 1시간 내 재발생 시 억제 |
| P2 | 24시간 | 동일 이벤트 24시간 내 재발생 시 억제 |

## 억제 정책 (Suppression)

### 계획된 작업 억제

유지보수 기간 동안 알림을 억제합니다.

```yaml
suppression_windows:
  - name: "주간 정기 점검"
    schedule:
      day: "sunday"
      start: "02:00"
      end: "06:00"
      timezone: "Asia/Seoul"
    suppress_levels: ["P1", "P2"]  # P0는 억제하지 않음

  - name: "배포 윈도우"
    schedule:
      day: "wednesday"
      start: "22:00"
      end: "23:00"
      timezone: "Asia/Seoul"
    suppress_levels: ["P2"]
```

### 수동 억제

운영자가 수동으로 특정 이벤트를 억제할 수 있습니다.

```yaml
manual_suppression:
  - rule_id: "azure-001"
    resource_pattern: "dev-*"     # dev 환경 VM 삭제는 억제
    reason: "개발 환경 자동 정리"
    expires: "2025-12-31T23:59:59Z"
```

## 쿨다운 (Cooldown)

각 탐지 룰에 정의된 `cooldown_minutes` 동안
동일 룰에 대한 알림을 반복 발송하지 않습니다.

### 쿨다운 로직

```
1. 이벤트 감지 → 탐지 룰 매칭
2. dedup_key 생성
3. 최근 알림 이력 조회 (cooldown_minutes 이내)
4. 이력 있음 → 억제 (로그만 기록)
5. 이력 없음 → 알림 발송 + 이력 기록
```

## 일간 다이제스트

억제된 이벤트를 포함하여 일간 요약 리포트를 생성합니다.

- 발송 시간: 매일 09:00 KST
- 내용: 전일 발생 이벤트 요약, 억제된 이벤트 목록, 미확인 알림 목록
- 채널: Email (운영팀 전체)
