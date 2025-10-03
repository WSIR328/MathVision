"""
数学知识点学习模块
提供详细的数学知识点展示和学习功能
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import font as tkfont


class KnowledgeLearningClass:
    """知识点学习类"""
    
    def __init__(self):
        """初始化知识点数据"""
        self.knowledge_data = self._load_knowledge_data()
    
    def _load_knowledge_data(self):
        """加载所有知识点数据"""
        return {
            1: {
                "title": "矩形积分法（黎曼和）",
                "content": """
【定义】
矩形积分法是数值积分的基本方法之一，通过将积分区间分割成若干小矩形，
用矩形面积之和来近似曲线下的面积。

【基本原理】
对于函数 f(x) 在区间 [a, b] 上的定积分：
∫[a,b] f(x)dx ≈ Σ f(xi) · Δx

其中：
- Δx = (b - a) / n  （子区间宽度）
- xi 是第 i 个子区间的采样点
- n 是分割的子区间数量

【三种采样方法】
1. 左端点法：xi = a + i·Δx
2. 右端点法：xi = a + (i+1)·Δx  
3. 中点法：xi = a + (i+0.5)·Δx

【误差分析】
- 分割越细（n 越大），近似越精确
- 中点法通常比左右端点法更精确
- 误差阶数：O(1/n)

【应用场景】
- 计算不规则图形面积
- 物理中的功、路程计算
- 概率论中的期望值计算
- 工程中的数值积分

【示例】
计算 ∫[0,1] x²dx：
- 精确值：1/3 ≈ 0.333333
- n=10 时近似值：≈ 0.335
- n=100 时近似值：≈ 0.33335
"""
            },
            2: {
                "title": "泰勒级数展开",
                "content": """
【定义】
泰勒级数是用无穷级数来表示一个函数的方法，是函数在某点附近的多项式近似。

【泰勒公式】
f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...

一般形式：
f(x) = Σ[n=0,∞] f⁽ⁿ⁾(a)(x-a)ⁿ/n!

【麦克劳林级数】
当 a = 0 时的特殊情况：
f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...

【常见函数的泰勒展开】
1. eˣ = 1 + x + x²/2! + x³/3! + x⁴/4! + ...

2. sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...

3. cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...

4. ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...  (|x| < 1)

5. (1+x)ⁿ = 1 + nx + n(n-1)x²/2! + ...

【收敛性】
- 收敛半径：级数收敛的 x 的范围
- 余项估计：Rn(x) = f⁽ⁿ⁺¹⁾(ξ)(x-a)⁽ⁿ⁺¹⁾/(n+1)!

【应用】
- 函数近似计算
- 微分方程求解
- 物理学中的近似分析
- 计算机科学中的算法优化

【几何意义】
泰勒展开的前 n 项构成 n 次多项式，是函数在展开点附近的最佳多项式近似。
"""
            },
            3: {
                "title": "函数的分割与区间分析",
                "content": """
【定义】
函数分割是将函数的定义域划分为若干子区间，在每个子区间上分析函数的性质。

【分割的目的】
1. 研究函数的单调性
2. 寻找函数的极值点
3. 分析函数的凹凸性
4. 计算定积分

【分割点的选择】
1. 导数为零的点（驻点）
2. 导数不存在的点
3. 函数不连续的点
4. 定义域的端点

【区间分析方法】
1. 单调性分析：
   - f'(x) > 0 → 函数递增
   - f'(x) < 0 → 函数递减

2. 凹凸性分析：
   - f''(x) > 0 → 函数凹（下凸）
   - f''(x) < 0 → 函数凸（上凸）

3. 极值判定：
   - 一阶导数检验
   - 二阶导数检验

【实际应用】
- 优化问题求解
- 函数图像绘制
- 不等式证明
- 方程根的定位

【示例】
分析 f(x) = x³ - 3x：
- f'(x) = 3x² - 3 = 3(x-1)(x+1)
- 分割点：x = -1, 1
- 区间 (-∞,-1)：递增
- 区间 (-1,1)：递减
- 区间 (1,∞)：递增
- 极大值点：x = -1
- 极小值点：x = 1
"""
            },
            4: {
                "title": "切线与法线",
                "content": """
