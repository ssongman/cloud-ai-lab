OpenSearch Dashboard 자체에는 내장된 CLI가 없지만, **Dev Tools**라는 기능이 있어서 콘솔처럼 사용할 수 있습니다.



## OpenSearch Dashboard에서 쿼리하기



**Dev Tools 사용 방법:**

1. OpenSearch Dashboard에 접속
2. 왼쪽 메뉴에서 **"Dev Tools"** 또는 **"개발 도구"** 클릭
3. Console 화면에서 REST API 형식으로 쿼리 작성

**샘플 쿼리:**

```bash
# 모든 인덱스 목록 조회
GET _cat/indices

# 특정 인덱스의 매핑 정보 확인
GET /my-index/_mapping

# 특정 인덱스에서 문서 조회 (최대 10개)
GET /my-index/_search
{
  "size": 10
}

# 모든 문서 조회
GET /my-index/_search
{
  "query": {
    "match_all": {}
  }
}

# 조건부 검색
GET /my-index/_search
{
  "query": {
    "match": {
      "field_name": "search_value"
    }
  }
}
```



## 실제 cli1

```json

GET _search
{
  "query": {
    "match_all": {}
  }
}

Get _cat/indices

Get /otel-v1-apm-service-map-sample/_mapping


Get /otel-v1-apm-service-map-sample/_search
{
  "size": 10
}

```



## 실제 cli2

```sh
GET _search
{
  "query": {
    "match_all": {}
  }
}

# index 종류
$ Get _cat/indices
green open opensearch_dashboards_sample_data_logs      xA8LpMT-TFyWt_S2kz_RGw 1 0 14074  0   8.2mb   8.2mb
green open opensearch_dashboards_sample_data_flights   j_KaoVUtQrGflDfOVdWlJg 1 0 13059  0   5.7mb   5.7mb
green open opensearch_dashboards_sample_data_ecommerce r2vVDBekRwmNGQYuKGRsZA 1 0  4675  0     4mb     4mb

# 구조확인
$ Get /opensearch_dashboards_sample_data_logs/_mapping

# 샘플 10개
$ Get /opensearch_dashboards_sample_data_logs/_search
{
  "size": 10
}


# 특정 날짜와 IP로 필터링하여 message를 조회하는 쿼리
$ GET /opensearch_dashboards_sample_data_logs/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "clientip": "120.49.143.213"
          }
        },
        {
          "range": {
            "timestamp": {
              "gte": "2026-02-01T00:00:00",
              "lt": "2026-02-02T00:00:00"
            }
          }
        }
      ]
    }
  },
  "_source": ["timestamp", "clientip", "message"],
  "size": 100
}


```





## curl 명령으로 조회

터미널에서 직접 조회하려면 `curl`을 사용할 수 있습니다:

```bash
# 인덱스 목록
curl -X GET "localhost:9200/_cat/indices?v"

# 특정 인덱스 조회
curl -X GET "localhost:9200/my-index/_search?pretty"

# 조건부 검색
curl -X GET "localhost:9200/my-index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}
'
```

Dev Tools가 가장 편리하고 문법 하이라이팅, 자동완성 등의 기능도 제공하므로 추천드립니다!