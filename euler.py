"""
Euler Cycle with Weighted Adjacency Matrix

Quy ước ma trận:
- matrix[i][j] = 0  : không có cạnh từ i đến j
- matrix[i][j] > 0  : có cạnh, giá trị là trọng số của cạnh

Output giữ giống code ban đầu:
- Nếu thành công: trả về path, ví dụ [0, 1, 2, 0]
- Nếu thất bại: trả về chuỗi thông báo lỗi

Lưu ý:
- Trọng số KHÔNG ảnh hưởng đến điều kiện tồn tại chu trình Euler.
- Thuật toán chỉ dùng matrix[i][j] > 0 để biết có cạnh hay không.
- Trọng số có thể tính riêng bằng hàm calculate_path_cost(path, adj_matrix).
- Code này giả định không có cạnh song song và không xét self-loop matrix[i][i].
"""

import copy


# ============================================================
# COMMON HELPERS
# ============================================================

def validate_square_matrix(matrix):
    """Kiểm tra ma trận có vuông không."""
    if not matrix:
        raise ValueError("Ma trận không được rỗng.")

    n = len(matrix)

    for row in matrix:
        if len(row) != n:
            raise ValueError("Ma trận kề phải là ma trận vuông.")

    return n


def validate_start_vertex(start_vertex, n):
    """Kiểm tra đỉnh bắt đầu hợp lệ."""
    if start_vertex < 0 or start_vertex >= n:
        raise ValueError("Đỉnh bắt đầu không hợp lệ.")


def calculate_path_cost(path, adj_matrix):
    """Tính tổng trọng số của đường đi / chu trình."""
    total_cost = 0

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        total_cost += adj_matrix[u][v]

    return total_cost


# ============================================================
# UNDIRECTED EULER CYCLE - FLEURY
# ============================================================

def validate_undirected_matrix(matrix):
    """Kiểm tra ma trận vô hướng có đối xứng không."""
    n = validate_square_matrix(matrix)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Ma trận vô hướng phải đối xứng: matrix[i][j] == matrix[j][i].")

    return n


def degree_undirected(matrix, vertex):
    """Tính bậc của một đỉnh trong đồ thị vô hướng."""
    n = len(matrix)

    # Giả định không xét self-loop, nên chỉ đếm j != vertex
    return sum(1 for j in range(n) if j != vertex and matrix[vertex][j] > 0)


def count_reachable_vertices_undirected(start, matrix):
    """Đếm số đỉnh có thể đi tới từ start trong đồ thị vô hướng hiện tại."""
    n = len(matrix)
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        count = 1

        for v in range(n):
            if matrix[u][v] > 0 and not visited[v]:
                count += dfs(v)

        return count

    return dfs(start)


def is_connected_undirected(matrix):
    """
    Kiểm tra liên thông cho đồ thị vô hướng.
    Chỉ yêu cầu các đỉnh có bậc > 0 nằm trong cùng một thành phần liên thông.
    Đỉnh cô lập được bỏ qua.
    """
    n = len(matrix)

    start = -1
    for i in range(n):
        if degree_undirected(matrix, i) > 0:
            start = i
            break

    # Đồ thị không có cạnh nào
    if start == -1:
        return True

    visited = [False] * n

    def dfs(u):
        visited[u] = True

        for v in range(n):
            if matrix[u][v] > 0 and not visited[v]:
                dfs(v)

    dfs(start)

    for i in range(n):
        if degree_undirected(matrix, i) > 0 and not visited[i]:
            return False

    return True


def has_eulerian_cycle_undirected(matrix):
    """
    Điều kiện có chu trình Euler trong đồ thị vô hướng:
    1. Các đỉnh có cạnh nằm trong cùng một thành phần liên thông.
    2. Mọi đỉnh đều có bậc chẵn.
    """
    n = validate_undirected_matrix(matrix)

    if not is_connected_undirected(matrix):
        return False

    for i in range(n):
        if degree_undirected(matrix, i) % 2 != 0:
            return False

    return True


