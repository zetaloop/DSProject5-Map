# city_graph.py

from typing import Dict, List, Tuple
import heapq


def get_cities() -> Dict[str, Tuple[int, int]]:
    """
    返回城市与其在画布上坐标的映射。
    这里 (x, y) 是在 Tkinter Canvas 中使用的像素坐标。
    """
    return {
        "北京": (500, 100),
        "西安": (400, 220),
        "武汉": (530, 250),
        "上海": (650, 150),
        "杭州": (620, 230),
        "广州": (500, 400),
        "深圳": (550, 450),
        "成都": (300, 300),
    }


def get_graph() -> Dict[str, Dict[str, int]]:
    """
    返回城市间的铁路连接和距离（加权）信息。
    graph[A][B] = 距离
    """
    return {
        "北京": {"西安": 1200, "上海": 1200, "武汉": 1200},
        "西安": {"北京": 1200, "成都": 700, "武汉": 600},
        "成都": {"西安": 700, "武汉": 1100},
        "武汉": {
            "北京": 1200,
            "西安": 600,
            "成都": 1100,
            "广州": 1000,
            "杭州": 800,
            "上海": 800,
        },
        "上海": {"北京": 1200, "武汉": 800, "杭州": 200},
        "杭州": {"上海": 200, "武汉": 800, "广州": 1200},
        "广州": {"武汉": 1000, "杭州": 1200, "深圳": 150},
        "深圳": {"广州": 150},
    }


def dijkstra(
    graph: Dict[str, Dict[str, int]], start: str, end: str
) -> Tuple[float, List[str], List[Tuple[str, str, str]]]:
    """
    使用 Dijkstra 算法查找从 start 到 end 的最短路径。
    返回 (最短距离, 路径, 动画步骤列表)

    动画步骤列表 steps 中，每个元素是一个三元组 (event_type, node/edge, info)
    其中:
    - event_type 可以是 "visit_node" 或 "visit_edge" 或 "path_found"
    - node/edge 表示操作的目标: 对于 "visit_node" 是节点名，对于 "visit_edge" 是 (nodeA, nodeB)
    - info 可以是一些附加信息，这里暂时可不使用，或者在 "path_found" 步骤里带上最终路径
    """
    # 距离表，前驱表
    distances = {city: float("inf") for city in graph}
    previous = {city: None for city in graph}
    distances[start] = 0

    # 最小堆
    pq = [(0, start)]

    # 动画步骤
    steps = []

    visited = set()

    while pq:
        current_dist, current_city = heapq.heappop(pq)

        if current_city in visited:
            continue

        # 标记访问节点
        steps.append(("visit_node", current_city, ""))

        visited.add(current_city)
        if current_city == end:
            # 找到目标
            break

        for neighbor, distance in graph[current_city].items():
            if neighbor in visited:
                continue

            new_dist = current_dist + distance
            # 标记访问边
            steps.append(("visit_edge", (current_city, neighbor), ""))

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_city
                heapq.heappush(pq, (new_dist, neighbor))

    # 回溯路径
    path = []
    if distances[end] < float("inf"):
        node = end
        while node is not None:
            path.insert(0, node)
            node = previous[node]

    # 在动画步骤中加一个 path_found 的记录
    steps.append(("path_found", end, {"path": path, "distance": distances[end]}))

    return distances[end], path, steps
