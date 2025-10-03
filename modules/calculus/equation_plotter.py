import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import warnings
from matplotlib import colors

from common.base_app import MathModuleApp
from knowledge import KnowledgeLearningClass

# 忽略特定警告
warnings.filterwarnings("ignore", category=UserWarning, module='sympy')

class EquationVisualizationApp(MathModuleApp):
    def __init__(self, master):
        print("Initializing EquationVisualizationApp")
        super().__init__(master)
        
        self.knowledge_learner = KnowledgeLearningClass()
        self.create_custom_colormaps()
        
        # 初始化变量
        self.equations = []
        self.equation_lines = []
        self.equation_colors = []
        self.current_mode = tk.StringVar(value="显式方程")
        self.x_range = tk.StringVar(value="-10,10")
        self.y_range = tk.StringVar(value="-10,10")
        self.resolution = tk.IntVar(value=500)
        self.show_grid = tk.BooleanVar(value=True)
        self.show_legend = tk.BooleanVar(value=True)
        self.line_width = tk.DoubleVar(value=2.0)
        self.colormap = tk.StringVar(value="viridis")
        self.auto_scale_y = tk.BooleanVar(value=True)  # 自动调整Y轴
        
        self.setup_specific_ui()
        self.equation_entry.insert(0, "x**2")
        self.bind_events()

    def setup_specific_ui(self):
        from themes.futuristic_theme import COLORS, FONTS, SPACING
        
        # ========== 方程输入区域 ==========
        equation_frame = self.create_control_section("📝 方程输入")
        equation_frame.configure(padding=SPACING["sm"])
        
        # 方程类型选择（更紧凑的布局）
        type_frame = ttk.Frame(equation_frame)
        type_frame.pack(fill=tk.X, pady=(0, SPACING["xs"]))
        
        ttk.Label(type_frame, text="类型:", font=FONTS["text"]).pack(side=tk.LEFT, padx=(0, SPACING["xs"]))
        equation_types = ["显式方程 y=f(x)", "隐式方程 f(x,y)=0", "参数方程", "极坐标方程"]
        equation_type_combo = ttk.Combobox(type_frame, textvariable=self.current_mode, 
                                          values=equation_types, width=18, state='readonly')
        equation_type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        equation_type_combo.bind("<<ComboboxSelected>>", self.on_equation_type_change)
        
        # 方程输入（更大的输入框）
        input_frame = ttk.Frame(equation_frame)
        input_frame.pack(fill=tk.X, pady=SPACING["xs"])
        
        ttk.Label(input_frame, text="方程:", font=FONTS["text"]).pack(side=tk.LEFT, padx=(0, SPACING["xs"]))
        self.equation_entry = ttk.Entry(input_frame, font=("Consolas", 11))
        self.equation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, SPACING["xs"]))
        
        # 添加按钮（使用图标样式）
        add_button = ttk.Button(input_frame, text="➕ 添加", command=self.add_equation, width=8)
        add_button.pack(side=tk.LEFT)
        
        # 快速示例按钮
        example_frame = ttk.Frame(equation_frame)
        example_frame.pack(fill=tk.X, pady=(SPACING["xs"], 0))
        
        ttk.Label(example_frame, text="示例:", font=FONTS["small"]).pack(side=tk.LEFT, padx=(0, SPACING["xs"]))
        
        examples = [
            ("x²", "x**2"),
            ("sin(x)", "sin(x)"),
            ("圆", "x**2+y**2-25"),
        ]
        
        for label, eq in examples:
            btn = ttk.Button(example_frame, text=label, 
                           command=lambda e=eq: self._insert_example(e),
                           width=6)
            btn.pack(side=tk.LEFT, padx=2)
        
        # ========== 方程列表区域 ==========
        list_frame = self.create_control_section("📋 方程列表")
        list_frame.configure(padding=SPACING["sm"])
        
        # 列表框（带滚动条）
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.equation_listbox = tk.Listbox(list_container, height=6, 
                                          font=("Consolas", 10),
                                          bg=COLORS["bg_medium"],
                                          fg=COLORS["text_primary"],
                                          selectbackground=COLORS["accent_primary"],
                                          selectforeground=COLORS["bg_dark"],
                                          relief=tk.FLAT,
                                          highlightthickness=1,
                                          highlightbackground=COLORS["bg_light"],
                                          yscrollcommand=scrollbar.set)
        self.equation_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.equation_listbox.yview)
        
        # 列表操作按钮
        list_btn_frame = ttk.Frame(list_frame)
        list_btn_frame.pack(fill=tk.X, pady=(SPACING["xs"], 0))
        
        delete_button = ttk.Button(list_btn_frame, text="🗑️ 删除", command=self.delete_equation, width=10)
        delete_button.pack(side=tk.LEFT, padx=(0, SPACING["xs"]))
        
        clear_button = ttk.Button(list_btn_frame, text="🧹 清空", command=self.clear_equations, width=10)
        clear_button.pack(side=tk.LEFT)
        
        # ========== 显示设置区域 ==========
        display_frame = self.create_control_section("⚙️ 显示设置")
        display_frame.configure(padding=SPACING["sm"])
        
        # X范围
        x_range_frame = ttk.Frame(display_frame)
        x_range_frame.pack(fill=tk.X, pady=(0, SPACING["xs"]))
        ttk.Label(x_range_frame, text="X范围:", font=FONTS["text"], width=8).pack(side=tk.LEFT)
        x_range_entry = ttk.Entry(x_range_frame, textvariable=self.x_range, width=12, font=("Consolas", 10))
        x_range_entry.pack(side=tk.LEFT, padx=SPACING["xs"])
        ttk.Label(x_range_frame, text="(min,max)", font=FONTS["small"]).pack(side=tk.LEFT)
        
        # Y范围
        y_range_frame = ttk.Frame(display_frame)
        y_range_frame.pack(fill=tk.X, pady=SPACING["xs"])
        ttk.Label(y_range_frame, text="Y范围:", font=FONTS["text"], width=8).pack(side=tk.LEFT)
        y_range_entry = ttk.Entry(y_range_frame, textvariable=self.y_range, width=12, font=("Consolas", 10))
        y_range_entry.pack(side=tk.LEFT, padx=SPACING["xs"])
        ttk.Label(y_range_frame, text="(min,max)", font=FONTS["small"]).pack(side=tk.LEFT)
        
        # 分辨率滑块
        resolution_frame = ttk.Frame(display_frame)
        resolution_frame.pack(fill=tk.X, pady=SPACING["xs"])
        ttk.Label(resolution_frame, text="分辨率:", font=FONTS["text"], width=8).pack(side=tk.LEFT)
        resolution_scale = ttk.Scale(resolution_frame, from_=100, to=1000, variable=self.resolution, orient=tk.HORIZONTAL)
        resolution_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=SPACING["xs"])
        self.resolution_label = ttk.Label(resolution_frame, text=str(self.resolution.get()), width=4, font=FONTS["small"])
        self.resolution_label.pack(side=tk.LEFT)
        resolution_scale.configure(command=lambda v: self.resolution_label.config(text=f"{int(float(v))}"))
        
        # 线宽滑块
        linewidth_frame = ttk.Frame(display_frame)
        linewidth_frame.pack(fill=tk.X, pady=SPACING["xs"])
        ttk.Label(linewidth_frame, text="线宽:", font=FONTS["text"], width=8).pack(side=tk.LEFT)
        line_width_scale = ttk.Scale(linewidth_frame, from_=0.5, to=5.0, variable=self.line_width, orient=tk.HORIZONTAL)
        line_width_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=SPACING["xs"])
        self.linewidth_label = ttk.Label(linewidth_frame, text=f"{self.line_width.get():.1f}", width=4, font=FONTS["small"])
        self.linewidth_label.pack(side=tk.LEFT)
        line_width_scale.configure(command=lambda v: self.linewidth_label.config(text=f"{float(v):.1f}"))
        
        # 选项复选框（更紧凑的布局）
        options_frame = ttk.Frame(display_frame)
        options_frame.pack(fill=tk.X, pady=(SPACING["sm"], 0))
        
        ttk.Checkbutton(options_frame, text="📊 网格", variable=self.show_grid, 
                       command=self.plot_equations).pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
        ttk.Checkbutton(options_frame, text="📌 图例", variable=self.show_legend, 
                       command=self.plot_equations).pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
        ttk.Checkbutton(options_frame, text="📏 自动Y轴", variable=self.auto_scale_y, 
                       command=self.plot_equations).pack(side=tk.LEFT)

        # ========== 操作按钮区域 ==========
        action_frame = self.create_control_section("🎨 操作")
        action_frame.configure(padding=SPACING["sm"])
        
        # 主要操作按钮（网格布局）
        btn_container = ttk.Frame(action_frame)
        btn_container.pack(fill=tk.X)
        
        plot_button = ttk.Button(btn_container, text="🎯 绘制", command=self.plot_equations)
        plot_button.grid(row=0, column=0, sticky=tk.EW, padx=(0, SPACING["xs"]), pady=(0, SPACING["xs"]))
        
        reset_button = ttk.Button(btn_container, text="🔄 重置", command=self.reset_view)
        reset_button.grid(row=0, column=1, sticky=tk.EW, padx=(0, 0), pady=(0, SPACING["xs"]))
        
        save_button = ttk.Button(btn_container, text="💾 保存", command=self.save_plot)
        save_button.grid(row=1, column=0, sticky=tk.EW, padx=(0, SPACING["xs"]), pady=(0, SPACING["xs"]))

        knowledge_button = ttk.Button(btn_container, text="📚 知识", 
                                      command=self.knowledge_learner.knowledge_learning_7_function)
        knowledge_button.grid(row=1, column=1, sticky=tk.EW, padx=(0, 0), pady=(0, SPACING["xs"]))
        
        # 配置列权重使按钮等宽
        btn_container.columnconfigure(0, weight=1)
        btn_container.columnconfigure(1, weight=1)
        
        # ========== 信息显示区域 ==========
        info_frame = self.create_control_section("ℹ️ 信息")
        info_frame.configure(padding=SPACING["sm"])
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, wrap=tk.WORD,
                                                   font=("Consolas", 9),
                                                   bg=COLORS["bg_medium"],
                                                   fg=COLORS["text_secondary"],
                                                   relief=tk.FLAT,
                                                   highlightthickness=1,
                                                   highlightbackground=COLORS["bg_light"])
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加欢迎信息
        welcome_text = """欢迎使用方程可视化工具！

📝 支持的方程类型：
  • 显式方程: y = f(x)
  • 隐式方程: f(x,y) = 0
  • 参数方程: x=f(t), y=g(t)
  • 极坐标: r = f(θ)

💡 提示：
  • 使用示例按钮快速插入
  • 自动Y轴可完整显示图形
  • 鼠标悬停显示坐标
"""
        self.info_text.insert(tk.END, welcome_text)
        self.info_text.config(state=tk.DISABLED)

        # 初始化绘图区域
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('方程可视化')
        self.refresh_plot()

    def _insert_example(self, equation):
        """插入示例方程"""
        self.equation_entry.delete(0, tk.END)
        self.equation_entry.insert(0, equation)
        self.equation_entry.focus()
    
    def create_custom_colormaps(self):
        self.custom_cmap1 = colors.LinearSegmentedColormap.from_list("BlueRed", [(0, "#1E88E5"), (0.5, "#FFFFFF"), (1, "#E53935")])
        self.custom_cmap2 = colors.LinearSegmentedColormap.from_list("Rainbow", [(0, "#9C27B0"), (0.2, "#3F51B5"), (0.4, "#03A9F4"), (0.6, "#4CAF50"), (0.8, "#FFEB3B"), (1, "#FF5722")])
        # 在新版本的 matplotlib 中，colormap 会自动注册
        try:
            plt.register_cmap(cmap=self.custom_cmap1)
            plt.register_cmap(cmap=self.custom_cmap2)
        except AttributeError:
            # 新版本的 matplotlib 不需要手动注册
            pass
        
    def bind_events(self):
        self.equation_listbox.bind('<<ListboxSelect>>', self.on_equation_select)
        # 使用 matplotlib 的事件系统而不是 tkinter
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def on_equation_select(self, event):
        selection = self.equation_listbox.curselection()
        if selection:
            index = selection[0]
            mode, equation = self.equations[index]
            self.current_mode.set(mode)
            self.equation_entry.delete(0, tk.END)
            self.equation_entry.insert(0, equation)
            self.update_status(f"已选择方程: {equation}")
    
    def on_equation_type_change(self, event=None):
        mode = self.current_mode.get()
        if mode == "显式方程":
            self.equation_entry.delete(0, tk.END)
            self.equation_entry.insert(0, "x**2")
            self.update_info("显式方程形式: y = f(x)\n例如: x**2, sin(x), x**3-2*x")
        elif mode == "隐式方程":
            self.equation_entry.delete(0, tk.END)
            self.equation_entry.insert(0, "x**2 + y**2 - 4")
            self.update_info("隐式方程形式: f(x,y) = 0\n例如: x**2 + y**2 - 4, x*y - 1")
        elif mode == "参数方程":
            self.equation_entry.delete(0, tk.END)
            self.equation_entry.insert(0, "t*cos(t), t*sin(t), 0, 10")
            self.update_info("参数方程形式: x(t), y(t), t_min, t_max\n例如: cos(t), sin(t), 0, 2*pi")
        elif mode == "极坐标方程":
            self.equation_entry.delete(0, tk.END)
            self.equation_entry.insert(0, "1 + cos(theta)")
            self.update_info("极坐标方程形式: r = f(theta)\n例如: 1 + cos(theta), 2*sin(3*theta)")

    def add_equation(self):
        equation = self.equation_entry.get().strip()
        if not equation:
            messagebox.showwarning("输入错误", "请输入有效的方程")
            return
        
        color = "#{:02x}{:02x}{:02x}".format(np.random.randint(0, 200), np.random.randint(0, 200), np.random.randint(0, 200))
        mode = self.current_mode.get()
        self.equations.append((mode, equation))
        self.equation_colors.append(color)
        
        equation_display = f"{mode}: {equation}"
        self.equation_listbox.insert(tk.END, equation_display)
        self.equation_listbox.itemconfig(tk.END, {'bg': color, 'fg': 'white'})
        self.equation_entry.delete(0, tk.END)
        self.update_status(f"已添加方程: {equation_display}")
        self.plot_equations()
    
    def delete_equation(self):
        selected = self.equation_listbox.curselection()
        if not selected:
            messagebox.showwarning("选择错误", "请先选择要删除的方程")
            return
        
        index = selected[0]
        self.equation_listbox.delete(index)
        self.equations.pop(index)
        self.equation_colors.pop(index)
        self.update_status("已删除选中的方程")
        self.plot_equations()
    
    def clear_equations(self):
        if not self.equations:
            return
        if messagebox.askyesno("确认", "确定要清空所有方程吗?"):
            self.equation_listbox.delete(0, tk.END)
            self.equations.clear()
            self.equation_colors.clear()
            self.clear_plot()
            self.update_status("已清空所有方程")

    def plot_equations(self):
        if not self.equations:
            self.clear_plot()
            return
        
        try:
            x_min, x_max = map(float, self.x_range.get().split(','))
            y_min, y_max = map(float, self.y_range.get().split(','))
            
            self.ax.clear()
            self.equation_lines = []
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('方程可视化')
            self.ax.grid(self.show_grid.get())
            
            for i, ((mode, equation), color) in enumerate(zip(self.equations, self.equation_colors)):
                if mode == "显式方程": self.plot_explicit(equation, color)
                elif mode == "隐式方程": self.plot_implicit(equation, color)
                elif mode == "参数方程": self.plot_parametric(equation, color)
                elif mode == "极坐标方程": self.plot_polar(equation, color)
            
            # 自动调整Y轴范围
            if self.auto_scale_y.get() and self.ax.lines:
                # 收集所有线的Y数据
                all_y_data = []
                for line in self.ax.lines:
                    ydata = line.get_ydata()
                    # 过滤掉 nan 和 inf
                    valid_y = ydata[np.isfinite(ydata)]
                    if len(valid_y) > 0:
                        all_y_data.extend(valid_y)
                
                if all_y_data:
                    y_min_auto = np.min(all_y_data)
                    y_max_auto = np.max(all_y_data)
                    # 添加一些边距
                    y_margin = (y_max_auto - y_min_auto) * 0.1
                    self.ax.set_ylim(y_min_auto - y_margin, y_max_auto + y_margin)
                else:
                    self.ax.set_ylim(y_min, y_max)
            else:
                self.ax.set_ylim(y_min, y_max)
            
            if self.show_legend.get() and self.equation_lines:
                self.ax.legend()
            
            self.refresh_plot()
            self.update_status(f"已绘制 {len(self.equations)} 个方程")
        except Exception as e:
            messagebox.showerror("绘图错误", f"绘制方程时出错: {str(e)}")

    def plot_explicit(self, equation, color):
        x_min, x_max = map(float, self.x_range.get().split(','))
        x = np.linspace(x_min, x_max, self.resolution.get())
        y = np.zeros_like(x)
        for i, xi in enumerate(x):
            try:
                y[i] = eval(equation, {"__builtins__": {}}, {"x": xi, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
            except:
                y[i] = np.nan
        line, = self.ax.plot(x, y, color=color, linewidth=self.line_width.get(), label=f"y = {equation}")
        self.equation_lines.append(line)

    def plot_implicit(self, equation, color):
        x_min, x_max = map(float, self.x_range.get().split(','))
        y_min, y_max = map(float, self.y_range.get().split(','))
        x = np.linspace(x_min, x_max, self.resolution.get()//5) # Lower res for performance
        y = np.linspace(y_min, y_max, self.resolution.get()//5)
        X, Y = np.meshgrid(x, y)
        Z = eval(equation, {"__builtins__": {}}, {"x": X, "y": Y, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
        self.ax.contour(X, Y, Z, [0], colors=color, linewidths=self.line_width.get())
        from matplotlib.lines import Line2D
        legend_artist = Line2D([0], [0], color=color, lw=self.line_width.get(), label=f"{equation} = 0")
        self.equation_lines.append(legend_artist)

    def plot_parametric(self, equation, color):
        parts = equation.split(',')
        x_expr, y_expr, t_min, t_max = [p.strip() for p in parts]
        t = np.linspace(float(t_min), float(t_max), self.resolution.get())
        x = eval(x_expr, {"__builtins__": {}}, {"t": t, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
        y = eval(y_expr, {"__builtins__": {}}, {"t": t, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
        line, = self.ax.plot(x, y, color=color, linewidth=self.line_width.get(), label=f"x={{x_expr}}, y={{y_expr}}")
        self.equation_lines.append(line)

    def plot_polar(self, equation, color):
        theta = np.linspace(0, 2 * np.pi, self.resolution.get())
        r = eval(equation, {"__builtins__": {}}, {"theta": theta, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi})
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        line, = self.ax.plot(x, y, color=color, linewidth=self.line_width.get(), label=f"r = {equation}")
        self.equation_lines.append(line)

    def reset_view(self):
        x_min, x_max = map(float, self.x_range.get().split(','))
        y_min, y_max = map(float, self.y_range.get().split(','))
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.refresh_plot()
        self.update_status("已重置视图")

    def on_mouse_move(self, event):
        if hasattr(event, 'inaxes') and event.inaxes and event.xdata is not None and event.ydata is not None:
            self.update_status(f"坐标: ({event.xdata:.4f}, {event.ydata:.4f})")

    def update_info(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED)