【切线定义】
曲线在某点的切线是通过该点且与曲线"相切"的直线，其斜率等于函数在该点的导数值。

【切线方程】
对于函数 y = f(x) 在点 (x₀, y₀) 处的切线方程：
y - y₀ = f'(x₀)(x - x₀)

或写成：
y = f'(x₀)·x + [f(x₀) - x₀·f'(x₀)]

【法线定义】
法线是过切点且垂直于切线的直线。

【法线方程】
y - y₀ = -1/f'(x₀) · (x - x₀)  （当 f'(x₀) ≠ 0）

【几何意义】
1. 切线：曲线在该点的瞬时变化方向
2. 法线：垂直于切线的方向
3. 切线斜率 × 法线斜率 = -1

【特殊情况】
1. f'(x₀) = 0：切线水平，法线垂直
2. f'(x₀) → ∞：切线垂直，法线水平
3. f'(x₀) 不存在：可能有尖点或拐点

【应用】
- 物理中的速度和加速度
- 光学中的反射和折射
- 工程中的曲线设计
- 经济学中的边际分析

【示例】
求 y = x² 在点 (1, 1) 处的切线和法线：
- f'(x) = 2x，f'(1) = 2
- 切线：y - 1 = 2(x - 1) → y = 2x - 1
- 法线：y - 1 = -1/2(x - 1) → y = -x/2 + 3/2
"""
            },
            5: {
                "title": "数列与级数",
                "content": """
【数列定义】
数列是按一定顺序排列的一列数，记作 {an}。

【常见数列】
1. 等差数列：an = a₁ + (n-1)d
   - 通项公式
   - 求和公式：Sn = n(a₁+an)/2

2. 等比数列：an = a₁·qⁿ⁻¹
   - 通项公式
   - 求和公式：Sn = a₁(1-qⁿ)/(1-q)

3. 斐波那契数列：an = an-1 + an-2
   - 递推关系
   - 通项公式（比内公式）

【数列极限】
lim(n→∞) an = L

判定方法：
1. 单调有界数列必有极限
2. 夹逼定理
3. 比值判别法
4. 根值判别法

【级数】
无穷级数：Σ[n=1,∞] an

【级数收敛性】
1. 正项级数：
   - 比较判别法
   - 比值判别法（达朗贝尔判别法）
   - 根值判别法（柯西判别法）
   - 积分判别法

2. 交错级数：
   - 莱布尼茨判别法

3. 任意项级数：
   - 绝对收敛
   - 条件收敛

【常见级数】
1. 几何级数：Σ qⁿ = 1/(1-q)  (|q| < 1)

2. 调和级数：Σ 1/n  （发散）

3. p-级数：Σ 1/nᵖ
   - p > 1 收敛
   - p ≤ 1 发散

【应用】
- 函数展开（泰勒级数）
- 数值计算
- 概率论
- 信号处理
"""
            },
            6: {
                "title": "微分方程",
                "content": """
【定义】
微分方程是含有未知函数及其导数的方程。

【分类】
1. 按阶数：
   - 一阶微分方程
   - 二阶微分方程
   - 高阶微分方程

2. 按线性：
   - 线性微分方程
   - 非线性微分方程

【一阶微分方程】
1. 可分离变量：dy/dx = f(x)g(y)
   解法：∫dy/g(y) = ∫f(x)dx

2. 齐次方程：dy/dx = f(y/x)
   解法：令 u = y/x

3. 一阶线性方程：dy/dx + P(x)y = Q(x)
   解法：y = e^(-∫P(x)dx)[∫Q(x)e^(∫P(x)dx)dx + C]

【二阶线性微分方程】
y'' + p(x)y' + q(x)y = f(x)

1. 齐次方程（f(x) = 0）：
   - 特征方程法
   - 通解结构

2. 非齐次方程：
   - 通解 = 齐次通解 + 特解
   - 常数变易法
   - 待定系数法

【特征方程法】
对于 y'' + py' + qy = 0：
特征方程：r² + pr + q = 0

1. 两个不等实根 r₁, r₂：
   y = C₁e^(r₁x) + C₂e^(r₂x)

2. 两个相等实根 r：
   y = (C₁ + C₂x)e^(rx)

