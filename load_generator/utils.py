"""
工具函数模块 - 提供数据生成、随机选择等工具函数
"""
import random
from datetime import datetime, timedelta
import config


def get_random_station(exclude: list[str] = []) -> str:
    """
    随机选择一个车站
    
    Args:
        exclude: 要排除的车站列表（例如，选择终点时排除起点）
    
    Returns:
        随机选择的车站名称
    """
    available_stations = [s for s in config.DEFAULT_STATIONS if s not in exclude]
    if not available_stations:
        # 如果没有可用车站，返回第一个车站
        return config.DEFAULT_STATIONS[0]
    return random.choice(available_stations)


def get_random_start_station() -> str:
    """
    随机选择一个起点站
    
    Returns:
        随机选择的起点站名称
    """
    return get_random_station()


def get_random_end_station(start_station: str | None = None) -> str:
    """
    随机选择一个终点站（排除起点站）
    
    Args:
        start_station: 起点站名称，如果提供则排除它
    
    Returns:
        随机选择的终点站名称
    """
    exclude = [start_station] if start_station else []
    return get_random_station(exclude)


def get_future_date(days_ahead: int | None = None, max_days: int = 30) -> str:
    """
    生成一个未来的日期字符串
    
    Args:
        days_ahead: 指定多少天后（如果为None则随机选择）
        max_days: 最大天数（当days_ahead为None时使用）
    
    Returns:
        日期字符串，格式：YYYY-MM-DD
    """
    if days_ahead is None:
        days_ahead = random.randint(1, max_days)
    
    future_date = datetime.now() + timedelta(days=days_ahead)
    return future_date.strftime("%Y-%m-%d")


def get_random_travel_date() -> str:
    """
    随机选择一个旅行日期（从配置的日期列表中选择，或生成未来日期）
    
    Returns:
        日期字符串，格式：YYYY-MM-DD
    """
    if config.DEFAULT_TRAVEL_DATES:
        return random.choice(config.DEFAULT_TRAVEL_DATES)
    # 如果没有配置日期，生成一个未来7-30天的随机日期
    return get_future_date(max_days=30)


def get_random_user() -> dict[str, str]:
    """
    随机选择一个用户凭据
    
    Returns:
        包含username和password的字典
    """
    if not config.DEFAULT_USERS:
        # 如果没有配置用户，返回默认值
        return {"username": "fdse_microservices", "password": "111111"}
    return random.choice(config.DEFAULT_USERS)


def get_random_user_credentials() -> tuple[str, str]:
    """
    随机获取一对用户名和密码
    
    Returns:
        (username, password) 元组
    """
    user = get_random_user()
    return user["username"], user["password"]

