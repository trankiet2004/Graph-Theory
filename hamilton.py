def is_safe(v, graph, path, pos):
    """Kiểm tra điều kiện để thêm đỉnh vào đường đi Hamilton"""
    if graph[path[pos - 1]][v] == 0:
        return False
    if v in path:
        return False
    return True


def hamilton_util(graph, path, pos, n, start_vertex):
    """Hàm đệ quy Quay lui tìm chu trình Hamilton"""
    if pos == n:
        if graph[path[pos - 1]][start_vertex]!= 0:
            return True
        return False

    for v in range(n):
        if v!= start_vertex and is_safe(v, graph, path, pos):
            path[pos] = v
            if hamilton_util(graph, path, pos + 1, n, start_vertex):
                return True
            path[pos] = -1
            
    return False


def find_hamiltonian_cycle(adj_matrix, start_vertex):
    """Khởi tạo và tìm chu trình Hamilton"""
    n = len(adj_matrix)
    if sum(sum(row) for row in adj_matrix) == 0:
        return "Đồ thị hiện chưa có cạnh nào."
        
    path = [-1] * n
    path[ 0 ] = start_vertex 

    if not hamilton_util(adj_matrix, path, 1, n, start_vertex):
        return "Không phát hiện được chu trình Hamilton xuất phát từ đỉnh này."

    path.append(start_vertex)
    return path