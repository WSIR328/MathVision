import tkinter as tk
from core.page_manager import BasePage

class ModuleAdapter(BasePage):
    def __init__(self, parent, controller, module_class):
        super().__init__(parent, controller)
        self.module = module_class(self)