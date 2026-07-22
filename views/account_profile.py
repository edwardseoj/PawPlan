import flet as ft

import logging
logger = logging.getLogger(__name__)

from utility.navigation import go_to

primary = "#0D6EFD"
orange = "#F5821F"
header_blue = "#1450B4"
nav_blue = "#0B4FB0"
black = "#000000"
white = "#FFFFFF"
soft_border = "#DDE3EE"
soft_blue_bg = "#EAF0FB"




DESTINATIONS = [
    ft.NavigationBarDestination(
        icon=ft.Icons.WIDGETS_OUTLINED,
        selected_icon=ft.Icons.HOUSE,
        label="Home",
    ),
    ft.NavigationBarDestination(
        icon=ft.Icons.WIDGETS_OUTLINED,
        selected_icon=ft.Icons.CALENDAR_MONTH,
        label="Calendar",
    ),
    ft.NavigationBarDestination(
        icon=ft.Icons.WIDGETS_OUTLINED,
        selected_icon=ft.Icons.PERSON,
        label="Profile",
    ),
]

LOGO_SIZE = 56

NAV_SHRINK_SCALE = 0.6
NAV_HOVER_SCALE = 1.1

# Sample owner data (swap for real data later)
OWNER = {
    "name": "Juan Dela Cruz",
    "username": "@juan_dcruz",
    "age": "20",
    "gender": "Male",
}


