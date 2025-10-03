"""
动画效果模块
提供页面切换和UI元素的动画效果
"""

import tkinter as tk


def fade_in(widget, duration=300, callback=None):
    """
    淡入动画效果
    
    Args:
        widget: 要应用动画的组件
        duration: 动画持续时间（毫秒）
        callback: 动画完成后的回调函数
    """
    # 简化实现：直接显示组件
    widget.pack(fill=tk.BOTH, expand=True)
    if callback:
        widget.after(duration, callback)


def slide_in(widget, direction='left', duration=300, callback=None):
    """
    滑入动画效果
    
    Args:
        widget: 要应用动画的组件
        direction: 滑入方向 ('left', 'right', 'top', 'bottom')
        duration: 动画持续时间（毫秒）
        callback: 动画完成后的回调函数
    """
    # 简化实现：直接显示组件
    widget.pack(fill=tk.BOTH, expand=True)
    if callback:
        widget.after(duration, callback)


def fade_out(widget, duration=300, callback=None):
    """
    淡出动画效果
    
    Args:
        widget: 要应用动画的组件
        duration: 动画持续时间（毫秒）
        callback: 动画完成后的回调函数
    """
    # 简化实现：直接隐藏组件
    if callback:
        widget.after(duration, callback)
    widget.pack_forget()


def slide_out(widget, direction='left', duration=300, callback=None):
    """
    滑出动画效果
    
    Args:
        widget: 要应用动画的组件
        direction: 滑出方向 ('left', 'right', 'top', 'bottom')
        duration: 动画持续时间（毫秒）
        callback: 动画完成后的回调函数
    """
    # 简化实现：直接隐藏组件
    if callback:
        widget.after(duration, callback)
    widget.pack_forget()
