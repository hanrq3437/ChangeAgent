# TrainTicket 负载生成器

基于Locust实现的TrainTicket微服务系统负载生成器，用于自动生成工作负载并收集正常运行场景下的数据。

## 功能特性

- ✅ **模块化设计**：使用Action和Flow模式，便于扩展和维护
- ✅ **真实业务流程**：模拟完整的用户购票流程（查票 → 登录 → 买票 → 付款）
- ✅ **灵活配置**：支持高速列车(G/D)和普通列车的购票流程
- ✅ **易于扩展**：可以轻松添加新的Action和Flow

## 项目结构

```
load_generator/
├── action/               # Action模块 - 按功能分类的API操作类
│   ├── __init__.py
│   ├── base_action.py    # Action基类
│   ├── auth_action.py    # 认证相关操作（登录、注册）
│   ├── query_action.py   # 查询相关操作（查票、查站点）
│   ├── booking_action.py # 预订相关操作（买票、查询订单）
│   └── payment_action.py # 支付相关操作（付款、账户管理）
├── flow/                 # Flow模块 - 按复杂程度分类的业务流程
│   ├── __init__.py
│   ├── base_flow.py      # Flow基类
│   ├── simple_flow.py    # 简单流程（只查票、只登录）
│   ├── booking_flow.py   # 完整购票流程（查票→登录→买票→付款）
│   └── complex_flow.py   # 复杂流程（包含订单确认等额外步骤）
├── config.py             # 配置文件
├── locustfile.py         # Locust主文件
├── requirements.txt      # 依赖包
└── README.md            # 本文档
```

## 架构设计

### Action模块设计

采用**多个类有继承关系**的设计方式，原因如下：

1. **职责分离**：每个Action类负责一类功能（认证、查询、预订、支付）
2. **易于维护**：修改某个功能不影响其他功能
3. **易于扩展**：添加新功能只需添加新的Action类
4. **符合单一职责原则**：每个类只做一件事

所有Action类继承自 `BaseAction`，提供通用的HTTP请求方法（`_post`, `_get`）。

### Flow模块设计

按**复杂程度**分类：

- **SimpleFlow**：简单流程，只包含单个或少量操作
  - `SimpleQueryFlow`：只执行查票操作
  - `SimpleLoginFlow`：只执行登录操作

- **BookingFlow**：完整购票流程
  - 查票 → 登录 → 买票 → 付款

- **ComplexFlow**：复杂流程，包含多个步骤或子流程
  - `ComplexBookingFlow`：完整购票 + 订单确认 + 支付状态查询

## 安装

1. 安装Python依赖：

```bash
pip install -r requirements.txt
```

## 配置

编辑 `config.py` 文件来配置TrainTicket系统的地址和其他参数：

```python
# TrainTicket系统的基础URL
BASE_URL = os.getenv("TRAINTICKET_BASE_URL", "http://localhost:8080")

# 默认测试用户
DEFAULT_USERS = [
    {"username": "fdse_microservices", "password": "111111"},
]
```

也可以通过环境变量设置：

```bash
export TRAINTICKET_BASE_URL=http://your-trainticket-host:8080
```

## 使用方法

### 1. 启动Locust Web界面

```bash
locust -f locustfile.py --host=http://localhost:8080
```

然后在浏览器中打开 `http://localhost:8080`（注意：这是Locust的Web界面，不是TrainTicket系统）

### 2. 使用命令行模式

```bash
# 无Web界面模式，直接运行
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --host=http://localhost:8080

# 参数说明：
# -u 10: 10个并发用户
# -r 2: 每秒启动2个用户
# -t 60s: 运行60秒
# --host: TrainTicket系统的基础URL
```

### 3. 分布式运行

```bash
# 主节点
locust -f locustfile.py --master --host=http://localhost:8080

# 从节点（在另一台机器上）
locust -f locustfile.py --worker --master-host=<master-ip>
```

## 工作流程

负载生成器模拟以下完整的用户购票流程：

1. **查票（QueryTicketAction）**
   - 随机选择起点站和终点站
   - 查询指定日期的车次信息
   - 选择有票的车次

2. **登录（LoginAction）**
   - 使用配置的用户名和密码登录
   - 获取认证token

3. **买票（PreserveTicketAction）**
   - 使用查询到的车次信息预订车票
   - 创建订单

4. **付款（PaymentAction）**
   - 对创建的订单进行支付

## 扩展开发

### 添加新的Action类

1. 在 `action/` 目录下创建新的Action文件，例如 `cancel_action.py`：

```python
from .base_action import BaseAction
from typing import Dict, Any

class CancelAction(BaseAction):
    """取消订单相关的API操作"""
    
    def cancel_order(self, order_id: str, user_id: str) -> Dict[str, Any]:
        """取消订单"""
        return self._get(
            f"/api/v1/cancelservice/cancel/{order_id}/{user_id}",
            name="cancel.order"
        )
```

2. 在 `action/__init__.py` 中导出新类：

```python
from .cancel_action import CancelAction
__all__ = [..., "CancelAction"]
```

### 添加新的Flow

1. 在 `flow/` 目录下创建新的Flow文件，例如 `cancel_flow.py`：

```python
from .base_flow import BaseFlow
from typing import Dict, Any, Optional

class CancelFlow(BaseFlow):
    """取消订单流程"""
    
    def execute(self, order_id: str, user_id: str) -> Dict[str, Any]:
        """执行取消订单流程"""
        result = {"success": False}
        try:
            # 使用BaseFlow中已初始化的Action
            cancel_result = self.booking.cancel_order(order_id, user_id)
            result["success"] = True
            result["data"] = cancel_result
        except Exception as e:
            result["error"] = str(e)
        return result
```

2. 在 `flow/__init__.py` 中导出新类

3. 在 `locustfile.py` 中添加新的task：

```python
from flow import CancelFlow

@task(1)
def cancel_flow_task(self):
    flow = CancelFlow(self.client)
    result = flow.execute(order_id="...", user_id="...")
```

## 注意事项

1. **用户账号**：确保配置的用户账号在TrainTicket系统中存在且可用
2. **系统地址**：确保 `BASE_URL` 配置正确，指向已部署的TrainTicket系统
3. **网络连接**：确保负载生成器能够访问TrainTicket系统的所有服务
4. **数据清理**：长时间运行可能会产生大量测试数据，需要定期清理

## 故障排查

### 连接错误

- 检查TrainTicket系统是否正常运行
- 检查 `BASE_URL` 配置是否正确
- 检查网络连接和防火墙设置

### 认证失败

- 检查用户名和密码是否正确
- 检查用户账号是否在系统中存在

### 查票失败

- 检查是否有可用的车次数据
- 检查日期格式是否正确（YYYY-MM-DD）

### 买票失败

- 检查是否有余票
- 检查联系人ID是否正确
- 检查用户是否有足够的余额

## 许可证

本项目用于AIOps研究和TrainTicket系统测试。

