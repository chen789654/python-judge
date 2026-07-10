"""
实验数据初始化脚本
运行方式: python seed_experiments.py

==================================================
课程结构：
  理论16课时（8次课，每次2课时）
  实验32课时（16次实验，每次2课时）
  
  一次理论课 → 对应两次实操实验课
==================================================

实验安排（16次实验 x 2课时 = 32课时）：

【第1单元】Python入门（理论1 → 实验1-2）
  理论1：环境搭建、print()、变量、数据类型
  实验1：环境配置 + 第一个Python程序（Hello World）
  实验2：交通数据中的变量与运算

【第2单元】输入输出与流程控制（理论2 → 实验3-4）  
  理论2：input()、类型转换、条件判断
  实验3：交通信息计算与格式化输出
  实验4：交通信号灯判断

【第3单元】循环与列表（理论3 → 实验5-6）
  理论3：for/while循环、列表
  实验5：路口车流量统计（循环）
  实验6：公交/地铁站点管理（列表）

【第4单元】字符串与函数（理论4 → 实验7-8）
  理论4：字符串操作、函数定义
  实验7：车牌号归属地识别（字符串）
  实验8：出租车计费系统（函数）

【第5单元】字典与数据组织（理论5 → 实验9-10）
  理论5：字典、数据综合
  实验9：地铁线路查询系统（字典）
  实验10：交通调查数据预处理

【第6单元】异常与数据处理（理论6 → 实验11-12）
  理论6：多行输入、异常处理
  实验11：交通调查数据处理
  实验12：交通数据异常检测

【第7单元】面向对象（理论7 → 实验13-14）
  理论7：类与对象、排序
  实验13：交通工具类设计
  实验14：车辆速度与拥堵分析

【第8单元】综合应用（理论8 → 实验15-16）
  理论8：集合、综合复习
  实验15：公交线路换乘查询
  实验16：综合交通数据分析报告
==================================================
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models import Problem, TestCase, User

app = create_app()

EXPERIMENTS = [
    # ═══════════════════════════════════════════════════════════════
    # 第1单元 Python入门（理论1 -> 实验1-2）
    # 理论：环境搭建、print()、变量、数据类型
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 1,
        "title": "实验1：我的第一个Python程序",
        "difficulty": "easy",
        "tags": "print,基本语法,字符串",
        "description": """# 实验1：我的第一个Python程序

**对应理论课：** Python环境搭建、print()输出、基本语法

**本课目标：** 学会在Judge平台上提交并运行第一个Python程序。

## 背景
欢迎来到Python编程世界！作为交通运输专业的学生，编程将成为你分析数据、解决交通问题的有力工具。本实验让你完成第一个Python程序。

## 题目
编写程序，在屏幕上输出以下三行内容：

```
我的第一个Python程序
我爱交通运输工程
Python + 交通 = 无限可能
```

> 提示：使用 `print('要输出的内容')` 来输出文本。每行内容用一个print()语句。

## 输入格式
本题无需输入。

## 输出格式
三行文字，如上所示。

## 示例
输出：
```
我的第一个Python程序
我爱交通运输工程
Python + 交通 = 无限可能
```""",
        "input_desc": "无输入",
        "output_desc": "三行指定文字",
        "sample_input": "",
        "sample_output": "我的第一个Python程序\n我爱交通运输工程\nPython + 交通 = 无限可能",
        "standard_answer": "# 实验1：我的第一个Python程序\n# 核心知识点：print()函数、字符串输出\nprint('我的第一个Python程序')\nprint('我爱交通运输工程')\nprint('Python + 交通 = 无限可能')",
        "test_cases": [
            ("", "我的第一个Python程序\n我爱交通运输工程\nPython + 交通 = 无限可能", True, 1.0),
        ]
    },
    {
        "order": 2,
        "title": "实验2：交通数据中的变量与运算",
        "difficulty": "easy",
        "tags": "变量,输入输出,运算符",
        "description": """# 实验2：交通数据中的变量与运算

**对应理论课：** 变量、数据类型、算术运算

## 背景
交通运输工程中经常需要进行各种数据计算。本实验学习使用变量存储数据，并进行基本的算术运算。

## 题目
某路段在早高峰和晚高峰的车流量数据如下：
- 早高峰车流量：A 辆/小时
- 晚高峰车流量：B 辆/小时

请编写程序，从键盘输入 A 和 B 的值，计算并输出：
1. 早高峰和晚高峰的总车流量 = A + B
2. 早高峰比晚高峰多（或少）多少辆 = A - B
3. 平均每小时车流量 = (A + B) / 2

> 提示：使用 `input().split()` 获取空格分隔的输入，`map(int, ...)` 转换为整数。

## 输入格式
一行两个整数，用空格隔开，分别代表 A 和 B。

## 输出格式
三行：第一行总和，第二行差值，第三行平均值（保留1位小数）。

