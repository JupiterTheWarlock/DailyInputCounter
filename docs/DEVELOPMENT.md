# 🛠️ DailyInputCounter 开发指南

欢迎参与 DailyInputCounter 项目的开发！这份文档将帮助你快速上手项目开发喵～

## 🏃‍♂️ 快速开始

### 开发环境要求

- **操作系统**: Windows 10/11 (主要开发平台)
- **Python**: 3.8+ (推荐 3.10)
- **IDE**: VSCode, PyCharm 或其他支持Python的IDE
- **Git**: 用于版本控制

### 环境配置

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/DailyInputCounter.git
   cd DailyInputCounter
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS (如果需要)
   source venv/bin/activate
   ```

3. **安装开发依赖**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **配置开发工具**
   ```bash
   # 安装 pre-commit hooks
   pre-commit install
   
   # 运行代码格式化
   black .
   
   # 运行代码检查
   flake8 .
   ```

## 📁 项目结构详解

```
DailyInputCounter/
├── main.py                    # 程序入口点
├── core/                      # 核心业务逻辑
│   ├── __init__.py
│   ├── keyboard_listener.py   # 键盘监听器
│   ├── character_analyzer.py  # 字符分析器
│   ├── data_storage.py        # 数据存储管理
│   └── statistics_manager.py  # 统计数据管理
├── gui/                       # 图形用户界面
│   ├── __init__.py
│   ├── main_window.py         # 主窗口
│   ├── history_window.py      # 历史数据窗口
│   ├── settings_window.py     # 设置窗口
│   └── components/            # UI组件
│       ├── __init__.py
│       ├── charts.py          # 图表组件
│       └── widgets.py         # 自定义控件
├── config/                    # 配置管理
│   ├── __init__.py
│   ├── settings.py           # 配置管理器
│   └── constants.py          # 常量定义
├── utils/                     # 工具模块
│   ├── __init__.py
│   ├── logger.py             # 日志工具
│   ├── validators.py         # 数据验证
│   └── helpers.py            # 辅助函数
├── tests/                     # 测试代码
│   ├── __init__.py
│   ├── test_character_analyzer.py
│   ├── test_data_storage.py
│   └── fixtures/             # 测试数据
├── data/                      # 数据目录
│   ├── input_stats.db        # SQLite数据库
│   └── exports/              # 导出文件
├── docs/                      # 文档
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── DEVELOPMENT.md
├── scripts/                   # 工具脚本
│   ├── build.py              # 构建脚本
│   ├── install.py            # 安装脚本
│   └── migrate_db.py         # 数据库迁移
├── requirements.txt           # 生产依赖
├── requirements-dev.txt       # 开发依赖
├── setup.py                   # 打包配置
├── pyproject.toml            # 现代Python配置
├── .gitignore                # Git忽略文件
├── .pre-commit-config.yaml   # Pre-commit配置
└── README.md                 # 项目说明
```

## 🎯 核心模块开发

### 1. 键盘监听器 (keyboard_listener.py)

**功能**: 监听全局键盘输入事件

**关键点**:
- 使用 `pynput.keyboard.Listener` 进行全局监听
- 处理线程安全问题
- 过滤特殊键和系统键

**示例代码**:
```python
from pynput import keyboard
import threading
from typing import Callable, Optional

class KeyboardListener:
    def __init__(self):
        self.listener: Optional[keyboard.Listener] = None
        self.is_listening = False
        self.callback: Optional[Callable] = None
        self._lock = threading.Lock()
    
    def start_listening(self, callback: Callable):
        """开始监听键盘事件"""
        with self._lock:
            if self.is_listening:
                return
            
            self.callback = callback
            self.listener = keyboard.Listener(on_press=self._on_key_press)
            self.listener.start()
            self.is_listening = True
    
    def _on_key_press(self, key):
        """内部键盘事件处理"""
        try:
            if hasattr(key, 'char') and key.char:
                if self.callback:
                    self.callback(key.char)
        except Exception as e:
            # 记录错误但不中断监听
            pass
```

### 2. 字符分析器 (character_analyzer.py)

**功能**: 分析字符类型（中文/英文/其他）

**关键点**:
- Unicode范围判断
- 性能优化
- 扩展性设计

**示例代码**:
```python
import re
from enum import Enum
from typing import Dict, Any

class CharType(Enum):
    CHINESE = "chinese"
    ENGLISH = "english"
    NUMBER = "number"
    SYMBOL = "symbol"
    OTHER = "other"

class CharacterAnalyzer:
    # 预编译正则表达式提升性能
    CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]')
    ENGLISH_PATTERN = re.compile(r'[a-zA-Z]')
    NUMBER_PATTERN = re.compile(r'[0-9]')
    
    @classmethod
    def analyze_char(cls, char: str) -> CharType:
        """分析单个字符的类型"""
        if cls.CHINESE_PATTERN.match(char):
            return CharType.CHINESE
        elif cls.ENGLISH_PATTERN.match(char):
            return CharType.ENGLISH
        elif cls.NUMBER_PATTERN.match(char):
            return CharType.NUMBER
        elif char in "!@#$%^&*()_+-=[]{}|;:,.<>?":
            return CharType.SYMBOL
        else:
            return CharType.OTHER
    
    @classmethod
    def analyze_text(cls, text: str) -> Dict[CharType, int]:
        """分析文本中各类型字符的数量"""
        result = {char_type: 0 for char_type in CharType}
        
        for char in text:
            char_type = cls.analyze_char(char)
            result[char_type] += 1
        
        return result
