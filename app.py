import streamlit as st
import pandas as pd

# Gọi các hàm thuật toán từ các tệp Python bên ngoài vào
from euler import find_eulerian_cycle_undirected, find_eulerian_cycle_directed
from hamilton import find_hamiltonian_cycle
from tsp import tsp

# ==========================================
# GIAO DIỆN STREAMLIT
# ==========================================

st.set_page_config(page_title="Hệ Thống Đồ Thị & TSP", layout="centered")
st.title("Phân Tích Đồ Thị & Bài Toán Người Giao Hàng (TSP)")

# Khởi tạo dữ liệu
if 'n_nodes' not in st.session_state:
    st.session_state.n_nodes = 5
if 'graph_mode' not in st.session_state:
    st.session_state.graph_mode = "Vô hướng (Undirected)"
if 'adj_matrix' not in st.session_state:
    st.session_state.adj_matrix = [[0 for _ in range(5)] for _ in range(5)]

# ---------------------------------------------------------
# BƯỚC 1: KHỞI TẠO ĐỒ THỊ
# ---------------------------------------------------------
st.header("1. Cài đặt hệ thống")

# Sử dụng tuple để khai báo các lựa chọn, tránh lỗi hiển thị bị nuốt mất mảng
mode_options = ("Vô hướng (Undirected)", "Có hướng (Directed)")
mode = st.radio("Chọn dạng đồ thị:", mode_options)

n = st.number_input("Nhập số lượng đỉnh (N):", min_value=3, max_value=20, value=st.session_state.n_nodes)

# Reset lại ma trận nếu người dùng đổi cấu hình
if n!= st.session_state.n_nodes or mode!= st.session_state.graph_mode:
    st.session_state.n_nodes = n
    st.session_state.graph_mode = mode
    st.session_state.adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    st.rerun()

# ---------------------------------------------------------
# BƯỚC 2: THÊM CẠNH VÀO MA TRẬN
# ---------------------------------------------------------
st.header("2. Nối các cạnh và Trọng số")

