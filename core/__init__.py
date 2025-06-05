"""
DailyInputCounter 核心功能模块

这个包包含了项目的核心功能：
- keyboard_listener: 键盘监听模块
- character_analyzer: 字符分析模块  
- data_storage: 数据存储模块
"""

__version__ = "1.0.0"
__author__ = "DailyInputCounter Team"

# 导出核心模块
from .keyboard_listener import KeyboardListener
from .character_analyzer import CharacterAnalyzer
from .data_storage import DataStorage

__all__ = ["KeyboardListener", "CharacterAnalyzer", "DataStorage"] 