# Contact Service API 文档

联系人服务（ts-contacts-service）的API文档。

## 目录

- [根据账户ID获取联系人](#根据账户ID获取联系人)

---

## 根据账户ID获取联系人

根据账户ID获取该账户的所有联系人信息。

### API信息
- **Endpoint**: `/api/v1/contactservice/contacts/account/{accountId}` (ts-contacts-service)
- **Method**: `GET`
- **Description**: 根据账户ID查询该账户的所有联系人
- **认证**: 需要，需要在header中带上token，比如`{"Authorization": f"Bearer {token}"}`

### 请求参数

**路径参数**:
- `accountId` (string, 必填): 账户ID，UUID格式（例如：`4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f`）

### 响应格式

成功响应：
```json
{
  "status": 1,
  "msg": "Success",
  "data": [
    {
      "id": "38e3e89a-fc5a-45f8-9deb-8352c4c3c606",
      "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
      "name": "Contacts_One",
      "documentType": 1,
      "documentNumber": "DocumentNumber_One",
      "phoneNumber": "ContactsPhoneNum_One"
    },
    {
      "id": "36ca3ee9-10f7-40cd-b315-103313b5427a",
      "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
      "name": "Contacts_Two",
      "documentType": 1,
      "documentNumber": "DocumentNumber_Two",
      "phoneNumber": "ContactsPhoneNum_Two"
    }
  ]
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

**响应字段说明**:
- `status` (integer): 状态码，1表示成功，0表示失败
- `msg` (string): 响应消息
- `data` (array): 联系人列表，每个联系人包含：
  - `id` (string): 联系人ID（UUID格式）
  - `accountId` (string): 账户ID（UUID格式）
  - `name` (string): 联系人姓名
  - `documentType` (integer): 证件类型，1表示身份证
  - `documentNumber` (string): 证件号码
  - `phoneNumber` (string): 电话号码

### Action方法

**方法名**: `get_contacts_by_account()`

**入参**:
- `account_id` (str): 账户ID（UUID格式）
- `token` (str): 认证token（需要先通过login方法获取）

**返回值**:
- `list[dict[str, object]]`: 联系人列表
  - 成功时返回: `[{"id": "...", "accountId": "...", "name": "...", "documentType": 1, "documentNumber": "...", "phoneNumber": "..."}, ...]`
  - 失败时返回: 空列表 `[]`

### 注意事项

- 该接口需要先登录获取token，然后在请求头中添加：`Authorization: Bearer {token}`
- `accountId` 必须是有效的UUID格式
- 如果账户不存在或没有联系人，返回的 `data` 可能为空数组 `[]`
- 联系人ID（`id`）可用于后续的预订车票等操作
- 证件类型：1表示身份证

---

## 服务说明

### ts-contacts-service
- 主要负责联系人信息管理
- 提供联系人的CRUD操作
- 支持按账户ID、联系人ID查询联系人
- 所有API返回都使用Response包装：`{"status": 1, "msg": "...", "data": ...}`

### 认证说明

该服务的大部分API需要认证，需要在请求头中添加：
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
2. **账户ID格式**: `accountId` 必须是有效的UUID格式
3. **联系人ID**: 联系人ID（`id`）是系统内部的UUID标识符，可用于预订车票等操作
4. **错误处理**: 所有API调用都应该检查响应状态，处理可能的错误情况
5. **响应格式**: 所有API都使用Response包装返回：`{"status": 1, "msg": "...", "data": ...}`

