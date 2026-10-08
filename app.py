import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG VÀ THÔNG TIN BẢNG GIÁ
# ---------------------------------------------------------
st.set_page_config(
    page_title="Quản Lý Hóa Đơn Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# Danh sách menu & Bảng giá (VND)
MENU_DRINKS = {
    "Trà sữa truyền thống": 25000,
    "Trà sữa Oolong": 30000,
    "Trà sữa Matcha": 32000,
    "Trà sữa Trái cây (Đào/Vải)": 28000,
    "Trà sữa Kem Trứng Nướng": 35000,
    "Trà Trái Cây Tươi": 25000
}

SIZE_PRICE = {
    "Nhỏ (S)": 0,
    "Vừa (M)": 5000,
    "Lớn (L)": 10000
}

TOPPING_PRICE = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding Flau": 8000,
    "Kem Cheese": 10000
}

ICE_LEVELS = ["100% Đá", "70% Đá", "50% Đá", "Không đá"]

# ---------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE (BỘ NHỚ TẠM)
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

def clear_order():
    st.session_state.cart = []
    st.session_state.paid = False

# ---------------------------------------------------------
# 3. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 Hệ Thống Tính Tiền & Xuất Hóa Đơn Trà Sữa")
st.markdown("---")

col_left, col_right = st.columns([1, 1], gap="large")

# ---------------------------------------------------------
# CỘT TRÁI: NHẬP THÔNG TIN VÀ CHỌN MÓN
# ---------------------------------------------------------
with col_left:
    st.subheader("📝 Nhập Thông Tin Đặt Hàng")
    
    # Thông tin khách hàng
    customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên khách hàng...")
    
    st.markdown("### Chọn Món Nước")
    
    # Form chọn chi tiết món nước
    drink_choice = st.selectbox("Loại trà sữa:", list(MENU_DRINKS.keys()))
    size_choice = st.selectbox("Size ly:", list(SIZE_PRICE.keys()))
    ice_choice = st.select_slider("Mức độ đá:", options=ICE_LEVELS)
    topping_choices = st.multiselect("Thêm Topping:", list(TOPPING_PRICE.keys()))
    quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)
    
    # Tính giá tiền cho 1 ly
    base_price = MENU_DRINKS[drink_choice]
    size_extra = SIZE_PRICE[size_choice]
    topping_extra = sum([TOPPING_PRICE[t] for t in topping_choices])
    item_unit_price = base_price + size_extra + topping_extra
    item_total = item_unit_price * quantity
    
    st.info(f"💰 Đơn giá/ly: **{item_unit_price:,} VNĐ** | Tổng món này: **{item_total:,} VNĐ**")
    
    # Nút thêm món vào giỏ