if mode == "Vô hướng (Undirected)":
    col1, col2, col3 = st.columns(3)
    with col1:
        u = st.selectbox("Nối từ đỉnh (U):", range(n))
    with col2:
        v = st.selectbox("Đến đỉnh (V):", range(n))
    with col3:
        weight = st.number_input("Trọng số (Khoảng cách):", min_value=1, value=1)
        
    if st.button("Thêm Cạnh (Vô hướng)", type="primary", use_container_width=True):
        if u == v:
            st.error("Không hỗ trợ khuyên vòng (U trùng V).")
        else:
            st.session_state.adj_matrix[u][v] = weight
            st.session_state.adj_matrix[v][u] = weight
            st.success(f"Đã cập nhật cạnh vô hướng {u} ⟷ {v} với khoảng cách {weight}.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        edge_type_opts = ("1 Chiều", "2 Chiều")
        edge_type = st.radio("Loại cạnh:", edge_type_opts)
    with col2:
        u = st.selectbox("Từ đỉnh (U):", range(n))
    with col3:
        v = st.selectbox("Đến đỉnh (V):", range(n))
    with col4:
        weight = st.number_input("Trọng số (Khoảng cách):", min_value=1, value=1)

    if st.button("Thêm Cạnh (Có hướng)", type="primary", use_container_width=True):
        if u == v:
            st.error("Không hỗ trợ khuyên vòng (U trùng V).")
        else:
            st.session_state.adj_matrix[u][v] = weight
            if edge_type == "2 Chiều":
                st.session_state.adj_matrix[v][u] = weight
            st.success(f"Đã cập nhật cạnh {u} ➔ {v} với khoảng cách {weight}.")

st.write("**Bảng Ma trận kề (Giá trị là Khoảng cách):**")
cols_labels = [str(i) for i in range(n)]
df_matrix = pd.DataFrame(st.session_state.adj_matrix, index=cols_labels, columns=cols_labels)
st.dataframe(df_matrix, use_container_width=True)

if st.button("Xóa trắng toàn bộ ma trận (Reset)"):
    st.session_state.adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    st.rerun()

st.divider()

# ---------------------------------------------------------
# BƯỚC 3 & 4: CHỌN CHU TRÌNH & XUẤT KẾT QUẢ
# ---------------------------------------------------------
st.header("3. Phân tích Chu trình & Tìm Đường")

# GỘP CẢ 3 LỰA CHỌN VÀO SELECTBOX ĐỂ BẠN CHỌN
cycle_options = ("Chu trình Euler", "Chu trình Hamilton", "Bài toán Người giao hàng (TSP)")
cycle_type = st.selectbox("Bạn muốn tìm:", cycle_options)

valid_starts = list()

if cycle_type == "Chu trình Euler":
    is_euler_valid = True
    
    if mode == "Vô hướng (Undirected)":
        odd_vertices = list()
        for i in range(n):
            if sum(1 for w in st.session_state.adj_matrix[i] if w > 0) % 2!= 0:
                odd_vertices.append(i)
                
        if len(odd_vertices) == 0:
            valid_starts = [i for i in range(n) if sum(1 for w in st.session_state.adj_matrix[i] if w > 0) > 0]
            st.info("Đồ thị có Chu trình khép kín (Mọi đỉnh bậc chẵn). Bạn có thể xuất phát từ bất kỳ đâu.")
        elif len(odd_vertices) == 2:
            valid_starts = odd_vertices
            st.info("Đồ thị có Đường đi Euler (2 đỉnh bậc lẻ). Theo luật, hệ thống chỉ cho phép xuất phát từ 1 trong 2 đỉnh này.")
        else:
            is_euler_valid = False
    else:
        start_nodes = list()
        end_nodes = list()
        for i in range(n):
            out_d = sum(1 for w in st.session_state.adj_matrix[i] if w > 0)
            in_d = sum(1 for j in range(n) if st.session_state.adj_matrix[j][i] > 0)
            if out_d - in_d == 1:
                start_nodes.append(i)
            elif in_d - out_d == 1:
                end_nodes.append(i)
            elif out_d!= in_d:
                is_euler_valid = False
                break
                
        if is_euler_valid:
            if len(start_nodes) == 0 and len(end_nodes) == 0:
                valid_starts = [i for i in range(n) if sum(1 for w in st.session_state.adj_matrix[i] if w > 0) > 0]
                st.info("Đồ thị có Chu trình khép kín. Bạn có thể xuất phát từ bất kỳ đâu.")
            elif len(start_nodes) == 1 and len(end_nodes) == 1:
                valid_starts = start_nodes
                st.info("Đồ thị có Đường đi Euler. Bạn chỉ được phép xuất phát từ đỉnh có lượng đường đi ra nhiều hơn đường đi vào.")
            else:
                is_euler_valid = False
else:
    valid_starts = list(range(n))

if not valid_starts:
    if cycle_type == "Chu trình Euler":
        st.warning("⚠️ Đồ thị hiện tại KHÔNG thỏa mãn điều kiện Euler (Số đỉnh bậc lẻ không phải là 0 hoặc 2).")
    else:
        st.warning("⚠️ Chưa có đủ điều kiện để tính toán.")
else:
    start_node = st.selectbox("Chọn đỉnh xuất phát (đã lọc các đỉnh hợp lệ):", valid_starts)
    
    if st.button("Kết Xuất Trình Tự", type="primary"):
        if cycle_type == "Chu trình Euler":
            if mode == "Vô hướng (Undirected)":
                result = find_eulerian_cycle_undirected(st.session_state.adj_matrix, start_node)
            else:
                result = find_eulerian_cycle_directed(st.session_state.adj_matrix, start_node)
                
            if isinstance(result, str):
                st.error(result)
            else:
                st.success(" ➔ ".join(map(str, result)))
                
        elif cycle_type == "Chu trình Hamilton":
            result = find_hamiltonian_cycle(st.session_state.adj_matrix, start_node)
            if isinstance(result, str):
                st.error(result)
            else:
                st.success(" ➔ ".join(map(str, result)))
                
        elif cycle_type == "Bài toán Người giao hàng (TSP)":
            cost, path = tsp(st.session_state.adj_matrix, start_node)
            if isinstance(cost, str):
                st.error(cost)
            else:
                st.success(f"Tổng quãng đường / chi phí nhỏ nhất: **{cost}**")
                st.info("Lộ trình tối ưu: " + " ➔ ".join(map(str, path)))