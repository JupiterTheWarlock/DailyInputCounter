#!/usr/bin/env python3
"""
Data Storage - 数据存储模块

负责管理每日输入统计数据的SQLite数据库存储。
MVP版本专注于简单、可靠的数据持久化。

作者：DailyInputCounter Team
版本：1.0.0-mvp
"""

import sqlite3
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class DataStorage:
    """数据存储管理器 - MVP版本"""
    
    def __init__(self, db_path: str = None):
        """
        初始化数据存储
        
        Args:
            db_path (str): 数据库文件路径，如果为None则使用默认路径
        """
        if db_path is None:
            # 使用默认数据目录
            self.db_path = Path("data") / "daily_stats.db"
        else:
            self.db_path = Path(db_path)
        
        # 确保数据目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        logger.info(f"数据存储初始化完成，数据库路径: {self.db_path}")
    
    def _init_database(self):
        """初始化数据库表结构"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 创建每日统计表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS daily_stats (
                        date TEXT PRIMARY KEY,
                        chinese_chars INTEGER DEFAULT 0,
                        english_chars INTEGER DEFAULT 0,
                        total_chars INTEGER DEFAULT 0,
                        total_keys INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建更新时间触发器
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS update_daily_stats_timestamp 
                    AFTER UPDATE ON daily_stats 
                    BEGIN
                        UPDATE daily_stats SET updated_at = CURRENT_TIMESTAMP 
                        WHERE date = NEW.date;
                    END
                ''')
                
                conn.commit()
                logger.info("数据库表结构初始化完成")
                
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def update_daily_stats(self, chinese_count: int, english_count: int, 
                          target_date: str = None, total_keys: int = None):
        """
        更新每日统计数据
        
        Args:
            chinese_count (int): 中文字符数
            english_count (int): 英文字符数
            target_date (str): 目标日期，格式YYYY-MM-DD，默认今天
            total_keys (int): 总按键数，可选
            
        Returns:
            bool: 操作是否成功
        """
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')
        
        total_chars = chinese_count + english_count
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 使用UPSERT操作（INSERT OR REPLACE）
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_stats 
                    (date, chinese_chars, english_chars, total_chars, total_keys, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (target_date, chinese_count, english_count, total_chars, total_keys))
                
                conn.commit()
                
                logger.debug(f"每日统计已更新: {target_date} - 中文:{chinese_count}, 英文:{english_count}")
                return True
                
        except Exception as e:
            logger.error(f"更新每日统计失败: {e}")
            return False
    
    def get_daily_stats(self, target_date: str = None) -> Optional[Dict]:
        """
        获取指定日期的统计数据
        
        Args:
            target_date (str): 目标日期，格式YYYY-MM-DD，默认今天
            
        Returns:
            dict: 统计数据，如果不存在则返回None
        """
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT date, chinese_chars, english_chars, total_chars, 
                           total_keys, created_at, updated_at
                    FROM daily_stats 
                    WHERE date = ?
                ''', (target_date,))
                
                row = cursor.fetchone()
                
                if row:
                    return {
                        'date': row[0],
                        'chinese_chars': row[1],
                        'english_chars': row[2],
                        'total_chars': row[3],
                        'total_keys': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    }
                else:
                    logger.debug(f"日期 {target_date} 没有统计数据")
                    return None
                
        except Exception as e:
            logger.error(f"获取每日统计失败: {e}")
            return None
    
    def get_recent_stats(self, days: int = 7) -> List[Dict]:
        """
        获取最近N天的统计数据
        
        Args:
            days (int): 天数
            
        Returns:
            list: 统计数据列表，按日期倒序排列
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT date, chinese_chars, english_chars, total_chars, 
                           total_keys, created_at, updated_at
                    FROM daily_stats 
                    ORDER BY date DESC 
                    LIMIT ?
                ''', (days,))
                
                rows = cursor.fetchall()
                
                result = []
                for row in rows:
                    result.append({
                        'date': row[0],
                        'chinese_chars': row[1],
                        'english_chars': row[2],
                        'total_chars': row[3],
                        'total_keys': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    })
                
                logger.debug(f"获取最近{days}天数据，共{len(result)}条记录")
                return result
                
        except Exception as e:
            logger.error(f"获取最近统计失败: {e}")
            return []
    
    def get_all_stats(self) -> List[Dict]:
        """
        获取所有统计数据
        
        Returns:
            list: 所有统计数据，按日期倒序排列
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT date, chinese_chars, english_chars, total_chars, 
                           total_keys, created_at, updated_at
                    FROM daily_stats 
                    ORDER BY date DESC
                ''')
                
                rows = cursor.fetchall()
                
                result = []
                for row in rows:
                    result.append({
                        'date': row[0],
                        'chinese_chars': row[1],
                        'english_chars': row[2],
                        'total_chars': row[3],
                        'total_keys': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    })
                
                logger.debug(f"获取所有数据，共{len(result)}条记录")
                return result
                
        except Exception as e:
            logger.error(f"获取所有统计失败: {e}")
            return []
    
    def delete_daily_stats(self, target_date: str) -> bool:
        """
        删除指定日期的统计数据
        
        Args:
            target_date (str): 目标日期，格式YYYY-MM-DD
            
        Returns:
            bool: 操作是否成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM daily_stats WHERE date = ?', (target_date,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"已删除日期 {target_date} 的统计数据")
                    return True
                else:
                    logger.warning(f"日期 {target_date} 没有统计数据可删除")
                    return False
                
        except Exception as e:
            logger.error(f"删除每日统计失败: {e}")
            return False
    
    def get_stats_summary(self) -> Dict:
        """
        获取统计摘要信息
        
        Returns:
            dict: 摘要信息
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取基本统计
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_days,
                        SUM(chinese_chars) as total_chinese,
                        SUM(english_chars) as total_english,
                        SUM(total_chars) as total_chars,
                        SUM(total_keys) as total_keys,
                        AVG(chinese_chars) as avg_chinese,
                        AVG(english_chars) as avg_english,
                        MIN(date) as first_date,
                        MAX(date) as last_date
                    FROM daily_stats
                ''')
                
                row = cursor.fetchone()
                
                if row and row[0] > 0:
                    return {
                        'total_days': row[0],
                        'total_chinese': row[1] or 0,
                        'total_english': row[2] or 0,
                        'total_chars': row[3] or 0,
                        'total_keys': row[4] or 0,
                        'avg_chinese': round(row[5] or 0, 1),
                        'avg_english': round(row[6] or 0, 1),
                        'first_date': row[7],
                        'last_date': row[8]
                    }
                else:
                    return {
                        'total_days': 0,
                        'total_chinese': 0,
                        'total_english': 0,
                        'total_chars': 0,
                        'total_keys': 0,
                        'avg_chinese': 0,
                        'avg_english': 0,
                        'first_date': None,
                        'last_date': None
                    }
                
        except Exception as e:
            logger.error(f"获取统计摘要失败: {e}")
            return {}
    
    def close(self):
        """关闭数据库连接（备用方法）"""
        # SQLite使用上下文管理器，不需要显式关闭
        logger.info("数据存储已关闭")
    
    def backup_database(self, backup_path: str = None) -> bool:
        """
        备份数据库
        
        Args:
            backup_path (str): 备份文件路径
            
        Returns:
            bool: 备份是否成功
        """
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.db_path.parent / f"daily_stats_backup_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"数据库已备份到: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"数据库备份失败: {e}")
            return False


# 测试函数
def test_data_storage():
    """测试数据存储功能"""
    print("🧪 测试数据存储...")
    
    # 创建测试数据库
    storage = DataStorage("test_daily_stats.db")
    
    # 测试更新数据
    today = date.today().strftime('%Y-%m-%d')
    print(f"📅 测试日期: {today}")
    
    # 更新今日数据
    if storage.update_daily_stats(100, 200, total_keys=350):
        print("✅ 数据更新成功")
    else:
        print("❌ 数据更新失败")
    
    # 读取今日数据
    stats = storage.get_daily_stats(today)
    if stats:
        print(f"📊 今日统计: 中文={stats['chinese_chars']}, 英文={stats['english_chars']}")
    else:
        print("❌ 读取数据失败")
    
    # 测试摘要
    summary = storage.get_stats_summary()
    print(f"📈 统计摘要: 总天数={summary.get('total_days', 0)}")
    
    # 测试最近数据
    recent = storage.get_recent_stats(3)
    print(f"📋 最近3天数据: {len(recent)}条记录")
    
    print("✅ 数据存储测试完成")
    
    # 清理测试文件
    import os
    try:
        os.remove("test_daily_stats.db")
        print("🗑️ 测试文件已清理")
    except:
        pass


if __name__ == "__main__":
    # 独立运行时进行测试
    test_data_storage() 