## 示例
输入：
```
1200 1500
```
输出：
```
2700
-300
1350.0
```""",
        "input_desc": "一行两个整数，用空格隔开，分别代表早高峰和晚高峰车流量",
        "output_desc": "三行：总和、差值（早-晚）、平均值（保留1位小数）",
        "sample_input": "1200 1500",
        "sample_output": "2700\n-300\n1350.0",
        "standard_answer": "# 实验2：交通数据中的变量与运算\n# 核心知识点：变量、input()、类型转换、算术运算\nA, B = map(int, input().split())\ntotal = A + B\ndiff = A - B\navg = total / 2\nprint(total)\nprint(diff)\nprint(avg)",
        "test_cases": [
            ("1200 1500", "2700\n-300\n1350.0", True, 1.0),
            ("800 650", "1450\n150\n725.0", True, 1.0),
            ("2000 1800", "3800\n200\n1900.0", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第2单元 输入输出与流程控制（理论2 -> 实验3-4）
    # 理论：input()、类型转换、条件判断
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 3,
        "title": "实验3：交通信息计算与格式化输出",
        "difficulty": "easy",
        "tags": "输入输出,数据类型,格式化字符串",
        "description": """# 实验3：交通信息计算与格式化输出

**对应理论课：** 数据类型转换、格式化输出

## 背景
高速公路上有测速点，需要根据行驶时间和距离计算平均速度。

## 题目
编写程序，从键盘输入行驶的**距离**（公里）和**时间**（小时），计算并输出平均速度（km/h）。

输出要求：
1. 平均速度（保留1位小数）+ 单位 " km/h"
2. 同时输出速度等级判定：
   - 如果速度 >= 120，输出 "超速"
   - 如果速度 >= 80，输出 "正常"
   - 否则输出 "慢速"

> 提示：使用 `float()` 转换小数输入，用 `f'{x:.1f}'` 格式化输出。

## 输入格式
一行两个数，用空格隔开：距离(公里) 时间(小时)

## 输出格式
第一行：平均速度 + " km/h"
第二行：速度等级

## 示例
输入：
```
120 1.5
```
输出：
```
80.0 km/h
正常
```""",
        "input_desc": "一行两个数：距离(公里) 时间(小时)",
        "output_desc": "第一行速度(km/h)，第二行等级",
        "sample_input": "120 1.5",
        "sample_output": "80.0 km/h\n正常",
        "standard_answer": "# 实验3：交通信息计算与格式化输出\n# 核心知识点：float类型、f-string格式化、条件判断\ndist, t = map(float, input().split())\nspeed = dist / t\nprint(f'{speed:.1f} km/h')\nif speed >= 120:\n    print('超速')\nelif speed >= 80:\n    print('正常')\nelse:\n    print('慢速')",
        "test_cases": [
            ("120 1.5", "80.0 km/h\n正常", True, 1.0),
            ("200 1.0", "200.0 km/h\n超速", True, 1.0),
            ("60 1.0", "60.0 km/h\n慢速", True, 1.0),
            ("150 2.0", "75.0 km/h\n慢速", False, 1.0),
        ]
    },
    {
        "order": 4,
        "title": "实验4：交通信号灯判断",
        "difficulty": "easy",
        "tags": "条件判断,if-elif-else,字符串",
        "description": """# 实验4：交通信号灯判断

**对应理论课：** 条件判断 if/elif/else

## 背景
作为一名交通工程师，需要根据信号灯状态判断通行规则。

## 题目
编写程序，输入一个表示交通信号灯颜色的字符串（不区分大小写），输出对应的通行指令：
- "red" 或 "红" -> 输出 "停止"
- "yellow" 或 "黄" -> 输出 "等待"
- "green" 或 "绿" -> 输出 "通行"
- 其他 -> 输出 "信号灯故障"

> 提示：用 `.strip().lower()` 去除空格并转为小写方便比较。

## 输入格式
一行字符串，表示信号灯颜色。

## 输出格式
一行字符串，表示通行指令。

## 示例
输入：
```
red
```
输出：
```
停止
```""",
        "input_desc": "一行字符串：red/yellow/green 或 红/黄/绿",
        "output_desc": "一行：停止/等待/通行/信号灯故障",
        "sample_input": "red",
        "sample_output": "停止",
        "standard_answer": "# 实验4：交通信号灯判断\n# 核心知识点：if/elif/else多分支、字符串方法、in运算符\ncolor = input().strip().lower()\nif color in ('red', '红'):\n    print('停止')\nelif color in ('yellow', '黄'):\n    print('等待')\nelif color in ('green', '绿'):\n    print('通行')\nelse:\n    print('信号灯故障')",
        "test_cases": [
            ("red", "停止", True, 1.0),
            ("green", "通行", True, 1.0),
            ("blue", "信号灯故障", True, 1.0),
            ("黄", "等待", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第3单元 循环与列表（理论3 -> 实验5-6）
    # 理论：for/while循环、列表
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 5,
        "title": "实验5：路口车流量统计（循环）",
        "difficulty": "easy",
        "tags": "循环,for循环,累加",
        "description": """# 实验5：路口车流量统计（循环）

