from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
import numpy as np
from utils import catmull_rom_spline, find_nearest_point
import sys

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []
        self.selected_point = None
        self.is_dragging = False
        self.drag_mode = None  # 'vertex' or 'segment'
        self.drag_segment_idx = None
        self.setMinimumSize(800, 600)
        self.points_changed_callback = None
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 绘制曲线
        if len(self.points) >= 2:
            curve_points = catmull_rom_spline(self.points)
            path = QPainterPath()
            path.moveTo(*curve_points[0])
            for point in curve_points[1:]:
                path.lineTo(*point)
            pen = QPen(QColor("#2196F3"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawPath(path)
        # 绘制控制点
        for i, point in enumerate(self.points):
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#FF5722" if i == self.selected_point else "#4CAF50"))
            painter.drawEllipse(QPointF(*point), 5, 5)
    
    def mousePressEvent(self, event):
        pos = event.position()
        point = (pos.x(), pos.y())
        if event.button() == Qt.MouseButton.LeftButton:
            # 左键：只在空白处添加顶点
            idx = find_nearest_point(point, self.points)
            if idx is None:
                self.points.append(point)
                self.selected_point = len(self.points) - 1
                self.update()
                if self.points_changed_callback:
                    self.points_changed_callback()
        elif event.button() == Qt.MouseButton.RightButton:
            # 右键：拖动顶点或线段
            idx = find_nearest_point(point, self.points)
            if idx is not None:
                self.selected_point = idx
                self.is_dragging = True
                self.drag_mode = 'vertex'
            else:
                # 检查是否在某条曲线段附近
                seg_idx = self.find_nearest_segment(point)
                if seg_idx is not None:
                    # 在线段上插入新顶点并拖动
                    insert_idx = seg_idx + 1
                    self.points.insert(insert_idx, point)
                    self.selected_point = insert_idx
                    self.is_dragging = True
                    self.drag_mode = 'segment'
                    self.update()
                    if self.points_changed_callback:
                        self.points_changed_callback()
    
    def mouseMoveEvent(self, event):
        if self.is_dragging and self.selected_point is not None:
            pos = event.position()
            self.points[self.selected_point] = (pos.x(), pos.y())
            self.update()
    
    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        self.drag_mode = None
        self.drag_segment_idx = None
    
    def find_nearest_segment(self, point, threshold=10):
        # 返回距离最近的线段索引（第i段为points[i]到points[i+1]），否则None
        min_dist = float('inf')
        nearest_idx = None
        for i in range(len(self.points) - 1):
            p1 = np.array(self.points[i])
            p2 = np.array(self.points[i+1])
            proj = self.project_point_to_segment(np.array(point), p1, p2)
            dist = np.linalg.norm(proj - np.array(point))
            if dist < min_dist and dist < threshold:
                min_dist = dist
                nearest_idx = i
        return nearest_idx
    
    @staticmethod
    def project_point_to_segment(p, a, b):
        # 投影点p到线段ab上
        ab = b - a
        t = np.dot(p - a, ab) / (np.dot(ab, ab) + 1e-8)
        t = np.clip(t, 0, 1)
        return a + t * ab
    
    def clear_points(self):
        self.points = []
        self.selected_point = None
        self.is_dragging = False
        self.drag_mode = None
        self.drag_segment_idx = None
        self.update()
        if self.points_changed_callback:
            self.points_changed_callback()

class CurveEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CURVEEDIT - 交互式曲线编辑器")
        self.setMinimumSize(1200, 800)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        self.canvas = Canvas()
        layout.addWidget(self.canvas)
        control_panel = QWidget()
        self.control_layout = QVBoxLayout(control_panel)
        control_panel.setFixedWidth(300)
        self.control_layout.addWidget(QLabel("控制面板"))
        self.clear_button = QPushButton("清除所有点")
        self.clear_button.clicked.connect(self.clear_all)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        self.control_layout.addWidget(self.clear_button)
        layout.addWidget(control_panel)
        self.canvas.points_changed_callback = self.update_panel

    def clear_all(self):
        self.canvas.clear_points()
        self.update_panel()

    def update_panel(self):
        pass  # 目前只保留清除按钮，无需动态内容

    def run(self):
        self.show()

def main():
    app = QApplication(sys.argv)
    editor = CurveEditor()
    editor.run()
    sys.exit(app.exec())
