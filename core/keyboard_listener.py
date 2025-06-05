#!/usr/bin/env python3
"""
Keyboard Listener - 键盘监听器

负责全局键盘事件监听，实时统计中英文字符输入量。
这是MVP版本的核心模块，专注于稳定性和基础功能。

作者：DailyInputCounter Team
版本：1.0.0-mvp
"""

import threading
import time
import logging
from datetime import datetime
from pynput import keyboard
from .character_analyzer import CharacterAnalyzer

logger = logging.getLogger(__name__)


class KeyboardListener:
    """键盘监听器 - MVP版本"""
    
    def __init__(self, save_callback=None, save_interval=100):
        """
        初始化键盘监听器
        
        Args:
            save_callback (callable): 数据保存回调函数，签名: (chinese_count, english_count)
            save_interval (int): 每多少次按键保存一次数据
        """
        self.analyzer = CharacterAnalyzer()
        self.save_callback = save_callback
        self.save_interval = save_interval
        
        # 统计计数器
        self.today_chinese = 0
        self.today_english = 0
        self.total_keys = 0
        
        # 控制变量
        self.is_listening = False
        self.listener = None
        self.start_time = None
        
        # 线程锁
        self._lock = threading.Lock()
        
        logger.info(f"键盘监听器初始化完成，保存间隔: {save_interval}")
    
    def on_key_press(self, key):
        """
        键盘按键事件处理
        
        Args:
            key: pynput键盘事件对象
        """
        try:
            # 获取字符
            char = None
            if hasattr(key, 'char') and key.char:
                char = key.char
            
            # 如果是有效字符，进行分析
            if char:
                char_type = self.analyzer.classify_character(char)
                
                with self._lock:
                    self.total_keys += 1
                    
                    if char_type == 'chinese':
                        self.today_chinese += 1
                        logger.debug(f"中文字符: '{char}' (总计: {self.today_chinese})")
                    elif char_type == 'english':
                        self.today_english += 1
                        logger.debug(f"英文字符: '{char}' (总计: {self.today_english})")
                    
                    # 定期保存数据
                    if self.total_keys % self.save_interval == 0:
                        self._save_data()
            
        except Exception as e:
            logger.warning(f"按键处理异常: {e}")
    
    def on_key_release(self, key):
        """
        键盘释放事件处理（暂时不使用）
        
        Args:
            key: pynput键盘事件对象
        """
        # MVP版本暂时不处理释放事件
        pass
    
    def _save_data(self):
        """内部数据保存方法"""
        if self.save_callback:
            try:
                self.save_callback(self.today_chinese, self.today_english)
                logger.debug(f"数据已保存: 中文={self.today_chinese}, 英文={self.today_english}")
            except Exception as e:
                logger.error(f"数据保存失败: {e}")
    
    def start_listening(self):
        """开始监听键盘事件"""
        if self.is_listening:
            logger.warning("键盘监听器已在运行中")
            return False
        
        try:
            self.is_listening = True
            self.start_time = datetime.now()
            
            # 创建监听器
            self.listener = keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )
            
            # 启动监听器
            self.listener.start()
            logger.info("键盘监听器启动成功")
            return True
            
        except Exception as e:
            logger.error(f"键盘监听器启动失败: {e}")
            self.is_listening = False
            return False
    
    def stop_listening(self):
        """停止监听键盘事件"""
        if not self.is_listening:
            logger.warning("键盘监听器未在运行")
            return False
        
        try:
            self.is_listening = False
            
            if self.listener:
                self.listener.stop()
                self.listener = None
            
            # 保存最后的数据
            self._save_data()
            
            end_time = datetime.now()
            duration = end_time - self.start_time if self.start_time else None
            
            logger.info(f"键盘监听器已停止，运行时间: {duration}")
            logger.info(f"本次统计 - 中文: {self.today_chinese}, 英文: {self.today_english}, 总按键: {self.total_keys}")
            
            return True
            
        except Exception as e:
            logger.error(f"键盘监听器停止失败: {e}")
            return False
    
    def get_current_stats(self):
        """
        获取当前统计数据
        
        Returns:
            dict: 当前统计信息
        """
        with self._lock:
            return {
                'chinese_count': self.today_chinese,
                'english_count': self.today_english,
                'total_count': self.today_chinese + self.today_english,
                'total_keys': self.total_keys,
                'is_listening': self.is_listening,
                'start_time': self.start_time,
                'uptime': datetime.now() - self.start_time if self.start_time else None
            }
    
    def reset_daily_stats(self):
        """重置每日统计（新的一天开始时调用）"""
        with self._lock:
            old_chinese = self.today_chinese
            old_english = self.today_english
            
            self.today_chinese = 0
            self.today_english = 0
            self.total_keys = 0
            
            logger.info(f"每日统计已重置，前一天统计: 中文={old_chinese}, 英文={old_english}")
    
    def set_save_callback(self, callback):
        """设置数据保存回调函数"""
        self.save_callback = callback
        logger.info("数据保存回调函数已更新")
    
    def force_save(self):
        """强制保存当前数据"""
        self._save_data()
        logger.info("强制保存数据完成")


