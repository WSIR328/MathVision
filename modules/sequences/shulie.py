import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
from matplotlib.lines import Line2D
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import warnings

from common.base_app import MathModuleApp
from knowledge import KnowledgeLearningClass

# 忽略sympy的警告
warnings.filterwarnings("ignore", category=UserWarning, module='sympy')

class SequenceModule(MathModuleApp):
    """数列功能模块，继承自MathModuleApp以实现UI和功能标准化"""

    def __init__(self, master):
        """
        初始化数列模块
        参数:
            master: 父容器 (由PageManager或主应用提供)
        """
        # 调用父类构造函数，设置标题
        super().__init__(master)
        
        self.knowledge_learner = KnowledgeLearningClass()
        
        # 数列相关变量
        self.sequence_points = []  # 存储数列点
        self.draw_sequence = tk.BooleanVar(value=False)  # 控制是否绘制数列
        
        # 序列表达式及计算结果
        self.sequence_expr = None
        self.sequence_values = None
        self.sequence_sum = None
        
        # 设置特定的UI
        self.setup_specific_ui()

    def setup_specific_ui(self):
        """创建数列模块特有的UI控件"""
        
        # 使用父类提供的control_frame
        controls = self.create_control_section("数列控制")
        
        # 数列通项输入区域
        input_frame = ttk.Frame(controls)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="数列通项:").pack(side=tk.LEFT, padx=5)
        self.sequence_entry = ttk.Entry(input_frame, width=20)
        self.sequence_entry.pack(side=tk.LEFT, padx=5)
        self.sequence_entry.insert(0, "1/n")
        
        ttk.Label(input_frame, text="开始项:").pack(side=tk.LEFT, padx=(15, 5))
        self.sequence_start_entry = ttk.Entry(input_frame, width=5)
        self.sequence_start_entry.pack(side=tk.LEFT, padx=5)
        self.sequence_start_entry.insert(0, "1")
        
        ttk.Label(input_frame, text="结束项:").pack(side=tk.LEFT, padx=(15, 5))
        self.sequence_end_entry = ttk.Entry(input_frame, width=5)
        self.sequence_end_entry.pack(side=tk.LEFT, padx=5)
        self.sequence_end_entry.insert(0, "20")
        
        # 数列显示控制
        control_frame = ttk.Frame(controls)
        control_frame.pack(fill=tk.X, pady=5)
        
        self.sequence_check = ttk.Checkbutton(
            control_frame, 
            text="显示数列", 
            variable=self.draw_sequence,
            command=self.toggle_sequence
        )
        self.sequence_check.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(
            control_frame,
            text="更新数列",
            command=self.update_sequence
        )
        update_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(
            control_frame,
            text="清除数列",
            command=self.clear_sequence
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 数列和计算区域
        sum_frame = ttk.Frame(controls)
        sum_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(sum_frame, text="数列和:").pack(side=tk.LEFT, padx=5)
        self.sequence_sum_text = tk.Text(sum_frame, height=1, width=20, font=("SimHei", 10))
        self.sequence_sum_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.sequence_sum_text.insert(tk.END, "未计算")
        self.sequence_sum_text.config(state=tk.DISABLED)
        
        calc_sum_button = ttk.Button(
            sum_frame,
            text="计算数列和",
            command=self.calculate_sequence_sum
        )
        calc_sum_button.pack(side=tk.LEFT, padx=5)
        
        # 数列收敛性分析区域
        convergence_frame = ttk.Frame(controls)
        convergence_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(convergence_frame, text="收敛性分析:").pack(side=tk.LEFT, padx=5)
        self.convergence_text = tk.Text(convergence_frame, height=2, width=40, font=("SimHei", 10))
        self.convergence_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.convergence_text.insert(tk.END, "未分析")
        self.convergence_text.config(state=tk.DISABLED)
        
        analyze_button = ttk.Button(
            convergence_frame,
            text="分析收敛性",
            command=self.analyze_convergence
        )
        analyze_button.pack(side=tk.LEFT, padx=5)

        knowledge_learning_integral_frame = ttk.Frame(controls)
        knowledge_learning_integral_frame.pack(fill=tk.X, pady=5)

        knowledge_learning= ttk.Button(
            knowledge_learning_integral_frame,
            text="知识介绍", 
            command=self.knowledge_learner.knowledge_learning_5_function
        )
        knowledge_learning.pack(side=tk.LEFT, padx=10)
        
        # 配置父类的绘图区域
        self.ax.set_xlabel('n')
        self.ax.set_ylabel('a_n')
        self.ax.set_title('数列可视化')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.refresh_plot()

    def toggle_sequence(self):
        """切换数列显示状态"""
        if self.draw_sequence.get():
            self.update_sequence()
        else:
            self.clear_sequence()
            self.refresh_plot()

    def update_sequence(self):
        """更新数列点"""
        try:
            expression = self.sequence_entry.get()
            start = int(self.sequence_start_entry.get())
            end = int(self.sequence_end_entry.get())
            
            if end < start:
                messagebox.showerror("数列错误", "结束项必须大于等于开始项")
                return
            
            x = sp.Symbol('n')
            expr = parse_expr(expression, transformations=(standard_transformations + (implicit_multiplication_application,)))
            self.sequence_expr = expr
            
            values = []
            for n in range(start, end + 1):
                try:
                    val = float(expr.subs(x, n))
                    values.append((n, val))
                except (ValueError, ZeroDivisionError, OverflowError):
                    continue
            
            self.sequence_values = values
            self.draw_sequence_points(values)
            
        except Exception as e:
            messagebox.showerror("数列错误", f"计算数列时出错: {str(e)}")
            self.clear_sequence()

    def draw_sequence_points(self, values):
        """绘制数列点"""
        self.clear_sequence()
        
        if not values:
            messagebox.showinfo("提示", "没有有效的数列值可以绘制")
            return
        
        x_vals = [val[0] for val in values]
        y_vals = [val[1] for val in values]
        
        sequence_line = Line2D(x_vals, y_vals, marker='o', color='purple', markersize=6, linestyle='-', linewidth=1)
        self.sequence_points.append(self.ax.add_line(sequence_line))
        
        self.ax.set_xlim(min(x_vals) - 1, max(x_vals) + 1)
        
        valid_y = [y for y in y_vals if not (np.isinf(y) or np.isnan(y))]
        if valid_y:
            y_min, y_max = min(valid_y), max(valid_y)
            y_range = y_max - y_min if y_max > y_min else 1
            self.ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
        
        self.refresh_plot()

    def calculate_sequence_sum(self):
        """计算数列和"""
        if not self.sequence_values:
            messagebox.showinfo("提示", "请先显示数列")
            return
        
        try:
            sum_value = sum(val[1] for val in self.sequence_values)
            self.sequence_sum_text.config(state=tk.NORMAL)
            self.sequence_sum_text.delete(1.0, tk.END)
            self.sequence_sum_text.insert(tk.END, f"{sum_value:.6f}")
            self.sequence_sum_text.config(state=tk.DISABLED)
            self.sequence_sum = sum_value
        except Exception as e:
            messagebox.showerror("计算错误", f"计算数列和时出错: {str(e)}")

    def analyze_convergence(self):
        """分析数列的收敛性"""
        if not self.sequence_expr:
            messagebox.showinfo("提示", "请先输入并显示数列")
            return
        
        try:
            n = sp.Symbol('n')
            limit_value = sp.limit(self.sequence_expr, n, sp.oo)
            
            if limit_value.is_finite:
                result = f"数列收敛于 {limit_value}"
            elif limit_value.is_infinite:
                result = "数列发散到无穷"
            else:
                result = "数列不收敛"
            
            self.convergence_text.config(state=tk.NORMAL)
            self.convergence_text.delete(1.0, tk.END)
            self.convergence_text.insert(tk.END, result)
            self.convergence_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("分析错误", f"分析数列收敛性时出错: {str(e)}")
            self.convergence_text.config(state=tk.NORMAL)
            self.convergence_text.delete(1.0, tk.END)
            self.convergence_text.insert(tk.END, f"无法分析: {str(e)}")
            self.convergence_text.config(state=tk.DISABLED)

    def clear_sequence(self):
        """清除数列点"""
        for point in self.sequence_points:
            point.remove()
        self.sequence_points = []
        self.refresh_plot()