import flet as ft
import json
from datetime import datetime
from typing import List, Dict, Any

def main(page: ft.Page):
    # ===================== CẤU HÌNH TRANG =====================
    page.title = "2zer011 - Cày Thuê Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 12
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.colors.BLACK
    page.window_width = 400
    page.window_height = 800

    # ===================== DỮ LIỆU =====================
    STORAGE_KEY = "2zer011_orders"
    orders: List[Dict[str, Any]] = []

    # Hàm tải dữ liệu từ client_storage
    def load_orders():
        nonlocal orders
        try:
            data = page.client_storage.get(STORAGE_KEY)
            if data:
                orders = json.loads(data)
            else:
                orders = []
        except Exception as e:
            print(f"Lỗi tải dữ liệu: {e}")
            orders = []
        refresh_ui()

    # Hàm lưu dữ liệu vào client_storage
    def save_orders():
        try:
            page.client_storage.set(STORAGE_KEY, json.dumps(orders))
        except Exception as e:
            print(f"Lỗi lưu dữ liệu: {e}")

    # ===================== THÀNH PHẦN UI CHÍNH =====================
    # Ref cho tổng doanh thu và danh sách
    total_revenue_text = ft.Ref[ft.Text]()
    search_field = ft.Ref[ft.TextField]()
    orders_column = ft.Ref[ft.Column]()

    # Hàm tính tổng doanh thu
    def calculate_total_revenue() -> int:
        total = 0
        for order in orders:
            try:
                total += int(order.get("total_money", 0))
            except:
                pass
        return total

    # Hàm refresh toàn bộ UI (cập nhật danh sách và tổng tiền)
    def refresh_ui():
        if total_revenue_text.current:
            total_revenue_text.current.value = f"{calculate_total_revenue():,} VNĐ"
        update_order_list()
        page.update()

    # Hàm cập nhật danh sách đơn hàng theo tìm kiếm
    def update_order_list():
        if not orders_column.current:
            return
        query = search_field.current.value.lower() if search_field.current else ""
        filtered = [o for o in orders if query in o.get("account", "").lower()]

        cards = []
        for idx, order in enumerate(filtered):
            # Xác định màu sắc theo trạng thái
            status = order.get("status", "Chờ xử lý")
            if status == "Hoàn thành":
                border_color = ft.colors.GREEN_ACCENT_400
                bg_color = ft.colors.with_opacity(0.1, ft.colors.GREEN)
            elif status == "Đang làm":
                border_color = ft.colors.ORANGE_ACCENT_400
                bg_color = ft.colors.with_opacity(0.1, ft.colors.ORANGE)
            else:
                border_color = ft.colors.CYAN_ACCENT_400
                bg_color = ft.colors.with_opacity(0.1, ft.colors.CYAN)

            card = ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.ASSIGNMENT_TURNED_IN, color=border_color),
                        title=ft.Text(f"{order['account']} - Lv.{order.get('current_level','?')}", 
                                      weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        subtitle=ft.Text(f"💰 {order.get('total_money',0):,} VNĐ | 🎯 +{order.get('target_level',0)} Lv",
                                         color=ft.colors.GREY_400),
                    ),
                    ft.Row([
                        ft.Chip(
                            label=ft.Text(status, size=12),
                            bgcolor=bg_color,
                            leading=ft.Icon(ft.icons.CIRCLE, size=8, color=border_color),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        ),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EDIT_NOTE,
                                icon_color=ft.colors.CYAN_200,
                                tooltip="Sửa đơn",
                                on_click=lambda e, o=order: open_order_form(o)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER,
                                icon_color=ft.colors.RED_ACCENT,
                                tooltip="Xóa đơn",
                                on_click=lambda e, o=order: confirm_delete_order(o)
                            ),
                        ], alignment=ft.MainAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                border=ft.border.all(1, border_color),
                border_radius=12,
                padding=8,
                margin=ft.margin.only(bottom=10),
                bgcolor=ft.colors.GREY_900,
                shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.with_opacity(0.3, border_color)),
                animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            )
            cards.append(card)

        orders_column.current.controls = cards if cards else [
            ft.Container(
                content=ft.Text("✨ Không có đơn hàng nào. Nhấn + để thêm.", 
                                color=ft.colors.GREY_500, text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=50)
            )
        ]
        page.update()

    # ===================== FORM THÊM/SỬA =====================
    def open_order_form(existing_order: Dict = None):
        is_edit = existing_order is not None

        # Tạo các trường nhập liệu
        account_field = ft.TextField(
            label="Tài khoản khách",
            prefix_icon=ft.icons.PERSON,
            border_color=ft.colors.CYAN_400,
            value=existing_order.get("account", "") if is_edit else "",
            autofocus=not is_edit,
        )
        password_field = ft.TextField(
            label="Mật khẩu",
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_color=ft.colors.CYAN_400,
            value=existing_order.get("password", "") if is_edit else "",
        )
        current_level = ft.TextField(
            label="Level hiện tại",
            prefix_icon=ft.icons.ARROW_UPWARD,
            border_color=ft.colors.CYAN_400,
            value=str(existing_order.get("current_level", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        primos = ft.TextField(
            label="Nguyên thạch / Diamonds",
            prefix_icon=ft.icons.DIAMOND,
            border_color=ft.colors.CYAN_400,
            value=str(existing_order.get("primos", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        resin = ft.TextField(
            label="Nhựa / Năng lượng (f)",
            prefix_icon=ft.icons.BOLT,
            border_color=ft.colors.CYAN_400,
            value=str(existing_order.get("resin", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        target_level = ft.TextField(
            label="Số level cần lên",
            prefix_icon=ft.icons.TRENDING_UP,
            border_color=ft.colors.CYAN_400,
            value=str(existing_order.get("target_level", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        item_needed = ft.TextField(
            label="Item cần lấy",
            prefix_icon=ft.icons.INVENTORY,
            border_color=ft.colors.CYAN_400,
            value=existing_order.get("item_needed", "") if is_edit else "",
        )
        material_farm = ft.TextField(
            label="Nguyên liệu cần farm",
            prefix_icon=ft.icons.AGRICULTURE,
            border_color=ft.colors.CYAN_400,
            value=existing_order.get("material_farm", "") if is_edit else "",
        )
        total_money = ft.TextField(
            label="Tổng tiền (VNĐ)",
            prefix_icon=ft.icons.MONEY,
            border_color=ft.colors.CYAN_400,
            value=str(existing_order.get("total_money", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        status_dropdown = ft.Dropdown(
            label="Trạng thái",
            border_color=ft.colors.CYAN_400,
            options=[
                ft.dropdown.Option("Chờ xử lý"),
                ft.dropdown.Option("Đang làm"),
                ft.dropdown.Option("Hoàn thành"),
            ],
            value=existing_order.get("status", "Chờ xử lý") if is_edit else "Chờ xử lý",
        )

        # Dialog lưu / hủy
        def save_order(e):
            # Validate bắt buộc
            if not account_field.value:
                page.snack_bar = ft.SnackBar(ft.Text("Vui lòng nhập tài khoản!"), bgcolor=ft.colors.RED_900)
                page.snack_bar.open = True
                page.update()
                return

            try:
                total_money_int = int(total_money.value) if total_money.value else 0
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Tiền phải là số nguyên!"), bgcolor=ft.colors.RED_900)
                page.snack_bar.open = True
                page.update()
                return

            # Xây dựng dict đơn hàng
            new_order = {
                "id": existing_order.get("id") if is_edit else datetime.now().isoformat(),
                "account": account_field.value,
                "password": password_field.value,
                "current_level": current_level.value,
                "primos": primos.value,
                "resin": resin.value,
                "target_level": target_level.value,
                "item_needed": item_needed.value,
                "material_farm": material_farm.value,
                "total_money": total_money_int,
                "status": status_dropdown.value,
            }

            if is_edit:
                # Cập nhật đơn hàng cũ
                for i, o in enumerate(orders):
                    if o.get("id") == existing_order.get("id"):
                        orders[i] = new_order
                        break
            else:
                orders.append(new_order)

            save_orders()
            refresh_ui()
            page.dialog.open = False
            page.update()
            page.snack_bar = ft.SnackBar(ft.Text("✅ Đã lưu đơn hàng!", color=ft.colors.CYAN_ACCENT), bgcolor=ft.colors.GREY_900)
            page.snack_bar.open = True
            page.update()

        def cancel_dialog(e):
            page.dialog.open = False
            page.update()

        form_content = ft.Column([
            ft.Text("📋 THÔNG TIN ĐƠN HÀNG", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
            account_field,
            password_field,
            ft.ResponsiveRow([
                ft.Column(col={"sm": 6}, controls=[current_level]),
                ft.Column(col={"sm": 6}, controls=[primos]),
            ]),
            ft.ResponsiveRow([
                ft.Column(col={"sm": 6}, controls=[resin]),
                ft.Column(col={"sm": 6}, controls=[target_level]),
            ]),
            item_needed,
            material_farm,
            ft.ResponsiveRow([
                ft.Column(col={"sm": 7}, controls=[total_money]),
                ft.Column(col={"sm": 5}, controls=[status_dropdown]),
            ]),
            ft.Row([
                ft.ElevatedButton("Lưu", on_click=save_order, 
                                  style=ft.ButtonStyle(bgcolor=ft.colors.CYAN_800, color=ft.colors.WHITE)),
                ft.TextButton("Hủy", on_click=cancel_dialog),
            ], alignment=ft.MainAxisAlignment.END),
        ], scroll=ft.ScrollMode.AUTO, spacing=10, height=550)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Chỉnh sửa đơn" if is_edit else "Thêm đơn hàng mới"),
            content=form_content,
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.colors.GREY_900,
        )
        page.dialog.open = True
        page.update()

    # ===================== XÁC NHẬN XÓA =====================
    def confirm_delete_order(order):
        def delete(e):
            nonlocal order
            orders[:] = [o for o in orders if o.get("id") != order.get("id")]
            save_orders()
            refresh_ui()
            page.dialog.open = False
            page.update()
            page.snack_bar = ft.SnackBar(ft.Text("🗑️ Đã xóa đơn hàng", color=ft.colors.RED_ACCENT), bgcolor=ft.colors.GREY_900)
            page.snack_bar.open = True
            page.update()

        def cancel_delete(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Xác nhận xóa"),
            content=ft.Text(f"Bạn có chắc muốn xóa đơn của tài khoản '{order.get('account')}'?"),
            actions=[
                ft.TextButton("Hủy", on_click=cancel_delete),
                ft.ElevatedButton("Xóa", on_click=delete, style=ft.ButtonStyle(bgcolor=ft.colors.RED_900)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.colors.GREY_900,
        )
        page.dialog.open = True
        page.update()

    # ===================== BUILD GIAO DIỆN =====================
    # AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("2zer011", weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
        center_title=True,
        bgcolor=ft.colors.BLACK,
        actions=[
            ft.IconButton(ft.icons.ADD_CARD, tooltip="Thêm đơn mới", on_click=lambda e: open_order_form())
        ],
        elevation=0,
    )

    # Thanh tìm kiếm
    search_bar = ft.TextField(
        ref=search_field,
        hint_text="🔍 Tìm theo tài khoản...",
        border_radius=30,
        filled=True,
        bgcolor=ft.colors.GREY_900,
        border_color=ft.colors.CYAN_800,
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: update_order_list(),
    )

    # Tổng doanh thu
    revenue_row = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.ATTACH_MONEY, color=ft.colors.CYAN_ACCENT),
            ft.Text("Tổng doanh thu:", color=ft.colors.GREY_400),
            ft.Text(ref=total_revenue_text, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT, size=20),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=12,
        border_radius=12,
        bgcolor=ft.colors.GREY_900,
        margin=ft.margin.only(top=10, bottom=10),
    )

    # Danh sách đơn hàng
    orders_list = ft.Column(ref=orders_column, spacing=0, scroll=ft.ScrollMode.AUTO)

    # Layout chính
    page.add(
        ft.Column([
            search_bar,
            revenue_row,
            ft.Divider(height=1, color=ft.colors.CYAN_800),
            ft.Text("📦 DANH SÁCH ĐƠN HÀNG", color=ft.colors.CYAN_400, weight=ft.FontWeight.BOLD),
            orders_list,
        ], expand=True, spacing=10)
    )

    # ===================== KHỞI ĐỘNG =====================
    load_orders()

# Chạy ứng dụng
if __name__ == "__main__":
    ft.app(target=main)