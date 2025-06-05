#!/usr/bin/env python3
"""
Character Analyzer - 字符分析器

负责对键盘输入的字符进行智能分类，区分中文字符和英文字符。
这是MVP版本，专注于核心功能实现。

作者：DailyInputCounter Team
版本：1.0.0-mvp
"""

import re
import logging

logger = logging.getLogger(__name__)


class CharacterAnalyzer:
    """字符分析器 - MVP版本"""
    
    # 字符分类正则表达式
    CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]')  # 中文汉字范围
    ENGLISH_PATTERN = re.compile(r'[a-zA-Z]')         # 英文字母
    
    def __init__(self):
        """初始化字符分析器"""
        logger.info("字符分析器初始化完成")
    
    @staticmethod
    def classify_character(char):
        """
        对单个字符进行分类
        
        Args:
            char (str): 要分析的字符
            
        Returns:
            str: 字符类型 ('chinese', 'english', 'other')
        """
        if not char or len(char) != 1:
            return 'other'
        
        try:
            # 检查是否为中文字符
            if CharacterAnalyzer.CHINESE_PATTERN.match(char):
                return 'chinese'
            
            # 检查是否为英文字符
            if CharacterAnalyzer.ENGLISH_PATTERN.match(char):
                return 'english'
            
            # 其他字符（数字、符号等）
            return 'other'
            
        except Exception as e:
            logger.warning(f"字符分类异常 '{char}': {e}")
            return 'other'
    
    @staticmethod
    def analyze_text(text):
        """
        批量分析文本，统计各类字符数量
        
        Args:
            text (str): 要分析的文本
            
        Returns:
            dict: 包含各类字符统计的字典
            {
                'chinese_count': int,
                'english_count': int,
                'other_count': int,
                'total_count': int
            }
        """
        if not text:
            return {
                'chinese_count': 0,
                'english_count': 0,
                'other_count': 0,
                'total_count': 0
            }
        
        chinese_count = 0
        english_count = 0
        other_count = 0
        
        try:
            for char in text:
                char_type = CharacterAnalyzer.classify_character(char)
                if char_type == 'chinese':
                    chinese_count += 1
                elif char_type == 'english':
                    english_count += 1
                else:
                    other_count += 1
            
            total_count = chinese_count + english_count + other_count
            
            result = {
                'chinese_count': chinese_count,
                'english_count': english_count,
                'other_count': other_count,
                'total_count': total_count
            }
            
            logger.debug(f"文本分析完成: {result}")
            return result
            
        except Exception as e:
            logger.error(f"文本分析异常: {e}")
            return {
                'chinese_count': 0,
                'english_count': 0,
                'other_count': 0,
                'total_count': 0
            }
    
    @staticmethod
    def get_character_info(char):
        """
        获取字符的详细信息（调试用）
        
        Args:
            char (str): 字符
            
        Returns:
            dict: 字符信息
        """
        if not char:
            return {'char': '', 'type': 'empty', 'unicode': None}
        
        char_type = CharacterAnalyzer.classify_character(char)
        unicode_code = ord(char) if len(char) == 1 else None
        
        return {
            'char': char,
            'type': char_type,
            'unicode': unicode_code,
            'unicode_hex': f'\\u{unicode_code:04x}' if unicode_code else None
        }


# 工具函数
def test_character_analyzer():
    """测试字符分析器功能"""
    print("🧪 测试字符分析器...")
    
    # 测试单个字符分类
    test_chars = ['你', 'h', 'e', '好', '1', '@', 'A', '中']
    print("单字符分类测试:")
    for char in test_chars:
        char_type = CharacterAnalyzer.classify_character(char)
        info = CharacterAnalyzer.get_character_info(char)
        print(f"  '{char}' -> {char_type} (Unicode: {info['unicode_hex']})")
    
    # 测试文本分析
    test_texts = [
        "hello world",
        "你好世界",
        "hello你好world世界",
        "print('Hello, 世界!')",
        "def calculate_sum(a, b): return a + b  # 计算和值",
    ]
    
    print("\n文本分析测试:")
    for text in test_texts:
        result = CharacterAnalyzer.analyze_text(text)
        print(f"  文本: '{text}'")
        print(f"    中文: {result['chinese_count']}, 英文: {result['english_count']}, 其他: {result['other_count']}")
    
    print("✅ 字符分析器测试完成")


if __name__ == "__main__":
    # 独立运行时进行测试
    test_character_analyzer() 