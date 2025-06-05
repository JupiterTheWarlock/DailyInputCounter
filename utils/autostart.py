#!/usr/bin/env python3
"""
AutoStart - 自启动管理模块

Windows系统自启动功能管理，通过注册表实现开机自启动。
MVP版本提供基础的开机自启动设置和管理功能。

作者：DailyInputCounter Team
版本：1.0.0-mvp
"""

import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AutoStart:
    """Windows自启动管理器 - MVP版本"""
    
    # 注册表路径（Windows启动项）
    REGISTRY_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "DailyInputCounter"
    
    def __init__(self):
        """初始化自启动管理器"""
        self.is_windows = os.name == 'nt'
        logger.info("自启动管理器初始化完成")
    
    @staticmethod
    def is_admin():
        """检查是否具有管理员权限"""
        if os.name == 'nt':
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        return True
    
    @staticmethod
    def get_exe_path():
        """获取当前程序路径"""
        if getattr(sys, 'frozen', False):
            # 如果是打包的exe文件
            return sys.executable
        else:
            # 如果是Python脚本
            main_py = Path(__file__).parent.parent / "main.py"
            python_exe = sys.executable
            return f'"{python_exe}" "{main_py}"'
    
    def enable(self):
        """启用开机自启动"""
        if not self.is_windows:
            logger.warning("非Windows系统，不支持注册表自启动")
            return False
        
        try:
            import winreg as reg
            
            # 获取程序路径
            exe_path = self.get_exe_path()
            
            # 打开注册表键
            key = reg.OpenKey(
                reg.HKEY_CURRENT_USER, 
                self.REGISTRY_PATH, 
                0, 
                reg.KEY_SET_VALUE
            )
            
            # 设置启动项
            reg.SetValueEx(
                key, 
                self.APP_NAME, 
                0, 
                reg.REG_SZ, 
                exe_path
            )
            
            # 关闭注册表键
            reg.CloseKey(key)
            
            logger.info(f"自启动已启用: {exe_path}")
            return True
            
        except ImportError:
            logger.error("winreg模块不可用")
            return False
        except Exception as e:
            logger.error(f"启用自启动失败: {e}")
            return False
    
    def disable(self):
        """禁用开机自启动"""
        if not self.is_windows:
            logger.warning("非Windows系统，不支持注册表自启动")
            return False
        
        try:
            import winreg as reg
            
            # 打开注册表键
            key = reg.OpenKey(
                reg.HKEY_CURRENT_USER, 
                self.REGISTRY_PATH, 
                0, 
                reg.KEY_SET_VALUE
            )
            
            # 删除启动项
            try:
                reg.DeleteValue(key, self.APP_NAME)
                logger.info("自启动已禁用")
                result = True
            except FileNotFoundError:
                logger.info("自启动项不存在，无需删除")
                result = True
            
            # 关闭注册表键
            reg.CloseKey(key)
            
            return result
            
        except ImportError:
            logger.error("winreg模块不可用")
            return False
        except Exception as e:
            logger.error(f"禁用自启动失败: {e}")
            return False
    
    def is_enabled(self):
        """检查是否已启用自启动"""
        if not self.is_windows:
            return False
        
        try:
            import winreg as reg
            
            # 打开注册表键
            key = reg.OpenKey(
                reg.HKEY_CURRENT_USER, 
                self.REGISTRY_PATH, 
                0, 
                reg.KEY_READ
            )
            
            # 查询启动项
            try:
                value, _ = reg.QueryValueEx(key, self.APP_NAME)
                reg.CloseKey(key)
                
                logger.debug(f"自启动状态: 已启用 ({value})")
                return True
                
            except FileNotFoundError:
                reg.CloseKey(key)
                logger.debug("自启动状态: 未启用")
                return False
            
        except ImportError:
            logger.error("winreg模块不可用")
            return False
        except Exception as e:
            logger.error(f"检查自启动状态失败: {e}")
            return False
    
    def toggle(self):
        """切换自启动状态"""
        if self.is_enabled():
            return self.disable()
        else:
            return self.enable()
    
    def get_status_info(self):
        """获取自启动状态信息"""
        if not self.is_windows:
            return {
                'supported': False,
                'enabled': False,
                'path': None,
                'message': '非Windows系统不支持'
            }
        
        enabled = self.is_enabled()
        path = self.get_exe_path() if enabled else None
        
        return {
            'supported': True,
            'enabled': enabled,
            'path': path,
            'message': '已启用' if enabled else '未启用'
        }


class AutoStartManager:
    """自启动管理器 - 高级封装"""
    
    def __init__(self):
        """初始化管理器"""
        self.autostart = AutoStart()
        logger.info("自启动管理器初始化完成")
    
    def setup_autostart_with_prompt(self):
        """带用户提示的自启动设置"""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            # 隐藏主窗口
            root = tk.Tk()
            root.withdraw()
            
            # 检查当前状态
            if self.autostart.is_enabled():
                result = messagebox.askyesno(
                    "自启动设置",
                    "检测到已启用开机自启动。\n\n是否要禁用开机自启动？"
                )
                if result:
                    success = self.autostart.disable()
                    if success:
                        messagebox.showinfo("成功", "开机自启动已禁用！")
                    else:
                        messagebox.showerror("失败", "禁用开机自启动失败！")
            else:
                result = messagebox.askyesno(
                    "自启动设置",
                    "是否要启用开机自启动？\n\n启用后程序将在系统启动时自动运行。"
                )
                if result:
                    success = self.autostart.enable()
                    if success:
                        messagebox.showinfo("成功", "开机自启动已启用！")
                    else:
                        messagebox.showerror("失败", "启用开机自启动失败！\n可能需要管理员权限。")
            
            root.destroy()
            
        except Exception as e:
            logger.error(f"自启动设置界面失败: {e}")
    
    def auto_enable_on_first_run(self):
        """首次运行时自动启用自启动"""
        if not self.autostart.is_enabled():
            logger.info("首次运行，尝试启用自启动...")
            if self.autostart.enable():
                logger.info("自启动已自动启用")
                return True
            else:
                logger.warning("自启动自动启用失败")
                return False
        else:
            logger.info("自启动已启用，跳过设置")
            return True


# 测试函数
def test_autostart():
    """测试自启动功能"""
    print("🧪 测试自启动功能...")
    
    autostart = AutoStart()
    
    # 检查系统支持
    if not autostart.is_windows:
        print("❌ 非Windows系统，跳过测试")
        return
    
    # 获取状态信息
    status = autostart.get_status_info()
    print(f"💻 系统支持: {status['supported']}")
    print(f"📊 当前状态: {status['message']}")
    print(f"📂 程序路径: {autostart.get_exe_path()}")
    
    # 测试切换功能（实际不执行，避免修改用户系统）
    original_enabled = autostart.is_enabled()
    print(f"🔧 原始状态: {'已启用' if original_enabled else '未启用'}")
    
    # 模拟测试（不实际修改注册表）
    print("✅ 自启动功能测试完成（模拟测试）")
    
    # 如果用户想要实际测试，取消下面的注释
    # print("🧪 实际测试自启动切换...")
    # if autostart.toggle():
    #     new_status = autostart.is_enabled()
    #     print(f"✅ 切换成功: {'已启用' if new_status else '未启用'}")
    #     # 恢复原始状态
    #     autostart.toggle()
    #     print("🔄 已恢复原始状态")
    # else:
    #     print("❌ 切换失败")


if __name__ == "__main__":
    # 独立运行时进行测试
    test_autostart() 