```

### 3. 数据存储 (data_storage.py)

**功能**: 管理SQLite数据库操作

**关键点**:
- 连接池管理
- 事务处理
- 异步操作支持

## 🎨 编码规范

### Python代码风格

1. **PEP 8**: 遵循Python官方编码规范
2. **Black**: 使用Black进行代码格式化
3. **类型注解**: 所有公共函数必须包含类型注解
4. **文档字符串**: 使用Google风格的docstring

**示例**:
```python
def calculate_daily_stats(
    date: str, 
    chinese_count: int, 
    english_count: int
) -> Dict[str, Any]:
    """计算每日统计数据。
    
    Args:
        date: 统计日期，格式为YYYY-MM-DD
        chinese_count: 中文字符数量
        english_count: 英文字符数量
    
    Returns:
        包含统计结果的字典
        
    Raises:
        ValueError: 当日期格式不正确时
    """
    # 实现代码...
```

### 命名规范

- **变量和函数**: `snake_case`
- **类**: `PascalCase`
- **常量**: `UPPER_SNAKE_CASE`
- **私有成员**: 以单下划线开头 `_private_var`
- **文件名**: `snake_case.py`

### 注释规范

```python
# 单行注释用于解释复杂逻辑
def complex_function():
    # 计算复杂的统计数据
    pass

"""
多行注释用于模块和类的说明
描述模块的主要功能和使用方法
"""

class ExampleClass:
    """类的文档字符串
    
    详细描述类的功能、使用方法和注意事项
    """
    pass
```

## 🧪 测试指南

### 测试结构

```
tests/
├── unit/                  # 单元测试
│   ├── test_analyzer.py
│   └── test_storage.py
├── integration/           # 集成测试
│   └── test_workflow.py
├── fixtures/              # 测试数据
│   └── sample_data.json
└── conftest.py           # pytest配置
```

### 编写测试

**单元测试示例**:
```python
import pytest
from core.character_analyzer import CharacterAnalyzer, CharType

class TestCharacterAnalyzer:
    def test_chinese_character(self):
        """测试中文字符识别"""
        assert CharacterAnalyzer.analyze_char('你') == CharType.CHINESE
        assert CharacterAnalyzer.analyze_char('好') == CharType.CHINESE
    
    def test_english_character(self):
        """测试英文字符识别"""
        assert CharacterAnalyzer.analyze_char('H') == CharType.ENGLISH
        assert CharacterAnalyzer.analyze_char('e') == CharType.ENGLISH
    
    @pytest.mark.parametrize("char,expected", [
        ('1', CharType.NUMBER),
        ('!', CharType.SYMBOL),
        (' ', CharType.OTHER),
    ])
    def test_various_characters(self, char, expected):
        """测试各种字符类型"""
        assert CharacterAnalyzer.analyze_char(char) == expected
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_character_analyzer.py

# 运行测试并生成覆盖率报告
pytest --cov=core tests/

# 运行测试并显示详细输出
pytest -v
```

## 🔄 Git工作流

### 分支策略

- **main**: 主分支，稳定版本
- **develop**: 开发分支，集成新功能
- **feature/xxx**: 功能分支
- **hotfix/xxx**: 热修复分支

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范:

```
type(scope): description

[optional body]

[optional footer]
```

**类型**:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat(analyzer): 添加数字字符识别功能

- 新增数字字符类型枚举
- 实现数字字符识别逻辑
- 添加相关单元测试

Closes #123
```

### 开发流程

1. **创建功能分支**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   ```

2. **开发和提交**
   ```bash
   # 开发代码...
   git add .
   git commit -m "feat: 添加新功能"
   ```

3. **推送和创建PR**
   ```bash
   git push origin feature/new-feature
   # 在GitHub创建Pull Request
   ```

4. **代码审查和合并**
   - 等待代码审查
   - 根据反馈修改代码
   - 合并到develop分支

## 🚀 构建和发布

### 本地构建

```bash
# 运行构建脚本
python scripts/build.py

# 生成可执行文件
pyinstaller --onefile main.py

# 创建安装包
python setup.py bdist_wheel
```

### CI/CD流程

项目使用GitHub Actions进行自动化构建:

```yaml
# .github/workflows/ci.yml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## 📚 学习资源

### 推荐阅读

- [Clean Code](https://book.douban.com/subject/4199741/): 代码整洁之道
- [Effective Python](https://effectivepython.com/): Python编程技巧
- [Python Design Patterns](https://python-patterns.guide/): Python设计模式

### 相关技术文档

- [pynput Documentation](https://pynput.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

## 🆘 获取帮助

如果在开发过程中遇到问题:

1. **查看文档**: 首先查看相关技术文档
2. **搜索Issues**: 在GitHub Issues中搜索类似问题
3. **提问**: 创建新的Issue详细描述问题
4. **讨论**: 在GitHub Discussions中参与讨论

## 🤝 贡献流程

1. **Fork仓库**
2. **创建功能分支**
3. **编写代码和测试**
4. **提交Pull Request**
5. **参与代码审查**
6. **合并代码**

感谢你参与DailyInputCounter的开发！让我们一起创造更好的工具喵～ 🐱 