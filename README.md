# 📊 DailyInputCounter - 每日输入统计器

一个用于统计Windows系统下每日中英文键盘输入量的小工具喵～

## 🎯 项目简介

DailyInputCounter 是一个轻量级的键盘输入统计工具，能够实时监听用户的键盘输入，智能识别并统计中文和英文字符的输入数量。通过这个工具，你可以了解自己每天的打字习惯和输入效率。

## ✨ 功能特性

- 🔍 **智能字符识别**: 自动区分中文汉字和英文字母
- 📈 **实时统计**: 实时显示当日输入的中英文字符数量
- 💾 **数据持久化**: 使用SQLite数据库本地存储历史数据
- 📊 **历史查看**: 查看每日、每周、每月的输入统计
- 📁 **数据导出**: 支持导出CSV格式的统计报告
- 🖥️ **简洁界面**: 友好的GUI界面，操作简单直观
- 🔐 **隐私保护**: 仅统计字符数量，不记录具体输入内容
- ⚡ **轻量运行**: 低内存占用，后台静默运行

## 🛠️ 技术架构

### 核心技术栈
- **Python 3.8+**: 主要开发语言
- **pynput**: 跨平台键盘监听库
- **SQLite**: 轻量级本地数据库
- **tkinter**: GUI界面框架
- **matplotlib**: 数据可视化

### 项目结构
```
DailyInputCounter/
├── main.py                    # 程序入口
├── core/                      # 核心功能模块
│   ├── __init__.py
│   ├── keyboard_listener.py   # 键盘监听
│   ├── character_analyzer.py  # 字符分析
│   └── data_storage.py        # 数据存储
├── gui/                       # 图形界面
│   ├── __init__.py
│   └── main_window.py         # 主窗口
├── config/                    # 配置管理
│   ├── __init__.py
│   └── settings.py            # 设置配置
├── data/                      # 数据目录
│   └── input_stats.db         # SQLite数据库
├── requirements.txt           # 依赖列表
├── docs/                      # 文档目录
│   ├── ARCHITECTURE.md        # 架构文档
│   ├── API.md                 # API文档
│   └── DEVELOPMENT.md         # 开发文档
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 环境要求
- Windows 10/11 (64位)
- Python 3.8 或更高版本
- 管理员权限 (用于全局键盘监听)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/DailyInputCounter.git
   cd DailyInputCounter
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

### 首次使用

1. 启动程序后，会出现主界面
2. 点击"开始监听"按钮开始统计
3. 程序会在系统托盘中运行
4. 实时查看当日输入统计
5. 可在"历史数据"标签页查看往日记录

## 📋 使用说明

### 主要功能

#### 🎯 实时统计
- 显示当日中文字符输入数量
- 显示当日英文字符输入数量
- 显示总字符数和输入效率

#### 📊 数据分析
- 按日期查看历史统计
- 生成输入趋势图表
- 导出统计数据到CSV文件

#### ⚙️ 设置选项
- 开机自动启动
- 数据保存路径设置
- 统计精度调整
- 界面主题切换

### 字符识别规则

| 字符类型 | 识别范围 | 示例 |
|---------|---------|------|
| 中文字符 | Unicode范围 \u4e00-\u9fff | 你好世界、汉字 |
| 英文字符 | a-z, A-Z | Hello, World |
| 其他字符 | 数字、符号等 | 123, !@# |

## 🔧 配置说明

### 配置文件位置
- Windows: `%APPDATA%/DailyInputCounter/config.json`

### 配置选项
```json
{
  "auto_start": true,
  "data_path": "./data",
  "save_interval": 60,
  "show_notifications": true,
  "theme": "light"
}
```

## 📈 数据结构

### 数据库表结构

**daily_stats** - 每日统计表
| 字段名 | 类型 | 说明 |
|-------|------|------|
| id | INTEGER | 主键 |
| date | TEXT | 统计日期 (YYYY-MM-DD) |
| chinese_chars | INTEGER | 中文字符数 |
| english_chars | INTEGER | 英文字符数 |
| total_chars | INTEGER | 总字符数 |
| created_at | TIMESTAMP | 创建时间 |

## 🔐 隐私说明

本工具严格保护用户隐私：
- ✅ 仅统计字符类型和数量
- ✅ 不记录具体输入内容
- ✅ 数据完全存储在本地
- ✅ 不上传任何信息到网络
- ✅ 用户完全控制数据的删除

## 🐛 常见问题

### Q: 程序需要管理员权限吗？
A: 是的，全局键盘监听需要管理员权限才能正常工作。

### Q: 会影响系统性能吗？
A: 不会，程序采用异步处理，内存占用小于20MB。

### Q: 支持其他操作系统吗？
A: 目前仅支持Windows，未来可能扩展到macOS和Linux。

### Q: 数据会丢失吗？
A: 程序每分钟自动保存数据，并在程序退出时完整保存所有数据。

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [pynput](https://github.com/moses-palmer/pynput) - 优秀的跨平台输入监听库
- 所有为开源社区贡献的开发者们

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/DailyInputCounter/issues)

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下喵～ 