# 📐 DailyInputCounter 架构设计文档

## 🏗️ 系统架构概览

DailyInputCounter 采用模块化设计，主要分为以下几个核心模块：

```
┌─────────────────────────────────────────────────────────────────┐
│                         GUI Layer (GUI层)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Main Window   │  │  Settings UI    │  │  Charts UI      │ │
│  │   主窗口界面     │  │   设置界面      │  │   图表界面      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic (业务逻辑层)                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Keyboard        │  │ Character       │  │ Statistics      │ │
│  │ Listener        │  │ Analyzer        │  │ Manager         │ │
│  │ 键盘监听器       │  │ 字符分析器       │  │ 统计管理器       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Access Layer (数据访问层)               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ SQLite          │  │ CSV Exporter    │  │ Config          │ │
│  │ Database        │  │ CSV导出器       │  │ Manager         │ │
│  │ 数据库访问       │  │                 │  │ 配置管理器       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 核心模块详解

### 1. 键盘监听模块 (Keyboard Listener)

**职责**: 监听全局键盘事件，捕获用户输入

**技术实现**:
- 使用 `pynput.keyboard` 实现全局键盘Hook
- 异步事件处理，避免阻塞主线程
- 过滤系统特殊键，只处理可见字符

**核心类**:
```python
class KeyboardListener:
    def __init__(self):
        self.listener = None
        self.is_listening = False
        self.callback = None
    
    def start_listening(self, callback):
        """开始监听键盘事件"""
        
    def stop_listening(self):
        """停止监听"""
        
    def on_key_press(self, key):
        """键盘按下事件处理"""
```

### 2. 字符分析模块 (Character Analyzer)

**职责**: 分析输入字符的类型（中文/英文/其他）

**技术实现**:
- Unicode 字符范围判断
- 中文字符识别：`\u4e00-\u9fff` (CJK统一汉字)
- 英文字符识别：`a-zA-Z`

**核心类**:
```python
class CharacterAnalyzer:
    @staticmethod
    def is_chinese_char(char):
        """判断是否为中文字符"""
        
    @staticmethod
    def is_english_char(char):
        """判断是否为英文字符"""
        
    @staticmethod
    def analyze_char(char):
        """分析字符类型，返回字符类型枚举"""
```

### 3. 数据存储模块 (Data Storage)

**职责**: 管理数据的持久化存储

**技术实现**:
- SQLite 数据库存储
- 异步写入机制
- 数据备份和恢复

**数据库设计**:
```sql
-- 每日统计表
CREATE TABLE daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    chinese_chars INTEGER DEFAULT 0,
    english_chars INTEGER DEFAULT 0,
    total_chars INTEGER DEFAULT 0,
    session_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 会话记录表 (记录每次使用程序的会话)
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    chinese_chars INTEGER DEFAULT 0,
    english_chars INTEGER DEFAULT 0,
    total_chars INTEGER DEFAULT 0
);

-- 小时统计表 (用于更细粒度的分析)
CREATE TABLE hourly_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    hour INTEGER NOT NULL,
    chinese_chars INTEGER DEFAULT 0,
    english_chars INTEGER DEFAULT 0,
    total_chars INTEGER DEFAULT 0,
    PRIMARY KEY (date, hour)
);
```

### 4. GUI界面模块

**职责**: 提供用户交互界面

**技术实现**:
- tkinter 原生GUI框架
- 响应式布局设计
- 实时数据更新

**主要窗口**:
- **MainWindow**: 主界面，显示实时统计
- **HistoryWindow**: 历史数据查看
- **SettingsWindow**: 配置设置
- **AboutWindow**: 关于页面

## 🔄 数据流设计

### 输入数据流
```
用户键盘输入 → KeyboardListener → CharacterAnalyzer → StatisticsManager → DataStorage
```

### 展示数据流
```
DataStorage → StatisticsManager → GUI Components → 用户界面
```

## ⚡ 性能优化策略

### 1. 异步处理
- 键盘事件监听使用独立线程
- 数据库操作异步执行
- GUI更新使用队列机制

### 2. 内存管理
- 定期清理内存缓存
- 使用生成器处理大量数据
- 限制历史数据加载量

### 3. 数据库优化
- 建立适当索引
- 批量写入减少I/O
- 定期数据库维护

## 🔐 安全性设计

### 1. 隐私保护
- 不存储具体输入内容
- 仅统计字符类型和数量
- 所有数据本地存储

### 2. 权限管理
- 最小权限原则
- 管理员权限提示
- 安全的文件访问

### 3. 数据安全
- 数据库加密选项
- 配置文件保护
- 安全的数据导出

## 🧪 测试策略

### 1. 单元测试
- 每个模块独立测试
- 字符识别准确性测试
- 数据存储一致性测试

### 2. 集成测试
- 模块间交互测试
- 数据流完整性测试
- 异常情况处理测试

### 3. 性能测试
- 长时间运行稳定性
- 内存泄漏检测
- 响应时间测试

## 🔮 扩展性设计

### 1. 插件系统 (未来)
- 支持自定义字符识别规则
- 可扩展的统计维度
- 第三方数据源集成

### 2. 多语言支持 (未来)
- 国际化框架
- 多语言字符识别
- 本地化界面

### 3. 云同步 (未来)
- 可选的云端数据同步
- 多设备数据共享
- 隐私保护的云存储

## 📊 监控和日志

### 1. 应用监控
- 性能指标收集
- 错误追踪
- 使用情况统计

### 2. 日志管理
- 分级日志记录
- 日志轮转机制
- 调试信息收集

这个架构设计确保了系统的**可维护性**、**可扩展性**和**性能**，同时严格保护用户隐私喵～ 