3. 共轭复根 α ± βi：
   y = e^(αx)(C₁cos(βx) + C₂sin(βx))

【应用】
- 物理：振动、波动、热传导
- 工程：电路分析、控制系统
- 生物：种群增长模型
- 经济：经济增长模型

【示例】
求解 y' = 2y，y(0) = 1：
- 分离变量：dy/y = 2dx
- 积分：ln|y| = 2x + C
- 通解：y = Ae^(2x)
- 代入初值：y = e^(2x)
"""
            },
            7: {
                "title": "方程可视化与图形分析",
                "content": """
【函数图像的基本要素】
1. 定义域和值域
2. 对称性（奇偶性）
3. 周期性
4. 单调性
5. 极值点
6. 拐点
7. 渐近线

【图像变换】
1. 平移变换：
   - y = f(x-h)：向右平移 h
   - y = f(x) + k：向上平移 k

2. 伸缩变换：
   - y = af(x)：纵向伸缩
   - y = f(ax)：横向伸缩

3. 对称变换：
   - y = -f(x)：关于 x 轴对称
   - y = f(-x)：关于 y 轴对称

【渐近线】
1. 水平渐近线：
   lim(x→±∞) f(x) = b → y = b

2. 垂直渐近线：
   lim(x→a) f(x) = ±∞ → x = a

3. 斜渐近线：
   y = kx + b，其中
   k = lim(x→∞) f(x)/x
   b = lim(x→∞) [f(x) - kx]

【参数方程】
x = x(t)
y = y(t)

常见参数曲线：
1. 圆：x = r·cos(t), y = r·sin(t)
2. 椭圆：x = a·cos(t), y = b·sin(t)
3. 摆线：x = a(t-sin(t)), y = a(1-cos(t))

【极坐标方程】
r = f(θ)

常见极坐标曲线：
1. 圆：r = a
2. 心形线：r = a(1+cos(θ))
3. 玫瑰线：r = a·sin(nθ)
4. 阿基米德螺线：r = aθ

【隐函数】
F(x, y) = 0

求导：dy/dx = -Fx/Fy

【应用】
- 工程设计中的曲线绘制
- 物理轨迹分析
- 数据可视化
- 计算机图形学
"""
            },
            8: {
                "title": "分形几何 - 科赫曲线",
                "content": """
【分形定义】
分形是具有自相似性的几何图形，在不同尺度下呈现相似的结构。

【科赫曲线（Koch Curve）】
由瑞典数学家 Helge von Koch 在 1904 年提出。

【构造过程】
初始：一条线段

迭代规则：
1. 将线段三等分
2. 以中间一段为底边，向外作等边三角形
3. 去掉底边
4. 对每条新线段重复此过程

【数学性质】
1. 长度：
   - 第 n 次迭代后长度 = L₀·(4/3)ⁿ
   - n → ∞ 时，长度 → ∞

2. 分形维数：
   D = log(4)/log(3) ≈ 1.2619

3. 自相似性：
   - 局部与整体相似
   - 无限精细的结构

【科赫雪花】
将三条科赫曲线首尾相连形成的封闭图形。

性质：
- 周长无限
- 面积有限
- 分形维数相同

【其他著名分形】
1. 谢尔宾斯基三角形
2. 曼德布罗特集
3. 朱利亚集
4. 龙形曲线
5. 希尔伯特曲线

【分形维数】
D = log(N)/log(r)
其中：
- N：自相似部分的数量
- r：缩放比例

【应用】
- 自然界模拟（海岸线、山脉、树木）
- 图像压缩
- 天线设计
- 艺术创作
- 金融市场分析

【哲学意义】
分形揭示了自然界中"无限复杂性"与"简单规则"的统一。
"""
            },
            9: {
                "title": "海森矩阵（Hessian Matrix）",
                "content": """
【定义】
海森矩阵是多元函数的二阶偏导数组成的方阵，用于研究函数的局部性质。

【二元函数的海森矩阵】
对于函数 f(x, y)：

H = | fxx  fxy |
    | fyx  fyy |

其中：
- fxx = ∂²f/∂x²
- fxy = ∂²f/∂x∂y
- fyx = ∂²f/∂y∂x
- fyy = ∂²f/∂y²