**对应理论课：** for循环、range()、累加器模式

## 背景
交通调查员记录了某路口连续 N 个小时的通过车辆数，需要统计总流量和平均流量。

## 题目
第一行输入一个正整数 N，表示统计的小时数。
接下来 N 行，每行一个整数，表示该小时通过的车辆数。

请计算并输出：
1. 总车流量（所有小时相加）
2. 平均每小时车流量（保留1位小数）

> 提示：用 `for i in range(N):` 循环读入N行数据，用一个变量累加求和。

## 输入格式
第一行：N（正整数）
接下来 N 行：每行一个整数

## 输出格式
第一行：总和
第二行：平均值（保留1位小数）

## 示例
输入：
```
5
120
150
90
200
110
```
输出：
```
670
134.0
```""",
        "input_desc": "第一行整数N，接下来N行每行一个整数",
        "output_desc": "第一行总和，第二行平均值（保留1位小数）",
        "sample_input": "5\n120\n150\n90\n200\n110",
        "sample_output": "670\n134.0",
        "standard_answer": "# 实验5：路口车流量统计（循环）\n# 核心知识点：for循环、range()、累加器模式\nN = int(input())\ntotal = 0\nfor i in range(N):\n    total += int(input())\navg = total / N\nprint(total)\nprint(avg)",
        "test_cases": [
            ("3\n100\n200\n150", "450\n150.0", True, 1.0),
            ("4\n80\n90\n70\n60", "300\n75.0", True, 1.0),
            ("2\n500\n300", "800\n400.0", False, 1.0),
        ]
    },
    {
        "order": 6,
        "title": "实验6：公交/地铁站点管理（列表）",
        "difficulty": "easy",
        "tags": "列表,增删改查",
        "description": """# 实验6：公交/地铁站点管理（列表）

**对应理论课：** 列表（list）的创建与操作

## 背景
一条公交/地铁线路有若干站点，需要用Python列表来管理。

## 题目
初始站点列表为：["火车站", "人民广场", "市政府", "大学城", "汽车站"]

编写程序，实现以下功能：
1. 在末尾添加一个新站点（用户输入）
2. 删除指定站点（用户输入）
3. 输出最终所有站点，用 " -> " 连接

> 提示：`.append()` 添加元素，`.remove()` 删除元素，`' -> '.join()` 连接。

## 输入格式
第一行：要添加的站点名称
第二行：要删除的站点名称

## 输出格式
一行，用 " -> " 连接所有站点

## 示例
输入：
```
机场
市政府
```
输出：
```
火车站 -> 人民广场 -> 大学城 -> 汽车站 -> 机场
```""",
        "input_desc": "第一行：新增站点名；第二行：要删除的站点名",
        "output_desc": "一行，用 -> 连接所有站点",
        "sample_input": "机场\n市政府",
        "sample_output": "火车站 -> 人民广场 -> 大学城 -> 汽车站 -> 机场",
        "standard_answer": "# 实验6：公交/地铁站点管理（列表）\n# 核心知识点：列表的append()、remove()、join()方法\nstations = [\"火车站\", \"人民广场\", \"市政府\", \"大学城\", \"汽车站\"]\nnew_station = input().strip()\ndel_station = input().strip()\nstations.append(new_station)\nif del_station in stations:\n    stations.remove(del_station)\nprint(' -> '.join(stations))",
        "test_cases": [
            ("机场\n市政府", "火车站 -> 人民广场 -> 大学城 -> 汽车站 -> 机场", True, 1.0),
            ("体育中心\n火车站", "人民广场 -> 市政府 -> 大学城 -> 汽车站 -> 体育中心", True, 1.0),
            ("码头\n公园", "火车站 -> 人民广场 -> 市政府 -> 大学城 -> 汽车站 -> 码头", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第4单元 字符串与函数（理论4 -> 实验7-8）
    # 理论：字符串操作、函数定义
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 7,
        "title": "实验7：车牌号归属地识别（字符串）",
        "difficulty": "medium",
        "tags": "字符串,字典,切片",
        "description": """# 实验7：车牌号归属地识别（字符串）

**对应理论课：** 字符串索引、切片、方法

## 背景
中国车牌号第一个汉字代表省份/直辖市。编写程序识别车牌对应的地区。

## 题目
已知部分车牌代码对应关系：
- 京->北京、沪->上海、粤->广东、苏->江苏
- 浙->浙江、川->四川、陕->陕西

输入一个车牌号（如 "陕A12345"），输出其归属地。
如果无法识别，输出 "未知地区"。

> 提示：用 `plate[0]` 取第一个字符，用字典做映射查找。

## 输入格式
一行字符串，表示车牌号。

## 输出格式
一行字符串，表示归属地。

