---
name: api-development
description: API 开发与调试。当需要设计 RESTful API、编写 API 端点、调试 HTTP 请求、编写 API 测试、或对接美柚后端（napi.xmmeiyou.com）时使用此 skill。覆盖 API 设计规范、OpenAPI 文档、请求调试、错误处理全流程。
---

# API 开发 Skill

## 概述

覆盖 API 全生命周期开发的标准化流程，从设计规范到实现、测试、文档，适用于美柚后端 API（napi.xmmeiyou.com）及其他内部服务。

## 适用场景

- 新 API 端点设计与实现
- 已有 API 的功能扩展或重构
- API 对接与调试
- API 文档生成（OpenAPI/Swagger）
- API 测试用例编写

## API 设计规范

### RESTful 命名规范

| 操作 | 方法 | 路径 | 示例 |
|------|------|------|------|
| 列表查询 | GET | `/v1/{resources}` | `GET /v1/consultations` |
| 单个查询 | GET | `/v1/{resources}/{id}` | `GET /v1/consultations/123` |
| 创建 | POST | `/v1/{resources}` | `POST /v1/consultations` |
| 全量更新 | PUT | `/v1/{resources}/{id}` | `PUT /v1/consultations/123` |
| 部分更新 | PATCH | `/v1/{resources}/{id}` | `PATCH /v1/consultations/123` |
| 删除 | DELETE | `/v1/{resources}/{id}` | `DELETE /v1/consultations/123` |

### 请求/响应格式

```json
// 成功响应
{
  "code": 0,
  "message": "success",
  "data": { ... }
}

// 错误响应
{
  "code": 40001,
  "message": "参数错误：缺少必填字段",
  "data": null
}

// 分页响应
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

### 状态码规范

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | 成功 | GET/PUT/PATCH 成功 |
| 201 | 已创建 | POST 创建资源成功 |
| 204 | 无内容 | DELETE 成功 |
| 400 | 请求错误 | 参数校验失败 |
| 401 | 未认证 | Token 过期或无效 |
| 403 | 无权限 | 权限不足 |
| 404 | 未找到 | 资源不存在 |
| 422 | 无法处理 | 业务逻辑校验失败 |
| 429 | 请求过多 | 触发限流 |
| 500 | 服务器错误 | 内部异常 |
| 502 | 网关错误 | 上游服务不可用 |
| 503 | 服务不可用 | 维护中或过载 |

## 开发工作流

### Step 1: 理解需求

- 明确 API 的输入、输出、业务逻辑
- 确认认证方式（JWT / API Key / OAuth）
- 确认限流策略

### Step 2: 编写 API 规范（Design First）

```yaml
# OpenAPI 3.0 格式
openapi: "3.0.0"
info:
  title: AI Consultation API
  version: "1.0.0"
paths:
  /v1/consultations:
    post:
      summary: 创建问诊记录
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [patient_id, chief_complaint]
              properties:
                patient_id:
                  type: string
                chief_complaint:
                  type: string
                department:
                  type: string
      responses:
        '201':
          description: 创建成功
        '400':
          description: 参数错误
```

### Step 3: 实现端点

- TypeScript/Node.js 或 Python/FastAPI
- 参数校验 + 业务逻辑 + 数据持久化
- 错误处理与日志

### Step 4: 编写测试

```python
# API 测试用例模板
import requests

BASE_URL = "https://napi.xmmeiyou.com"

def test_create_consultation():
    resp = requests.post(
        f"{BASE_URL}/v1/consultations",
        json={
            "patient_id": "test_001",
            "chief_complaint": "孕期腹痛",
            "department": "obstetrics"
        },
        headers={"Authorization": "Bearer <token>"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["code"] == 0
    assert "id" in data["data"]
```

### Step 5: 调试与验证

使用 Claude_in_Chrome 或 curl 进行 API 调试：

```bash
# 基本请求
curl -s -w '\nHTTP_STATUS:%{http_code}' \
  -X POST https://napi.xmmeiyou.com/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model":"model-name","input":"query","stream":false}'

# 查看响应头
curl -sI https://napi.xmmeiyou.com/v1/health

# 性能测试
curl -s -w '\nTime: %{time_total}s' \
  -X POST https://napi.xmmeiyou.com/v1/endpoint \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 错误处理模式

```python
# 统一错误处理
class APIError(Exception):
    def __init__(self, code: int, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

# 业务错误码定义
ERROR_CODES = {
    "INVALID_PARAM": (40001, "参数错误"),
    "AUTH_FAILED": (40100, "认证失败"),
    "TOKEN_EXPIRED": (40101, "Token过期"),
    "PERMISSION_DENIED": (40300, "权限不足"),
    "NOT_FOUND": (40400, "资源不存在"),
    "RATE_LIMITED": (42900, "请求频率超限"),
    "INTERNAL_ERROR": (50000, "内部错误"),
}
```

## 关键约束

- 所有 AI 模型调用 API 必须记录 request_id 用于追溯
- 医学相关 API 须包含 disclaimer 字段
- 敏感数据传输使用 HTTPS 加密
- API 密钥不得硬编码，使用环境变量或密钥管理服务
- 生产环境 API 变更需走灰度发布流程
- 与 CC-Switch 代理协作时注意 base_url 转发配置