def is_valid_edge_undirected(u, v, matrix):
    """
    Kiểm tra cạnh (u, v) có hợp lệ để đi tiếp theo luật Fleury không.

    Luật Fleury:
    - Nếu từ u chỉ còn 1 cạnh, bắt buộc phải đi cạnh đó.
    - Nếu có nhiều lựa chọn, tránh đi qua cạnh cầu.
    """
    n = len(matrix)

    # Nếu đây là lựa chọn duy nhất thì phải đi
    current_degree = degree_undirected(matrix, u)
    if current_degree == 1:
        return True

    # Đếm số đỉnh reachable trước khi xóa cạnh
    count_before = count_reachable_vertices_undirected(u, matrix)

    # Lưu trọng số cũ
    old_uv = matrix[u][v]
    old_vu = matrix[v][u]

    # Xóa tạm cạnh bằng cách gán về 0
    # Không dùng -= 1 vì matrix[u][v] là trọng số, không phải số lượng cạnh.
    matrix[u][v] = 0
    matrix[v][u] = 0

    # Đếm số đỉnh reachable sau khi xóa cạnh
    count_after = count_reachable_vertices_undirected(u, matrix)

    # Phục hồi cạnh
    matrix[u][v] = old_uv
    matrix[v][u] = old_vu

    # Nếu count giảm, cạnh này là cầu, không nên đi
    return count_after == count_before


def find_eulerian_cycle_undirected(adj_matrix, start_vertex):
    """
    Tìm chu trình Euler cho đồ thị vô hướng bằng thuật toán Fleury.

    Return giống code ban đầu:
    - Nếu thành công: path
    - Nếu thất bại: chuỗi thông báo lỗi
    """
    n = validate_undirected_matrix(adj_matrix)
    validate_start_vertex(start_vertex, n)

    if not has_eulerian_cycle_undirected(adj_matrix):
        return "Đồ thị vô hướng không có chu trình Euler."

    # Đếm số cạnh, không cộng trọng số
    total_edges = sum(
        1
        for i in range(n)
        for j in range(i + 1, n)
        if adj_matrix[i][j] > 0
    )

    # Nếu đồ thị không có cạnh nào
    if total_edges == 0:
        return [start_vertex]

    if degree_undirected(adj_matrix, start_vertex) == 0:
        return "Đỉnh bắt đầu là đỉnh cô lập, không nằm trong chu trình Euler."

    temp_matrix = copy.deepcopy(adj_matrix)
    path = [start_vertex]
    u = start_vertex

    for _ in range(total_edges):
        next_v = -1

        for v in range(n):
            if temp_matrix[u][v] > 0:
                if is_valid_edge_undirected(u, v, temp_matrix):
                    next_v = v
                    break

        if next_v == -1:
            return "Không thể hoàn thành chu trình Euler."

        path.append(next_v)

        # Xóa cạnh đã đi qua
        temp_matrix[u][next_v] = 0
        temp_matrix[next_v][u] = 0

        u = next_v

    if path[0] != path[-1]:
        return "Không phải chu trình Euler vì điểm đầu và điểm cuối khác nhau."

    return path


# ============================================================
# DIRECTED EULER CYCLE - HIERHOLZER
# ============================================================

def out_degree_directed(matrix, vertex):
    """Tính out-degree của một đỉnh trong đồ thị có hướng."""
    n = len(matrix)

    # Giả định không xét self-loop
    return sum(1 for j in range(n) if j != vertex and matrix[vertex][j] > 0)


def in_degree_directed(matrix, vertex):
    """Tính in-degree của một đỉnh trong đồ thị có hướng."""
    n = len(matrix)

    # Giả định không xét self-loop
    return sum(1 for i in range(n) if i != vertex and matrix[i][vertex] > 0)


def dfs_directed(matrix, start, visited):
    """DFS trên đồ thị có hướng."""
    n = len(matrix)
    visited[start] = True

    for v in range(n):
        if matrix[start][v] > 0 and not visited[v]:
            dfs_directed(matrix, v, visited)


def transpose_matrix(matrix):
    """Tạo ma trận chuyển vị của đồ thị có hướng."""
    n = len(matrix)

    return [[matrix[j][i] for j in range(n)] for i in range(n)]


