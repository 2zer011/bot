import flet as ft
import json
from datetime import datetime
from typing import List, Dict, Any

def main(page: ft.Page):
    # ===================== CẤU HÌNH TRANG =====================
    page.title = "2zer011 - Cày Thuê Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 12
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = ft.colors.BLACK
    page.window_width = 400
    page.window_height = 800

    # Gradient background tạo hiệu ứng glassmorphism nền
    page.decor = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.BLUE_GREY_900, ft.colors.BLACK],
        )
    )

    # ===================== DỮ LIỆU =====================
    STORAGE_KEY = "2zer011_orders"
    orders: List[Dict[str, Any]] = []

    def load_orders():
        nonlocal orders
        try:
            data = page.client_storage.get(STORAGE_KEY)
            if data:
                orders = json.loads(data)
            else:
                orders = []
        except:
            orders = []
        refresh_ui()

    def save_orders():
        try:
            page.client_storage.set(STORAGE_KEY, json.dumps(orders))
        except:
            pass

    # ===================== UI REFS =====================
    total_revenue_text = ft.Ref[ft.Text]()
    search_field = ft.Ref[ft.TextField]()
    orders_column = ft.Ref[ft.Column]()

    def calculate_total_revenue() -> int:
        return sum(int(o.get("total_money", 0) or 0) for o in orders)

    def refresh_ui():
        if total_revenue_text.current:
            total_revenue_text.current.value = f"{calculate_total_revenue():,} VNĐ"
        update_order_list()
        page.update()

    # ===================== DANH SÁCH ĐƠN HÀNG =====================
    def build_order_card(order: Dict, index: int) -> ft.Container:
        status = order.get("status", "Chờ xử lý")
        if status == "Hoàn thành":
            accent = ft.colors.GREEN_ACCENT_400
            bg_tint = ft.colors.with_opacity(0.15, ft.colors.GREEN)
        elif status == "Đang làm":
            accent = ft.colors.ORANGE_ACCENT_400
            bg_tint = ft.colors.with_opacity(0.15, ft.colors.ORANGE)
        else:
            accent = ft.colors.CYAN_ACCENT_400
            bg_tint = ft.colors.with_opacity(0.1, ft.colors.CYAN)

        # Hiển thị thêm thông tin ngắn gọn
        detail = f"🎯 +{order.get('target_level','?')} Lv | 💎 {order.get('primos','?')} | ⚡ {order.get('resin','?')}"

        return ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.icons.ASSIGNMENT_TURNED_IN, color=accent),
                    title=ft.Row([
                        ft.Text(f"{order['account']}", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Container(  # Chip trạng thái nhỏ gọn
                            content=ft.Text(status, size=11, color=ft.colors.BLACK),
                            bgcolor=accent,
                            border_radius=20,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        )
                    ], spacing=10),
                    subtitle=ft.Column([
                        ft.Text(detail, color=ft.colors.GREY_400, size=12),
                        ft.Text(f"💰 {order.get('total_money',0):,} VNĐ", color=accent, weight=ft.FontWeight.BOLD),
                    ], spacing=2),
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
            ]),
            border=ft.border.all(1.5, accent),
            border_radius=16,
            padding=10,
            margin=ft.margin.only(bottom=12),
            bgcolor=ft.colors.GREY_900,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.4, accent)),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
            animate_opacity=300,
        )

    def update_order_list():
        if not orders_column.current:
            return
        query = search_field.current.value.lower().strip() if search_field.current else ""
        filtered = [o for o in orders if query in o.get("account", "").lower()]

        cards = [build_order_card(o, i) for i, o in enumerate(filtered)]
        orders_column.current.controls = cards if cards else [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.INBOX, size=48, color=ft.colors.GREY_700),
                    ft.Text("Chưa có đơn hàng nào", color=ft.colors.GREY_500, size=16),
                    ft.ElevatedButton(
                        "Tạo đơn đầu tiên",
                        on_click=lambda e: open_order_form(),
                        style=ft.ButtonStyle(bgcolor=ft.colors.CYAN_800, color=ft.colors.WHITE),
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=60),
            )
        ]
        page.update()

    # ===================== FORM THÊM / SỬA =====================
    def open_order_form(existing_order: Dict = None):
        is_edit = existing_order is not None

        # Tạo style chung cho TextField
        field_style = {
            "border_color": ft.colors.CYAN_400,
            "focused_border_color": ft.colors.CYAN_ACCENT,
            "cursor_color": ft.colors.CYAN_ACCENT,
            "text_style": ft.TextStyle(color=ft.colors.WHITE),
        }

        account_field = ft.TextField(
            label="Tài khoản", prefix_icon=ft.icons.PERSON,
            value=existing_order.get("account", "") if is_edit else "",
            **field_style
        )
        password_field = ft.TextField(
            label="Mật khẩu", prefix_icon=ft.icons.LOCK,
            password=True, can_reveal_password=True,
            value=existing_order.get("password", "") if is_edit else "",
            **field_style
        )
        current_level = ft.TextField(
            label="Level hiện tại", prefix_icon=ft.icons.ARROW_UPWARD,
            value=str(existing_order.get("current_level", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER, **field_style
        )
        primos = ft.TextField(
            label="Nguyên thạch / Diamonds", prefix_icon=ft.icons.DIAMOND,
            value=str(existing_order.get("primos", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER, **field_style
        )
        resin = ft.TextField(
            label="Nhựa / Năng lượng", prefix_icon=ft.icons.BOLT,
            value=str(existing_order.get("resin", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER, **field_style
        )
        target_level = ft.TextField(
            label="Số level cần lên", prefix_icon=ft.icons.TRENDING_UP,
            value=str(existing_order.get("target_level", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER, **field_style
        )
        item_needed = ft.TextField(
            label="Item cần lấy", prefix_icon=ft.icons.INVENTORY,
            value=existing_order.get("item_needed", "") if is_edit else "",
            **field_style
        )
        material_farm = ft.TextField(
            label="Nguyên liệu cần farm", prefix_icon=ft.icons.AGRICULTURE,
            value=existing_order.get("material_farm", "") if is_edit else "",
            **field_style
        )
        total_money = ft.TextField(
            label="Tổng tiền (VNĐ)", prefix_icon=ft.icons.MONEY,
            value=str(existing_order.get("total_money", "")) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER, **field_style
        )
        status_dropdown = ft.Dropdown(
            label="Trạng thái",
            border_color=ft.colors.CYAN_400,
            focused_border_color=ft.colors.CYAN_ACCENT,
            options=[
                ft.dropdown.Option("Chờ xử lý"),
                ft.dropdown.Option("Đang làm"),
                ft.dropdown.Option("Hoàn thành"),
            ],
            value=existing_order.get("status", "Chờ xử lý") if is_edit else "Chờ xử lý",
        )

        def save_order(e):
            if not account_field.value:
                show_snack("Vui lòng nhập tài khoản!", is_error=True)
                return
            try:
                money = int(total_money.value) if total_money.value else 0
            except ValueError:
                show_snack("Tiền phải là số nguyên!", is_error=True)
                return

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
                "total_money": money,
                "status": status_dropdown.value,
            }

            if is_edit:
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
            show_snack("✅ Đã lưu đơn hàng!")

        def cancel_dialog(e):
            page.dialog.open = False
            page.update()

        form_content = ft.Column([
            ft.Text("📋 THÔNG TIN ĐƠN HÀNG", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
            ft.Divider(height=1, color=ft.colors.CYAN_800),
            account_field, password_field,
            ft.ResponsiveRow([
                ft.Column(col={"sm": 6}, controls=[current_level]),
                ft.Column(col={"sm": 6}, controls=[primos]),
            ]),
            ft.ResponsiveRow([
                ft.Column(col={"sm": 6}, controls=[resin]),
                ft.Column(col={"sm": 6}, controls=[target_level]),
            ]),
            item_needed, material_farm,
            ft.ResponsiveRow([
                ft.Column(col={"sm": 7}, controls=[total_money]),
                ft.Column(col={"sm": 5}, controls=[status_dropdown]),
            ]),
            ft.Row([
                ft.ElevatedButton("Lưu", on_click=save_order,
                                  style=ft.ButtonStyle(bgcolor=ft.colors.CYAN_800, color=ft.colors.WHITE)),
                ft.TextButton("Hủy", on_click=cancel_dialog),
            ], alignment=ft.MainAxisAlignment.END),
        ], spacing=12, height=550, scroll=ft.ScrollMode.ADAPTIVE)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Chỉnh sửa đơn" if is_edit else "Thêm đơn hàng mới",
                          color=ft.colors.CYAN_ACCENT),
            content=form_content,
            actions=[],
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor=ft.colors.GREY_900,
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=24),
        )
        page.dialog.open = True
        page.update()

    # ===================== XÓA ĐƠN =====================
    def confirm_delete_order(order):
        def delete(e):
            orders[:] = [o for o in orders if o.get("id") != order.get("id")]
            save_orders()
            refresh_ui()
            page.dialog.open = False
            page.update()
            show_snack("🗑️ Đã xóa đơn hàng", is_error=True)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Xác nhận xóa", color=ft.colors.RED_ACCENT),
            content=ft.Text(f"Bạn có chắc muốn xóa đơn của '{order.get('account')}'?"),
            actions=[
                ft.TextButton("Hủy", on_click=lambda e: close_dialog()),
                ft.ElevatedButton("Xóa", on_click=delete,
                                  style=ft.ButtonStyle(bgcolor=ft.colors.RED_900, color=ft.colors.WHITE)),
            ],
            bgcolor=ft.colors.GREY_900,
        )
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    # ===================== TIỆN ÍCH =====================
    def show_snack(msg: str, is_error=False):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_900 if is_error else ft.colors.GREY_800,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    # ===================== XUẤT / NHẬP DỮ LIỆU (BACKUP) =====================
    def export_data(e):
        try:
            file_picker = ft.FilePicker(on_result=lambda r: save_export(r))
            page.overlay.append(file_picker)
            page.update()
            file_picker.save_file(
                file_name=f"2zer011_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                allowed_extensions=["json"]
            )
        except Exception as ex:
            show_snack(f"Lỗi xuất file: {ex}", True)

    def save_export(result: ft.FilePickerResultEvent):
        if result.path:
            try:
                with open(result.path, "w", encoding="utf-8") as f:
                    json.dump(orders, f, ensure_ascii=False, indent=2)
                show_snack(f"✅ Đã xuất {len(orders)} đơn hàng!")
            except Exception as ex:
                show_snack(f"Lỗi ghi file: {ex}", True)

    def import_data(e):
        file_picker = ft.FilePicker(on_result=lambda r: load_import(r))
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["json"])

    def load_import(result: ft.FilePickerResultEvent):
        if result.files:
            try:
                with open(result.files[0].path, "r", encoding="utf-8") as f:
                    imported = json.load(f)
                nonlocal orders
                orders = imported
                save_orders()
                refresh_ui()
                show_snack(f"✅ Đã nhập {len(orders)} đơn hàng!")
            except Exception as ex:
                show_snack(f"File không hợp lệ: {ex}", True)

    # ===================== GIAO DIỆN CHÍNH =====================
    page.appbar = ft.AppBar(
        title=ft.Text("2zer011", weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT),
        center_title=True,
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
        toolbar_height=60,
        elevation=0,
        actions=[
            ft.PopupMenuButton(
                icon=ft.icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(text="Xuất dữ liệu (Backup)", on_click=export_data),
                    ft.PopupMenuItem(text="Nhập dữ liệu (Restore)", on_click=import_data),
                ],
                tooltip="Tùy chọn",
            ),
            ft.IconButton(ft.icons.ADD_CARD, tooltip="Thêm đơn mới", on_click=lambda e: open_order_form()),
        ],
    )

    # Thanh tìm kiếm
    search_bar = ft.TextField(
        ref=search_field,
        hint_text="🔍 Tìm theo tài khoản...",
        border_radius=30,
        filled=True,
        bgcolor=ft.colors.GREY_900,
        border_color=ft.colors.CYAN_800,
        focused_border_color=ft.colors.CYAN_ACCENT,
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: update_order_list(),
    )

    # Tổng doanh thu
    revenue_container = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.ATTACH_MONEY, color=ft.colors.CYAN_ACCENT, size=30),
            ft.Column([
                ft.Text("TỔNG DOANH THU", color=ft.colors.GREY_400, size=12),
                ft.Text(ref=total_revenue_text, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_ACCENT, size=24),
            ], spacing=0),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=16,
        border_radius=16,
        bgcolor=ft.colors.with_opacity(0.7, ft.colors.GREY_900),
        border=ft.border.all(1, ft.colors.CYAN_800),
        margin=ft.margin.only(top=10, bottom=10),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.colors.CYAN_900, ft.colors.BLACK],
        ),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.with_opacity(0.3, ft.colors.CYAN_400)),
    )

    # Danh sách đơn hàng
    orders_list = ft.Column(ref=orders_column, spacing=0, scroll=ft.ScrollMode.ADAPTIVE)

    # Layout chính
    page.add(
        ft.Column([
            search_bar,
            revenue_container,
            ft.Divider(height=1, color=ft.colors.CYAN_800),
            ft.Row([
                ft.Text("📦 DANH SÁCH ĐƠN HÀNG", color=ft.colors.CYAN_400, weight=ft.FontWeight.BOLD, size=16),
                ft.Text(f"{len(orders)} đơn", color=ft.colors.GREY_500),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            orders_list,
        ], expand=True, spacing=10)
    )

    # Khởi tạo dữ liệu
    load_orders()

if __name__ == "__main__":
    ft.app(target=main)