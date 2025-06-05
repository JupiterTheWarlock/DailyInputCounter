# 📖 DailyInputCounter API 文档

本文档详细描述了 DailyInputCounter 项目各个模块的 API 接口和使用方法喵～

## 🏗️ 模块概览

```
核心模块 (core/)
├── KeyboardListener      # 键盘监听接口
├── CharacterAnalyzer     # 字符分析接口  
├── DataStorage          # 数据存储接口
└── StatisticsManager    # 统计管理接口

GUI模块 (gui/)
├── MainWindow           # 主窗口接口
├── HistoryWindow        # 历史窗口接口
└── SettingsWindow       # 设置窗口接口

工具模块 (utils/)
├── Logger              # 日志工具接口
├── Validators          # 数据验证接口
└── Helpers             # 辅助工具接口
```

## 🎯 核心模块 API

### KeyboardListener

全局键盘监听器，用于捕获用户的键盘输入事件。

#### 类定义

```python
class KeyboardListener:
    """全局键盘监听器
    
    用于监听全局键盘事件，捕获用户输入的字符。
    支持开始/停止监听，并通过回调函数处理键盘事件。
    """
```

#### 方法

##### `__init__()`

```python
def __init__(self) -> None:
    """初始化键盘监听器"""
```

##### `start_listening(callback)`

```python
def start_listening(self, callback: Callable[[str], None]) -> bool:
    """开始监听键盘事件
    
    Args:
        callback: 键盘事件回调函数，接收字符参数
        
    Returns:
        bool: 启动成功返回True，否则返回False
        
    Raises:
        RuntimeError: 当监听器已经在运行时
        PermissionError: 当缺少必要权限时
    """
```

##### `stop_listening()`

```python
def stop_listening(self) -> bool:
    """停止监听键盘事件
    
    Returns:
        bool: 停止成功返回True，否则返回False
    """
```

##### `is_listening`

```python
@property
def is_listening(self) -> bool:
    """检查是否正在监听
    
    Returns:
        bool: 正在监听返回True，否则返回False
    """
```

#### 使用示例

```python
from core.keyboard_listener import KeyboardListener

def on_key_pressed(char: str):
    print(f"按下了字符: {char}")

# 创建监听器
listener = KeyboardListener()

# 开始监听
listener.start_listening(on_key_pressed)

# 检查状态
if listener.is_listening:
    print("正在监听键盘事件")

# 停止监听
listener.stop_listening()
```

---

### CharacterAnalyzer

字符类型分析器，用于识别和分类不同类型的字符。

#### 枚举定义

```python
class CharType(Enum):
    """字符类型枚举"""
    CHINESE = "chinese"    # 中文字符
    ENGLISH = "english"    # 英文字符
    NUMBER = "number"      # 数字字符
    SYMBOL = "symbol"      # 符号字符
    OTHER = "other"        # 其他字符
```

#### 类定义

```python
class CharacterAnalyzer:
    """字符分析器
    
    提供字符类型识别功能，支持中文、英文、数字、符号等字符的分类。
    """
```

#### 静态方法

##### `analyze_char(char)`

```python
@staticmethod
def analyze_char(char: str) -> CharType:
    """分析单个字符的类型
    
    Args:
        char: 要分析的字符
        
    Returns:
        CharType: 字符类型枚举值
        
    Examples:
        >>> CharacterAnalyzer.analyze_char('你')
        CharType.CHINESE
        >>> CharacterAnalyzer.analyze_char('A')
        CharType.ENGLISH
    """
```

##### `analyze_text(text)`

```python
@staticmethod
def analyze_text(text: str) -> Dict[CharType, int]:
    """分析文本中各类型字符的数量
    
    Args:
        text: 要分析的文本
        
    Returns:
        Dict[CharType, int]: 各字符类型的统计数量
        
    Examples:
        >>> CharacterAnalyzer.analyze_text("Hello你好123")
        {
            CharType.ENGLISH: 5,
            CharType.CHINESE: 2,
            CharType.NUMBER: 3,
            CharType.SYMBOL: 0,
            CharType.OTHER: 0
        }
    """
```

