# Detection Rules - 탐지 룰 정의

## 룰 포맷

```yaml
rule_id: "<unique-id>"
name: "<룰 이름>"
description: "<설명>"
severity: P0 | P1 | P2
enabled: true | false
provider: azure | aws | all
conditions:
  event_type: "<이벤트 타입 패턴>"
  status: "<상태>"
  resource_pattern: "<리소스 패턴 (선택)>"
  time_window: "<시간 윈도우 (선택)>"
  threshold: <횟수 임계값 (선택)>
channels: ["mattermost", "email", "sms"]
cooldown_minutes: <중복 알림 방지 시간>
tags: []
```

## Azure 탐지 룰

### AZURE-001: VM 삭제 감지
```yaml
rule_id: "azure-001"
name: "Azure VM 삭제 감지"
severity: P0
provider: azure
conditions:
  event_type: "Microsoft.Compute/virtualMachines/delete"
  status: "Succeeded"
channels: ["mattermost", "email", "sms"]
cooldown_minutes: 30
```

### AZURE-002: NSG 룰 변경 감지
```yaml
rule_id: "azure-002"
name: "NSG 보안 룰 변경 감지"
severity: P0
provider: azure
conditions:
  event_type: "Microsoft.Network/networkSecurityGroups/securityRules/write"
  status: "Succeeded"
channels: ["mattermost", "email"]
cooldown_minutes: 15
```

### AZURE-003: RBAC 변경 감지
```yaml
rule_id: "azure-003"
name: "RBAC 역할 할당 변경"
severity: P0
provider: azure
conditions:
  event_type: "Microsoft.Authorization/roleAssignments/write"
channels: ["mattermost", "email", "sms"]
cooldown_minutes: 60
```

## AWS 탐지 룰

### AWS-001: EC2 인스턴스 종료 감지
```yaml
rule_id: "aws-001"
name: "EC2 인스턴스 종료 감지"
severity: P0
provider: aws
conditions:
  event_type: "TerminateInstances"
  status: "Success"
channels: ["mattermost", "email", "sms"]
cooldown_minutes: 30
```

### AWS-002: 보안 그룹 변경 감지
```yaml
rule_id: "aws-002"
name: "보안 그룹 인바운드 룰 변경"
severity: P0
provider: aws
conditions:
  event_type: "AuthorizeSecurityGroupIngress"
channels: ["mattermost", "email"]
cooldown_minutes: 15
```

### AWS-003: IAM 사용자 변경 감지
```yaml
rule_id: "aws-003"
name: "IAM 사용자 생성/삭제"
severity: P0
provider: aws
conditions:
  event_type: "CreateUser|DeleteUser"
channels: ["mattermost", "email", "sms"]
cooldown_minutes: 60
```

## 복합 탐지 룰

### COMP-001: 다중 실패 감지 (Brute Force)
```yaml
rule_id: "comp-001"
name: "다중 인증 실패 감지"
severity: P0
provider: all
conditions:
  event_type: "SignInFailure|ConsoleLoginFailure"
  status: "Failure"
  time_window: "5m"
  threshold: 10
channels: ["mattermost", "email", "sms"]
cooldown_minutes: 30
```
