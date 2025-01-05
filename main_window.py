import tkinter as tk
import sv_ttk
import darkdetect
from tkinter import ttk, messagebox
from typing import Dict, Tuple
from city_graph import get_cities, get_graph, dijkstra
from city_map import CityMap


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("铁路最短路径查找系统")
        self.geometry("1000x600")

        # 根据系统暗/亮模式使用 sv-ttk 主题
        if darkdetect.isDark():
            sv_ttk.use_dark_theme()
        else:
            sv_ttk.use_light_theme()

        # 数据
        self.cities = get_cities()
        self.graph = get_graph()

        # 左边：地图画布
        self.city_map = CityMap(self, width=700, height=600)
        self.city_map.draw_map(self.cities, self.graph)

        # 右边：控制面板
        self.control_frame = ttk.Frame(self, padding=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # 出发城市、目标城市下拉框
        city_names = list(self.cities.keys())
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        ttk.Label(self.control_frame, text="出发城市").pack(pady=5)
        self.start_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.start_var,
            values=city_names,
            state="readonly",
        )
        self.start_combo.pack(pady=5)

        ttk.Label(self.control_frame, text="目的城市").pack(pady=5)
        self.end_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.end_var,
            values=city_names,
            state="readonly",
        )
        self.end_combo.pack(pady=5)

        # 查询按钮
        self.search_button = ttk.Button(
            self.control_frame, text="开始搜索", command=self.search_path
        )
        self.search_button.pack(pady=10)

        # 重置按钮
        self.reset_button = ttk.Button(
            self.control_frame, text="重置", command=self.reset_map
        )
        self.reset_button.pack(pady=10)

        # 显示结果
        self.result_label = ttk.Label(
            self.control_frame, text="最短距离： - \n最短路径： -", wraplength=200
        )
        self.result_label.pack(pady=10)

        # 动画步骤列表以及当前步骤索引
        self.steps = []
        self.current_step_index = 0

    def search_path(self):
        start_city = self.start_var.get()
        end_city = self.end_var.get()

        if not start_city or not end_city:
            messagebox.showwarning("提示", "请选择出发城市和目的城市")
            return
        if start_city == end_city:
            messagebox.showinfo("提示", "出发城市与目的城市相同")
            return

        distance, path, steps = dijkstra(self.graph, start_city, end_city)
        if distance == float("inf"):
            self.result_label.configure(text="无可达路径")
            return

        # 展示距离和路径
        self.result_label.configure(
            text=f"最短距离：{distance}\n最短路径：{' -> '.join(path)}"
        )

        # 准备可视化动画
        self.steps = steps
        self.current_step_index = 0

        # 禁用搜索按钮，防止重复点击
        self.search_button.config(state=tk.DISABLED)
        # 开始执行动画
        self.animate_steps()

    def animate_steps(self):
        """
        逐步显示搜索过程。
        steps 中的每个元素: (event_type, data, info)
        """
        if self.current_step_index >= len(self.steps):
            # 动画结束，启用搜索按钮
            self.search_button.config(state=tk.NORMAL)
            return

        event_type, data, info = self.steps[self.current_step_index]
        self.current_step_index += 1

        if event_type == "visit_node":
            # 高亮节点
            city = data
            self.city_map.highlight_node(city, color="yellow")

        elif event_type == "visit_edge":
            # 高亮边
            cityA, cityB = data
            self.city_map.highlight_edge(cityA, cityB, color="red")

        elif event_type == "path_found":
            # 查找结束，显示最终路径
            path = info["path"]
            distance = info["distance"]
            # 高亮整条路径
            self.city_map.highlight_path(path, color="blue")

        # 间隔一定时间后播放下一步
        self.after(500, self.animate_steps)

    def reset_map(self):
        """
        重置地图颜色、文本信息。
        """
        self.city_map.reset_map(self.cities, self.graph)
        self.result_label.configure(text="最短距离： - \n最短路径： -")
        self.steps = []
        self.current_step_index = 0
        self.search_button.config(state=tk.NORMAL)
