#!/usr/bin/env python3
"""
快速启动MVP - DailyInputCounter

简化的启动脚本，直接启动MVP窗口进行测试
跳过复杂的配置和权限检查，专注于功能验证

作者：DailyInputCounter Team
版本：1.0.0-mvp
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def quick_test():
    """快速功能测试"""
    print("🐱 DailyInputCounter MVP 快速测试")
    print("=" * 40)
    
    # 测试字符分析器
    try:
        from core.character_analyzer import CharacterAnalyzer
        analyzer = CharacterAnalyzer()
        result = analyzer.analyze_text("hello你好123")
        print(f"✅ 字符分析器工作正常")
        print(f"   测试结果: 中文={result['chinese_count']}, 英文={result['english_count']}")
    except Exception as e:
        print(f"❌ 字符分析器异常: {e}")
        return False
    
    # 测试数据存储
    try:
        from core.data_storage import DataStorage
        storage = DataStorage("test_quick.db")
        storage.update_daily_stats(10, 20)
        stats = storage.get_daily_stats()
        print(f"✅ 数据存储工作正常")
        print(f"   今日统计: 中文={stats['chinese_chars']}, 英文={stats['english_chars']}")
        
        # 清理测试文件
        try:
            os.remove("test_quick.db")
        except:
            pass
    except Exception as e:
        print(f"❌ 数据存储异常: {e}")
        return False
    
    print("🎉 基础功能测试通过！")
    return True

def start_mvp_gui():
    """启动MVP GUI"""
    print("\n🖥️ 启动MVP界面...")
    
    try:
        from gui.mvp_window import MVPWindow
        
        print("✅ GUI模块导入成功")
        print("⚠️ 注意：键盘监听功能可能需要管理员权限")
        print("📝 即将打开MVP界面，请测试各项功能")
        
        app = MVPWindow()
        app.run()
        
        print("👋 MVP界面已关闭")
        
    except ImportError as e:
        print(f"❌ GUI模块导入失败: {e}")
        print("🔧 请检查依赖是否正确安装：pip install pynput")
        return False
        
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 启动DailyInputCounter MVP...")
    
    # 快速功能测试
    if quick_test():
        # 启动GUI
        start_mvp_gui()
    else:
        print("❌ 基础功能测试失败，请检查模块")
        sys.exit(1)
    
    print("✨ MVP测试完成喵～") 