import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import numpy as np
import re
import scipy.stats as stats
import os

from common.base_app import MathModuleApp
from themes.futuristic_theme import COLORS, FONTS

DEFAULT_DATA = "10.5 12.1 9.8 11.5 13.2 10.9 11.8 12.5 10.1 11.3\n" \
               "14.0 8.9 11.0 12.8 10.7 11.9 13.5 9.5 12.2 11.6"

class AnalysisApp(MathModuleApp):
    def __init__(self, master):
        super().__init__(master, title="统计分析工具")
        self.data = np.array([])
        self.last_loaded_file = None
        
        # The figure from the base class has one axes, but we need two.
        self.ax.remove()
        self.ax_hist = self.figure.add_subplot(2, 1, 1)
        self.ax_box = self.figure.add_subplot(2, 1, 2)

        self.setup_specific_ui()
        self.perform_analysis()

    def setup_specific_ui(self):
        # Input Area
        input_section = self.create_control_section("数据输入与操作")
        ttk.Label(input_section, text="输入数据 (空格、逗号或换行分隔) 或从文件加载:").pack(anchor=tk.W, padx=5, pady=(5,2))
        self.data_input_text = scrolledtext.ScrolledText(input_section, height=8, width=40, wrap=tk.WORD)
        self.data_input_text.pack(fill=tk.X, padx=5, pady=2)
        self.data_input_text.insert("1.0", DEFAULT_DATA)
        ttk.Label(input_section, text=".txt 或 .csv 文件，所有数值将视为单个数据集。", font=("Arial", 8), foreground="grey").pack(anchor=tk.W, padx=5, pady=(0, 5))

        # Action Buttons
        button_frame = ttk.Frame(input_section)
        button_frame.pack(pady=5)
        self.create_button(button_frame, "从文件加载", self.load_data_from_file).pack(side=tk.LEFT, padx=5)
        self.create_button(button_frame, "生成随机数据", self.generate_random_data).pack(side=tk.LEFT, padx=5)
        self.create_button(button_frame, "清空输入", self.clear_input_data).pack(side=tk.LEFT, padx=5)
        self.create_button(button_frame, "计算并绘图", self.perform_analysis).pack(side=tk.LEFT, padx=5)

        # Results Area
        result_frame = self.create_control_section("描述性统计结果")
        self.result_tree = ttk.Treeview(result_frame, columns=("Statistic", "Value"), show="headings", height=15)
        self.result_tree.heading("Statistic", text="统计量")
        self.result_tree.heading("Value", text="值")
        self.result_tree.column("Statistic", anchor=tk.W, width=120)
        self.result_tree.column("Value", anchor=tk.E, width=120)
        tree_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=tree_scrollbar.set)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_data_from_file(self):
        filepath = filedialog.askopenfilename(title="选择数据文件", filetypes=[("文本文件", "*.txt"), ("CSV 文件", "*.csv"), ("所有文件", "*.*")])
        if not filepath:
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.data_input_text.delete("1.0", tk.END)
            self.data_input_text.insert("1.0", content)
            self.last_loaded_file = filepath
            messagebox.showinfo("加载成功", f"已从 {os.path.basename(filepath)} 加载数据。")
        except Exception as e:
            messagebox.showerror("文件读取错误", f"无法读取文件 '{os.path.basename(filepath)}':\n{e}")
            self.last_loaded_file = None

    def generate_random_data(self):
        random_data = np.random.normal(loc=15.0, scale=2.5, size=50)
        data_string = " ".join([f"{x:.2f}" for x in random_data])
        self.data_input_text.delete("1.0", tk.END)
        self.data_input_text.insert("1.0", data_string)
        self.last_loaded_file = None
        self.perform_analysis()
        messagebox.showinfo("生成成功", "已生成50个正态分布的随机数。")

    def clear_input_data(self):
        self.data_input_text.delete("1.0", tk.END)
        self.data = np.array([])
        self.last_loaded_file = None
        self.clear_results_and_plot()

    def parse_data(self):
        raw_text = self.data_input_text.get("1.0", tk.END).strip()
        if not raw_text:
            self.data = np.array([])
            return False
        potential_numbers = re.split(r'[\s,]+', raw_text)
        numbers = [item for item in potential_numbers if item]
        try:
            self.data = np.array([float(num) for num in numbers])
            return self.data.size > 0
        except ValueError:
            messagebox.showerror("输入错误", "数据包含非数值内容，请检查输入。")
            return False

    def calculate_descriptive_stats(self):
        if self.data.size == 0: return None
        stats_dict = {
            '样本量': len(self.data),
            '均值': np.mean(self.data),
            '中位数': np.median(self.data),
            '标准差': np.std(self.data, ddof=1),
            '方差': np.var(self.data, ddof=1),
            '最小值': np.min(self.data),
            '最大值': np.max(self.data),
            '范围': np.ptp(self.data),
            'Q1': np.percentile(self.data, 25),
            'Q3': np.percentile(self.data, 75),
            'IQR': np.percentile(self.data, 75) - np.percentile(self.data, 25),
            '偏度': stats.skew(self.data),
            '峰度': stats.kurtosis(self.data)
        }
        return stats_dict

    def display_stats(self, stats_dict):
        for item in self.result_tree.get_children(): self.result_tree.delete(item)
        if stats_dict:
            if self.last_loaded_file: self.result_tree.insert("", tk.END, values=("数据来源", os.path.basename(self.last_loaded_file)))
            count = stats_dict.pop('样本量')
            self.result_tree.insert("", tk.END, values=("样本量 (N)", f"{int(count)}"))
            for key, value in stats_dict.items():
                formatted_value = f"{value:.4e}" if abs(value) > 1e4 or (abs(value) < 1e-3 and value != 0) else f"{value:.4f}"
                self.result_tree.insert("", tk.END, values=(key, formatted_value))
        else:
            self.result_tree.insert("", tk.END, values=("状态", "无数据或计算失败"))

    def update_plots(self):
        self.ax_hist.clear()
        self.ax_box.clear()
        if self.data.size == 0:
            self.ax_hist.set_title("直方图 (无数据)")
            self.ax_box.set_title("箱线图 (无数据)")
        else:
            self.ax_hist.hist(self.data, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)
            self.ax_hist.set_title(f"数据直方图 (N={len(self.data)})")
            self.ax_hist.set_xlabel("值")
            self.ax_hist.set_ylabel("频数")
            self.ax_hist.grid(axis='y', linestyle='--', alpha=0.7)
            self.ax_box.boxplot(self.data, vert=False, patch_artist=True, showmeans=True)
            self.ax_box.set_title("数据箱线图")
            self.ax_box.set_xlabel("值")
            self.ax_box.set_yticks([])
            self.ax_box.grid(axis='x', linestyle='--', alpha=0.7)
        self.figure.tight_layout()
        self.refresh_plot()

    def perform_analysis(self):
        if self.parse_data():
            stats_dict = self.calculate_descriptive_stats()
            self.display_stats(stats_dict)
            self.update_plots()

    def clear_results_and_plot(self):
        for item in self.result_tree.get_children(): self.result_tree.delete(item)
        self.ax_hist.clear()
        self.ax_box.clear()
        self.ax_hist.set_title("直方图")
        self.ax_box.set_title("箱线图")
        self.refresh_plot()