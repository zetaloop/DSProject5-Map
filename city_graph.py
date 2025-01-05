# city_graph.py

from typing import Dict, List, Tuple
import heapq


def get_cities() -> Dict[str, Tuple[int, int]]:
    """
    返回城市与其在画布上坐标的映射。
    坐标根据实际地理位置进行了简化映射。
    """
    return {
        "北京": (400, 150),
        "天津": (430, 170),
        "西安": (300, 320),
        "武汉": (430, 350),
        "上海": (550, 300),
        "杭州": (520, 330),
        "南京": (480, 280),
        "广州": (400, 500),
        "深圳": (420, 530),
        "成都": (200, 400),
        "重庆": (250, 380),
        "长沙": (400, 400),
        "郑州": (380, 280),
        "济南": (420, 200),
        "合肥": (450, 300),
        "南昌": (450, 380),
        "福州": (500, 420),
        "厦门": (480, 450),
        "昆明": (200, 480),
        "贵阳": (280, 440),
        "哈尔滨": (500, 50),
        "长春": (480, 80),
        "沈阳": (460, 120),
    }


def get_graph() -> Dict[str, Dict[str, int]]:
    """
    返回城市间的铁路连接和距离（加权）信息。
    距离单位：公里
    """
    return {
        "北京": {"天津": 120, "西安": 1200, "济南": 400, "沈阳": 700},
        "天津": {"北京": 120, "济南": 300, "沈阳": 600},
        "西安": {"北京": 1200, "成都": 700, "武汉": 800, "郑州": 500, "重庆": 700},
        "成都": {"西安": 700, "重庆": 300, "昆明": 600, "贵阳": 700},
        "重庆": {"成都": 300, "西安": 700, "贵阳": 400, "长沙": 900},
        "武汉": {"西安": 800, "郑州": 500, "长沙": 350, "南昌": 400, "合肥": 400},
        "郑州": {"西安": 500, "武汉": 500, "济南": 400, "合肥": 500},
        "济南": {"北京": 400, "天津": 300, "郑州": 400, "合肥": 600},
        "上海": {"南京": 300, "杭州": 200, "合肥": 400},
        "南京": {"上海": 300, "合肥": 300, "杭州": 300},
        "杭州": {"上海": 200, "南京": 300, "南昌": 500, "福州": 600},
        "合肥": {"南京": 300, "上海": 400, "武汉": 400, "郑州": 500, "济南": 600},
        "长沙": {"武汉": 350, "南昌": 400, "广州": 600, "贵阳": 600, "重庆": 900},
        "南昌": {"武汉": 400, "长沙": 400, "杭州": 500, "福州": 600},
        "广州": {"长沙": 600, "深圳": 150, "南昌": 800, "贵阳": 800},
        "深圳": {"广州": 150, "厦门": 500},
        "福州": {"杭州": 600, "南昌": 600, "厦门": 300},
        "厦门": {"福州": 300, "深圳": 500},
        "昆明": {"成都": 600, "贵阳": 400},
        "贵阳": {"昆明": 400, "成都": 700, "重庆": 400, "长沙": 600, "广州": 800},
        "哈尔滨": {"长春": 300},
        "长春": {"哈尔滨": 300, "沈阳": 300},
        "沈阳": {"长春": 300, "北京": 700, "天津": 600},
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