def is_strongly_connected_directed(matrix):
    """
    Kiểm tra liên thông mạnh cho đồ thị có hướng.
    Chỉ xét các đỉnh có in-degree + out-degree > 0.
    """
    n = validate_square_matrix(matrix)

    vertices_with_edges = []

    for i in range(n):
        if in_degree_directed(matrix, i) + out_degree_directed(matrix, i) > 0:
            vertices_with_edges.append(i)

    # Đồ thị không có cạnh
    if not vertices_with_edges:
        return True

    start = vertices_with_edges[0]

    visited = [False] * n
    dfs_directed(matrix, start, visited)

    for v in vertices_with_edges:
        if not visited[v]:
            return False

    transposed = transpose_matrix(matrix)

    visited = [False] * n
    dfs_directed(transposed, start, visited)

    for v in vertices_with_edges:
        if not visited[v]:
            return False

    return True


def has_eulerian_cycle_directed(matrix):
    """
    Điều kiện có chu trình Euler trong đồ thị có hướng:
    1. Mọi đỉnh có in-degree = out-degree.
    2. Các đỉnh có cạnh thuộc cùng một thành phần liên thông mạnh.
    """
    n = validate_square_matrix(matrix)

    if not is_strongly_connected_directed(matrix):
        return False

    for i in range(n):
        if in_degree_directed(matrix, i) != out_degree_directed(matrix, i):
            return False

    return True


def find_eulerian_cycle_directed(adj_matrix, start_vertex):
    """
    Tìm chu trình Euler cho đồ thị có hướng bằng thuật toán Hierholzer.

    Return giống code ban đầu:
    - Nếu thành công: path
    - Nếu thất bại: chuỗi thông báo lỗi
    """
    n = validate_square_matrix(adj_matrix)
    validate_start_vertex(start_vertex, n)

    if not has_eulerian_cycle_directed(adj_matrix):
        return "Đồ thị có hướng không có chu trình Euler."

    total_edges = sum(
        1
        for i in range(n)
        for j in range(n)
        if i != j and adj_matrix[i][j] > 0
    )

    # Nếu đồ thị không có cạnh nào
    if total_edges == 0:
        return [start_vertex]

    if in_degree_directed(adj_matrix, start_vertex) + out_degree_directed(adj_matrix, start_vertex) == 0:
        return "Đỉnh bắt đầu là đỉnh cô lập, không nằm trong chu trình Euler."

    temp_matrix = copy.deepcopy(adj_matrix)

    stack = [start_vertex]
    path = []

    while stack:
        u = stack[-1]

        next_v = -1

        for v in range(n):
            if temp_matrix[u][v] > 0:
                next_v = v
                break

        if next_v != -1:
            stack.append(next_v)

            # Xóa cạnh đã đi qua
            temp_matrix[u][next_v] = 0
        else:
            path.append(stack.pop())

    path.reverse()

    if len(path) != total_edges + 1:
        return "Không đi qua đủ tất cả các cạnh."

    if path[0] != path[-1]:
        return "Không phải chu trình Euler vì điểm đầu và điểm cuối khác nhau."

    return path


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    # Ví dụ 1: Đồ thị vô hướng có chu trình Euler
    undirected_matrix = [
        [0, 2, 0, 8],
        [2, 0, 4, 0],
        [0, 4, 0, 6],
        [8, 0, 6, 0]
    ]

    result = find_eulerian_cycle_undirected(undirected_matrix, start_vertex=0)
    print("Undirected Euler Cycle:")
    print(result)

    if isinstance(result, list):
        print("Cost:", calculate_path_cost(result, undirected_matrix))

    print()

    # Ví dụ 2: Đồ thị có hướng có chu trình Euler
    directed_matrix = [
        [0, 3, 0],
        [0, 0, 5],
        [7, 0, 0]
    ]

    result = find_eulerian_cycle_directed(directed_matrix, start_vertex=0)
    print("Directed Euler Cycle:")
    print(result)

    if isinstance(result, list):
        print("Cost:", calculate_path_cost(result, directed_matrix))