## 示例
输入：
```
沪A88888
```
输出：
```
上海
```""",
        "input_desc": "一行字符串（车牌号）",
        "output_desc": "一行字符串（归属地或'未知地区'）",
        "sample_input": "沪A88888",
        "sample_output": "上海",
        "standard_answer": "# 实验7：车牌号归属地识别（字符串）\n# 核心知识点：字符串索引[0]、字典映射、in判断\nplate = input().strip()\ncode_map = {\n    '京': '北京', '沪': '上海', '粤': '广东',\n    '苏': '江苏', '浙': '浙江', '川': '四川', '陕': '陕西'\n}\nif plate and plate[0] in code_map:\n    print(code_map[plate[0]])\nelse:\n    print('未知地区')",
        "test_cases": [
            ("沪A88888", "上海", True, 1.0),
            ("粤B12345", "广东", True, 1.0),
            ("湘C99999", "未知地区", True, 1.0),
            ("陕A00001", "陕西", False, 1.0),
        ]
    },
    {
        "order": 8,
        "title": "实验8：出租车计费系统（函数）",
        "difficulty": "medium",
        "tags": "函数,分支,数学运算",
        "description": """# 实验8：出租车计费系统（函数）

**对应理论课：** 函数的定义与调用

## 背景
某城市出租车计费规则：
- 起步价 8元（含3公里）
- 超过3公里部分，每公里 2.2元
- 超过10公里部分，每公里 3.0元
- 等待时间超过5分钟，每分钟加收 0.5元

## 题目
编写函数 `calc_fee(distance, wait_time)`，根据行驶里程和等待时间计算总车费。
从键盘输入两个数，调用函数计算并输出最终车费（保留1位小数）。

> 提示：用 `def calc_fee(d, w):` 定义函数，函数体用 if-elif-else 分段计算。

## 输入格式
一行两个数，用空格隔开：行驶里程(公里) 等待时间(分钟)

## 输出格式
一行一个数，车费（保留1位小数）

## 示例
输入：
```
5 10
```
输出：
```
16.0
```""",
        "input_desc": "一行两个数：里程(公里) 等待时间(分钟)",
        "output_desc": "一行：车费（保留1位小数）",
        "sample_input": "5 10",
        "sample_output": "16.0",
        "standard_answer": "# 实验8：出租车计费系统（函数）\n# 核心知识点：函数定义def、返回值return、分段函数\ndef calc_fee(distance, wait_time):\n    if distance <= 3:\n        fee = 8\n    elif distance <= 10:\n        fee = 8 + (distance - 3) * 2.2\n    else:\n        fee = 8 + 7 * 2.2 + (distance - 10) * 3.0\n    if wait_time > 5:\n        fee += (wait_time - 5) * 0.5\n    return fee\n\nd, w = map(float, input().split())\nprint(calc_fee(d, w))",
        "test_cases": [
            ("5 10", "16.0", True, 1.0),
            ("2 0", "8.0", True, 1.0),
            ("12 8", "32.5", True, 1.0),
            ("3 5", "8.0", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第5单元 字典与数据组织（理论5 -> 实验9-10）
    # 理论：字典、数据综合
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 9,
        "title": "实验9：地铁线路查询系统（字典）",
        "difficulty": "medium",
        "tags": "字典,列表,查找",
        "description": """# 实验9：地铁线路查询系统（字典）

**对应理论课：** 字典（dict）的创建与查询

## 背景
某城市地铁线路信息用字典存储，每条线路对应一个站点列表。

## 题目
已知地铁线路数据：
```
lines = {
    1: ['火车站', '人民广场', '文化宫', '体育中心', '机场'],
    2: ['大学城', '科技园', '人民广场', '市政府', '高铁站'],
    3: ['汽车站', '火车站', '市中心', '动物园', '海洋公园']
}
```
输入一个站点名称，输出经过该站点的所有线路编号（从小到大排序，用空格隔开）。
如果没有找到，输出 "未找到"。

> 提示：用 `.items()` 遍历字典，用 `in` 判断站点是否在线路中。

## 输入格式
一行字符串，站点名称。

## 输出格式
一行，线路编号（空格隔开）或 "未找到"。

## 示例
输入：
```
人民广场
```
输出：
```
1 2
```""",
        "input_desc": "一行字符串，站点名称",
        "output_desc": "一行，线路编号（空格隔开）或'未找到'",
        "sample_input": "人民广场",
        "sample_output": "1 2",
        "standard_answer": "# 实验9：地铁线路查询系统（字典）\n# 核心知识点：字典遍历items()、成员判断in\nlines = {\n    1: ['火车站', '人民广场', '文化宫', '体育中心', '机场'],\n    2: ['大学城', '科技园', '人民广场', '市政府', '高铁站'],\n    3: ['汽车站', '火车站', '市中心', '动物园', '海洋公园']\n}\nstation = input().strip()\nresult = []\nfor line_no, stations in lines.items():\n    if station in stations:\n        result.append(str(line_no))\nif result:\n    print(' '.join(result))\nelse:\n    print('未找到')",
        "test_cases": [
            ("人民广场", "1 2", True, 1.0),
            ("火车站", "1 3", True, 1.0),
            ("市中心", "3", True, 1.0),
            ("博物馆", "未找到", False, 1.0),
        ]
    },
    {
        "order": 10,
        "title": "实验10：交通调查数据预处理（综合）",
        "difficulty": "medium",
        "tags": "字典,列表,循环,综合",
        "description": """# 实验10：交通调查数据预处理（综合）