def account_profile_view(page: ft.Page) -> ft.View:
    nav_routes = ["/homepage", "/calendar", "/account_profile"]

    def go_help(e):
        logger.info("Help clicked")

    def go_logout(e):
        logger.info("Log out clicked")

    section_state = {"active": "owner"}

    def select_section(section):
        def handler(e):
            section_state["active"] = section
            owner_tab.bgcolor = primary if section == "owner" else soft_blue_bg
            owner_tab_text.color = white if section == "owner" else primary
            pet_tab.bgcolor = primary if section == "pet" else soft_blue_bg
            pet_tab_text.color = white if section == "pet" else primary
            logger.info(f"Profile section switched to: {section}")
            profile_nav_bar.update()
        return handler


    appbar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
        bgcolor=white,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            width=LOGO_SIZE,
                            height=LOGO_SIZE,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Image(
                                src="pawplan_icon.png",
                                width=LOGO_SIZE,
                                height=LOGO_SIZE,
                                fit=ft.BoxFit.CONTAIN,
                            ),
                        ),
                        ft.Row(
                            spacing=2,
                            controls=[
                                ft.Text("Paw", size=22, weight=ft.FontWeight.W_800, color=orange),
                                ft.Text("Plan", size=22, weight=ft.FontWeight.W_800, color="#0B2E6B"),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.NOTIFICATIONS_NONE, color=black, size=26),
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color=black,
                            items=[
                                ft.PopupMenuItem(
                                    content=ft.Text("Settings"),
                                    icon=ft.Icons.SETTINGS_OUTLINED,
                                    on_click=go_to(page, "/settings"),
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Text("Help"),
                                    icon=ft.Icons.HELP_OUTLINE,
                                    on_click=go_help,
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Text("Log out"),
                                    icon=ft.Icons.LOGOUT,
                                    on_click=go_logout,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )

    # Header
    header = ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=16),
        bgcolor=header_blue,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Account Profile",
                    color=white,
                    size=22,
                    weight=ft.FontWeight.W_800,
                ),
            ],
        ),
    )

    # Owner and Pet Profile Toggle
    owner_tab_text = ft.Text(
        "Owner", color=white, weight=ft.FontWeight.W_700, size=14, text_align=ft.TextAlign.CENTER
    )
    pet_tab_text = ft.Text(
        "Pet", color=primary, weight=ft.FontWeight.W_700, size=14, text_align=ft.TextAlign.CENTER
    )

    owner_tab = ft.Container(
        expand=True,
        bgcolor=primary,
        border_radius=8,
        padding=ft.Padding.symmetric(vertical=8, horizontal=0),
        on_click=select_section("owner"),
        content=owner_tab_text,
    )
    pet_tab = ft.Container(
        expand=True,
        bgcolor=soft_blue_bg,
        border_radius=8,
        padding=ft.Padding.symmetric(vertical=8, horizontal=0),
        on_click=select_section("pet"),
        content=pet_tab_text,
    )

    profile_nav_bar = ft.Container(
        bgcolor=soft_blue_bg,
        border_radius=10,
        padding=ft.Padding.all(4),
        content=ft.Row(
            spacing=4,
            controls=[owner_tab, pet_tab],
        ),
    )

    # Owner Profile
    def detail_row(label, value):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, size=13, color="#6B7280", weight=ft.FontWeight.W_600),
                ft.Text(value, size=14, color=black, weight=ft.FontWeight.W_700),
            ],
        )

    owner_profile = ft.Container(
        padding=ft.Padding.all(20),
        bgcolor=white,
        border_radius=12,
        border=ft.Border.all(1, soft_border),
        content=ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=80,
                    height=80,
                    bgcolor=soft_blue_bg,
                    border_radius=40,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.PERSON, size=44, color=primary),
                ),
                ft.Text(
                    OWNER["name"],
                    size=20,
                    weight=ft.FontWeight.W_800,
                    color=black,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Username: {OWNER['username']}",
                    size=13,
                    color="#6B7280",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=1, bgcolor=soft_border),
                detail_row("Age", OWNER["age"]),
                detail_row("Gender", OWNER["gender"]),
            ],
        ),
    )

    profile_details = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=16, bottom=16),
        content=ft.Column(
            spacing=12,
            controls=[
                profile_nav_bar,
                owner_profile,
            ],
        ),
    )

    # ---------------- Floating nav bar ----------------
    nav_state = {"resting_scale": 1.0, "hovering": False}
    # This is the Account Profile page, so "Profile" (index 2) starts active.
    nav_active_index = {"value": 2}
    nav_icon_containers = []
    nav_labels = []

    def apply_nav_scale(scale):
        floating_nav.scale = scale
        floating_nav.update()

    def update_nav_highlight():
        active = nav_active_index["value"]
        for i, (icon_box, label_text) in enumerate(zip(nav_icon_containers, nav_labels)):
            icon_box.bgcolor = orange if i == active else None
            label_text.weight = ft.FontWeight.W_700 if i == active else ft.FontWeight.W_600
        floating_nav.update()

    def nav_destination_tapped(index):
        async def handler(e):
            nav_active_index["value"] = index
            update_nav_highlight()
            restore_nav(e)

            target_route = nav_routes[index]
            logger.info(f"Bottom nav tapped: {target_route}")
            if page.route != target_route:
                await page.push_route(target_route)
        return handler

    def pill_destination(index, label, icon):
        is_active = nav_active_index["value"] == index

        icon_box = ft.Container(
            width=34,
            height=34,
            border_radius=17,
            bgcolor=orange if is_active else None,
            alignment=ft.Alignment.CENTER,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
            content=ft.Icon(icon, color=white, size=20),
        )
        label_text = ft.Text(
            label,
            size=11,
            color=white,
            weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_600,
        )

        nav_icon_containers.append(icon_box)
        nav_labels.append(label_text)

        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border_radius=20,
            on_click=nav_destination_tapped(index),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                tight=True,
                controls=[icon_box, label_text],
            ),
        )

    floating_nav = ft.Container(
        bgcolor=nav_blue,
        border_radius=32,
        padding=ft.Padding.symmetric(horizontal=18, vertical=10),
        margin=ft.Margin.symmetric(horizontal=16, vertical=10),
        scale=1.0,
        animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        shadow=ft.BoxShadow(
            blur_radius=16,
            spread_radius=1,
            color="#00000055",
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            tight=True,
            controls=[
                pill_destination(i, dest.label, dest.selected_icon)
                for i, dest in enumerate(DESTINATIONS)
            ],
        ),
    )

    def shrink_nav():
        nav_state["resting_scale"] = NAV_SHRINK_SCALE
        if not nav_state["hovering"]:
            apply_nav_scale(NAV_SHRINK_SCALE)

    def restore_nav(e=None):
        nav_state["resting_scale"] = 1.0
        if not nav_state["hovering"]:
            apply_nav_scale(1.0)

    def handle_nav_hover(e: ft.HoverEvent):
        is_hovering = e.data == "true"
        nav_state["hovering"] = is_hovering
        if is_hovering:
            apply_nav_scale(NAV_HOVER_SCALE)
        else:
            apply_nav_scale(nav_state["resting_scale"])

    floating_nav.on_click = restore_nav
    floating_nav.on_hover = handle_nav_hover

    def handle_content_scroll(e: ft.OnScrollEvent):
        if e.event_type == ft.ScrollType.USER:
            shrink_nav()

    main_content = ft.Column(
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        on_scroll=handle_content_scroll,
        controls=[
            appbar,
            header,
            profile_details,
            ft.Container(height=100),
        ],
    )

    return ft.View(
        route="/account_profile",
        bgcolor=white,
        padding=0,
        spacing=0,
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    main_content,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[floating_nav],
                    ),
                ],
            )
        ],
    )


def _standalone_main(page: ft.Page):
    page.title = "Account Profile"
    page.window.width = 430
    page.window.height = 900
    page.views.append(account_profile_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(_standalone_main, assets_dir="assets")