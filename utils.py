import numpy as np

def catmull_rom_spline(points, num_points=20, alpha=0.5):
    """
    Catmull-Rom样条曲线生成器
    
    数学原理：
    1. 每段曲线由4个控制点决定：P0, P1, P2, P3
    2. P1和P2是当前段的端点，P0和P3用于计算切线方向
    3. 曲线方程：P(t) = 0.5 * (2P1 + (-P0 + P2)t + (2P0 - 5P1 + 4P2 - P3)t² + (-P0 + 3P1 - 3P2 + P3)t³)
    4. t ∈ [0,1] 是插值参数
    
    参数:
        points: 控制点列表 [(x1,y1), (x2,y2), ...]
        num_points: 每段曲线的插值点数
        alpha: 张力参数 (0.0-1.0)，影响曲线的"紧致度"
    
    返回:
        曲线点列表 [(x1,y1), (x2,y2), ...]
    """
    if len(points) < 2:
        return points

    # 确保输入点为浮点数
    points = [tuple(map(float, p)) for p in points]
    
    # 添加首尾点以处理边界
    # 对于首段：复制第一个点作为P0
    # 对于尾段：复制最后一个点作为P3
    pts = [points[0]] + list(points) + [points[-1]]
    
    curve = []
    # 对每段曲线进行插值
    for i in range(1, len(pts) - 2):
        # 获取当前段的四个控制点
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        
        # 在[0,1]范围内生成均匀分布的参数t
        for t in np.linspace(0, 1, num_points, endpoint=False):
            # 计算t的幂
            t2 = t * t  # t²
            t3 = t2 * t  # t³
            
            # Catmull-Rom矩阵系数
            # 第一行：2P1
            # 第二行：(-P0 + P2)t
            # 第三行：(2P0 - 5P1 + 4P2 - P3)t²
            # 第四行：(-P0 + 3P1 - 3P2 + P3)t³
            x = 0.5 * ((2 * p1[0]) +
                       (-p0[0] + p2[0]) * t +
                       (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3)
            
            y = 0.5 * ((2 * p1[1]) +
                       (-p0[1] + p2[1]) * t +
                       (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3)
            
            curve.append((x, y))
    
    # 添加最后一个控制点，确保曲线严格穿过所有控制点
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