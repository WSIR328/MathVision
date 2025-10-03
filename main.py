import tkinter as tk
import logging
import os
from typing import Optional, Type

# --- 核心模块导入 ---
from core.page_manager import PageManager, BasePage, NavigationBar
from core.config_manager import config_manager
from core.thread_manager import shutdown_thread_manager
from core.search_manager import search_manager, SearchWidget

# --- UI组件和主题 ---
from themes.futuristic_theme import COLORS, FONTS
from components.cards import InteractiveCard
from components.buttons import FuturisticButton
from components.module_adapter import ModuleAdapter

# --- 数学功能模块导入 ---
# 高等数学
from modules.calculus.equation_plotter import EquationVisualizationApp
from modules.calculus.kehe import KeheApp
from modules.calculus.weifen import DirectionFieldApp
from modules.calculus.trig_plot_app import TrigPlotApp
from modules.calculus.haisen import HessianApp
from modules.sequences.shulie import SequenceModule

# 线性代数
from modules.linear_algebra.gaosixiaoyuan import GaussianEliminationApp
from modules.linear_algebra.guodujuzhen import MatrixTransitionApp
from modules.linear_algebra.hanglieshi import DeterminantApp
from modules.linear_algebra.jibianhuan import MatrixTransformationApp
from modules.linear_algebra.jisuan import VectorOperationsApp
from modules.linear_algebra.juzhenduibi import MatrixComparisonApp
from modules.linear_algebra.tezheng import EigenvalueApp
from modules.linear_algebra.zhuanzhi import MatrixAnimationApp

# 概率统计
from modules.probability.fenxi import AnalysisApp
from modules.probability.gailvlunn import ProbabilityApp
from modules.probability.beiye import BayesianApp
from modules.probability.game import GamePuzzleApp
from modules.probability.mengka import MonteCarloApp
from modules.probability.suiji import RandomVariableApp
from modules.probability.suijiguocheng import StochasticProcessApp
from modules.probability.tuiduan import HypothesisTestingApp
from modules.probability.zhixin import ConfidenceIntervalApp

# --- AI 模块 ---
from modules.ai_wrapper import AIDataAnalysisWrapper

# --- 页面定义 ---

class MainPage(BasePage):
    """主页面 - 显示主要功能卡片"""
    def initialize(self):
        self.controller.update_title("MathVision 主页")
        # ... (UI代码与之前类似，此处省略以保持简洁)
        title_label = tk.Label(self, text="欢迎来到数学可视化工具", font=FONTS["title"], bg=COLORS["bg_light"], fg=COLORS["text_primary"])
        title_label.pack(pady=40)
        cards_frame = tk.Frame(self, bg=COLORS["bg_light"])
        cards_frame.pack(expand=True)
        cards_data = [
            ("高等数学", lambda: self.controller.show_page("AdvancedMathPage")),
            ("线性代数", lambda: self.controller.show_page("LinearAlgebraPage")),
            ("概率统计", lambda: self.controller.show_page("ProbabilityPage")),
            ("AI 数据分析", lambda: self.controller.show_page("AIDataAnalysisPage")),
        ]
        # 使用2x2网格布局
        for i, (title, action) in enumerate(cards_data):
            row = i // 2
            col = i % 2
            card = FuturisticButton(cards_frame, text=title, command=action, width=200, height=100)
            card.grid(row=row, column=col, padx=20, pady=20)

class ModuleMenuPage(BasePage):
    """显示特定学科下所有模块的菜单页面"""
    def setup(self, title: str, modules: dict):
        self.page_title = title
        self.modules = modules

    def initialize(self):
        self.controller.update_title(self.page_title)
        
        container = tk.Frame(self, bg=COLORS["bg_light"])
        container.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        for i, (name, module_class) in enumerate(self.modules.items()):
            btn = FuturisticButton(container, text=name, command=lambda m=module_class: self._open_module(m), width=300, height=60)
            btn.pack(pady=15)

    def _open_module(self, module_class: Type[BasePage]):
        """通用模块加载方法"""
        page_name = module_class.__name__
        if not self.controller.get_page(page_name):
            # 使用ModuleAdapter包装模块
            self.controller.register_page(page_name, ModuleAdapter, module_class=module_class)
        self.controller.show_page(page_name)

# --- 主应用 ---

class MathVisionApp:
    def __init__(self):
        self.root = tk.Tk()
        self._setup_window()
        
        self.page_manager = PageManager(self.root)
        self.navbar = NavigationBar(self.root, self.page_manager)
        self.page_manager.set_navbar(self.navbar)
        self.navbar.pack(side=tk.TOP, fill=tk.X)
        
        self._register_pages()
        self.page_manager.show_page("MainPage")

    def _setup_window(self):
        self.root.title("数学可视化教学工具 2.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLORS["bg_light"])

    def _register_pages(self):
        self.page_manager.register_page("MainPage", MainPage)

        # 定义模块
        adv_math_modules = {
            "方程可视化": EquationVisualizationApp,
            "科赫雪花": KeheApp,
            "微分方程方向场": DirectionFieldApp,
            "海森矩阵": HessianApp,
            "数列分析": SequenceModule,
            "三角函数可视化": TrigPlotApp
        }
        lin_alg_modules = {
            "高斯消元": GaussianEliminationApp,
            "矩阵变换": MatrixTransformationApp,
            "特征值": EigenvalueApp,
            "过渡矩阵": MatrixTransitionApp,
            "行列式": DeterminantApp,
            "向量运算": VectorOperationsApp,
            "矩阵对比": MatrixComparisonApp,
            "矩阵动画": MatrixAnimationApp,
        }
        prob_modules = {
            "统计分析": AnalysisApp,
            "概率分布": ProbabilityApp,
            "贝叶斯": BayesianApp,
            "游戏益智": GamePuzzleApp,
            "蒙特卡洛": MonteCarloApp,
            "随机变量": RandomVariableApp,
            "随机过程": StochasticProcessApp,
            "假设检验": HypothesisTestingApp,
            "置信区间": ConfidenceIntervalApp,
        }

        # 创建并注册菜单页面
        adv_math_page = self.page_manager.register_page("AdvancedMathPage", ModuleMenuPage)
        adv_math_page.setup("高等数学", adv_math_modules)

        lin_alg_page = self.page_manager.register_page("LinearAlgebraPage", ModuleMenuPage)
        lin_alg_page.setup("线性代数", lin_alg_modules)

        prob_page = self.page_manager.register_page("ProbabilityPage", ModuleMenuPage)
        prob_page.setup("概率统计", prob_modules)
        
        # 注册 AI 数据分析页面
        self.page_manager.register_page("AIDataAnalysisPage", ModuleAdapter, module_class=AIDataAnalysisWrapper)

    def run(self):
        try:
            self.root.mainloop()
        finally:
            shutdown_thread_manager()

if __name__ == "__main__":
    app = MathVisionApp()
    app.run()