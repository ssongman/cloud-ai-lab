# Routing & Escalation - 라우팅 및 에스컬레이션 정책

## 알림 라우팅

### 채널별 라우팅 규칙

| 우선순위 | Mattermost | Email | SMS |
|----------|------------|-------|-----|
| P0 | `#cloud-alerts-p0` | 전체 운영팀 | 온콜 담당자 |
| P1 | `#cloud-alerts-p1` | 담당자 | - |
| P2 | `#cloud-alerts-daily` | 일간 다이제스트 | - |

### 담당자 매핑

```yaml
teams:
  - name: "cloud-ops"
    members:
      - name: "담당자A"
        email: "a@example.com"
        phone: "+82-10-xxxx-xxxx"
        mattermost: "@user-a"
      - name: "담당자B"
        email: "b@example.com"
        phone: "+82-10-xxxx-xxxx"
        mattermost: "@user-b"

  - name: "security-ops"
    members:
      - name: "보안담당자"
        email: "sec@example.com"
        phone: "+82-10-xxxx-xxxx"
        mattermost: "@sec-user"
```

### 이벤트 유형별 담당 팀

| 이벤트 카테고리 | 담당 팀 |
|----------------|---------|
| Compute (VM/EC2) | cloud-ops |
| Network (NSG/SG) | cloud-ops, security-ops |
| IAM/RBAC | security-ops |
| Database (RDS/SQL) | cloud-ops |
| Storage (S3/Blob) | cloud-ops |

## 에스컬레이션 정책

### P0 에스컬레이션 체인

```
[0분]  → 1차 알림: 온콜 담당자 (Mattermost + Email + SMS)
[15분] → 미확인 시 2차 알림: 팀 리더 (Mattermost + Email + SMS)
[30분] → 미확인 시 3차 알림: 매니저 (Email + SMS + 전화)
[60분] → 미확인 시 4차 알림: 디렉터 (Email + 전화)
```

### P1 에스컬레이션 체인

```
[0분]  → 1차 알림: 담당자 (Mattermost + Email)
[30분] → 미확인 시 2차 알림: 팀 리더 (Mattermost + Email)
[60분] → 미확인 시 3차 알림: 매니저 (Email)
```

### 온콜 로테이션

```yaml
oncall:
  schedule: weekly
  rotation:
    - week: odd   # 홀수 주
      primary: "담당자A"
      secondary: "담당자B"
    - week: even  # 짝수 주
      primary: "담당자B"
      secondary: "담당자A"
  timezone: "Asia/Seoul"
```

## 알림 확인 (Acknowledge)

- 운영자가 알림을 확인하면 에스컬레이션 중지
- Mattermost 리액션 또는 API 호출로 확인 처리
- 확인 이력은 OpenSearch에 기록
