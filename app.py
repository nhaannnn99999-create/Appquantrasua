```python
import streamlit as st
from datetime import datetime
import pandas as pd
import io

# ============================================================
# CẤU HÌNH APP
# ============================================================

st.set_page_config(
    page_title="Milk Tea POS",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        color: #777;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .price-box {
        padding: 18px;
        border-radius: 15px;
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        text-align: center;
    }

    .price-title {
        font-size: 15px;
        color: #666;
    }

    .price-number {
        font-size: 30px;
        font-weight: 800;
        color: #ea580c;
    }

    .total-box {
        padding: 22px;
        border-radius: 15px;
        background-color: #fff7ed;
        border: 2px solid #fb923c;
        text-align: center;
    }

    .total-label {
        font-size: 17px;
        font-weight: 600;
    }

    .total-number {
        font-size: 36px;
        font-weight: 900;
        color: #ea580c;
    }

    .invoice-header {
        padding: 20px;
        border-radius: 12px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
    }

    .thank-you {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin-top: 20px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DỮ LIỆU MENU
# Bạn có thể thay đổi giá tại đây
# ============================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa ô long": 32000,
    "Trà sữa bạc hà": 35000,
    "Trà sữa caramel": 38000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Trà tắc": 25000,
    "Matcha latte": 40000,
    "Socola latte": 40000
}

SIZE_PRICE = {
    "S": 0,
    "M": 5000,
    "L": 10000
}

TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Trân châu hoàng kim": 7000,
    "Kem cheese": 10000
}

SUGAR = [
    "0% đường",
    "30% đường",
    "50% đường",
    "70% đường",
    "100% đường"
]

ICE = [
    "Không đá",
    "30% đá",
    "50% đá",
    "70% đá",
    "100% đá"
]

PAYMENT = [
    "Tiền mặt",
    "Chuyển khoản",
    "Ví điện tử"
]

# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# ============================================================
# HÀM
# ============================================================

def format_money(number):
    return f"{number:,.0f} VNĐ"


def calculate_price(drink, size, topping):
    return (
        MENU[drink]
        + SIZE_PRICE[size]
        + TOPPING_PRICE[topping]
    )


def make_invoice_text(invoice):

    text = []

    text.append("=" * 48)
    text.append("                 MILK TEA SHOP")
    text.append("                  HÓA ĐƠN")
    text.append("=" * 48)

    text.append(f"Mã hóa đơn : {invoice['id']}")
    text.append(f"Thời gian  : {invoice['time']}")
    text.append(f"Khách hàng : {invoice['customer']}")
    text.append("-" * 48)

    for i, item in enumerate(invoice["items"], 1):

        text.append(
            f"{i}. {item['drink']} - Size {item['size']}"
        )

        text.append(
            f"   Topping: {item['topping']}"
        )

        text.append(
            f"   Đường: {item['sugar']} | Đá: {item['ice']}"
        )

        text.append(
            f"   {item['quantity']} x "
            f"{format_money(item['unit_price'])} = "
            f"{format_money(item['total'])}"
        )

    text.append("-" * 48)

    text.append(
        f"Tạm tính   : {format_money(invoice['subtotal'])}"
    )

    if invoice["discount"] > 0:
        text.append(
            f"Giảm giá   : -{format_money(invoice['discount'])}"
        )

    text.append(
        f"TỔNG TIỀN  : {format_money(invoice['total'])}"
    )

    text.append(
        f"Thanh toán : {invoice['payment']}"
    )

    text.append("=" * 48)
    text.append("              CẢM ƠN QUÝ KHÁCH!")
    text.append("=" * 48)

    return "\n".join(text)


def create_excel(invoice):

    data = []

    for item in invoice["items"]:

        data.append({
            "Mã hóa đơn": invoice["id"],
            "Thời gian": invoice["time"],
            "Khách hàng": invoice["customer"],
            "Tên món": item["drink"],
            "Size": item["size"],
            "Topping": item["topping"],
            "Đường": item["sugar"],
            "Đá": item["ice"],
            "Số lượng": item["quantity"],
            "Đơn giá": item["unit_price"],
            "Thành tiền": item["total"]
        })

    df = pd.DataFrame(data)

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Hoa Don"
        )

    return output.getvalue()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧋 MILK TEA POS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Hệ thống bán hàng & tính tiền trà sữa'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Khách hàng")

    customer_name = st.text_input(
        "Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng..."
    )

    st.session_state.customer_name = customer_name

    st.divider()

    st.header("💳 Thanh toán")

    payment_method = st.selectbox(
        "Phương thức thanh toán",
        PAYMENT
    )

    st.divider()

    st.header("🎁 Khuyến mãi")

    discount_percent = st.number_input(
        "Giảm giá (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0
    )

# ============================================================
# CHỌN MÓN
# ============================================================

st.header("🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:

    drink = st.selectbox(
        "Loại trà sữa / đồ uống",
        list(MENU.keys())
    )

    size = st.selectbox(
        "Size ly",
        list(SIZE_PRICE.keys())
    )

    topping = st.selectbox(
        "Topping",
        list(TOPPING_PRICE.keys())
    )

with col2:

    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR,
        index=2
    )

    ice = st.selectbox(
        "Mức độ đá",
        ICE,
        index=2
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=99,
        value=1,
        step=1
    )

# ============================================================
# GIÁ MÓN ĐANG CHỌN
# ============================================================

unit_price = calculate_price(
    drink,
    size,
    topping
)

current_total = unit_price * quantity

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="price-box">
            <div class="price-title">Giá đồ uống</div>
            <div class="price-number">
                {format_money(MENU[drink])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    extra = SIZE_PRICE[size] + TOPPING_PRICE[topping]

    st.markdown(
        f"""
        <div class="price-box">
            <div class="price-title">Size + Topping</div>
            <div class="price-number">
                {format_money(extra)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="price-box">
            <div class="price-title">Thành tiền</div>
            <div class="price-number">
                {format_money(current_total)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ============================================================
# THÊM MÓN
# ============================================================

if st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    type="primary",
    use_container_width=True
):

    new_item = {
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": current_total
    }

    st.session_state.cart.append(new_item)

    st.success(
        f"Đã thêm {quantity} x {drink}!"
    )

# ============================================================
# GIỎ HÀNG
# ============================================================

st.divider()

st.header("🛒 Hóa đơn hiện tại")

if not st.session_state.cart:

    st.info(
        "Chưa có món nào trong hóa đơn."
    )

else:

    for index, item in enumerate(
        st.session_state.cart
    ):

        col1, col2, col3, col4 = st.columns(
            [3.5, 2, 2, 0.8]
        )

        with col1:

            st.markdown(
                f"**{index + 1}. {item['drink']}**"
            )

            st.caption(
                f"Size {item['size']} • "
                f"{item['topping']} • "
                f"{item['sugar']} • "
                f"{item['ice']}"
            )

        with col2:

            st.write(
                f"Số lượng: **{item['quantity']}**"
            )

        with col3:

            st.write(
                f"**{format_money(item['total'])}**"
            )

        with col4:

            if st.button(
                "🗑️",
                key=f"delete_{index}"
            ):

                st.session_state.cart.pop(index)

                st.rerun()

    # ========================================================
    # TỔNG
    # ========================================================

    subtotal = sum(
        item["total"]
        for item in st.session_state.cart
    )

    discount = (
        subtotal
        * discount_percent
        / 100
    )

    total = subtotal - discount

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Tạm tính:** "
            f"{format_money(subtotal)}"
        )

        st.write(
            f"**Giảm giá:** "
            f"-{format_money(discount)}"
        )

    with col2:

        st.markdown(
            f"""
            <div class="total-box">
                <div class="total-label">
                    TỔNG THANH TOÁN
                </div>
                <div class="total-number">
                    {format_money(total)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# THANH TOÁN
# ============================================================

if st.session_state.cart:

    st.divider()

    st.header("💰 Thanh toán")

    if not customer_name.strip():

        st.warning(
            "⚠️ Vui lòng nhập tên khách hàng."
        )

    else:

        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True
        ):

            now = datetime.now()

            invoice = {
                "id": now.strftime(
                    "HD%Y%m%d%H%M%S"
                ),

                "time": now.strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),

                "customer": customer_name,

                "items": st.session_state.cart.copy(),

                "subtotal": subtotal,

                "discount": discount,

                "total": total,

                "payment": payment_method
            }

            st.session_state.invoice = invoice

            # Xóa giỏ hàng
            st.session_state.cart = []

            st.success(
                "✅ Thanh toán thành công!"
            )

            st.rerun()

# ============================================================
# HÓA ĐƠN SAU KHI THANH TOÁN
# ============================================================

if st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()

    st.header("🧾 HÓA ĐƠN")

    # --------------------------------------------------------
    # THÔNG TIN HÓA ĐƠN
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="invoice-header">

        <h2 style="text-align:center;">
        🧋 MILK TEA SHOP
        </h2>

        <p>
        <b>Mã hóa đơn:</b>
        {invoice['id']}
        </p>

        <p>
        <b>Thời gian:</b>
        {invoice['time']}
        </p>

        <p>
        <b>Khách hàng:</b>
        {invoice['customer']}
        </p>

        <p>
        <b>Phương thức thanh toán:</b>
        {invoice['payment']}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # BẢNG CHI TIẾT
    # --------------------------------------------------------

    invoice_table = []

    for i, item in enumerate(
        invoice["items"],
        start=1
    ):

        invoice_table.append({
            "STT": i,
            "Đồ uống": item["drink"],
            "Size": item["size"],
            "Topping": item["topping"],
            "Đường": item["sugar"],
            "Đá": item["ice"],
            "SL": item["quantity"],
            "Đơn giá": format_money(
                item["unit_price"]
            ),
            "Thành tiền": format_money(
                item["total"]
            )
        })

    df_invoice = pd.DataFrame(
        invoice_table
    )

    st.dataframe(
        df_invoice,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # TỔNG TIỀN
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Tạm tính:** "
            f"{format_money(invoice['subtotal'])}"
        )

        st.write(
            f"**Giảm giá:** "
            f"-{format_money(invoice['discount'])}"
        )

    with col2:

        st.markdown(
            f"""
            <div class="total-box">

                <div class="total-label">
                    TỔNG THANH TOÁN
                </div>

                <div class="total-number">
                    {format_money(invoice['total'])}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="thank-you">'
        '🎉 CẢM ƠN QUÝ KHÁCH!'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # XUẤT HÓA ĐƠN
    # ========================================================

    st.divider()

    st.header("📥 Xuất hóa đơn")

    invoice_text = make_invoice_text(
        invoice
    )

    excel_file = create_excel(
        invoice
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📄 TẢI HÓA ĐƠN TXT",
            data=invoice_text,
            file_name=f"{invoice['id']}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.download_button(
            "📊 XUẤT HÓA ĐƠN EXCEL",
            data=excel_file,
            file_name=f"{invoice['id']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    # ========================================================
    # XEM HÓA ĐƠN DẠNG TEXT
    # ========================================================

    with st.expander("👁️ Xem hóa đơn dạng văn bản"):

        st.code(
            invoice_text,
            language="text"
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧋 Milk Tea POS • Streamlit"
)
```
