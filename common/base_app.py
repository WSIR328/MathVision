"""
数学模块基类
为所有数学功能模块提供统一的基础框架
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from themes.futuristic_theme import COLORS, FONTS


class MathModuleApp(tk.Frame):
    """数学模块基类"""
    
    def __init__(self, master=None, title="数学模块", **kwargs):
        super().__init__(master, bg=COLORS.get("bg_light", "#f0f0f0"), **kwargs)
        self.master = master
        self.title = title
        
        # 创建主布局
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建左右分栏
        self.control_frame = tk.Frame(self, bg=COLORS.get("bg_light", "#f0f0f0"), width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.control_frame.pack_propagate(False)
        
        self.plot_frame = tk.Frame(self, bg=COLORS.get("bg_light", "#f0f0f0"))
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建 matplotlib 图形
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # 创建画布
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建工具栏
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
    
    def create_control_section(self, title):
        """创建控制区域的一个部分"""
        frame = ttk.LabelFrame(self.control_frame, text=title, padding=10)
        frame.pack(fill=tk.X, padx=5, pady=5)
        return frame
    
    def save_plot(self):
        """保存图像"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            self.show_info(f"图像已保存到: {filename}")
    
    def refresh_plot(self):
        """刷新图形 - 子类应该重写此方法"""
        self.canvas.draw()
    
    def update_status(self, message):
        """更新状态信息 - 可以在子类中重写"""
        print(f"状态: {message}")
    
    def clear_plot(self):
        """清空图形"""
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid(True)
        self.canvas.draw()
    
    def clear_sequence(self):
        """清空数列显示 - 用于数列模块"""
        # 子类可以重写此方法
        pass
    
    def create_header(self, title):
        """创建标题栏"""
        header_frame = tk.Frame(self, bg=COLORS.get("bg_dark", "#2c3e50"))
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=FONTS.get("title", ("Arial", 20, "bold")),
            bg=COLORS.get("bg_dark", "#2c3e50"),
            fg=COLORS.get("text_primary", "#ffffff")
        )
        title_label.pack(pady=10)
        
        return header_frame
    
    def create_button(self, parent, text, command, **kwargs):
        """创建统一样式的按钮"""
        btn = ttk.Button(parent, text=text, command=command, **kwargs)
        return btn
    
    def create_label(self, parent, text, **kwargs):
        """创建统一样式的标签"""
        label = tk.Label(
            parent,
            text=text,
            bg=kwargs.pop('bg', COLORS.get("bg_light", "#f0f0f0")),
            fg=kwargs.pop('fg', COLORS.get("text_primary", "#000000")),
            **kwargs
        )
        return label
    
    def show_error(self, message):
        """显示错误消息"""
        from tkinter import messagebox
        messagebox.showerror("错误", message)
    
    def show_info(self, message):
        """显示信息消息"""
        from tkinter import messagebox
        messagebox.showinfo("信息", message)
    
    def show_warning(self, message):
        """显示警告消息"""
        from tkinter import messagebox
        messagebox.showwarning("警告", message)
