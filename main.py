import flet as ft
import json
import os

# Tên file lưu trữ dữ liệu
DATA_FILE = "orders_data.json"

def main(page: ft.Page):
    page.title = "Quản Lý Đơn Cày Thuê"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.padding = 20

    # Hàm lưu dữ liệu
    def save_data(data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # Hàm tải dữ liệu
    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    orders = load_data()

    # Các trường nhập liệu (UI)
    tf_tk = ft.TextField(label="Tài khoản (TK)", border_color="blue")
    tf_mk = ft.TextField(label="Mật khẩu (MK)", password=True, can_reveal_password=True)
    tf_lv_hien_tai = ft.TextField(label="Level hiện tại", keyboard_type=ft.KeyboardType.NUMBER, col=6)
    tf_nguyen_thach = ft.TextField(label="Nguyên thạch hiện tại", keyboard_type=ft.KeyboardType.NUMBER, col=6)
    tf_don_cay = ft.TextField(label="Nội dung cày (Số LV, Item, Nguyên liệu...)", multiline=True)
    tf_tien = ft.TextField(label="Tổng tiền (VNĐ)", keyboard_type=ft.KeyboardType.NUMBER)

    order_list_column = ft.Column()

    def render_orders():
        order_list_column.controls.clear()
        for i, order in enumerate(reversed(orders)):
            order_list_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Đơn hàng #{len(orders)-i}", weight="bold", size=18, color="yellow"),
                        ft.Text(f"TK: {order['tk']} | MK: {order['mk']}"),
                        ft.Text(f"Trạng thái: LV {order['lv']} | NT: {order['nt']}"),
                        ft.Text(f"Yêu cầu: {order['req']}"),
                        ft.Text(f"Giá: {order['price']} VNĐ", color="greenaccent"),
                    ]),
                    padding=15,
                    border_radius=10,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                )
            )
        page.update()

    def add_order_click(e):
        if not tf_tk.value or not tf_tien.value:
            return
        
        new_order = {
            "tk": tf_tk.value,
            "mk": tf_mk.value,
            "lv": tf_lv_hien_tai.value,
            "nt": tf_nguyen_thach.value,
            "req": tf_don_cay.value,
            "price": tf_tien.value
        }
        orders.append(new_order)
        save_data(orders)
        
        # Reset form
        tf_tk.value = tf_mk.value = tf_lv_hien_tai.value = ""
        tf_nguyen_thach.value = tf_don_cay.value = tf_tien.value = ""
        
        render_orders()

    # Giao diện chính
    page.add(
        ft.Text("HỆ THỐNG CÀY THUÊ", size=30, weight="bold", color="blue"),
        ft.Divider(),
        ft.Column([
            tf_tk,
            tf_mk,
            ft.Row([tf_lv_hien_tai, tf_nguyen_thach]),
            tf_don_cay,
            tf_tien,
            ft.ElevatedButton("LƯU ĐƠN HÀNG", on_click=add_order_click, bgcolor="blue", color="white"),
        ]),
        ft.Divider(),
        ft.Text("DANH SÁCH ĐƠN", size=20, weight="bold"),
        order_list_column
    )

    render_orders()

ft.app(target=main)
