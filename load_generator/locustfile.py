"""
Locust负载测试文件 - TrainTicket系统负载生成器
"""
import logging
from locust import HttpUser, task, between
from flow import SimpleQueryFlow, SimpleLoginFlow, BookingFlow

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrainTicketUser(HttpUser):
    """
    TrainTicket系统的Locust用户类
    模拟用户执行查询和登录操作
    """
    
    # 用户操作之间的等待时间（秒）
    wait_time = between(1, 3)
    
    def on_start(self):
        """用户启动时执行，用于初始化"""
        logger.info("新用户启动")
    
    @task(3)
    def simple_query_flow(self):
        """
        执行简单查询流程（只查票，不买票）
        权重为3，表示执行频率较高
        Flow内部会自动生成起点、终点和日期
        """
        flow = SimpleQueryFlow(self.client)
        result = flow.execute()
        
        if result["success"]:
            logger.info("简单查询流程完成")
        else:
            logger.warning(f"简单查询流程失败: {result.get('error')}")
    
    @task(1)
    def simple_login_flow(self):
        """
        执行简单登录流程
        权重为1，模拟用户登录场景
        Flow内部会自动生成用户名和密码
        """
        flow = SimpleLoginFlow(self.client)
        result = flow.execute()
        
        if result["success"]:
            logger.info("简单登录流程完成")
        else:
            logger.warning(f"简单登录流程失败: {result.get('error')}")
    
    @task(2)
    def booking_flow(self):
        """
        执行订票流程（查票 -> 登录 -> 获取联系人 -> 订票）
        权重为2，模拟完整的购票场景
        Flow内部会自动生成起点、终点、日期和用户凭据
        """
        flow = BookingFlow(self.client)
        result = flow.execute()
        
        if result["success"]:
            logger.info(f"订票流程完成，车次: {result.get('trip_id')}")
        else:
            logger.warning(f"订票流程失败: {result.get('error')}")


"""
运行方法示例：

无头模式运行（快速测试）：
   locust -f locustfile.py --host=http://10.10.1.98:32677 --headless -u 10 -r 3 -t 30s
   参数说明：
   -u 10: 10个并发用户
   -r 3: 每秒启动3个用户（ramp-up rate）
   -t 30s: 运行30秒

保存测试结果到CSV：
   locust -f locustfile.py --host=http://10.10.1.98:32677 --headless -u 100 -r 10 -t 60s --csv=results

持续运行（后台运行，适合长期压力测试）：
    # 前台运行（可以看到实时输出）
    locust -f locustfile.py --host=http://10.10.1.98:32677 --headless -u 100 -r 10
    
    # 后台运行（使用 nohup）
    nohup locust -f locustfile.py --host=http://10.10.1.98:32677 --headless -u 100 -r 10 > locust.log 2>&1 &
    
    # 查看运行状态
    ps aux | grep locust
    
    # 停止后台运行的Locust
    pkill -f locust
"""
