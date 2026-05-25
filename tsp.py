def held_karp_tsp(adj_matrix, start_vertex):
    n = len(adj_matrix)
    memo = {}

    if sum(1 for row in adj_matrix for w in row if w > 0) == 0:
        return "Đồ thị hiện chưa có cạnh nào.", [ ]

    def dp(mask, u):
        if mask == (1 << n) - 1:
            cost = adj_matrix[u][start_vertex]
            return (cost, start_vertex) if cost > 0 else (float('inf'), start_vertex)

        if (mask, u) in memo:
            return memo[(mask, u)]

        min_cost = float('inf')
        best_next = -1

        for v in range(n):
            if (mask & (1 << v)) == 0:
                cost_to_v = adj_matrix[u][v]
                if cost_to_v > 0:
                    res_cost, _ = dp(mask | (1 << v), v)
                    total_cost = cost_to_v + res_cost
                    if total_cost < min_cost:
                        min_cost = total_cost
                        best_next = v

        memo[(mask, u)] = (min_cost, best_next)
        return memo[(mask, u)]

    min_total_cost, first_step = dp(1 << start_vertex, start_vertex)

    if min_total_cost == float('inf'):
        return "Không tồn tại chu trình Hamilton (TSP vô nghiệm trên đồ thị này).", [ ]

    path = [ start_vertex ]
    mask = 1 << start_vertex
    curr = start_vertex

    while True:
        _, nxt = memo.get((mask, curr), (None, start_vertex))
        if nxt == start_vertex or nxt == -1:
            path.append(start_vertex)
            break
        path.append(nxt)
        mask |= (1 << nxt)
        curr = nxt

    return min_total_cost, path