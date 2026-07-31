import flet as ft
import logging

from utility.navigation import go_to
from utility.theme import get_colors, ON_BRAND, ORANGE, NAV_BLUE

logger = logging.getLogger(f"pawplan.{__name__}")


TODAYS_TASKS = [
    {"time": "8:00 am Daily", "task": "Feed Bella", "done": False},
    {"time": "12:00 pm Daily", "task": "Walk Max", "done": False},
    {"time": "10:00am, June 13", "task": "Vet Appointment for Bella", "done": False},
]

UPCOMING_TASKS = []

# colors used for the task pills
pill_colors = ["#6C5CE7", "#F05648"]

orange = ORANGE
nav_blue = NAV_BLUE

NAV_SHRINK_SCALE = 0.6
NAV_HOVER_SCALE = 1.1
LOGO_SIZE = 70

DESTINATIONS = [
    ft.NavigationBarDestination(
        icon=ft.Icons.WIDGETS_OUTLINED,
        selected_icon=ft.Icons.HOUSE,
        label="Home",
    ),
    ft.NavigationBarDestination(
        icon=ft.Icons.WIDGETS_OUTLINED,
        selected_icon=ft.Icons.CHECKLIST,
        label="Taskboard",
    ),
    ft.NavigationBarDestination(
        icon=ft.Icons.WIDGETS_OUTLINED,
        selected_icon=ft.Icons.PERSON,
        label="Profile",
    ),
]


def taskboard_view(page: ft.Page) -> ft.View:
    toggleColor = get_colors(page)
    black = toggleColor["text"]
    white = toggleColor["surface"]


    pill_nav_routes = ["/homepage", "/taskboard", "/account_profile"]

    # ---------------- Branded app header (logo, notifications, settings) ----------------
    # Matches homepage.py's appbar so the same top bar appears on every main tab.
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
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )

    appbar_divider = ft.Container(height=5, bgcolor=orange)

    page_title = ft.Container(
        padding=ft.Padding.only(left=8, right=20, top=16, bottom=8),
        bgcolor=white,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Taskboard",
                    size=28,
                    weight=ft.FontWeight.W_800,
                    color=black,
                ),
            ],
        ),
    )

    def task_label(item):
        return f"{item['time']} - {item['task']}"

    def task_pill(item, index):
        color = "#0B4FB0"

        label_text = ft.Text(
            task_label(item),
            color=ON_BRAND,
            size=14,
            weight=ft.FontWeight.W_600,
            expand=True,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH if item["done"] else None,
                decoration_color=ON_BRAND,
            ),
        )

        pill_container = ft.Container(
            margin=ft.Margin.only(top=6, bottom=6),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=30,
            bgcolor=color,
            opacity=0.5 if item["done"] else 1.0,
            animate_opacity=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

        def on_check_change(e: ft.ControlEvent):
            item["done"] = e.control.value
            label_text.style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH if item["done"] else None,
                decoration_color=ON_BRAND,
            )
            pill_container.opacity = 0.5 if item["done"] else 1.0
            label_text.update()
            pill_container.update()

        checkbox = ft.Checkbox(
            value=item["done"],
            on_change=on_check_change,
            check_color=color,
            fill_color=ON_BRAND,
            active_color=ON_BRAND,
        )

        pill_container.content = ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                checkbox,
                label_text,
            ],
        )

        return pill_container

    today_pills = ft.Column(
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[task_pill(t, i) for i, t in enumerate(TODAYS_TASKS)],
    )

    upcoming_pills = ft.Column(
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        controls=(
            [task_pill(t, i) for i, t in enumerate(UPCOMING_TASKS)]
            if UPCOMING_TASKS
            else [
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(vertical=20),
                    content=ft.Text(
                        "No upcoming tasks",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=toggleColor["muted_text"],
                    ),
                )
            ]
        ),
    )

    def section_header(label):
        return ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=24, bottom=10),
            content=ft.Text(
                label,
                size=22,
                weight=ft.FontWeight.W_800,
                color=black,
            ),
        )

    def section_box(content_column, min_height=300):
        return ft.Container(
            margin=ft.Margin.only(left=20, right=20),
            padding=ft.Padding.symmetric(horizontal=10, vertical=10),
            border=ft.Border.all(width=2.5, color=black),
            border_radius=20,
            height=min_height,
            content=content_column,
        )

    todays_task_section = ft.Column(
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            section_header("Today's Task"),
            section_box(today_pills),
        ],
    )

    upcoming_task_section = ft.Column(
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            section_header("Upcoming Task"),
            section_box(upcoming_pills, min_height=300),
        ],
    )

    nav_state = {"resting_scale": 1.0, "hovering": False}
    nav_active_index = {"value": 1}
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

            target_route = pill_nav_routes[index]
            logger.debug(f"Bottom nav tapped: {target_route}")
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
            content=ft.Icon(icon, color=ON_BRAND, size=20),
        )
        label_text = ft.Text(
            label,
            size=11,
            color=ON_BRAND,
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
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        on_scroll=handle_content_scroll,
        controls=[
            appbar,
            appbar_divider,
            page_title,
            todays_task_section,
            upcoming_task_section,
            ft.Container(height=100),
        ],
    )

    floating_nav_overlay = ft.Container(
        left=0,
        right=0,
        bottom=20,
        alignment=ft.Alignment.CENTER,
        content=floating_nav,
    )

    return ft.View(
        route="/taskboard",
        bgcolor=toggleColor["bg"],
        padding=0,
        spacing=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    main_content,
                    floating_nav_overlay,
                ],
            )
        ],
    )


def _standalone_main(page: ft.Page):
    page.title = "PawPlan"
    page.window.width = 430
    page.window.height = 900
    page.views.append(taskboard_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(_standalone_main)