**对应理论课：** 字典与列表的综合运用

## 背景
交通调查中记录了多个路段在不同方向的流量数据，需要按路段汇总。

## 题目
输入多行数据，每行格式为：`路段名称 流量`
以 `END` 结束。

要求按路段名称汇总总流量，并输出：
1. 每个路段的总流量（按输入顺序）
2. 总流量最高的路段名称

> 提示：用字典 `flow = {}` 存储每个路段的总流量，`flow[name] = flow.get(name, 0) + v` 累加。

## 输入格式
多行，每行：路段名称 流量，以END结束

## 输出格式
第一行开始：每行一个路段的总流量（格式：`路段名: 总流量`）
最后一行：总流量最高的路段名

## 示例
输入：
```
钟楼 1200
小寨 800
钟楼 600
小寨 700
END
```
输出：
```
钟楼: 1800
小寨: 1500
钟楼
```""",
        "input_desc": "多行：路段名称 流量，END结束",
        "output_desc": "每路段总流量，最后一行最大路段名",
        "sample_input": "钟楼 1200\n小寨 800\n钟楼 600\n小寨 700\nEND",
        "sample_output": "钟楼: 1800\n小寨: 1500\n钟楼",
        "standard_answer": "# 实验10：交通调查数据预处理（综合）\n# 核心知识点：字典统计、get()方法、max(key=)\nflow = {}\nwhile True:\n    line = input().strip()\n    if line == 'END':\n        break\n    name, val = line.split()\n    flow[name] = flow.get(name, 0) + int(val)\n\nfor name, total in flow.items():\n    print(f'{name}: {total}')\n\nmax_name = max(flow, key=flow.get)\nprint(max_name)",
        "test_cases": [
            ("钟楼 1200\n小寨 800\n钟楼 600\n小寨 700\nEND", "钟楼: 1800\n小寨: 1500\n钟楼", True, 1.0),
            ("北站 500\n北站 400\n南站 600\nEND", "北站: 900\n南站: 600\n北站", True, 1.0),
            ("A路 300\nB路 200\nA路 100\nC路 400\nEND", "A路: 400\nB路: 200\nC路: 400\nA路", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第6单元 异常与数据处理（理论6 -> 实验11-12）
    # 理论：多行输入、异常处理
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 11,
        "title": "实验11：交通调查数据处理",
        "difficulty": "medium",
        "tags": "循环,字符串处理,列表",
        "description": """# 实验11：交通调查数据处理

**对应理论课：** 多行数据输入、字符串分割

## 背景
交通检测器生成流量数据记录，每条记录包含路段名和车流量，需读取全部数据并分析。

## 题目
编写程序，读取多行输入（直到遇到 `END` 结束），每行格式为：`路段名称,车流量`

统计并输出：
1. 总车流量
2. 平均车流量（保留1位小数）
3. 车流量最大的路段名称

> 提示：用 `while True` + `break` 读取不定行数，用 `split(',')` 分割数据。

## 输入格式
多行，每行格式：路段名称,车流量，最后一行是 END

## 输出格式
第一行：总车流量
第二行：平均车流量
第三行：车流量最大的路段名称

## 示例
输入：
```
长安街,1200
二环路,1800
三环路,1500
END
```
输出：
```
4500
1500.0
二环路
```""",
        "input_desc": "多行输入，格式：路段名称,车流量，以END结束",
        "output_desc": "三行：总和、平均值、最大流量路段名",
        "sample_input": "长安街,1200\n二环路,1800\n三环路,1500\nEND",
        "sample_output": "4500\n1500.0\n二环路",
        "standard_answer": "# 实验11：交通调查数据处理\n# 核心知识点：while True/break、split()分割、max()函数\ndata = []\nwhile True:\n    line = input().strip()\n    if line == 'END':\n        break\n    name, count = line.split(',')\n    data.append((name, int(count)))\n\ntotal = sum(c for _, c in data)\navg = total / len(data)\nmax_road = max(data, key=lambda x: x[1])[0]\n\nprint(total)\nprint(avg)\nprint(max_road)",
        "test_cases": [
            ("长安街,1200\n二环路,1800\n三环路,1500\nEND", "4500\n1500.0\n二环路", True, 1.0),
            ("解放路,800\n建设路,600\nEND", "1400\n700.0\n解放路", True, 1.0),
            ("高速路,3000\n快速路,2500\n主干道,1800\nEND", "7300\n2433.3\n高速路", False, 1.0),
        ]
    },
    {
        "order": 12,
        "title": "实验12：交通数据异常检测（异常处理）",
        "difficulty": "medium",
        "tags": "异常处理,try-except",
        "description": """# 实验12：交通数据异常检测（异常处理）

