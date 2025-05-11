import numpy as np

def catmull_rom_spline(points, num_points=20, tensions=0.5):
    """
    支持分段张力的Catmull-Rom样条曲线
    points: 控制点列表
    num_points: 每段插值点数
    tensions: float或list，每段的张力参数
    """
    if len(points) < 2:
        return points
    points = [tuple(map(float, p)) for p in points]
    pts = [points[0]] + list(points) + [points[-1]]
    n_seg = len(points) - 1
    # 统一tensions为list
    if isinstance(tensions, (float, int)):
        tensions = [tensions] * n_seg
    curve = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        alpha = tensions[i-1] if i-1 < len(tensions) else 0.5
        for t in np.linspace(0, 1, num_points, endpoint=False):
            t2 = t * t
            t3 = t2 * t
            # Catmull-Rom标准公式，带张力参数
            # 张力影响插值的"紧致度"，这里用常规公式，alpha可用于后续扩展
            x = 0.5 * ((2 * p1[0]) +
                       (-p0[0] + p2[0]) * t +
                       (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) +
                       (-p0[1] + p2[1]) * t +
                       (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3)
            curve.append((x, y))
    curve.append(points[-1])
    return curve

def distance(point1, point2):
    """计算两点之间的欧氏距离"""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_nearest_point(point, points, threshold=10):
    """
    找到距离给定点最近的控制点
    
    参数:
        point: 目标点 (x,y)
        points: 控制点列表
        threshold: 最大距离阈值
    
    返回:
        最近点的索引，如果没有点满足阈值则返回None
    """
    min_dist = float('inf')
    nearest_idx = None
    
    for i, p in enumerate(points):
        dist = distance(point, p)
        if dist < min_dist and dist < threshold:
            min_dist = dist
            nearest_idx = i
    
    return nearest_idx 