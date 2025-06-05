#!/usr/bin/env python3
"""
MVP Window - MVP版本GUI界面

极简版图形界面，专注于核心功能展示：
- 实时显示今日统计
- 简单的日期查询
- 监听控制按钮

作者：DailyInputCounter Team
版本：1.0.0-mvp
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from datetime import datetime, date
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from core.keyboard_listener import KeyboardListenerManager
from core.data_storage import DataStorage
from utils.autostart import AutoStartManager

logger = logging.getLogger(__name__)


class MVPWindow:
    """MVP版本主窗口"""
    
    def __init__(self):
        """初始化MVP窗口"""
        self.root = tk.Tk()
        self.root.title("🐱 AI率统计器 MVP")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 初始化组件
        self.listener_manager = KeyboardListenerManager()
        self.data_storage = DataStorage()
        self.autostart_manager = AutoStartManager()
        
        # 状态变量
        self.is_monitoring = False
        self.current_stats = {
            'chinese_count': 0,
            'english_count': 0,
            'total_count': 0
        }
        
        # 创建界面
        self._create_widgets()
        
        # 启动定时更新
        self._start_update_timer()
        
        logger.info("MVP窗口初始化完成")
    
    def _create_widgets(self):
        """创建界面组件"""
        # 主标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)
        
        title_label = ttk.Label(
            title_frame, 
            text="🐱 程序员AI率统计器 MVP", 
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="追踪每日中英文输入量，了解AI辅助率喵～", 
            font=("微软雅黑", 9)
        )
        subtitle_label.pack()
        
        # 今日统计区域
        self._create_today_stats_section()
        
        # 控制按钮区域
        self._create_control_section()
        
        # 查询历史区域
        self._create_query_section()
        
        # 状态栏
        self._create_status_section()
    
    def _create_today_stats_section(self):
        """创建今日统计区域"""
        stats_frame = ttk.LabelFrame(self.root, text="📊 今日统计", padding="10")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # 统计显示
        self.stats_var = tk.StringVar()
        self.stats_var.set("今日尚未开始统计...")
        
        stats_display = ttk.Label(
            stats_frame, 
            textvariable=self.stats_var,
            font=("Consolas", 11),
            justify="left"
        )
        stats_display.pack(anchor="w")
        
        # 今日摘要
        self.summary_var = tk.StringVar()
        self.summary_var.set("")
        
        summary_display = ttk.Label(
            stats_frame,
            textvariable=self.summary_var,
            font=("微软雅黑", 9),
            foreground="blue"
        )
        summary_display.pack(anchor="w", pady=(5, 0))
    
    def _create_control_section(self):
        """创建控制按钮区域"""
        control_frame = ttk.LabelFrame(self.root, text="🎮 监听控制", padding="10")
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(control_frame)
        button_frame.pack()
        
        # 开始/停止按钮
        self.toggle_button = ttk.Button(
            button_frame,
            text="🚀 开始监听",
            command=self._toggle_monitoring,
            width=15
        )
        self.toggle_button.pack(side="left", padx=5)
        
        # 保存按钮
        save_button = ttk.Button(
            button_frame,
            text="💾 立即保存",
            command=self._force_save,
            width=15
        )
        save_button.pack(side="left", padx=5)
        
        # 重置按钮
        reset_button = ttk.Button(
            button_frame,
            text="🔄 重置今日",
            command=self._reset_today,
            width=15
        )
        reset_button.pack(side="left", padx=5)
        
        # 自启动设置按钮
        autostart_button = ttk.Button(
            button_frame,
            text="⚙️ 自启动",
            command=self._setup_autostart,
            width=15
        )
        autostart_button.pack(side="left", padx=5)
    
    def _create_query_section(self):
        """创建查询历史区域"""
        query_frame = ttk.LabelFrame(self.root, text="🔍 历史查询", padding="10")
        query_frame.pack(fill="x", padx=20, pady=10)
        
        # 查询输入框
        input_frame = ttk.Frame(query_frame)
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="查询日期:").pack(side="left")
        
        self.query_date_var = tk.StringVar()
        self.query_date_var.set(date.today().strftime('%Y-%m-%d'))
        
        date_entry = ttk.Entry(
            input_frame,
            textvariable=self.query_date_var,
            width=12
        )
        date_entry.pack(side="left", padx=5)
        
        query_button = ttk.Button(
            input_frame,
            text="查询",
            command=self._query_date_stats,
            width=8
        )
        query_button.pack(side="left", padx=5)
        
        # 查询结果显示
        self.query_result_var = tk.StringVar()
        self.query_result_var.set("请输入日期进行查询...")
        
        result_display = ttk.Label(
            query_frame,
            textvariable=self.query_result_var,
            font=("Consolas", 9),
            foreground="green"
        )
        result_display.pack(anchor="w", pady=(10, 0))
    
    def _create_status_section(self):
        """创建状态栏"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_var = tk.StringVar()
        self.status_var.set("📱 状态: 就绪")
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("微软雅黑", 8)
        )
        status_label.pack(side="left", padx=10, pady=5)
        
        # 运行时间显示
        self.uptime_var = tk.StringVar()
        self.uptime_var.set("")
        
        uptime_label = ttk.Label(
            status_frame,
            textvariable=self.uptime_var,
            font=("微软雅黑", 8),
            foreground="gray"
        )
        uptime_label.pack(side="right", padx=10, pady=5)
    
    def _toggle_monitoring(self):
        """切换监听状态"""
        if not self.is_monitoring:
            # 开始监听
            if self._start_monitoring():
                self.is_monitoring = True
                self.toggle_button.config(text="⏹️ 停止监听")
                self.status_var.set("📱 状态: 正在监听...")
                logger.info("用户启动监听")
            else:
                messagebox.showerror("错误", "启动监听失败！\n可能需要管理员权限。")
        else:
            # 停止监听
            if self._stop_monitoring():
                self.is_monitoring = False
                self.toggle_button.config(text="🚀 开始监听")
                self.status_var.set("📱 状态: 已停止")
                logger.info("用户停止监听")
            else:
                messagebox.showerror("错误", "停止监听失败！")
    
    def _start_monitoring(self):
        """启动监听"""
        try:
            return self.listener_manager.start(
                save_callback=self._on_data_save,
                save_interval=50  # MVP版本更频繁保存
            )
        except Exception as e:
            logger.error(f"启动监听失败: {e}")
            return False
    
    def _stop_monitoring(self):
        """停止监听"""
        try:
            return self.listener_manager.stop()
        except Exception as e:
            logger.error(f"停止监听失败: {e}")
            return False
    
    def _on_data_save(self, chinese_count, english_count):
        """数据保存回调"""
        try:
            # 保存到数据库
            success = self.data_storage.update_daily_stats(
                chinese_count, 
                english_count,
                total_keys=chinese_count + english_count
            )
            
            if success:
                logger.debug(f"数据已保存: 中文={chinese_count}, 英文={english_count}")
            else:
                logger.warning("数据保存失败")
                
        except Exception as e:
            logger.error(f"数据保存回调异常: {e}")
    
    def _force_save(self):
        """强制保存数据"""
        if self.is_monitoring and self.listener_manager.listener:
            self.listener_manager.listener.force_save()
            self.status_var.set("📱 状态: 数据已保存")
            messagebox.showinfo("提示", "数据已强制保存！")
        else:
            messagebox.showwarning("警告", "监听器未运行，无法保存！")
    
    def _reset_today(self):
        """重置今日统计"""
        if messagebox.askyesno("确认", "确定要重置今日统计数据吗？"):
            try:
                if self.is_monitoring and self.listener_manager.listener:
                    self.listener_manager.listener.reset_daily_stats()
                
                # 清空数据库中的今日数据
                today = date.today().strftime('%Y-%m-%d')
                self.data_storage.delete_daily_stats(today)
                
                self.status_var.set("📱 状态: 今日数据已重置")
                messagebox.showinfo("提示", "今日统计数据已重置！")
                
            except Exception as e:
                logger.error(f"重置数据失败: {e}")
                messagebox.showerror("错误", f"重置失败: {e}")
    
    def _setup_autostart(self):
        """设置自启动"""
        try:
            self.autostart_manager.setup_autostart_with_prompt()
        except Exception as e:
            logger.error(f"自启动设置失败: {e}")
            messagebox.showerror("错误", f"自启动设置失败: {e}")
    
    def _query_date_stats(self):
        """查询指定日期统计"""
        query_date = self.query_date_var.get().strip()
        
        try:
            # 验证日期格式
            datetime.strptime(query_date, '%Y-%m-%d')
            
            # 查询数据
            stats = self.data_storage.get_daily_stats(query_date)
            
            if stats:
                result_text = (
                    f"📅 {query_date} 统计:\n"
                    f"中文字符: {stats['chinese_chars']:,}\n"
                    f"英文字符: {stats['english_chars']:,}\n"
                    f"总计: {stats['total_chars']:,}\n"
                    f"更新时间: {stats.get('updated_at', 'N/A')}"
                )
                self.query_result_var.set(result_text)
            else:
                self.query_result_var.set(f"📅 {query_date}: 暂无统计数据")
                
        except ValueError:
            messagebox.showerror("错误", "日期格式错误！\n请使用 YYYY-MM-DD 格式")
        except Exception as e:
            logger.error(f"查询数据失败: {e}")
            messagebox.showerror("错误", f"查询失败: {e}")
    
    def _update_display(self):
        """更新界面显示"""
        try:
            # 获取当前统计
            if self.is_monitoring and self.listener_manager.listener:
                stats = self.listener_manager.get_stats()
                
                # 更新今日统计显示
                stats_text = (
                    f"今日统计 ({date.today().strftime('%Y-%m-%d')}):\n"
                    f"中文字符: {stats['chinese_count']:,}\n"
                    f"英文字符: {stats['english_count']:,}\n"
                    f"总计: {stats['total_count']:,}\n"
                    f"总按键: {stats['total_keys']:,}"
                )
                self.stats_var.set(stats_text)
                
                # 更新摘要信息
                if stats['total_count'] > 0:
                    chinese_ratio = stats['chinese_count'] / stats['total_count'] * 100
                    summary_text = f"中英文比例: {chinese_ratio:.1f}% : {100-chinese_ratio:.1f}%"
                    
                    # AI率简单评估
                    if stats['total_count'] > 1000:
                        ai_hint = " | 输出量较高，人工输出较多 💪"
                    elif stats['total_count'] > 200:
                        ai_hint = " | 输出量中等，正常工作状态 😊"
                    else:
                        ai_hint = " | 输出量较低，可能AI辅助较多 🤖"
                    
                    self.summary_var.set(summary_text + ai_hint)
                else:
                    self.summary_var.set("今日尚未开始输入...")
                
                # 更新运行时间
                if stats['uptime']:
                    uptime_str = str(stats['uptime']).split('.')[0]  # 去掉微秒
                    self.uptime_var.set(f"运行时间: {uptime_str}")
                
            else:
                # 从数据库获取今日统计
                today_stats = self.data_storage.get_daily_stats()
                if today_stats:
                    stats_text = (
                        f"今日统计 ({date.today().strftime('%Y-%m-%d')}):\n"
                        f"中文字符: {today_stats['chinese_chars']:,}\n"
                        f"英文字符: {today_stats['english_chars']:,}\n"
                        f"总计: {today_stats['total_chars']:,}"
                    )
                    self.stats_var.set(stats_text)
                else:
                    self.stats_var.set("今日尚未开始统计...")
                    self.summary_var.set("")
                    self.uptime_var.set("")
                
        except Exception as e:
            logger.warning(f"更新显示失败: {e}")
    
    def _start_update_timer(self):
        """启动定时更新"""
        self._update_display()
        # 每2秒更新一次界面
        self.root.after(2000, self._start_update_timer)
    
    def run(self):
        """运行主窗口"""
        try:
            # 设置关闭事件
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            
            logger.info("MVP窗口开始运行")
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"窗口运行异常: {e}")
            raise
    
    def _on_closing(self):
        """窗口关闭事件"""
        try:
            # 停止监听
            if self.is_monitoring:
                self._stop_monitoring()
            
            # 关闭数据存储
            self.data_storage.close()
            
            logger.info("MVP窗口正常关闭")
            self.root.destroy()
            
        except Exception as e:
            logger.error(f"窗口关闭异常: {e}")
            self.root.destroy()


# 测试函数
def test_mvp_window():
    """测试MVP窗口"""
    print("🧪 启动MVP窗口测试...")
    
    try:
        app = MVPWindow()
        app.run()
        print("✅ MVP窗口测试完成")
        
    except Exception as e:
        print(f"❌ MVP窗口测试失败: {e}")


if __name__ == "__main__":
    # 独立运行时启动测试
    test_mvp_window() 