**对应理论课：** 异常处理 try/except

## 背景
交通传感器有时会传回异常数据（如空值、字母、符号等非数字数据），需要编写程序来过滤。

## 题目
输入 N 个数据，每个数据可能是有效的数字，也可能是无效数据。

对每个数据：
- 如果是有效整数，累加到总和
- 如果是无效数据（无法转换为整数），忽略并记录错误次数

最后输出：有效数据总和、错误数据个数。

> 提示：用 `try: int(val)` 尝试转换，捕获 `ValueError` 处理无效数据。

## 输入格式
第一行：N（整数）
接下来 N 行：每行一个字符串

## 输出格式
第一行：有效数据总和
第二行：错误数据个数

## 示例
输入：
```
5
100
abc
200
-50
3.14
```
输出：
```
250
2
```""",
        "input_desc": "第一行N，接下来N行每行一个字符串",
        "output_desc": "第一行有效总和，第二行错误个数",
        "sample_input": "5\n100\nabc\n200\n-50\n3.14",
        "sample_output": "250\n2",
        "standard_answer": "# 实验12：交通数据异常检测（异常处理）\n# 核心知识点：try/except异常捕获、ValueError\nN = int(input())\ntotal = 0\nerrors = 0\nfor i in range(N):\n    val = input().strip()\n    try:\n        total += int(val)\n    except ValueError:\n        errors += 1\nprint(total)\nprint(errors)",
        "test_cases": [
            ("3\n100\n200\n300", "600\n0", True, 1.0),
            ("4\n50\nxx\n70\nyy", "120\n2", True, 1.0),
            ("2\nabc\ndef", "0\n2", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第7单元 面向对象（理论7 -> 实验13-14）
    # 理论：类与对象、排序
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 13,
        "title": "实验13：交通工具类设计（面向对象）",
        "difficulty": "medium",
        "tags": "面向对象,类,继承",
        "description": """# 实验13：交通工具类设计（面向对象）

**对应理论课：** 类与对象、继承

## 背景
使用面向对象的思想来管理不同类型的交通工具，包括轨道交通车辆。

## 题目
定义一个基类 `Vehicle`，属性：名称(name)、速度(km/h)、载客量(capacity)。
方法：`info()` 返回描述字符串。

再定义两个子类：
- `Bus`：额外属性 route（线路号）
- `Train`：额外属性 line（线路名，如"2号线"）

> 提示：子类用 `super().__init__()` 调用父类的构造方法。

## 输入格式
第一行：类型(Bus/Train) 名称 速度 载客量
第二行：如果是Bus则输入线路号；如果是Train则输入线路名

## 输出格式
info() 输出的字符串

## 示例
输入：
```
Bus 公交车 40 60
K1
```
输出：
```
公交车: 速度40km/h, 载客60人, 线路K1
```""",
        "input_desc": "第一行：类型 名称 速度 载客量；第二行：线路信息",
        "output_desc": "info()输出的字符串",
        "sample_input": "Bus 公交车 40 60\nK1",
        "sample_output": "公交车: 速度40km/h, 载客60人, 线路K1",
        "standard_answer": "# 实验13：交通工具类设计（面向对象）\n# 核心知识点：class、__init__、super()继承\nclass Vehicle:\n    def __init__(self, name, speed, capacity):\n        self.name = name\n        self.speed = speed\n        self.capacity = capacity\n    def info(self):\n        return f'{self.name}: 速度{self.speed}km/h, 载客{self.capacity}人'\n\nclass Bus(Vehicle):\n    def __init__(self, name, speed, capacity, route):\n        super().__init__(name, speed, capacity)\n        self.route = route\n    def info(self):\n        return f'{self.name}: 速度{self.speed}km/h, 载客{self.capacity}人, 线路{self.route}'\n\nclass Train(Vehicle):\n    def __init__(self, name, speed, capacity, line):\n        super().__init__(name, speed, capacity)\n        self.line = line\n    def info(self):\n        return f'{self.name}: 速度{self.speed}km/h, 载客{self.capacity}人, {self.line}'\n\nparts = input().split()\ntype_name = parts[0]\nname = parts[1]\nspeed = int(parts[2])\ncapacity = int(parts[3])\n\nif type_name == 'Bus':\n    route = input().strip()\n    v = Bus(name, speed, capacity, route)\nelse:\n    line = input().strip()\n    v = Train(name, speed, capacity, line)\n\nprint(v.info())",
        "test_cases": [
            ("Bus 公交车 40 60\nK1", "公交车: 速度40km/h, 载客60人, 线路K1", True, 1.0),
            ("Train 高铁 300 1200\n2号线", "高铁: 速度300km/h, 载客1200人, 2号线", True, 1.0),
            ("Bus 校车 30 40\nX01", "校车: 速度30km/h, 载客40人, 线路X01", False, 1.0),
        ]
    },
    {
        "order": 14,
        "title": "实验14：车辆速度与拥堵分析（排序+统计）",
        "difficulty": "medium",
        "tags": "排序,统计,列表",
        "description": """# 实验14：车辆速度与拥堵分析（排序+统计）