【多元函数的海森矩阵】
对于 n 元函数 f(x₁, x₂, ..., xn)：

H = [∂²f/∂xi∂xj]  (i,j = 1,2,...,n)

【极值判定】
在驻点 (x₀, y₀) 处（即 fx = fy = 0）：

1. 判别式 D = fxx·fyy - (fxy)²

2. 判定规则：
   - D > 0 且 fxx > 0 → 极小值
   - D > 0 且 fxx < 0 → 极大值
   - D < 0 → 鞍点
   - D = 0 → 无法判定

【正定性】
1. 正定：所有特征值 > 0 → 极小值
2. 负定：所有特征值 < 0 → 极大值
3. 不定：特征值有正有负 → 鞍点

【泰勒展开中的应用】
f(x+h, y+k) ≈ f(x,y) + [fx·h + fy·k] 
              + 1/2[fxx·h² + 2fxy·hk + fyy·k²]

矩阵形式：
f(x+Δx) ≈ f(x) + ∇f·Δx + 1/2·Δx^T·H·Δx

【应用领域】
1. 优化算法：
   - 牛顿法
   - 拟牛顿法
   - 信赖域方法

2. 机器学习：
   - 损失函数优化
   - 神经网络训练
   - 凸优化

3. 经济学：
   - 效用函数分析
   - 成本函数优化

4. 物理学：
   - 势能面分析
   - 稳定性判定

【计算技巧】
1. 对称性：fxy = fyx（在连续条件下）
2. 数值计算：有限差分法
3. 自动微分：计算机自动求导

【示例】
f(x, y) = x² + xy + y²

海森矩阵：
H = | 2  1 |
    | 1  2 |

在原点 (0,0)：
- D = 2×2 - 1² = 3 > 0
- fxx = 2 > 0
- 结论：(0,0) 是极小值点
"""
            }
        }
    
    def show_knowledge(self, knowledge_id):
        """显示知识点详细内容"""
        if knowledge_id not in self.knowledge_data:
            return
        
        knowledge = self.knowledge_data[knowledge_id]
        
        # 创建知识点窗口
        window = tk.Toplevel()
        window.title(f"知识点学习 - {knowledge['title']}")
        window.geometry("800x600")
        window.configure(bg="#E6F3FF")
        
        # 创建主框架
        main_frame = ttk.Frame(window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_font = tkfont.Font(family="SimHei", size=16, weight="bold")
        title_label = tk.Label(
            main_frame,
            text=knowledge['title'],
            font=title_font,
            bg="#E6F3FF",
            fg="#2C3E50"
        )
        title_label.pack(pady=(0, 20))
        
        # 内容文本框
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        content_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("SimHei", 11),
            bg="#FFFFFF",
            fg="#2C3E50",
            padx=15,
            pady=15
        )
        content_text.pack(fill=tk.BOTH, expand=True)
        
        # 插入内容
        content_text.insert("1.0", knowledge['content'])
        content_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 关闭按钮
        close_btn = ttk.Button(
            main_frame,
            text="关闭",
            command=window.destroy
        )
        close_btn.pack(pady=(20, 0))
    
    # 知识点方法
    def knowledge_learning_1_function(self):
        """矩形积分知识"""
        self.show_knowledge(1)
    
    def knowledge_learning_2_function(self):
        """泰勒展开知识"""
        self.show_knowledge(2)
    
    def knowledge_learning_3_function(self):
        """分割线知识"""
        self.show_knowledge(3)
    
    def knowledge_learning_4_function(self):
        """切线知识"""
        self.show_knowledge(4)
    
    def knowledge_learning_5_function(self):
        """数列分析知识"""
        self.show_knowledge(5)
    
    def knowledge_learning_6_function(self):
        """微分方程知识"""
        self.show_knowledge(6)
    
    def knowledge_learning_7_function(self):
        """方程可视化知识"""
        self.show_knowledge(7)
    
    def knowledge_learning_8_function(self):
        """科赫曲线知识"""
        self.show_knowledge(8)
    
    def knowledge_learning_9_function(self):
        """海森矩阵知识"""
        self.show_knowledge(9)
