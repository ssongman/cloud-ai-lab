#!/bin/bash
set -euo pipefail

# OpenSearch Kubernetes 설치 스크립트

NAMESPACE="opensearch"
RELEASE_NAME="opensearch"

echo "=== OpenSearch 설치 시작 ==="

# 1. Helm repo 추가
echo "[1/4] Helm repo 추가..."
helm repo add opensearch https://opensearch-project.github.io/helm-charts/ || true
helm repo update

# 2. Namespace 생성
echo "[2/4] Namespace 생성..."
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

# 3. OpenSearch 설치
echo "[3/4] OpenSearch 설치..."
helm upgrade --install "${RELEASE_NAME}" opensearch/opensearch \
  --namespace "${NAMESPACE}" \
  --set replicas=3 \
  --set persistence.size=50Gi \
  --set resources.requests.memory=4Gi \
  --set resources.requests.cpu=1000m \
  --set resources.limits.memory=8Gi \
  --set resources.limits.cpu=2000m \
  --wait --timeout=600s

# 4. 설치 확인
echo "[4/4] 설치 확인..."
kubectl get pods -n "${NAMESPACE}"
kubectl get svc -n "${NAMESPACE}"

echo "=== OpenSearch 설치 완료 ==="