##### `is_chinese_char(char)`

```python
@staticmethod
def is_chinese_char(char: str) -> bool:
    """判断是否为中文字符
    
    Args:
        char: 要判断的字符
        
    Returns:
        bool: 是中文字符返回True，否则返回False
    """
```

##### `is_english_char(char)`

```python
@staticmethod
def is_english_char(char: str) -> bool:
    """判断是否为英文字符
    
    Args:
        char: 要判断的字符
        
    Returns:
        bool: 是英文字符返回True，否则返回False
    """
```

#### 使用示例

```python
from core.character_analyzer import CharacterAnalyzer, CharType

# 分析单个字符
char_type = CharacterAnalyzer.analyze_char('你')
print(f"字符类型: {char_type}")  # CharType.CHINESE

# 分析文本
text = "Hello你好World世界123!"
stats = CharacterAnalyzer.analyze_text(text)
print(f"英文字符: {stats[CharType.ENGLISH]}")  # 10
print(f"中文字符: {stats[CharType.CHINESE]}")  # 4

# 字符类型判断
print(CharacterAnalyzer.is_chinese_char('你'))  # True
print(CharacterAnalyzer.is_english_char('A'))   # True
```

---

### DataStorage

数据持久化存储管理器，负责SQLite数据库操作。

#### 类定义

```python
class DataStorage:
    """数据存储管理器
    
    负责管理SQLite数据库的连接、数据的增删改查操作。
    提供线程安全的数据访问接口。
    """
```

#### 方法

##### `__init__(db_path)`

```python
def __init__(self, db_path: str = "data/input_stats.db") -> None:
    """初始化数据存储管理器
    
    Args:
        db_path: 数据库文件路径，默认为 "data/input_stats.db"
    """
```

##### `initialize_database()`

```python
def initialize_database(self) -> bool:
    """初始化数据库表结构
    
    创建必要的表和索引，如果表已存在则跳过。
    
    Returns:
        bool: 初始化成功返回True，否则返回False
        
    Raises:
        DatabaseError: 数据库操作失败时
    """
```

##### `save_daily_stats(stats)`

```python
def save_daily_stats(self, stats: DailyStats) -> bool:
    """保存每日统计数据
    
    Args:
        stats: 每日统计数据对象
        
    Returns:
        bool: 保存成功返回True，否则返回False
        
    Raises:
        ValueError: 当统计数据格式不正确时
        DatabaseError: 数据库操作失败时
    """
```

##### `get_daily_stats(date)`

```python
def get_daily_stats(self, date: str) -> Optional[DailyStats]:
    """获取指定日期的统计数据
    
    Args:
        date: 日期字符串，格式为 "YYYY-MM-DD"
        
    Returns:
        Optional[DailyStats]: 统计数据对象，如果不存在返回None
        
    Raises:
        ValueError: 当日期格式不正确时
        DatabaseError: 数据库查询失败时
    """
```

##### `get_stats_range(start_date, end_date)`

```python
def get_stats_range(
    self, 
    start_date: str, 
    end_date: str
) -> List[DailyStats]:
    """获取日期范围内的统计数据
    
    Args:
        start_date: 开始日期，格式为 "YYYY-MM-DD"
        end_date: 结束日期，格式为 "YYYY-MM-DD"
        
    Returns:
        List[DailyStats]: 统计数据列表，按日期排序
        
    Raises:
        ValueError: 当日期格式不正确或范围无效时
        DatabaseError: 数据库查询失败时
    """
```

##### `export_to_csv(output_path, start_date, end_date)`

```python
def export_to_csv(
    self, 
    output_path: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> bool:
    """导出数据到CSV文件
    
    Args:
        output_path: 输出文件路径
        start_date: 开始日期，可选
        end_date: 结束日期，可选
        
    Returns:
        bool: 导出成功返回True，否则返回False
        
    Raises:
        IOError: 文件写入失败时
        DatabaseError: 数据库查询失败时
    """
```

#### 数据模型

##### `DailyStats`