class KeyboardListenerManager:
    """键盘监听器管理器 - 简化版本"""
    
    def __init__(self):
        """初始化管理器"""
        self.listener = None
        self.is_running = False
        logger.info("键盘监听器管理器初始化完成")
    
    def create_listener(self, save_callback=None, save_interval=100):
        """
        创建键盘监听器实例
        
        Args:
            save_callback: 数据保存回调
            save_interval: 保存间隔
            
        Returns:
            KeyboardListener: 监听器实例
        """
        self.listener = KeyboardListener(save_callback, save_interval)
        return self.listener
    
    def start(self, save_callback=None, save_interval=100):
        """启动监听器"""
        if self.is_running:
            logger.warning("管理器已在运行中")
            return False
        
        if not self.listener:
            self.create_listener(save_callback, save_interval)
        
        if self.listener.start_listening():
            self.is_running = True
            logger.info("键盘监听器管理器启动成功")
            return True
        else:
            logger.error("键盘监听器管理器启动失败")
            return False
    
    def stop(self):
        """停止监听器"""
        if not self.is_running:
            logger.warning("管理器未在运行")
            return False
        
        if self.listener and self.listener.stop_listening():
            self.is_running = False
            logger.info("键盘监听器管理器已停止")
            return True
        else:
            logger.error("键盘监听器管理器停止失败")
            return False
    
    def get_stats(self):
        """获取统计信息"""
        if self.listener:
            return self.listener.get_current_stats()
        else:
            return {
                'chinese_count': 0,
                'english_count': 0,
                'total_count': 0,
                'total_keys': 0,
                'is_listening': False,
                'start_time': None,
                'uptime': None
            }


# 测试函数
def test_keyboard_listener():
    """测试键盘监听器功能"""
    print("🧪 测试键盘监听器...")
    print("⚠️  注意：这是一个交互式测试，需要管理员权限")
    print("📝 请在5秒内开始打字测试...")
    
    def test_save_callback(chinese, english):
        print(f"💾 保存回调: 中文={chinese}, 英文={english}")
    
    # 创建监听器
    listener = KeyboardListener(save_callback=test_save_callback, save_interval=5)
    
    try:
        # 启动监听
        if listener.start_listening():
            print("✅ 监听器启动成功，开始5秒测试...")
            
            # 运行5秒
            time.sleep(5)
            
            # 获取统计
            stats = listener.get_current_stats()
            print("📊 测试结果:")
            print(f"   中文字符: {stats['chinese_count']}")
            print(f"   英文字符: {stats['english_count']}")
            print(f"   总字符: {stats['total_count']}")
            print(f"   总按键: {stats['total_keys']}")
            
        else:
            print("❌ 监听器启动失败")
    
    finally:
        # 停止监听
        listener.stop_listening()
        print("✅ 键盘监听器测试完成")


if __name__ == "__main__":
    # 独立运行时进行测试
    test_keyboard_listener() 