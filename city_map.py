import tkinter as tk
from typing import Dict, Tuple, List


class CityMap(tk.Canvas):
    """
    用于在 Tkinter Canvas 上显示城市和铁路连接。
    提供绘制、标记高亮等方法。
    """

    def __init__(self, master=None, width=800, height=600):
        super().__init__(
            master, width=width, height=height, bg="white", highlightthickness=0
        )
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 记录城市对应的图形对象ID，以方便后续高亮
        self.city_nodes = {}
        # 记录边对应的图形对象ID
        # 由于边是无向的，可将 (cityA, cityB) 和 (cityB, cityA) 视为同一条边
        # 这里用 frozenset({cityA, cityB}) 作为 key
        self.edges = {}

    def draw_map(
        self, cities: Dict[str, Tuple[int, int]], graph: Dict[str, Dict[str, int]]
    ):
        """
        绘制所有城市和连线。
        """
        self.delete("all")  # 清空画布
        self.city_nodes.clear()
        self.edges.clear()

        # 先画边
        for cityA, neighbors in graph.items():
            (xA, yA) = cities[cityA]
            for cityB, dist in neighbors.items():
                (xB, yB) = cities[cityB]
                edge_key = frozenset({cityA, cityB})
                # 避免重复绘制同一条边
                if edge_key not in self.edges:
                    line_id = self.create_line(xA, yA, xB, yB, fill="#888", width=1)
                    # 在边的中点显示距离
                    mid_x, mid_y = (xA + xB) / 2, (yA + yB) / 2
                    dist_text = self.create_text(
                        mid_x, mid_y, text=str(dist), fill="#555", font=("等线", 8)
                    )
                    self.edges[edge_key] = (line_id, dist_text)

        # 再画城市节点
        for city, (x, y) in cities.items():
            r = 6  # 圆形半径变小 (原来是10)
            node_id = self.create_oval(
                x - r, y - r, x + r, y + r, fill="white", outline="black", width=1
            )
            text_id = self.create_text(
                x,
                y - 15,  # 标签位置略微上移
                text=city,
                fill="black",
                font=("等线", 8, "bold"),  # 字体变小
            )
            self.city_nodes[city] = (node_id, text_id)

    def highlight_node(self, city: str, color: str = "yellow"):
        """
        高亮某个城市节点。
        """
        if city in self.city_nodes:
            node_id, text_id = self.city_nodes[city]
            self.itemconfig(node_id, fill=color)

    def highlight_edge(self, cityA: str, cityB: str, color: str = "red"):
        """
        高亮某条边。
        """
        edge_key = frozenset({cityA, cityB})
        if edge_key in self.edges:
            line_id, dist_text_id = self.edges[edge_key]
            self.itemconfig(line_id, fill=color, width=2)

    def highlight_path(self, path: List[str], color: str = "blue"):
        """
        按照路径列表依次高亮边和节点。
        """
        for i in range(len(path) - 1):
            cityA = path[i]
            cityB = path[i + 1]
            self.highlight_edge(cityA, cityB, color=color)
        # 同时高亮节点
        for city in path:
            self.highlight_node(city, color=color)

    def reset_map(
        self, cities: Dict[str, Tuple[int, int]], graph: Dict[str, Dict[str, int]]
    ):
        """
        重置所有节点、边的颜色。
        """
        # 重绘即可
        self.draw_map(cities, graph)
