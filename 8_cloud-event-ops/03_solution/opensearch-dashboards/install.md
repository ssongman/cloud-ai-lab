# OpenSearch Dashboards 설치 가이드 (Kubernetes)

## 사전 요구사항

- OpenSearch 클러스터 설치 완료
- Helm v3

## 설치 방법

### 1. OpenSearch Dashboards 설치

```bash
helm install opensearch-dashboards opensearch/opensearch-dashboards \
  --namespace opensearch \
  --set opensearchHosts="https://opensearch-cluster-master:9200" \
  --set replicaCount=1 \
  --set resources.requests.memory=1Gi \
  --set resources.requests.cpu=500m
```

### 2. 설치 확인

```bash
kubectl get pods -n opensearch -l app.kubernetes.io/name=opensearch-dashboards
```

### 3. 접속

```bash
# Port Forward로 로컬 접속
kubectl port-forward svc/opensearch-dashboards 5601:5601 -n opensearch
```

브라우저에서 `http://localhost:5601` 접속

### 기본 인증 정보

- Username: `admin`
- Password: `admin` (초기값, 반드시 변경 필요)

## 대시보드 구성

1. Index Pattern 생성: `cloud-events-*`
2. 기본 대시보드 임포트
3. 시각화 위젯 구성
