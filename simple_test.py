#!/usr/bin/env python3
"""
简单测试脚本 - 不依赖外部库的基础功能测试
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """测试基础模块导入"""
    print("🧪 测试基础模块导入...")
    
    try:
        # 测试字符分析器 (不依赖外部库)
        from core.character_analyzer import CharacterAnalyzer
        analyzer = CharacterAnalyzer()
        
        # 测试字符分类
        result1 = analyzer.classify_character('你')
        result2 = analyzer.classify_character('h')
        result3 = analyzer.classify_character('1')
        
        print(f"✅ 字符分析器正常: '你'→{result1}, 'h'→{result2}, '1'→{result3}")
        
        # 测试文本分析
        text_result = analyzer.analyze_text("hello你好123")
        print(f"✅ 文本分析正常: {text_result}")
        
    except Exception as e:
        print(f"❌ 字符分析器测试失败: {e}")
        return False
    
    try:
        # 测试数据存储 (SQLite是内置的)
        from core.data_storage import DataStorage
        storage = DataStorage("simple_test.db")
        
        # 测试数据保存
        success = storage.update_daily_stats(10, 20)
        print(f"✅ 数据存储正常: 保存结果={success}")
        
        # 测试数据读取
        stats = storage.get_daily_stats()
        if stats:
            print(f"✅ 数据读取正常: 中文={stats['chinese_chars']}, 英文={stats['english_chars']}")
        
        # 清理测试文件
        try:
            os.remove("simple_test.db")
        except:
            pass
            
    except Exception as e:
        print(f"❌ 数据存储测试失败: {e}")
        return False
    
    try:
        # 测试自启动模块 (winreg是内置的)
        from utils.autostart import AutoStart
        autostart = AutoStart()
        status = autostart.get_status_info()
        print(f"✅ 自启动模块正常: 支持={status['supported']}")
        
    except Exception as e:
        print(f"❌ 自启动模块测试失败: {e}")
        return False
    
    return True

def test_gui_import():
    """测试GUI模块导入 (不启动)"""
    print("\n🖥️ 测试GUI模块导入...")
    
    try:
        # 只测试导入，不启动GUI
        from gui.mvp_window import MVPWindow
        print("✅ GUI模块导入成功")
        return True
        
    except Exception as e:
        print(f"❌ GUI模块导入失败: {e}")
        # 检查是否是因为缺少pynput
        if "pynput" in str(e):
            print("⚠️ 可能是因为缺少pynput依赖")
        return False

def test_keyboard_listener_import():
    """测试键盘监听器导入"""
    print("\n⌨️ 测试键盘监听器导入...")
    
    try:
        # 尝试导入键盘监听器
        from core.keyboard_listener import KeyboardListenerManager
        print("✅ 键盘监听器模块导入成功")
        return True
        
    except ImportError as e:
        print(f"❌ 键盘监听器导入失败: {e}")
        if "pynput" in str(e):
            print("⚠️ 缺少pynput依赖，无法使用键盘监听功能")
        return False
    except Exception as e:
        print(f"❌ 键盘监听器异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 DailyInputCounter 简单测试")
    print("=" * 40)
    
    # 测试基础功能 (不依赖外部库)
    basic_ok = test_basic_imports()
    
    # 测试键盘监听器导入
    keyboard_ok = test_keyboard_listener_import()
    
    # 测试GUI导入
    gui_ok = test_gui_import()
    
    print("\n" + "=" * 40)
    print("📊 测试结果:")
    print(f"  基础功能: {'✅ 正常' if basic_ok else '❌ 异常'}")
    print(f"  键盘监听: {'✅ 正常' if keyboard_ok else '❌ 异常 (可能缺少pynput)'}")
    print(f"  GUI模块: {'✅ 正常' if gui_ok else '❌ 异常'}")
    
    if basic_ok:
        print("\n🎉 核心功能正常，可以进行基础数据分析！")
        if keyboard_ok and gui_ok:
            print("🚀 所有功能正常，可以启动完整应用！")
        else:
            print("⚠️ 完整功能需要安装依赖: pip install pynput")
    else:
        print("\n❌ 基础功能异常，请检查代码")
    
    return basic_ok

if __name__ == "__main__":
    main() 