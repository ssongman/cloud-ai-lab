# Event Catalog - 이벤트 분류 기준

## 우선순위 정의

| 등급 | 설명 | 대응 시간 | 알림 채널 |
|------|------|-----------|-----------|
| **P0** | 긴급 - 즉시 대응 필요 | < 5분 | Mattermost + Email + SMS |
| **P1** | 중요 - 빠른 대응 필요 | < 30분 | Mattermost + Email |
| **P2** | 참고 - 인지 필요 | 일간 리포트 | Email (일간 다이제스트) |

## Azure 이벤트 목록

### P0 (긴급)
| 이벤트 | 설명 |
|--------|------|
| `Microsoft.Compute/virtualMachines/delete` | VM 삭제 |
| `Microsoft.Network/networkSecurityGroups/securityRules/write` | NSG 룰 변경 |
| `Microsoft.Authorization/roleAssignments/write` | RBAC 역할 할당 변경 |
| `Microsoft.KeyVault/vaults/delete` | Key Vault 삭제 |
| `Microsoft.Sql/servers/firewallRules/write` | SQL 방화벽 룰 변경 |

### P1 (중요)
| 이벤트 | 설명 |
|--------|------|
| `Microsoft.Compute/virtualMachines/write` | VM 설정 변경 |
| `Microsoft.Storage/storageAccounts/write` | 스토리지 설정 변경 |
| `Microsoft.Network/virtualNetworks/write` | VNet 변경 |
| `Microsoft.Web/sites/config/write` | App Service 설정 변경 |

### P2 (참고)
| 이벤트 | 설명 |
|--------|------|
| `Microsoft.Compute/virtualMachines/start` | VM 시작 |
| `Microsoft.Compute/virtualMachines/deallocate` | VM 할당 해제 |
| `Microsoft.Resources/tags/write` | 리소스 태그 변경 |

## AWS 이벤트 목록

### P0 (긴급)
| 이벤트 | 설명 |
|--------|------|
| `TerminateInstances` | EC2 인스턴스 종료 |
| `AuthorizeSecurityGroupIngress` | 보안 그룹 인바운드 룰 변경 |
| `CreateUser` / `DeleteUser` | IAM 사용자 생성/삭제 |
| `PutBucketPolicy` | S3 버킷 정책 변경 |
| `DeleteDBInstance` | RDS 인스턴스 삭제 |

### P1 (중요)
| 이벤트 | 설명 |
|--------|------|
| `RunInstances` | EC2 인스턴스 생성 |
| `ModifyDBInstance` | RDS 설정 변경 |
| `CreateVpc` / `DeleteVpc` | VPC 생성/삭제 |
| `UpdateFunctionConfiguration` | Lambda 설정 변경 |

### P2 (참고)
| 이벤트 | 설명 |
|--------|------|
| `StartInstances` / `StopInstances` | EC2 시작/중지 |
| `CreateSnapshot` | EBS 스냅샷 생성 |
| `TagResource` | 리소스 태그 변경 |
