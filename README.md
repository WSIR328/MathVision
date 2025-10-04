# MathVision 🎓

<div align="center">

![MathVision Logo](logo.png)

**一个功能强大的数学可视化教学工具**

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [模块介绍](#-模块介绍) • [技术栈](#-技术栈) • [贡献指南](#-贡献指南)

</div>

---

## 📖 项目简介

MathVision 是一个基于 Python 和 Tkinter 开发的综合性数学可视化教学工具，由西安电子科技大学学生开发，龚老师指导，旨在通过直观的图形界面和动画演示，帮助学生和教师更好地理解和教授数学概念。

### ✨ 主要亮点

- 🎨 **现代化界面** - 采用深色科技风格，视觉体验出色
- 🧮 **功能全面** - 涵盖高等数学、线性代数、概率统计等多个领域
- 📊 **实时可视化** - 动态图表和动画演示，直观展示数学概念
- 🤖 **AI 辅助** - 集成 DeepSeek AI，智能数据分析
- 📚 **知识学习** - 内置 9 个数学知识点详细说明
- 🚀 **易于使用** - 简洁的操作界面，无需编程基础

---

## 🎯 功能特性

### 📐 高等数学模块

- **方程绘图器** - 绘制各种函数图像，支持参数调整
- **微分方程求解** - 求解常微分方程，可视化解的图像
- **海森矩阵分析** - 多元函数极值分析，3D 曲面可视化
- **科赫曲线** - 分形几何演示，动画展示迭代过程
- **三角函数绘图** - 三角函数可视化，参数实时调整

### 🔢 线性代数模块

- **矩阵计算器** - 矩阵加减乘除、求逆、行列式计算
- **特征值分析** - 计算特征值和特征向量，可视化展示
- **高斯消元法** - 动画演示消元过程，逐步求解
- **基变换可视化** - 2D 线性变换动画演示
- **行列式计算** - 多种方法计算行列式
- **矩阵转置** - 可视化转置过程
- **矩阵对比** - 对比分析两个矩阵
- **过渡矩阵** - 基变换的过渡矩阵计算

### 📊 概率统计模块

- **概率论基础** - 概率计算、条件概率、全概率公式
- **贝叶斯分析** - 贝叶斯定理应用和可视化
- **随机变量** - 离散型和连续型随机变量分析
- **随机过程** - 马尔可夫链、泊松过程等
- **统计分析** - 描述性统计、相关性分析、回归分析
- **假设检验** - t 检验、卡方检验、F 检验
- **置信区间** - 各种参数的置信区间计算
- **蒙特卡洛模拟** - 随机模拟和概率估计
- **概率游戏** - 三门问题、生日悖论等经典问题

### 🔢 数列模块

- **数列分析** - 等差数列、等比数列、斐波那契数列
- **数列求和** - 各种数列的求和公式
- **数列极限** - 极限计算和收敛性分析

### 🤖 AI 数据分析

- **智能分析** - 基于 DeepSeek AI 的自然语言数据分析
- **数据导入** - 支持 Excel (.xlsx, .xls) 和 CSV 文件
- **自动可视化** - 自动生成各种图表
- **自然语言查询** - 用自然语言提问，AI 自动分析

### 📚 知识点学习

内置 9 个详细的数学知识点：
1. 矩形积分法（黎曼和）
2. 泰勒级数展开
3. 函数的分割与区间分析
4. 切线与法线
5. 数列与级数
6. 微分方程
7. 方程可视化与图形分析
8. 分形几何 - 科赫曲线
9. 海森矩阵

---

## 🚀 快速开始

### 环境要求

- Python 3.11 或更高版本
- Windows 操作系统（推荐）
- 4GB 以上内存

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/WSIR328/MathVision.git
cd MathVision
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **运行程序**

```bash
python main.py
```

### 使用 AI 功能

AI 数据分析功能需要 DeepSeek API Key：

1. 访问 [DeepSeek](https://www.deepseek.com/) 获取 API Key
2. 在程序中点击 "AI 数据分析"
3. 首次使用时输入 API Key
4. 开始使用智能数据分析功能

---

## 📦 模块介绍

### 项目结构

```
MathVision/
├── main.py                    # 主程序入口
├── ai.py                      # AI 数据分析模块
├── knowledge.py               # 知识点学习模块
├── common/                    # 公共基础模块
├── components/                # UI 组件
├── core/                      # 核心功能
├── themes/                    # 主题配置
└── modules/                   # 功能模块
    ├── calculus/             # 微积分模块
    ├── linear_algebra/       # 线性代数模块
    ├── probability/          # 概率统计模块
    └── sequences/            # 数列模块
```

详细的项目结构说明请查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🛠️ 技术栈

### 核心技术

- **Python 3.11** - 编程语言
- **Tkinter** - GUI 框架
- **Matplotlib** - 数据可视化
- **NumPy** - 数值计算
- **SciPy** - 科学计算
- **Pandas** - 数据处理
- **PandasAI** - AI 数据分析
- **SymPy** - 符号计算

### 开发工具

- **PyInstaller** - 程序打包
- **Git** - 版本控制

---

## 📚 文档

- [完整项目结构说明](PROJECT_STRUCTURE.md) - 详细的文件和目录说明
- [快速参考手册](QUICK_REFERENCE.md) - 快速查找功能和命令

---

## 🔨 打包发布

将程序打包为独立的 exe 文件：

```bash
python build_exe.py
```

打包后的文件位于 `dist/` 目录。

---

## 🤝 贡献指南

欢迎贡献代码和建议！

### 贡献步骤

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起 Pull Request

### 开发规范

- 遵循 PEP 8 代码规范
- 添加适当的注释和文档字符串
- 测试新功能确保正常运行
- 更新相关文档

---

## 🐛 问题反馈

如果你发现了 bug 或有功能建议，请：

1. 查看 [Issues](https://github.com/WSIR328/MathVision/issues) 是否已有相关问题
2. 如果没有，创建新的 Issue
3. 详细描述问题或建议

---

## 📝 更新日志

### v2.0.0 (2025-10-04)

- ✨ 全新的现代化界面设计
- 🤖 集成 AI 数据分析功能
- 📚 添加知识点学习模块
- 🎨 优化主题和视觉效果
- 🐛 修复多个已知问题
- 📦 重构代码结构，提高可维护性

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 👨‍💻 作者

**WSIR328**

- GitHub: [@WSIR328](https://github.com/WSIR328)

---

## 🙏 致谢

感谢以下开源项目：

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [PandasAI](https://github.com/gventuri/pandas-ai)

---

## 📞 联系方式

如有任何问题或建议，欢迎通过以下方式联系：

- 💬 GitHub Issues: [提交问题](https://github.com/WSIR328/MathVision/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by WSIR328

</div>
