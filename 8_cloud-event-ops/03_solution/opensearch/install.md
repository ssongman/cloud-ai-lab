

# OpenSearch 설치 가이드 (Kubernetes)



# 1. 개요

Opensearch, Opensearch Dashbaord 설치가이드



# 2. Opensearch Install

## 1) Helm Repo 추가

```bash
$ helm repo add opensearch https://opensearch-project.github.io/helm-charts/
$ helm repo update

$ helm search repo opensearch
NAME                                    CHART VERSION   APP VERSION     DESCRIPTION
opensearch/opensearch                   3.4.0           3.4.0           A Helm chart for OpenSearch
opensearch/opensearch-dashboards        3.4.0           3.4.0           A Helm chart for OpenSearch Dashboards
opensearch/data-prepper                 0.3.1           2.8.0           A Helm chart for Data Prepper



```



## 2) Namespace 생성

```bash
$ kubectl create namespace opensearch

```



## 3) OpenSearch 설치

> **주의**: OpenSearch 2.12+ 부터 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 환경변수가 필수



### 비밀번호를 Secret으로 관리하는 방법 (권장)

비밀번호는 대문자 + 소문자 + 숫자 + 특수문자 포함, 8자 이상이어야 함

```bash
# 1. Secret 생성
$ kubectl -n opensearch create secret generic opensearch-admin-password \
  --from-literal=password="Opensearchpass123!"

# 삭제시...
$ kubectl -n opensearch delete secret opensearch-admin-password

```



```sh


# 2. Secret 참조로 설치
$ helm upgrade --install opensearch opensearch/opensearch \
  --namespace opensearch \
  --set replicas=1 \
  --set persistence.size=10Gi \
  --set resources.requests.memory=4Gi \
  --set resources.requests.cpu=1000m \
  --set extraEnvs[0].name=OPENSEARCH_INITIAL_ADMIN_PASSWORD \
  --set extraEnvs[0].valueFrom.secretKeyRef.name=opensearch-admin-password \
  --set extraEnvs[0].valueFrom.secretKeyRef.key=password

# 확인
$ helm -n opensearch ls 
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
opensearch      opensearch      1               2026-02-08 09:14:37.939251963 +0000 UTC deployed        opensearch-3.4.0        3.4.0


# 삭제시..
$ helm -n opensearch delete opensearch


```



## 4) 설치 확인

```bash
$ kubectl get pods -n opensearch
NAME                          READY   STATUS    RESTARTS   AGE
opensearch-cluster-master-0   1/1     Running   0          30s


$ kubectl get svc -n opensearch
NAME                                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
opensearch-cluster-master            ClusterIP   10.43.11.105   <none>        9200/TCP,9300/TCP,9600/TCP   30s
opensearch-cluster-master-headless   ClusterIP   None           <none>        9200/TCP,9300/TCP,9600/TCP   30s


```



## 5) 참고

- [OpenSearch Helm Charts](https://github.com/opensearch-project/helm-charts)
- [OpenSearch Documentation](https://opensearch.org/docs/latest/)







# 2. OpenSearch Dashboards



## 1) helm values.yaml

```sh

$ helm search repo opensearch-dashboards
NAME                                    CHART VERSION   APP VERSION     DESCRIPTION
opensearch/opensearch                   3.4.0           3.4.0           A Helm chart for OpenSearch
opensearch/opensearch-dashboards        3.4.0           3.4.0           A Helm chart for OpenSearch Dashboards
opensearch/data-prepper                 0.3.1           2.8.0           A Helm chart for Data Prepper

$ helm show values opensearch/opensearch-dashboards
...
ingress:
  enabled: false
  # For Kubernetes >= 1.18 you should specify the ingress-controller via the field ingressClassName
  # See https://kubernetes.io/blog/2020/04/02/improvements-to-the-ingress-api-in-kubernetes-1.18/#specifying-the-class-of-an-ingress
  # ingressClassName: nginx
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  labels: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          backend:
            serviceName: ""
            servicePort: ""
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local
  
  
```



## 2) OpenSearch Dashboards Install

```bash

$ helm -n opensearch install opensearch-dashboards opensearch/opensearch-dashboards \
  --set opensearchHosts="https://opensearch-cluster-master:9200" \
  --set replicaCount=1 \  
  --set resources.requests.memory=1Gi \
  --set resources.requests.cpu=500m \
  --set resources.limits.memory=2Gi \
  --set resources.limits.cpu=1000m

```



#### values.yaml 방식으로 설치

```sh
$ cat <<'EOF' | helm -n opensearch install opensearch-dashboards opensearch/opensearch-dashboards -f -
opensearchHosts: "https://opensearch-cluster-master:9200"
replicaCount: 1

resources:
  requests:
    memory: 1Gi
    cpu: 500m
  limits:
    memory: 2Gi
    cpu: 1000m

ingress:
  enabled: true
  ingressClassName: traefik
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  labels: {}
  hosts:
    - host: osdb.ssongman.com
      paths:
        - backend:
            service:
              name: opensearch-dashboards
              port:
                number: 80
          path: /
  tls:
    - hosts:
        - osdb.ssongman.com
      secretName: osdb-tls
EOF


```



#### 확인

```sh


$ helm -n opensearch ls
NAME                    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
...
opensearch-dashboards   opensearch      1               2026-02-08 12:02:22.925890907 +0000 UTC deployed        opensearch-dashboards-3.4.0     3.4.0



## 삭제시...
$ helm -n opensearch delete opensearch-dashboards


```



## 2) 설치 확인

```bash
kubectl get pods -n opensearch -l app.kubernetes.io/name=opensearch-dashboards


```



## 3) 접속

```bash
# Port Forward로 로컬 접속
kubectl port-forward svc/opensearch-dashboards 5601:5601 -n opensearch

# 브라우저에서 `http://localhost:5601` 접속



# host 로
https//osdb.ssongman.com


```





### 기본 인증 정보

- Username: `admin`
- Password: `Opensearchpass123!`   opensearch password 



## 대시보드 구성

1. Index Pattern 생성: `cloud-events-*`
2. 기본 대시보드 임포트
3. 시각화 위젯 구성





