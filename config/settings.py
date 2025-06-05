"""
DailyInputCounter 配置管理模块

提供应用程序的配置管理功能，包括默认配置、配置文件读写等。
"""

import os
import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class Settings:
    """应用程序设置数据类"""
    
    # 基础设置
    auto_start: bool = True
    data_path: str = "./data"
    save_interval: int = 60  # 自动保存间隔（秒）
    
    # 界面设置
    theme: str = "light"
    show_notifications: bool = True
    window_position: Dict[str, int] = None
    window_size: Dict[str, int] = None
    
    # 统计设置
    chinese_char_range: str = "\\u4e00-\\u9fff"  # 中文字符Unicode范围
    english_char_range: str = "a-zA-Z"  # 英文字符范围
    count_numbers: bool = False  # 是否统计数字
    count_symbols: bool = False  # 是否统计符号
    
    # 高级设置
    debug_mode: bool = False
    log_level: str = "INFO"
    backup_enabled: bool = True
    backup_interval_days: int = 7
    
    def __post_init__(self):
        """初始化后处理"""
        if self.window_position is None:
            self.window_position = {"x": 100, "y": 100}
        if self.window_size is None:
            self.window_size = {"width": 800, "height": 600}


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        self.logger = logging.getLogger(__name__)
        
        # 确定配置文件路径
        if config_file is None:
            # Windows: %APPDATA%/DailyInputCounter/config.json
            if os.name == 'nt':
                app_data = os.environ.get('APPDATA', '')
                self.config_dir = Path(app_data) / "DailyInputCounter"
            else:
                # 其他系统使用当前目录
                self.config_dir = Path.cwd() / "config"
            
            self.config_file = self.config_dir / "config.json"
        else:
            self.config_file = Path(config_file)
            self.config_dir = self.config_file.parent
        
        # 创建配置目录
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.settings = self.load_config()
    
    def load_config(self) -> Settings:
        """
        加载配置文件
        
        Returns:
            Settings: 配置对象
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 创建Settings对象
                settings = Settings()
                
                # 更新配置值
                for key, value in config_data.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)
                    else:
                        self.logger.warning(f"未知配置项: {key}")
                
                self.logger.info(f"配置文件加载成功: {self.config_file}")
                return settings
            else:
                self.logger.info("配置文件不存在，使用默认配置")
                return Settings()
                
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            self.logger.info("使用默认配置")
            return Settings()
    
    def save_config(self) -> bool:
        """
        保存配置到文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            # 转换为字典
            config_data = {}
            for field in self.settings.__dataclass_fields__:
                config_data[field] = getattr(self.settings, field)
            
            # 写入文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"配置文件保存成功: {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        获取配置项的值
        
        Args:
            key: 配置项键名
            default: 默认值
            
        Returns:
            Any: 配置项的值
        """
        return getattr(self.settings, key, default)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """
        设置配置项的值
        
        Args:
            key: 配置项键名
            value: 配置项的值
            
        Returns:
            bool: 设置是否成功
        """
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            return True
        else:
            self.logger.warning(f"无效的配置项: {key}")
            return False
    
    def reset_to_default(self) -> None:
        """重置为默认配置"""
        self.settings = Settings()
        self.logger.info("配置已重置为默认值")
    
    def get_data_path(self) -> Path:
        """获取数据目录路径"""
        data_path = Path(self.settings.data_path)
        if not data_path.is_absolute():
            data_path = Path.cwd() / data_path
        return data_path
    
    def ensure_data_directory(self) -> bool:
        """确保数据目录存在"""
        try:
            data_path = self.get_data_path()
            data_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"创建数据目录失败: {e}")
            return False


# 全局配置管理器实例
config_manager = ConfigManager()

def get_config() -> ConfigManager:
    """获取全局配置管理器实例"""
    return config_manager

def get_settings() -> Settings:
    """获取当前设置对象"""
    return config_manager.settings 