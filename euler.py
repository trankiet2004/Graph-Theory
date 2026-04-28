import copy

def find_eulerian_cycle_undirected(adj_matrix, start_vertex):
    """Tìm chu trình Euler cho đồ thị VÔ HƯỚNG"""
    n = len(adj_matrix)
    
    # Điều kiện Euler vô hướng: Mọi đỉnh phải có bậc chẵn
    for i in range(n):
        degree = sum(adj_matrix[i])
        if degree % 2!= 0:
            return f"Không thể tạo chu trình: Đỉnh {i} có bậc lẻ ({degree}). Đồ thị vô hướng yêu cầu mọi đỉnh đều phải có bậc chẵn."

    temp_matrix = copy.deepcopy(adj_matrix)
    stack = [ start_vertex ]
    cycle = []

    # Thuật toán Hierholzer cho đồ thị vô hướng
    while stack:
        u = stack[-1]
        found_edge = False
        
        for v in range(n):
            if temp_matrix[u][v] > 0:
                stack.append(v)
                # XÓA CẠNH Ở CẢ 2 CHIỀU (đốt cầu hoàn toàn để không đi lại)
                temp_matrix[u][v] -= 1
                temp_matrix[v][u] -= 1  
                found_edge = True
                break
                
        if not found_edge:
            cycle.append(stack.pop())

    # Kiểm tra xem có đồ thị bị đứt gãy không
    for row in temp_matrix:
        if sum(row) > 0:
            return "Đồ thị bị rời rạc, không thể đi qua tất cả các cạnh trong một chu trình."

    return cycle[::-1]


def find_eulerian_cycle_directed(adj_matrix, start_vertex):
    """Tìm chu trình Euler cho đồ thị CÓ HƯỚNG"""
    n = len(adj_matrix)
    
    # Điều kiện Euler có hướng: Bậc vào phải bằng bậc ra ở mọi đỉnh
    for i in range(n):
        out_degree = sum(adj_matrix[i])
        in_degree = sum(adj_matrix[j][i] for j in range(n))
        if out_degree!= in_degree:
            return f"Không thể tạo chu trình: Đỉnh {i} có số đường vào ({in_degree}) khác đường ra ({out_degree})."

    temp_matrix = copy.deepcopy(adj_matrix)
    stack = [ start_vertex ]
    cycle = []

    # Thuật toán Hierholzer cho đồ thị có hướng
    while stack:
        u = stack[-1]
        found_edge = False
        
        for v in range(n):
            if temp_matrix[u][v] > 0:
                stack.append(v)
                # CHỈ XÓA CẠNH 1 CHIỀU ĐÃ ĐI QUA
                temp_matrix[u][v] -= 1  
                found_edge = True
                break
                
        if not found_edge:
            cycle.append(stack.pop())

    for row in temp_matrix:
        if sum(row) > 0:
            return "Đồ thị bị rời rạc, không thể đi qua tất cả các cạnh."

    return cycle[::-1]