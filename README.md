# Python Web API 项目

一个基于 Flask 框架构建的纯后端 API 服务。

## 功能特性

- 🔗 完整的 RESTful API 接口
- 📊 CRUD 操作支持
- ⚡ 轻量级 Flask 框架
- 🛠 标准化 JSON 响应格式
- 🔧 错误处理机制

## 技术栈

- **后端框架**: Flask 2.3.3
- **开发语言**: Python 3.x
- **数据格式**: JSON

## 项目结构

```
py-coding/
├── app.py              # 主应用文件
├── requirements.txt    # 依赖包列表
└── README.md          # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 测试 API

服务器启动后，访问：http://127.0.0.1:5000

## API 接口文档

### 基础信息
- **基础 URL**: `http://127.0.0.1:5000`
- **响应格式**: JSON
- **字符编码**: UTF-8

### 接口列表

#### 1. 获取 API 信息
- **URL**: `/`
- **方法**: GET
- **描述**: 获取 API 基本信息和可用端点

**响应示例**:
```json
{
    "message": "Python Web API 服务",
    "version": "1.0.0",
    "endpoints": {
        "GET /": "API 信息",
        "GET /api/data": "获取所有数据",
        "GET /api/data/<id>": "获取指定 ID 的数据",
        "POST /api/data": "创建新数据",
        "PUT /api/data/<id>": "更新指定 ID 的数据",
        "DELETE /api/data/<id>": "删除指定 ID 的数据"
    }
}
```

#### 2. 获取所有数据
- **URL**: `/api/data`
- **方法**: GET
- **描述**: 获取所有数据列表

**响应示例**:
```json
{
    "status": "success",
    "message": "数据获取成功",
    "count": 3,
    "data": [
        {
            "id": 1,
            "name": "项目1",
            "description": "这是第一个项目",
            "created_at": "2024-01-01"
        }
    ]
}
```

#### 3. 获取单条数据
- **URL**: `/api/data/<id>`
- **方法**: GET
- **描述**: 根据 ID 获取指定数据

**响应示例**:
```json
{
    "status": "success",
    "message": "数据获取成功",
    "data": {
        "id": 1,
        "name": "项目1",
        "description": "这是第一个项目",
        "created_at": "2024-01-01"
    }
}
```

#### 4. 创建新数据
- **URL**: `/api/data`
- **方法**: POST
- **描述**: 创建新的数据记录

**请求体**:
```json
{
    "name": "新项目",
    "description": "项目描述（可选）"
}
```

**响应示例**:
```json
{
    "status": "success",
    "message": "数据创建成功",
    "data": {
        "id": 4,
        "name": "新项目",
        "description": "项目描述",
        "created_at": "2024-01-15 14:30:00"
    }
}
```

#### 5. 更新数据
- **URL**: `/api/data/<id>`
- **方法**: PUT
- **描述**: 更新指定 ID 的数据

**请求体**:
```json
{
    "name": "更新后的项目名",
    "description": "更新后的描述"
}
```

**响应示例**:
```json
{
    "status": "success",
    "message": "数据更新成功",
    "data": {
        "id": 1,
        "name": "更新后的项目名",
        "description": "更新后的描述",
        "created_at": "2024-01-01",
        "updated_at": "2024-01-15 14:35:00"
    }
}
```

#### 6. 删除数据
- **URL**: `/api/data/<id>`
- **方法**: DELETE
- **描述**: 删除指定 ID 的数据

**响应示例**:
```json
{
    "status": "success",
    "message": "ID 为 1 的数据已删除"
}
```

## 测试示例

### 使用 curl 测试

```bash
# 获取 API 信息
curl http://127.0.0.1:5000/

# 获取所有数据
curl http://127.0.0.1:5000/api/data

# 获取指定数据
curl http://127.0.0.1:5000/api/data/1

# 创建新数据
curl -X POST http://127.0.0.1:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name": "测试项目", "description": "这是一个测试项目"}'

# 更新数据
curl -X PUT http://127.0.0.1:5000/api/data/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "更新的项目", "description": "更新的描述"}'

# 删除数据
curl -X DELETE http://127.0.0.1:5000/api/data/1
```

## 错误处理

API 使用标准的 HTTP 状态码：

- `200` - 成功
- `201` - 创建成功
- `400` - 请求错误
- `404` - 资源未找到
- `500` - 服务器内部错误

错误响应格式：
```json
{
    "status": "error",
    "message": "错误描述"
}
```

## 部署

### 生产环境部署

```bash
# 安装 Gunicorn
pip install gunicorn

# 运行生产服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 许可证

MIT License
