"""
DailyInputCounter 配置管理模块

这个包包含了项目的配置管理功能：
- settings: 设置配置管理
"""

__version__ = "1.0.0"
__author__ = "DailyInputCounter Team"

# 导出配置模块
from .settings import Settings, ConfigManager

__all__ = ["Settings", "ConfigManager"] 