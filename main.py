import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Nhập các hàm thuật toán từ các tệp riêng biệt
from euler import find_eulerian_cycle_undirected, find_eulerian_cycle_directed
from hamilton import find_hamiltonian_cycle
from tsp import tsp

# ==========================================
# PHẦN 1: LỚP ĐỒ HỌA PYQT5 (NODES & EDGES)
# ==========================================

class EdgeItem(QGraphicsLineItem):
    def __init__(self, node1, node2, weight=1, is_directed=False):
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.is_directed = is_directed
        self.setZValue(-1)
        
        # Cho phép chọn (Selectable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.update_position()

    def update_position(self):
        self.setLine(QLineF(self.node1.scenePos(), self.node2.scenePos()))

    def shape(self):
        # Mở rộng vùng tương tác của đoạn thẳng lên 15 pixel để người dùng dễ click/chọn
        path = QPainterPath()
        path.moveTo(self.line().p1())
        path.lineTo(self.line().p2())
        stroker = QPainterPathStroker()
        stroker.setWidth(15)
        return stroker.createStroke(path)

    def mouseDoubleClickEvent(self, event):
        # Click đúp để thay đổi trọng số
        new_weight, ok = QInputDialog.getInt(None, "Đổi trọng số", "Nhập khoảng cách/trọng số mới:", self.weight, 1, 1000000)
        if ok:
            self.weight = new_weight
            self.update()
        super().mouseDoubleClickEvent(event)

    def paint(self, painter, option, widget=None):
        # Xóa khung viền nét đứt mặc định khi được chọn
        option.state &= ~QStyle.State_Selected
        
        # Đổi màu thành đỏ nếu người dùng đang chọn cạnh này
        if self.isSelected():
            painter.setPen(QPen(Qt.red, 3))
        else:
            painter.setPen(QPen(Qt.gray, 2))
            
        line = self.line()
        painter.drawLine(line)
        
        if self.is_directed and line.length() > 30:
            line_arrow = QLineF(line)
            line_arrow.setLength(line_arrow.length() - 15)
            p2 = line_arrow.p2()
            
            angle = math.atan2(line_arrow.dy(), line_arrow.dx())
            arrowSize = 12
            arrowP1 = p2 - QPointF(math.cos(angle - math.pi / 6) * arrowSize,
                                   math.sin(angle - math.pi / 6) * arrowSize)
            arrowP2 = p2 - QPointF(math.cos(angle + math.pi / 6) * arrowSize,
                                   math.sin(angle + math.pi / 6) * arrowSize)
            
            if self.isSelected():
                painter.setBrush(Qt.red)
                painter.setPen(QPen(Qt.red, 1))
            else:
                painter.setBrush(Qt.gray)
                painter.setPen(QPen(Qt.gray, 1))
                
            painter.drawPolygon(QPolygonF([p2, arrowP1, arrowP2]))

        mid_x = (line.p1().x() + line.p2().x()) / 2
        mid_y = (line.p1().y() + line.p2().y()) / 2
        
        painter.setPen(Qt.darkRed)
        font = painter.font()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        
        text_rect = QRectF(mid_x - 10, mid_y - 10, 20, 20)
        painter.fillRect(text_rect, QColor(255, 255, 255, 200))
        painter.drawText(text_rect, Qt.AlignCenter, str(self.weight))


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y):
        super().__init__(-15, -15, 30, 30)
        self.node_id = node_id
        self.edge_list = list()
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(173, 216, 230))) 
        
        # Cho phép kéo thả và cho phép chọn (Selectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edge_list:
                edge.update_position()
        return super().itemChange(change, value)

    def paint(self, painter, option, widget=None):
        option.state &= ~QStyle.State_Selected
        
        # Đổi viền thành đỏ nếu người dùng đang chọn đỉnh này
        if self.isSelected():
            painter.setPen(QPen(Qt.red, 3))
        else:
            painter.setPen(QPen(Qt.black, 2))
            
        painter.setBrush(self.brush())
        painter.drawEllipse(self.boundingRect())
        
        painter.setPen(Qt.black)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, str(self.node_id))


class GraphView(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        
        self.nodes = list()
        self.edges = list()
        self.drawing_edge = False
        self.start_node = None
        self.temp_line = None

    def keyPressEvent(self, event):
        """Xóa vật thể khi nhấn Delete hoặc Backspace"""
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            selected_items = self.scene.selectedItems()
            
            # Xóa cạnh trước để tránh lỗi dữ liệu liên kết
            for item in selected_items:
                if isinstance(item, EdgeItem):
                    self.remove_edge(item)
                    
            # Xóa đỉnh sau
            for item in selected_items:
                if isinstance(item, NodeItem):
                    self.remove_node(item)
                    
            self.main_window.update_ui()
        super().keyPressEvent(event)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        if edge in edge.node1.edge_list:
            edge.node1.edge_list.remove(edge)
        if edge in edge.node2.edge_list:
            edge.node2.edge_list.remove(edge)
        if edge.scene() == self.scene:
            self.scene.removeItem(edge)

    def remove_node(self, node):
        # Hủy toàn bộ các con đường dính vào đỉnh này
        for edge in list(node.edge_list):
            self.remove_edge(edge)
            
        if node in self.nodes:
            self.nodes.remove(node)
        if node.scene() == self.scene:
            self.scene.removeItem(node)
            
        # Cập nhật lại số thứ tự cho các đỉnh còn lại
        for i, n in enumerate(self.nodes):
            n.node_id = i
            n.update()

    def mouseDoubleClickEvent(self, event):
        # Kiểm tra xem có click đúp trúng vật thể nào không
        item = self.itemAt(event.pos())
        if item:
            super().mouseDoubleClickEvent(event)
            return
            
        # Nếu click đúp vào nền trắng thì tạo đỉnh mới
        pos = self.mapToScene(event.pos())
        node = NodeItem(len(self.nodes), pos.x(), pos.y())
        self.scene.addItem(node)
        self.nodes.append(node)
        self.main_window.update_ui()
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, NodeItem) and event.button() == Qt.RightButton:
            self.drawing_edge = True
            self.start_node = item
            self.temp_line = self.scene.addLine(QLineF(item.scenePos(), self.mapToScene(event.pos())), QPen(Qt.red, 2, Qt.DashLine))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing_edge and self.temp_line:
            self.temp_line.setLine(QLineF(self.start_node.scenePos(), self.mapToScene(event.pos())))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.drawing_edge:
            self.drawing_edge = False
            if self.temp_line:
                self.scene.removeItem(self.temp_line)
                self.temp_line = None
            
            item = self.itemAt(event.pos())
            if isinstance(item, NodeItem) and item!= self.start_node:
                is_directed = (self.main_window.combo_mode.currentText() == "Có hướng (Directed)")
                
                exists = False
                for e in self.edges:
                    if e.node1 == self.start_node and e.node2 == item:
                        exists = True
                    if not is_directed and e.node2 == self.start_node and e.node1 == item:
                        exists = True
                        
                if not exists:
                    current_weight = self.main_window.spin_weight.value()
                    edge = EdgeItem(self.start_node, item, current_weight, is_directed)
                    self.scene.addItem(edge)
                    self.edges.append(edge)
                    self.start_node.add_edge(edge)
                    item.add_edge(edge)
                    self.main_window.update_ui()
        super().mouseReleaseEvent(event)

    def clear_graph(self):
        self.scene.clear()
        self.nodes.clear()
        self.edges.clear()
        self.main_window.update_ui()