**对应理论课：** 排序与统计综合应用

## 背景
交通调查记录了多辆车的通过速度，需要排序并分析拥堵情况。

## 题目
第一行输入一个正整数 N，表示车辆数。
接下来 N 行，每行格式：车牌号 速度（整数）

要求：
1. 按速度从高到低排序输出：车牌号 速度
2. 输出速度低于40 km/h的车辆数（即拥堵车辆）

> 提示：用列表存储(车牌,速度)，`sort(key=lambda x: x[1], reverse=True)` 降序排序。

## 输入格式
第一行：N（正整数）
接下来 N 行：每行 车牌号 速度

## 输出格式
前 N 行：排序结果（每行 车牌号 速度）
最后一行：低速车辆数

## 示例
输入：
```
4
陕A001 65
陕B002 35
陕C003 55
陕D004 30
```
输出：
```
陕A001 65
陕C003 55
陕B002 35
陕D004 30
2
```""",
        "input_desc": "第一行N，接下来N行每行 车牌 速度",
        "output_desc": "降序输出每行 车牌号 速度，最后一行低速车辆数",
        "sample_input": "4\n陕A001 65\n陕B002 35\n陕C003 55\n陕D004 30",
        "sample_output": "陕A001 65\n陕C003 55\n陕B002 35\n陕D004 30\n2",
        "standard_answer": "# 实验14：车辆速度与拥堵分析（排序+统计）\n# 核心知识点：sort()排序、lambda表达式\nN = int(input())\ncars = []\nfor i in range(N):\n    plate, speed = input().split()\n    cars.append((plate, int(speed)))\n\ncars.sort(key=lambda x: x[1], reverse=True)\n\nslow_count = 0\nfor plate, speed in cars:\n    print(plate, speed)\n    if speed < 40:\n        slow_count += 1\n\nprint(slow_count)",
        "test_cases": [
            ("3\n陕A1 50\n陕B2 60\n陕C3 30", "陕B2 60\n陕A1 50\n陕C3 30\n1", True, 1.0),
            ("2\n沪A01 100\n京A02 25", "沪A01 100\n京A02 25\n1", True, 1.0),
            ("2\n陕K01 75\n陕K02 80", "陕K02 80\n陕K01 75\n0", False, 1.0),
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    # 第8单元 综合应用（理论8 -> 实验15-16）
    # 理论：集合、综合复习
    # ═══════════════════════════════════════════════════════════════
    {
        "order": 15,
        "title": "实验15：公交线路换乘查询（集合）",
        "difficulty": "hard",
        "tags": "集合,查找,交集",
        "description": """# 实验15：公交线路换乘查询（集合）

**对应理论课：** 集合（set）的概念与运算

## 背景
某城市有3条公交线路，需要查询两站之间是否需要换乘。

## 题目
三条线路站点如下：
```
1路: A B C D E
2路: F C G H
3路: I J K D G
```
输入两个站点名称，判断：
- 如果在同一条线路上 -> 输出线路号
- 如果不在同一条线路上，但可通过一个换乘站到达 -> 输出 "换乘一次"
- 否则 -> 输出 "无法到达"

> 提示：用集合 `set` 存储站点，用 `&` 求交集判断是否有共同换乘站。

## 输入格式
一行两个站点名，用空格隔开

## 输出格式
线路号 / "换乘一次" / "无法到达"

## 示例
输入：
```
A D
```
输出：
```
1
```""",
        "input_desc": "一行两个站点名，空格隔开",
        "output_desc": "线路号 / 换乘一次 / 无法到达",
        "sample_input": "A D",
        "sample_output": "1",
        "standard_answer": "# 实验15：公交线路换乘查询（集合）\n# 核心知识点：集合set、交集&、综合逻辑判断\nlines = {\n    1: {'A', 'B', 'C', 'D', 'E'},\n    2: {'F', 'C', 'G', 'H'},\n    3: {'I', 'J', 'K', 'D', 'G'}\n}\n\ns1, s2 = input().split()\n\nline_of_s1 = [ln for ln, stops in lines.items() if s1 in stops]\nline_of_s2 = [ln for ln, stops in lines.items() if s2 in stops]\n\ncommon = set(line_of_s1) & set(line_of_s2)\nif common:\n    print(min(common))\n    exit()\n\nfor ln1 in line_of_s1:\n    for ln2 in line_of_s2:\n        if lines[ln1] & lines[ln2]:\n            print('换乘一次')\n            exit()\n\nprint('无法到达')",
        "test_cases": [
            ("A D", "1", True, 1.0),
            ("A F", "换乘一次", True, 1.0),
            ("A I", "无法到达", True, 1.0),
            ("D G", "换乘一次", False, 1.0),
        ]
    },
    {
        "order": 16,
        "title": "实验16：综合实验——交通数据分析报告",
        "difficulty": "hard",
        "tags": "综合,字典,列表,统计",
        "description": """# 实验16：综合实验——交通数据分析报告

