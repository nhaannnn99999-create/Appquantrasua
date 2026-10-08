import streamlit as st
from datetime import datetime
import pandas as pd
import io

# =========================
# CẤU HÌNH
# =========================
st.set_page_config(
    page_title="Quản lý Bill Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Matcha latte": 40000,
    "Socola đá xay": 45000,
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
}

SUGAR_LEVEL = [
    "0% - Không đường",
    "30%",
    "50%",
    "70%",
    "100%"
]

ICE_LEVEL = [
    "0% - Không đá",
    "30%",
    "50%",
    "70%",
    "100%"
]

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(number):
    return f"{number:,.0f} đ".replace(",", ".")


# =========================
# KHỞI TẠO SESSION
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "invoice" not in st.session_state:
    st.session_state.invoice = None


# =========================
# HEADER
# =========================
st.title("🧋 QUẢN LÝ BILL QUÁN TRÀ SỮA")
st.caption("Tạo đơn hàng • Tính tiền • Thanh toán • Xuất hóa đơn")

st.divider()


# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input(
        "Tên khách hàng",
        placeholder="Nhập tên khách hàng..."
    )

with col2:
    customer_phone = st.text_input(
        "Số điện thoại",
        placeholder="Không bắt buộc"
    )


st.divider()


# =========================
# THÊM MÓN
# =========================
st.subheader("🧋 Thêm món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / thức uống",
        list(MENU.keys())
    )

    size = st.selectbox(
        "Size",
        list(SIZE_PRICE.keys())
    )

    topping = st.selectbox(
        "Topping",
        list(TOPPING_PRICE.keys())
    )

with col2:
    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR_LEVEL
    )

    ice = st.selectbox(
        "Mức độ đá",
        ICE_LEVEL
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )


# =========================
# TÍNH GIÁ MÓN
