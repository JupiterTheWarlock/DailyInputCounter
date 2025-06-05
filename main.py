#!/usr/bin/env python3
"""
DailyInputCounter - 每日输入统计器

主程序入口文件，负责初始化应用程序并启动GUI界面。

作者：DailyInputCounter Team
版本：1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import get_config, get_settings


def setup_logging():
    """设置日志系统"""
    settings = get_settings()
    
    # 设置日志级别
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # 创建日志目录
    log_dir = get_config().get_data_path() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # 文件处理器
    file_handler = logging.FileHandler(
        log_dir / f"dailyinput_{Path(__file__).stem}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    logging.info("日志系统初始化完成")


def check_admin_privileges():
    """检查是否具有管理员权限（Windows）"""
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return True  # 非Windows系统暂时返回True


def show_admin_warning():
    """显示管理员权限警告"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        result = messagebox.askyesno(
            "权限警告",
            "检测到程序没有管理员权限！\n\n"
            "为了实现全局键盘监听功能，建议以管理员权限运行程序。\n\n"
            "是否继续运行？（功能可能受限）"
        )
        
        root.destroy()
        return result
    except Exception as e:
        logging.warning(f"无法显示权限警告窗口: {e}")
        return True  # 默认继续运行


def main():
    """主函数"""
    try:
        # 打印启动信息
        print("🐱 DailyInputCounter - 每日输入统计器")
        print("=" * 50)
        
        # 设置日志系统
        setup_logging()
        logging.info("程序启动中...")
        
        # 加载配置
        config = get_config()
        settings = get_settings()
        logging.info(f"配置加载完成，数据路径: {config.get_data_path()}")
        
        # 确保数据目录存在
        if not config.ensure_data_directory():
            logging.error("无法创建数据目录，程序退出")
            return 1
        
        # 检查管理员权限（Windows）
        if os.name == 'nt' and not check_admin_privileges():
            logging.warning("未检测到管理员权限")
            if not show_admin_warning():
                logging.info("用户取消运行")
                return 0
        
        # 尝试导入GUI模块（延迟导入避免在权限检查前初始化tkinter）
        try:
            from gui.mvp_window import MVPWindow
            logging.info("MVP GUI模块导入成功")
            
            # 创建并启动MVP窗口
            logging.info("启动MVP窗口...")
            app = MVPWindow()
            app.run()
            
        except ImportError as e:
            logging.error(f"MVP GUI模块导入失败: {e}")
            print("❌ MVP GUI模块导入失败！")
            print(f"错误详情: {e}")
            print("🔧 请检查依赖是否正确安装")
            return 1
            
        except Exception as e:
            logging.error(f"MVP窗口运行失败: {e}")
            print(f"❌ MVP窗口运行失败: {e}")
            return 1
        
        logging.info("程序正常退出")
        return 0
        
    except KeyboardInterrupt:
        logging.info("用户中断程序")
        return 0
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
        logging.exception("详细错误信息:")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 