```python
@dataclass
class DailyStats:
    """每日统计数据模型"""
    date: str                    # 日期 (YYYY-MM-DD)
    chinese_chars: int = 0       # 中文字符数
    english_chars: int = 0       # 英文字符数
    total_chars: int = 0         # 总字符数
    session_count: int = 0       # 会话数量
    created_at: Optional[str] = None    # 创建时间
    updated_at: Optional[str] = None    # 更新时间
```

#### 使用示例

```python
from core.data_storage import DataStorage, DailyStats
from datetime import date

# 初始化存储管理器
storage = DataStorage("data/my_stats.db")
storage.initialize_database()

# 创建统计数据
stats = DailyStats(
    date="2024-01-01",
    chinese_chars=150,
    english_chars=300,
    total_chars=450
)

# 保存数据
storage.save_daily_stats(stats)

# 获取数据
daily_stats = storage.get_daily_stats("2024-01-01")
if daily_stats:
    print(f"中文字符: {daily_stats.chinese_chars}")

# 获取范围数据
stats_list = storage.get_stats_range("2024-01-01", "2024-01-07")

# 导出CSV
storage.export_to_csv("exports/stats.csv", "2024-01-01", "2024-01-31")
```

---

### StatisticsManager

统计数据管理器，提供高级的统计分析功能。

#### 类定义

```python
class StatisticsManager:
    """统计管理器
    
    提供统计数据的高级分析功能，包括趋势分析、汇总统计等。
    """
```

#### 方法

##### `__init__(storage)`

```python
def __init__(self, storage: DataStorage) -> None:
    """初始化统计管理器
    
    Args:
        storage: 数据存储管理器实例
    """
```

##### `get_current_stats()`

```python
def get_current_stats(self) -> DailyStats:
    """获取当前日期的统计数据
    
    Returns:
        DailyStats: 今日统计数据，如果不存在则创建新的
    """
```

##### `update_stats(char_type, count)`

```python
def update_stats(self, char_type: CharType, count: int = 1) -> None:
    """更新统计数据
    
    Args:
        char_type: 字符类型
        count: 增加的数量，默认为1
        
    Raises:
        ValueError: 当字符类型无效或数量为负数时
    """
```

##### `get_weekly_summary(week_start)`

```python
def get_weekly_summary(self, week_start: str) -> WeeklySummary:
    """获取周统计摘要
    
    Args:
        week_start: 周开始日期，格式为 "YYYY-MM-DD"
        
    Returns:
        WeeklySummary: 周统计摘要对象
        
    Raises:
        ValueError: 当日期格式不正确时
    """
```

##### `get_monthly_summary(year, month)`

```python
def get_monthly_summary(self, year: int, month: int) -> MonthlySummary:
    """获取月统计摘要
    
    Args:
        year: 年份
        month: 月份 (1-12)
        
    Returns:
        MonthlySummary: 月统计摘要对象
        
    Raises:
        ValueError: 当年月参数无效时
    """
```

##### `get_trend_analysis(days)`

```python
def get_trend_analysis(self, days: int = 30) -> TrendAnalysis:
    """获取趋势分析
    
    Args:
        days: 分析天数，默认30天
        
    Returns:
        TrendAnalysis: 趋势分析结果
    """
```

#### 使用示例

```python
from core.statistics_manager import StatisticsManager
from core.data_storage import DataStorage

# 初始化
storage = DataStorage()
stats_manager = StatisticsManager(storage)

# 更新统计
stats_manager.update_stats(CharType.CHINESE, 5)
stats_manager.update_stats(CharType.ENGLISH, 10)

# 获取当前统计
current = stats_manager.get_current_stats()
print(f"今日中文: {current.chinese_chars}")

# 获取周统计
weekly = stats_manager.get_weekly_summary("2024-01-01")
print(f"本周总计: {weekly.total_chars}")

# 趋势分析
trend = stats_manager.get_trend_analysis(7)
print(f"平均每日: {trend.daily_average}")
```

## 🖥️ GUI 模块 API

### MainWindow

主窗口界面类，提供应用程序的主要用户界面。

#### 类定义

```python
class MainWindow:
    """主窗口类
    
    应用程序的主界面，显示实时统计数据和控制面板。
    """
```

