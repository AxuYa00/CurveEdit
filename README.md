# CURVEEDIT - 交互式曲线编辑器（PyQt6 版本）

CURVEEDIT 是一个基于 Python 和 PyQt6 框架开发的交互式曲线编辑工具。  
用户可通过鼠标在画布中添加、拖动控制点，系统自动绘制平滑的 Catmull-Rom 样条曲线。

## ✨主要功能

- 支持鼠标左键添加控制点
- 支持右键拖动已有点，或在曲线中插入新点
- 实时绘制平滑的 Catmull-Rom 样条曲线
- 清除全部点功能
- 可拓展张力调节、数据导出等功能

## 🧩安装要求

- Python 3.9+
- PyQt6
- NumPy

## 🚀安装步骤

1. 克隆仓库
```bash
git clone https://github.com/AxuYa00/CurveEdit.git
cd CurveEdit
```
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## ▶️使用方法

运行主程序：
```bash
python main.py
```
## 🖱 操作说明

-左键点击空白处：添加控制点

-右键点击控制点：拖动点移动

-右键点击曲线：插入新点后可拖动

-点击右侧按钮：清除所有点


