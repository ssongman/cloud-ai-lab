#!/bin/bash
set -euo pipefail

# Mattermost Webhook 테스트 스크립트

WEBHOOK_URL="${1:?Usage: $0 <WEBHOOK_URL>}"

echo "=== Mattermost Webhook 테스트 ==="

curl -s -X POST "${WEBHOOK_URL}" \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "CloudEventOps",
    "text": "### :white_check_mark: Webhook 테스트 성공\n\nCloud Event Ops 알림 시스템 연동 테스트입니다.\n\n| 항목 | 내용 |\n|---|---|\n| 상태 | 테스트 |\n| 시간 | '"$(date -u +%Y-%m-%dT%H:%M:%SZ)"' |\n| 메시지 | Webhook 연동이 정상적으로 동작합니다. |"
  }'

echo ""
echo "=== 테스트 완료 ==="
