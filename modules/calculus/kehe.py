import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, colorchooser
import numpy as np
import math
import traceback

from common.base_app import MathModuleApp
from knowledge import KnowledgeLearningClass

class KeheApp(MathModuleApp):
    def __init__(self, master):
        super().__init__(master)
        
        self.knowledge_learner = KnowledgeLearningClass()
        self.equation_colors = ["#1E88E5", "#E53935", "#43A047", "#FDD835", "#5E35B1", "#00ACC1", "#FF6D00"]
        self.current_color_index = 0
        self.x_range = tk.StringVar(value="-1.5,1.5")
        self.y_range = tk.StringVar(value="-1.5,1.5")
        self.iteration_depth = tk.IntVar(value=3)
        self.show_grid = tk.BooleanVar(value=True)
        self.line_width = tk.DoubleVar(value=1.5)
        
        self.setup_specific_ui()
        self.plot_koch_snowflake()

    def setup_specific_ui(self):
        controls = self.create_control_section("控制面板")
        
        depth_frame = ttk.Frame(controls)
        depth_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(depth_frame, text="迭代深度:").pack(side=tk.LEFT)
        depth_scale = ttk.Scale(depth_frame, from_=0, to=6, variable=self.iteration_depth, orient=tk.HORIZONTAL, length=150, command=lambda e: self.plot_koch_snowflake())
        depth_scale.pack(side=tk.LEFT, padx=5)
        depth_label = ttk.Label(depth_frame, text="3")
        depth_label.pack(side=tk.LEFT)
        self.iteration_depth.trace_add("write", lambda *args: depth_label.config(text=str(self.iteration_depth.get())))
        
        draw_button = ttk.Button(controls, text="绘制科赫雪花", command=self.plot_koch_snowflake)
        draw_button.pack(fill=tk.X, pady=5)
        
        range_frame = self.create_control_section("坐标范围")
        ttk.Label(range_frame, text="X范围 (min,max):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(range_frame, textvariable=self.x_range, width=15).grid(row=0, column=1, pady=2)
        ttk.Label(range_frame, text="Y范围 (min,max):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(range_frame, textvariable=self.y_range, width=15).grid(row=1, column=1, pady=2)
        
        width_frame = ttk.Frame(controls)
        width_frame.pack(fill=tk.X, pady=5)
        ttk.Label(width_frame, text="线宽:").pack(side=tk.LEFT)
        ttk.Scale(width_frame, from_=0.5, to=4.0, variable=self.line_width, orient=tk.HORIZONTAL, length=150, command=lambda e: self.plot_koch_snowflake()).pack(side=tk.LEFT, expand=True)
        
        grid_check = ttk.Checkbutton(controls, text="显示网格", variable=self.show_grid, command=self.update_plot_settings)
        grid_check.pack(anchor=tk.W, pady=5)
        
        color_button = ttk.Button(controls, text="选择颜色", command=self.choose_color)
        color_button.pack(fill=tk.X, pady=5)
        
        reset_button = ttk.Button(controls, text="重置视图", command=self.reset_view)
        reset_button.pack(fill=tk.X, pady=5)

        save_button = ttk.Button(controls, text="保存图像", command=self.save_plot)
        save_button.pack(fill=tk.X, pady=5)

        knowledge_learning = ttk.Button(controls, text="知识介绍", command=self.knowledge_learner.knowledge_learning_8_function)
        knowledge_learning.pack(fill=tk.X,pady=5)
        
        info_frame = self.create_control_section("科赫雪花信息")
        self.info_text = scrolledtext.ScrolledText(info_frame, width=30, height=10, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.insert(tk.END, "科赫雪花是一种经典的分形...\n使用滑块调整迭代深度，观察复杂度的变化。")
        self.info_text.config(state=tk.DISABLED)

        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('科赫雪花分形')
        self.update_plot_settings()

    def koch_curve(self, p1, p2, depth):
        if depth == 0:
            return [p1, p2]
        
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        
        p1_1 = (x1 + dx/3, y1 + dy/3)
        p2_1 = (x1 + 2*dx/3, y1 + 2*dy/3)
        
        angle = math.atan2(dy, dx) + math.pi/3
        length = dist/3
        px = x1 + dx/3 + length * math.cos(angle)
        py = y1 + dy/3 + length * math.sin(angle)
        p_mid = (px, py)
        
        points = []
        points.extend(self.koch_curve(p1, p1_1, depth-1)[:-1])
        points.extend(self.koch_curve(p1_1, p_mid, depth-1)[:-1])
        points.extend(self.koch_curve(p_mid, p2_1, depth-1)[:-1])
        points.extend(self.koch_curve(p2_1, p2, depth-1))
        return points

    def plot_koch_snowflake(self):
        self.ax.clear()
        self.update_plot_settings()
        
        try:
            depth = self.iteration_depth.get()
            side_length = 2.0
            height = side_length * math.sqrt(3) / 2
            p1 = (-side_length/2, -height/3)
            p2 = (side_length/2, -height/3)
            p3 = (0, 2*height/3)
            
            curve1 = self.koch_curve(p1, p2, depth)
            curve2 = self.koch_curve(p2, p3, depth)
            curve3 = self.koch_curve(p3, p1, depth)
            
            x1, y1 = zip(*curve1)
            x2, y2 = zip(*curve2)
            x3, y3 = zip(*curve3)
            
            color = self.equation_colors[self.current_color_index % len(self.equation_colors)]
            line_width = self.line_width.get()
            
            self.ax.plot(x1, y1, color=color, linewidth=line_width)
            self.ax.plot(x2, y2, color=color, linewidth=line_width)
            self.ax.plot(x3, y3, color=color, linewidth=line_width)
            
            self.refresh_plot()
            self.update_status(f"已绘制科赫雪花 (迭代深度: {depth})")
            total_segments = 3 * (4 ** depth)
            self.update_info(f"科赫雪花 (迭代深度: {depth})\n\n特性:\n- 总线段数: {total_segments}...")
        except Exception as e:
            messagebox.showerror("绘图错误", f"绘制科赫雪花时出错: {str(e)}")
            traceback.print_exc()
            self.update_status("绘图失败")

    def choose_color(self):
        color = colorchooser.askcolor(title="选择颜色")
        if color[1]:
            self.equation_colors[self.current_color_index % len(self.equation_colors)] = color[1]
            self.plot_koch_snowflake()

    def update_plot_settings(self):
        self.ax.grid(self.show_grid.get())
        self.reset_view()

    def reset_view(self):
        try:
            x_min, x_max = map(float, self.x_range.get().split(','))
            y_min, y_max = map(float, self.y_range.get().split(','))
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
            self.refresh_plot()
            self.update_status("已重置视图")
        except Exception as e:
            messagebox.showerror("视图错误", f"重置视图时出错: {str(e)}")

    def update_info(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED)