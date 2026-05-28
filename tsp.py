def tsp(adj_matrix, start_vertex):
    # Vẫn giữ nguyên tên hàm để không làm hỏng cấu trúc import ở các file khác
    n = len(adj_matrix)

    # Kiểm tra đồ thị rỗng
    if sum(1 for row in adj_matrix for w in row if w > 0) == 0:
        return "Đồ thị hiện chưa có cạnh nào.", []

    # Khởi tạo các biến lưu kết quả toàn cục cho hàm đệ quy
    min_total_cost = float('inf')
    best_path = []
    
    # Mảng đánh dấu các đỉnh đã thăm
    visited = [False] * n

    def backtrack(curr_vertex, visited_count, current_cost, path):
        nonlocal min_total_cost, best_path

        # Nhánh cận (Pruning): Cắt tỉa nếu chi phí hiện tại đã vượt mức tối ưu đang có
        if current_cost >= min_total_cost:
            return

        # Điều kiện dừng: Đã đi qua tất cả n đỉnh
        if visited_count == n:
            # Kiểm tra xem có đường từ đỉnh cuối quay về đỉnh xuất phát hay không
            cost_to_start = adj_matrix[curr_vertex][start_vertex]
            if cost_to_start > 0:
                total_cost = current_cost + cost_to_start
                if total_cost < min_total_cost:
                    min_total_cost = total_cost
                    best_path = path[:] + [start_vertex]
            return

        # Duyệt qua các đỉnh kề chưa được thăm
        for next_vertex in range(n):
            if not visited[next_vertex]:
                edge_cost = adj_matrix[curr_vertex][next_vertex]
                if edge_cost > 0:
                    # Bước tiến: Đánh dấu đỉnh, cộng dồn chi phí và đưa vào đường đi
                    visited[next_vertex] = True
                    path.append(next_vertex)

                    # Gọi đệ quy để đi tiếp
                    backtrack(next_vertex, visited_count + 1, current_cost + edge_cost, path)

                    # Bước quay lui (Backtrack): Phục hồi trạng thái để xét nhánh (đỉnh) khác
                    path.pop()
                    visited[next_vertex] = False

    # Khởi tạo trạng thái cho đỉnh xuất phát ban đầu
    visited[start_vertex] = True
    backtrack(start_vertex, 1, 0, [start_vertex])

    # Trả về kết quả theo đúng định dạng cũ
    if min_total_cost == float('inf'):
        return "Không tồn tại chu trình Hamilton (TSP vô nghiệm trên đồ thị này).", []

    return min_total_cost, best_path