"""
AI 数据分析模块包装器
将 DataAnalyzerGUI 适配为可嵌入的模块
"""

import tkinter as tk
from tkinter import ttk
from ai import DataAnalyzerGUI
from themes.futuristic_theme import COLORS, FONTS


class AIDataAnalysisWrapper(tk.Frame):
    """AI 数据分析模块包装器"""
    
    def __init__(self, master):
        super().__init__(master, bg=COLORS.get("bg_light", "#f0f0f0"))
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建说明和启动按钮
        self.create_ui()
    
    def create_ui(self):
        """创建UI"""
        container = tk.Frame(self, bg=COLORS.get("bg_light", "#f0f0f0"))
        container.pack(expand=True)
        
        # 标题
        title_label = tk.Label(
            container,
            text="🤖 AI 数据分析助手",
            font=FONTS.get("title", ("Arial", 24, "bold")),
            bg=COLORS.get("bg_light", "#f0f0f0"),
            fg=COLORS.get("text_primary", "#000000")
        )
        title_label.pack(pady=20)
        
        # 说明文本
        desc_frame = tk.Frame(container, bg=COLORS.get("bg_medium", "#ffffff"), 
                             relief=tk.FLAT, bd=0)
        desc_frame.pack(pady=20, padx=40, fill=tk.BOTH)
        
        desc_text = """
        智能数据分析助手基于 DeepSeek AI，提供强大的数据分析能力：
        
        ✨ 主要功能：
        • 智能数据分析 - 使用自然语言提问
        • 多种图表类型 - 柱状图、折线图、饼图、散点图等
        • 支持多种格式 - Excel (.xlsx, .xls) 和 CSV 文件
        • 统计分析 - 基础统计、趋势分析、相关性分析
        
        📝 使用说明：
        1. 点击下方按钮打开 AI 数据分析窗口
        2. 首次使用需要配置 DeepSeek API Key
        3. 加载数据文件或使用示例数据
        4. 选择分析类型或输入自定义问题
        5. 查看分析结果和可视化图表
        
        💡 提示：
        • AI 分析窗口会在新窗口中打开
        • 可以同时使用多个分析窗口
        • 分析结果可以保存为文件
        """
        
        desc_label = tk.Label(
            desc_frame,
            text=desc_text,
            font=FONTS.get("text", ("Arial", 11)),
            bg=COLORS.get("bg_medium", "#ffffff"),
            fg=COLORS.get("text_primary", "#000000"),
            justify=tk.LEFT,
            padx=20,
            pady=20
        )
        desc_label.pack()
        
        # 启动按钮
        button_frame = tk.Frame(container, bg=COLORS.get("bg_light", "#f0f0f0"))
        button_frame.pack(pady=30)
        
        launch_button = ttk.Button(
            button_frame,
            text="🚀 打开 AI 数据分析",
            command=self.launch_ai_analyzer
        )
        launch_button.pack()
        
        # 提示信息
        hint_label = tk.Label(
            container,
            text="注意：AI 分析功能需要 DeepSeek API Key",
            font=FONTS.get("small", ("Arial", 9)),
            bg=COLORS.get("bg_light", "#f0f0f0"),
            fg=COLORS.get("text_secondary", "#666666")
        )
        hint_label.pack(pady=10)
    
    def launch_ai_analyzer(self):
        """启动 AI 数据分析器"""
        # 创建新窗口
        ai_window = tk.Toplevel(self.master)
        ai_window.title("AI 数据分析助手")
        ai_window.geometry("1200x800")
        
        # 创建 AI 分析器实例
        analyzer = DataAnalyzerGUI(ai_window)
        
        print("AI 数据分析窗口已打开")