#### 方法

##### `__init__(stats_manager)`

```python
def __init__(self, stats_manager: StatisticsManager) -> None:
    """初始化主窗口
    
    Args:
        stats_manager: 统计管理器实例
    """
```

##### `show()`

```python
def show(self) -> None:
    """显示主窗口"""
```

##### `hide()`

```python
def hide(self) -> None:
    """隐藏主窗口"""
```

##### `update_display()`

```python
def update_display(self) -> None:
    """更新显示数据
    
    刷新界面上的统计数据显示。
    """
```

##### `start_monitoring()`

```python
def start_monitoring(self) -> bool:
    """开始监听
    
    Returns:
        bool: 启动成功返回True，否则返回False
    """
```

##### `stop_monitoring()`

```python
def stop_monitoring(self) -> bool:
    """停止监听
    
    Returns:
        bool: 停止成功返回True，否则返回False
    """
```

## 🔧 工具模块 API

### Logger

日志管理工具，提供统一的日志记录功能。

#### 函数

##### `setup_logger(name, level)`

```python
def setup_logger(
    name: str, 
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别 ("DEBUG", "INFO", "WARNING", "ERROR")
        log_file: 日志文件路径，可选
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
```

##### `get_logger(name)`

```python
def get_logger(name: str) -> logging.Logger:
    """获取日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器实例
    """
```

#### 使用示例

```python
from utils.logger import setup_logger, get_logger

# 设置日志
logger = setup_logger("main", "DEBUG", "logs/app.log")

# 使用日志
logger.info("应用程序启动")
logger.warning("这是一个警告")
logger.error("发生错误")

# 获取已配置的日志记录器
logger = get_logger("main")
```

### Validators

数据验证工具，提供常用的数据验证功能。

#### 函数

##### `validate_date(date_str)`

```python
def validate_date(date_str: str) -> bool:
    """验证日期格式
    
    Args:
        date_str: 日期字符串，格式应为 "YYYY-MM-DD"
        
    Returns:
        bool: 格式正确返回True，否则返回False
    """
```

##### `validate_char_count(count)`

```python
def validate_char_count(count: int) -> bool:
    """验证字符数量
    
    Args:
        count: 字符数量
        
    Returns:
        bool: 数量有效返回True（>=0），否则返回False
    """
```

#### 使用示例

```python
from utils.validators import validate_date, validate_char_count

# 验证日期
if validate_date("2024-01-01"):
    print("日期格式正确")

# 验证字符数量
if validate_char_count(100):
    print("字符数量有效")
```

## 🚨 异常处理

### 自定义异常

```python
class DailyInputCounterError(Exception):
    """基础异常类"""
    pass

class KeyboardListenerError(DailyInputCounterError):
    """键盘监听异常"""
    pass

class DatabaseError(DailyInputCounterError):
    """数据库操作异常"""
    pass

class ValidationError(DailyInputCounterError):
    """数据验证异常"""
    pass
```

### 异常处理示例

```python
from core.keyboard_listener import KeyboardListener, KeyboardListenerError

try:
    listener = KeyboardListener()
    listener.start_listening(callback)
except KeyboardListenerError as e:
    logger.error(f"键盘监听失败: {e}")
except PermissionError:
    logger.error("权限不足，请以管理员身份运行")
except Exception as e:
    logger.error(f"未知错误: {e}")
```

## 📊 数据格式

### JSON 配置格式

```json
{
  "auto_start": true,
  "save_interval": 60,
  "data_path": "./data",
  "log_level": "INFO",
  "gui": {
    "theme": "light",
    "window_size": [800, 600],
    "show_tray_icon": true
  },
  "database": {
    "backup_enabled": true,
    "backup_interval": 24
  }
}
```

### CSV 导出格式

```csv
date,chinese_chars,english_chars,total_chars,session_count
2024-01-01,150,300,450,5
2024-01-02,200,250,450,3
2024-01-03,180,320,500,4
```

这个API文档为开发者提供了完整的接口说明，让使用和扩展变得更加容易喵～ 🐱 