import streamlit as st
import pandas as pd

# ==========================================
# PHẦN 1: CÁC THUẬT TOÁN XỬ LÝ ĐỒ THỊ
# ==========================================
import euler
import hamilton


# ==========================================
# PHẦN 2: GIAO DIỆN STREAMLIT
# ==========================================

st.set_page_config(page_title="Tạo Đồ Thị", layout="centered")
st.title("Xây Dựng Đồ Thị & Phân Tích Chu Trình")

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
mode = st.radio("Chọn dạng đồ thị:", ("Vô hướng (Undirected)", "Có hướng (Directed)"))
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
st.header("2. Nối các cạnh")

if mode == "Vô hướng (Undirected)":
    col1, col2 = st.columns(2)
    with col1:
        u = st.selectbox("Nối từ đỉnh (U):", range(n))
    with col2:
        v = st.selectbox("Đến đỉnh (V):", range(n))
        
    if st.button("Thêm Cạnh (Vô hướng)", type="primary", use_container_width=True):
        if u == v:
            st.error("Không hỗ trợ khuyên vòng (U trùng V).")
        else:
            # Ghi nhận đối xứng cho cả 2 chiều
            st.session_state.adj_matrix[u][v] += 1
            st.session_state.adj_matrix[v][u] += 1
            st.success(f"Đã thêm thành công cạnh vô hướng kết nối đỉnh {u} và {v}.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        edge_type = st.radio("Chọn loại cạnh:", ["1 Chiều", "2 Chiều"])
    with col2:
        u = st.selectbox("Từ đỉnh (U):", range(n))
    with col3:
        v = st.selectbox("Đến đỉnh (V):", range(n))

    if st.button("Thêm Cạnh (Có hướng)", type="primary", use_container_width=True):
        if u == v:
            st.error("Không hỗ trợ khuyên vòng (U trùng V).")
        else:
            st.session_state.adj_matrix[u][v] += 1
            if edge_type == "2 Chiều":
                st.session_state.adj_matrix[v][u] += 1
            st.success(f"Đã thêm thành công: Cạnh nối từ đỉnh {u} đến {v}.")


st.write(f"**Bảng Ma trận kề {mode}:**")
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
st.header("3. Phân tích Chu trình")

cycle_type = st.selectbox("Bạn muốn tìm:", ["Chu trình Euler", "Chu trình Hamilton"])
valid_starts = []

# Lọc đỉnh xuất phát theo loại đồ thị và thuật toán
if cycle_type == "Chu trình Euler":
    is_euler_valid = True
    
    if mode == "Vô hướng (Undirected)":
        for i in range(n):
            if sum(st.session_state.adj_matrix[i]) % 2!= 0:
                is_euler_valid = False
                break
    else:
        for i in range(n):
            out_degree = sum(st.session_state.adj_matrix[i])
            in_degree = sum(st.session_state.adj_matrix[j][i] for j in range(n))
            if out_degree!= in_degree:
                is_euler_valid = False
                break
                
    if is_euler_valid:
        valid_starts = [i for i in range(n) if sum(st.session_state.adj_matrix[i]) > 0]
else:
    # Đối với Hamilton
    valid_starts = list(range(n))  # Tất cả đỉnh đều có thể là điểm xuất phát cho Hamilton


if not valid_starts:
    if cycle_type == "Chu trình Euler":
        st.warning("⚠️ Đồ thị hiện tại KHÔNG thỏa mãn điều kiện Euler. Hãy quay lại Bước 2 để thiết lập lại các cạnh.")
    else:
        st.warning("⚠️ Chưa có đủ điều kiện để tính toán.")
else:
    start_node = st.selectbox("Chọn đỉnh xuất phát (đã lọc các đỉnh hợp lệ):", valid_starts)
    
    if st.button("Kết Xuất Trình Tự", type="primary"):
        if cycle_type == "Chu trình Euler":
            if mode == "Vô hướng (Undirected)":
                result = euler.find_eulerian_cycle_undirected(st.session_state.adj_matrix, start_node)
            else:
                result = euler.find_eulerian_cycle_directed(st.session_state.adj_matrix, start_node)
        else:
            result = hamilton.find_hamiltonian_cycle(st.session_state.adj_matrix, start_node)
            
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(" ➔ ".join(map(str, result)))