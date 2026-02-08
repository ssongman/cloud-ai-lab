# Mattermost 알림 설정 가이드

## 개요

Mattermost Incoming Webhook을 사용하여 이벤트 알림을 발송합니다.

## Webhook 설정

### 1. Mattermost에서 Incoming Webhook 생성

1. Mattermost → Integrations → Incoming Webhooks
2. "Add Incoming Webhook" 클릭
3. 설정:
   - **Display Name**: Cloud Event Ops Alert
   - **Description**: 클라우드 이벤트 알림 봇
   - **Channel**: 알림 수신 채널 선택
4. "Save" → Webhook URL 복사

### 2. Webhook URL 형식

```
https://<mattermost-host>/hooks/<webhook-id>
```

### 3. 테스트 메시지 전송

```bash
./webhook-test.sh <WEBHOOK_URL>
```

## 메시지 포맷

```json
{
  "channel": "cloud-alerts",
  "username": "CloudEventOps",
  "icon_url": "https://example.com/icon.png",
  "text": "### :warning: P0 Alert\n| 항목 | 내용 |\n|---|---|\n| Provider | Azure |\n| Event | VM Deleted |\n| Resource | prod-web-01 |\n| Time | 2025-01-01 12:00:00 UTC |"
}
```

## 채널 구성 (권장)

| 채널 | 용도 | 대상 |
|-------|------|------|
| `#cloud-alerts-p0` | P0 긴급 알림 | 전체 운영팀 |
| `#cloud-alerts-p1` | P1 중요 알림 | 담당자 |
| `#cloud-alerts-daily` | P2 일간 리포트 | 운영팀 |
