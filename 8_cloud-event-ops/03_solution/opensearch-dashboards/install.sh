#!/bin/bash
set -euo pipefail

# OpenSearch Dashboards Kubernetes 설치 스크립트

NAMESPACE="opensearch"
RELEASE_NAME="opensearch-dashboards"

echo "=== OpenSearch Dashboards 설치 시작 ==="

# 1. OpenSearch Dashboards 설치
echo "[1/3] OpenSearch Dashboards 설치..."
helm upgrade --install "${RELEASE_NAME}" opensearch/opensearch-dashboards \
  --namespace "${NAMESPACE}" \
  --set opensearchHosts="https://opensearch-cluster-master:9200" \
  --set replicaCount=1 \
  --set resources.requests.memory=1Gi \
  --set resources.requests.cpu=500m \
  --set resources.limits.memory=2Gi \
  --set resources.limits.cpu=1000m \
  --wait --timeout=300s

# 2. 설치 확인
echo "[2/3] 설치 확인..."
kubectl get pods -n "${NAMESPACE}" -l app.kubernetes.io/name=opensearch-dashboards

# 3. 접속 정보 출력
echo "[3/3] 접속 정보..."
echo "Port Forward: kubectl port-forward svc/${RELEASE_NAME} 5601:5601 -n ${NAMESPACE}"
echo "URL: http://localhost:5601"

echo "=== OpenSearch Dashboards 설치 완료 ==="