# ==========================================
# PHẦN 2: GIAO DIỆN PHẦN MỀM CHÍNH
# ==========================================

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Vẽ Đồ thị Tương tác & TSP (PyQt5)")
        self.resize(1100, 650)

        main_layout = QHBoxLayout(self)

        self.view = GraphView(self)
        main_layout.addWidget(self.view, stretch=3)

        control_panel = QVBoxLayout()
        main_layout.addLayout(control_panel, stretch=1)

        lbl_guide = QLabel("HƯỚNG DẪN THAO TÁC:\n"
                           "- Tạo đỉnh: Click đúp Chuột Trái\n"
                           "- Nối cạnh: Kéo thả Chuột Phải\n"
                           "- Di chuyển: Kéo thả Chuột Trái\n"
                           "- Sửa trọng số: Click đúp Chuột Trái vào cạnh\n"
                           "- Xóa: Chọn vật thể + Nhấn phím Delete")
        lbl_guide.setStyleSheet("color: #1a5f7a; font-weight: bold; border: 1px solid #1a5f7a; padding: 5px;")
        lbl_guide.setWordWrap(True)
        control_panel.addWidget(lbl_guide)
        
        panel_weight = QHBoxLayout()
        panel_weight.addWidget(QLabel("Trọng số khi vẽ cạnh mới:"))
        self.spin_weight = QSpinBox()
        self.spin_weight.setRange(1, 1000000)
        self.spin_weight.setValue(1)
        panel_weight.addWidget(self.spin_weight)
        control_panel.addLayout(panel_weight)

        control_panel.addWidget(QLabel("Dạng cấu trúc đồ thị:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(("Vô hướng (Undirected)", "Có hướng (Directed)"))
        self.combo_mode.currentIndexChanged.connect(self.view.clear_graph)
        control_panel.addWidget(self.combo_mode)

        control_panel.addWidget(QLabel("Chọn bài toán giải quyết:"))
        self.combo_algo = QComboBox()
        self.combo_algo.addItems(("Chu trình Euler (Fleury)", "Chu trình Hamilton", "Người giao hàng (TSP)"))
        self.combo_algo.currentIndexChanged.connect(self.update_ui)
        control_panel.addWidget(self.combo_algo)

        control_panel.addWidget(QLabel("Điểm xuất phát hợp lệ:"))
        self.combo_start = QComboBox()
        control_panel.addWidget(self.combo_start)

        self.btn_solve = QPushButton("Tính Toán Lộ Trình")
        self.btn_solve.setStyleSheet("background-color: #2b7a78; color: white; font-weight: bold; padding: 10px; border-radius: 4px;")
        self.btn_solve.clicked.connect(self.solve_graph)
        control_panel.addWidget(self.btn_solve)

        self.btn_clear = QPushButton("Reset Đồ Thị")
        self.btn_clear.setStyleSheet("background-color: #e06d53; color: white; font-weight: bold; padding: 5px; border-radius: 4px;")
        self.btn_clear.clicked.connect(self.view.clear_graph)
        control_panel.addWidget(self.btn_clear)

        control_panel.addWidget(QLabel("Kết quả chi tiết:"))
        self.txt_result = QTextEdit()
        self.txt_result.setReadOnly(True)
        control_panel.addWidget(self.txt_result)

    def get_binary_adjacency_matrix(self):
        n = len(self.view.nodes)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        is_directed = (self.combo_mode.currentText() == "Có hướng (Directed)")
        
        for edge in self.view.edges:
            u = edge.node1.node_id
            v = edge.node2.node_id
            matrix[u][v] = 1
            if not is_directed:
                matrix[v][u] = 1
        return matrix

    def get_weighted_adjacency_matrix(self):
        n = len(self.view.nodes)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        is_directed = (self.combo_mode.currentText() == "Có hướng (Directed)")
        
        for edge in self.view.edges:
            u = edge.node1.node_id
            v = edge.node2.node_id
            dist = edge.weight 
            matrix[u][v] = dist
            if not is_directed:
                matrix[v][u] = dist
        return matrix

    def update_ui(self):
        self.combo_start.clear()
        n = len(self.view.nodes)
        if n == 0:
            return

        matrix = self.get_binary_adjacency_matrix()
        algo = self.combo_algo.currentText()
        is_directed = (self.combo_mode.currentText() == "Có hướng (Directed)")

        if algo == "Chu trình Euler (Fleury)":
            if not is_directed:
                odd_vertices = [i for i in range(n) if sum(matrix[i]) % 2!= 0]
                if len(odd_vertices) == 0:
                    self.combo_start.addItems([str(i) for i in range(n) if sum(matrix[i]) > 0])
                elif len(odd_vertices) == 2:
                    self.combo_start.addItems([str(i) for i in odd_vertices])
            else:
                start_nodes = list()
                end_nodes = list()
                valid = True
                for i in range(n):
                    out_d = sum(matrix[i])
                    in_d = sum(matrix[j][i] for j in range(n))
                    if out_d - in_d == 1:
                        start_nodes.append(i)
                    elif in_d - out_d == 1:
                        end_nodes.append(i)
                    elif out_d!= in_d:
                        valid = False
                        break
                if valid:
                    if len(start_nodes) == 0 and len(end_nodes) == 0:
                        self.combo_start.addItems([str(i) for i in range(n) if sum(matrix[i]) > 0])
                    elif len(start_nodes) == 1 and len(end_nodes) == 1:
                        self.combo_start.addItems([str(i) for i in start_nodes])
        else:
            self.combo_start.addItems([str(i) for i in range(n)])

    def solve_graph(self):
        n = len(self.view.nodes)
        if n == 0:
            self.txt_result.setText("Lỗi: Đồ thị trống!")
            return
        if self.combo_start.count() == 0:
            self.txt_result.setText("Lỗi: Đồ thị không thỏa mãn điều kiện tồn tại chu trình/đường đi Euler.")
            return

        start_node = int(self.combo_start.currentText())
        algo = self.combo_algo.currentText()
        is_directed = (self.combo_mode.currentText() == "Có hướng (Directed)")

        self.txt_result.clear()
        
        if algo == "Chu trình Euler (Fleury)":
            binary_matrix = self.get_binary_adjacency_matrix()
            if is_directed:
                res = find_eulerian_cycle_directed(binary_matrix, start_node)
            else:
                res = find_eulerian_cycle_undirected(binary_matrix, start_node)
                
            if isinstance(res, str):
                self.txt_result.setText(res)
            else:
                self.txt_result.setText("Kết quả Đường đi Euler:\n" + " ➔ ".join(map(str, res)))
        
        elif algo == "Chu trình Hamilton":
            binary_matrix = self.get_binary_adjacency_matrix()
            res = find_hamiltonian_cycle(binary_matrix, start_node)
            if isinstance(res, str):
                self.txt_result.setText(res)
            else:
                self.txt_result.setText("Kết quả Chu trình Hamilton:\n" + " ➔ ".join(map(str, res)))
        
        elif algo == "Người giao hàng (TSP)":
            weighted_matrix = self.get_weighted_adjacency_matrix()
            cost, path = tsp(weighted_matrix, start_node)
            if isinstance(cost, str):
                self.txt_result.setText(cost)
            else:
                self.txt_result.setText(f"Tổng trọng số (khoảng cách) ngắn nhất: {cost}\n\nLộ trình giao hàng tối ưu:\n" + " ➔ ".join(map(str, path)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())