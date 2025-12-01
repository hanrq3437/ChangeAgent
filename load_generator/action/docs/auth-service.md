# Auth Service API 文档

认证服务（ts-auth-service）和用户服务（ts-user-service）的API文档。

## 目录

- [用户注册](#用户注册)
- [用户登录](#用户登录)
- [获取所有用户](#获取所有用户)
- [删除用户](#删除用户)

---

## 用户注册

创建新的用户账户。

### API信息
- **Endpoint**: `/api/v1/adminuserservice/users` (ts-admin-user-service)
- **Method**: `POST`
- **Description**: 创建用户账户
- **认证**: 需要，需要在header中带上token，比如`{"Authorization": f"Bearer {token}"}`

### 请求参数

```json
{
  "userName": "string",
  "password": "string",
  "gender": "integer",
  "documentType": "integer",
  "documentNum": "string",
  "email": "string"
}
```

参数说明：
- `userName` (string, 必填): 用户名
- `password` (string, 必填): 密码
- `gender` (integer, 必填): 性别，1表示男性，0表示女性
- `documentType` (integer, 必填): 证件类型，1表示身份证
- `documentNum` (string, 必填): 证件号码，通常为18位身份证号
- `email` (string, 必填): 邮箱地址

### 响应格式

成功响应：
```json
{
  "status": 1,
  "msg": "REGISTER USER SUCCESS",
  "data": {
    "userId": "string",
    "userName": "string",
    "password": "string",
    "gender": 1,
    "documentType": 1,
    "documentNum": "string",
    "email": "string"
  }
}
```

失败响应：
```json
{
  "status": 0,
  "msg": "Error message",
  "data": null
}
```

### Action方法

**方法名**: `register()`

**入参**:
- `user_name` (str): 用户名
- `password` (str): 密码
- `gender` (int): 性别，1表示男性，0表示女性
- `document_type` (int): 证件类型，1表示身份证
- `document_num` (str): 证件号码
- `email` (str): 邮箱地址
- `token` (str): 认证token（需要先通过login方法获取）

**返回值**:
- `dict[str, object]`: 注册响应数据
  - 成功时返回: `{"status": 1, "msg": "REGISTER USER SUCCESS", "data": {"userId": "...", "userName": "...", ...}}`
  - 失败时返回: `{"status": 0, "msg": "Error message", "data": null}` 或空字典 `{}`

### 注意事项

- 注册接口需要先登录获取token，然后在请求头中添加：`Authorization: Bearer {token}`
- 证件号码通常为18位身份证号
- 性别字段：1表示男性，0表示女性
- 证件类型：1表示身份证
- 注册成功后，返回的数据中包含生成的 `userId`，可用于后续操作



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

## 删除用户

删除指定的用户账户。

### API信息
- **Endpoint**: `/api/v1/adminuserservice/users/{userId}` (ts-admin-user-service)
- **Method**: `DELETE`
- **Description**: 删除指定用户账户
- **认证**: 需要，需要在header中带上token，比如`{"Authorization": f"Bearer {token}"}`

### 请求参数

**路径参数**:
- `userId` (string, 必填): 用户ID，系统内部的UUID格式标识符（例如：`ed5c5491-c4e1-431d-bc14-cff9e04c9d75`）

**重要说明**:
- `userId` **不是** `userName`（用户名），而是系统内部生成的一串UUID格式的唯一标识符
- 要删除用户，必须先获取该用户的 `userId`，常见方式包括：
  1. **从注册响应中获取**：注册用户时，响应中的 `data.userId` 字段包含新创建用户的ID
  2. **从登录响应中获取**：登录成功后，响应中的 `data.userId` 字段包含当前登录用户的ID
  3. **从用户列表查询**：调用"获取所有用户"接口，从返回的用户列表中找到目标用户的 `userId`
  4. **通过用户名查询**：如果有按用户名查询用户的接口，可以从查询结果中获取 `userId`

### 响应格式

成功响应：
```json
{
  "status": 1,
  "msg": "DELETE SUCCESS",
  "data": null
}
```

失败响应：
```json
{
  "status": 0,
  "msg": "Error message",
  "data": null
}
```

### Action方法

**方法名**: `delete_user()`

**入参**:
- `user_id` (str): 用户ID（UUID格式），不是用户名
- `token` (str): 认证token（需要先通过login方法获取）

**返回值**:
- `dict[str, object]`: 删除响应数据
  - 成功时返回: `{"status": 1, "msg": "DELETE SUCCESS", "data": null}`
  - 失败时返回: `{"status": 0, "msg": "Error message", "data": null}` 或空字典 `{}`

### 注意事项

- 删除接口需要先登录获取token，然后在请求头中添加：`Authorization: Bearer {token}`
- **重要**：`userId` 是系统内部的UUID标识符，不是 `userName`（用户名）
- 删除操作不可逆，请谨慎使用
- 通常需要管理员权限才能删除用户
- 如果用户不存在或已被删除，可能会返回错误信息


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