**对应理论课：** 课程综合应用（期末项目）

## 背景
这是一个综合实验，要求你处理一份完整的交通调查数据，生成分析报告。综合运用本学期学过的列表、字典、循环、条件判断等知识。

## 题目
输入多个路口的交通数据，每行格式：`路口名称 方向 车流量 平均速度`
以 `END` 结束。

要求：
1. 统计每个路口的总车流量，输出格式：`路口名称: 总车流量`
2. 找出车流量最大的路口
3. 计算所有路口的平均车速（保留1位小数）
4. 输出车速低于40km/h的路口名称（去重，按输入顺序，用逗号隔开，如没有则输出"无"）

> 提示：用字典统计各路口总流量，用列表记录低速路口并去重。

## 输入格式
多行，每行：路口名称 方向 车流量 平均速度，以 END 结束

## 输出格式
第一行开始：每个路口的总车流量（每行一个）
接着一行：车流量最大的路口名称
接着一行：平均车速（保留1位小数）
接着一行：低速路口（逗号隔开）或"无"

## 示例
输入：
```
钟楼 东 500 45
钟楼 西 600 38
小寨 南 800 35
小寨 北 700 42
END
```
输出：
```
钟楼: 1100
小寨: 1500
小寨
40.0
钟楼,小寨
```""",
        "input_desc": "多行：路口 方向 车流量 速度，END结束",
        "output_desc": "见示例格式",
        "sample_input": "钟楼 东 500 45\n钟楼 西 600 38\n小寨 南 800 35\n小寨 北 700 42\nEND",
        "sample_output": "钟楼: 1100\n小寨: 1500\n小寨\n40.0\n钟楼,小寨",
        "standard_answer": "# 实验16：综合实验——交通数据分析报告\n# 核心知识点：字典统计、max(key=)、列表去重、综合应用\n# 综合运用：循环、字典、列表、字符串、条件判断\ndata = []\nwhile True:\n    line = input().strip()\n    if line == 'END':\n        break\n    parts = line.split()\n    name, direction, volume, speed = parts[0], parts[1], int(parts[2]), int(parts[3])\n    data.append((name, direction, volume, speed))\n\nflow = {}\nspeeds = []\nlow_speed_roads = []\nfor name, direction, volume, speed in data:\n    flow[name] = flow.get(name, 0) + volume\n    speeds.append(speed)\n    if speed < 40 and name not in low_speed_roads:\n        low_speed_roads.append(name)\n\nfor name, total in flow.items():\n    print(f'{name}: {total}')\n\nmax_road = max(flow, key=flow.get)\nprint(max_road)\n\navg_speed = sum(speeds) / len(speeds)\nprint(avg_speed)\n\nif low_speed_roads:\n    print(','.join(low_speed_roads))\nelse:\n    print('无')",
        "test_cases": [
            ("钟楼 东 500 45\n钟楼 西 600 38\n小寨 南 800 35\n小寨 北 700 42\nEND", "钟楼: 1100\n小寨: 1500\n小寨\n40.0\n钟楼,小寨", True, 1.0),
            ("北站 南 300 50\n北站 北 400 55\nEND", "北站: 700\n北站\n52.5\n无", True, 1.0),
            ("路口A 东 100 30\n路口B 西 200 25\nEND", "路口A: 100\n路口B: 200\n路口B\n27.5\n路口A,路口B", False, 1.0),
        ]
    },
]


def seed():
    app = create_app()
    with app.app_context():
        teacher = User.query.filter_by(role='teacher').first()
        if not teacher:
            print('错误：请先创建教师账号 (python create_admin.py)')
            return

        print(f'使用教师账号: {teacher.username}')

        existing = Problem.query.filter(Problem.experiment_order > 0).all()
        for p in existing:
            db.session.delete(p)
        db.session.commit()
        print('已清空旧实验数据')

        for exp in EXPERIMENTS:
            problem = Problem(
                title=exp['title'],
                description=exp['description'],
                input_description=exp['input_desc'],
                output_description=exp['output_desc'],
                sample_input=exp['sample_input'],
                sample_output=exp['sample_output'],
                standard_answer=exp['standard_answer'],
                experiment_order=exp['order'],
                difficulty=exp['difficulty'],
                tags=exp['tags'],
                visible=True,
                created_by=teacher.id,
            )
            db.session.add(problem)
            db.session.flush()

            for input_data, expected, is_public, weight in exp['test_cases']:
                tc = TestCase(
                    problem_id=problem.id,
                    input_data=input_data,
                    expected_output=expected,
                    is_public=is_public,
                    score_weight=weight,
                    sort_order=1,
                )
                db.session.add(tc)

            print(f'  [{exp["order"]:2d}] {exp["title"]}')

        db.session.commit()
        print(f'\n全部 {len(EXPERIMENTS)} 道实验题已导入完成！')


if __name__ == '__main__':
    seed()
