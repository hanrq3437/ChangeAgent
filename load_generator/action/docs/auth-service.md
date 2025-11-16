# Auth Service API 文档

认证服务（ts-auth-service）和用户服务（ts-user-service）的API文档。

## 目录

- [用户注册](#用户注册)
- [用户登录](#用户登录)
- [获取所有用户](#获取所有用户)

---

## 用户注册

创建新用户账户。**该功能经测试，无法使用。**

### API信息
- **Endpoint**: `/api/v1/auth` (ts-auth-service)
- **Method**: `POST`
- **Description**: 创建用户账户（由ts-user-service调用，创建默认角色用户）
- **认证**: 不需要

---

## 用户登录

用户登录并获取认证token。

### API信息
- **Endpoint**: `/api/v1/users/login` (ts-auth-service)
- **Method**: `POST`
- **Description**: 登录检查并分发token给用户
- **认证**: 不需要

### 请求参数

```json
{
  "username": "string",
  "password": "string",
  "verificationCode": "string (可选)"
}
```

### 响应格式

成功响应：
```json
{
  "status": 1,
  "msg": "login success",
  "data": {
    "userId": "string",
    "username": "string",
    "token": "string"
  }
}
```

失败响应：
```json
{
  "status": 0,
  "msg": "Incorrect username or password.",
  "data": null
}
```

或验证码失败：
```json
{
  "status": 0,
  "msg": "Verification failed.",
  "data": null
}
```

### Action方法

**方法名**: `login()`

**入参**:
- `username` (str): 用户名
- `password` (str): 密码

**返回值**:
- `dict[str, object]`: 登录响应数据
  - 成功时返回: `{"status": 1, "msg": "login success", "data": {"userId": "...", "username": "...", "token": "..."}}`
  - 失败时返回: `{"status": 0, "msg": "Error message", "data": null}` 或空字典 `{}`

### 注意事项

- 登录成功后，需要保存返回的 `token`，用于后续需要认证的API请求
- Token通常需要在请求头中添加：`Authorization: Bearer {token}`
- Token可能有有效期限制，过期后需要重新登录
- 可选参数 `verificationCode` 用于验证码验证

---

## 获取所有用户

获取系统中所有用户的信息列表。

### API信息
- **Endpoint**: `/api/v1/users` (ts-auth-service)
- **Method**: `GET`
- **Description**: 获取所有用户信息
- **认证**: 需要，需要在header中带上token，比如`{"Authorization": f"Bearer {token}"}`

### 请求参数

无

### 响应格式

成功响应（直接返回User实体列表，不是Response包装）：
```json
[
  {
    "userId": "string",
    "username": "string",
    "password": "string",
    "roles": ["ROLE_USER"],
    "authorities": [
      {
        "authority": "ROLE_USER"
      }
    ],
    "accountNonExpired": true,
    "accountNonLocked": true,
    "credentialsNonExpired": true,
    "enabled": true
  },
  ...
]
```

### Action方法

**方法名**: `get_all_users()`

**入参**:
- 无

**返回值**:
- `list[dict[str, object]]`: 用户列表
  - 成功时返回: `[{"userId": "...", "username": "...", "password": "...", "roles": [...], ...}, ...]`
  - 失败时返回: 空列表 `[]`

---

## 服务说明

### ts-auth-service
- 主要负责用户认证相关操作
- 提供用户注册、登录功能
- 管理用户token的生成和分发
- User实体包含Spring Security的UserDetails信息（roles, authorities等）

### ts-user-service
- 主要负责用户信息管理
- 提供用户信息的CRUD操作
- 支持按ID、用户名查询用户
- User实体包含用户基本信息（gender, documentType, documentNum, email等）
- 所有API返回都使用Response包装：`{"status": 1, "msg": "...", "data": ...}`

### 认证说明

大部分API需要认证，需要在请求头中添加：
```
Authorization: Bearer {token}
```

其中 `token` 通过登录接口获取。

---

## 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 注意事项

1. **Token管理**: 登录后获取的token需要妥善保存，用于后续API调用
2. **权限控制**: 某些操作（如删除用户、获取所有用户）可能需要管理员权限
3. **密码安全**: 注册和更新用户时，密码应该加密传输
4. **服务选择**: 注意区分 `ts-auth-service` 和 `ts-user-service` 的不同端点
5. **错误处理**: 所有API调用都应该检查响应状态，处理可能的错误情况
6. **响应格式差异**: 
   - `ts-auth-service` 的 `/api/v1/users` GET 直接返回User列表，不使用Response包装
   - `ts-user-service` 的所有API都使用Response包装返回
7. **User实体差异**:
   - `ts-auth-service` 的User包含Spring Security相关字段（roles, authorities等）
   - `ts-user-service` 的User包含用户基本信息（gender, documentType等）
