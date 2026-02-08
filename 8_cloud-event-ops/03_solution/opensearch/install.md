# OpenSearch 설치 가이드 (Kubernetes)

## 사전 요구사항

- Kubernetes 클러스터 (v1.25+)
- Helm v3
- StorageClass 설정 완료

## 설치 방법

### 1. Helm Repo 추가

```bash
helm repo add opensearch https://opensearch-project.github.io/helm-charts/
helm repo update
```

### 2. Namespace 생성

```bash
kubectl create namespace opensearch
```

### 3. OpenSearch 설치

```bash
helm install opensearch opensearch/opensearch \
  --namespace opensearch \
  --set replicas=3 \
  --set persistence.size=50Gi \
  --set resources.requests.memory=4Gi \
  --set resources.requests.cpu=1000m
```

### 4. 설치 확인

```bash
kubectl get pods -n opensearch
kubectl get svc -n opensearch
```

## 설정 커스터마이징

- `values.yaml` 파일을 통해 상세 설정 가능
- 보안 플러그인, TLS, 리소스 등 조정

## 참고

- [OpenSearch Helm Charts](https://github.com/opensearch-project/helm-charts)
- [OpenSearch Documentation](https://opensearch.org/docs/latest/)
