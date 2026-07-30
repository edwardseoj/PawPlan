import flet as ft
import logging

from utility.navigation import go_to

logger = logging.getLogger(f"pawplan.{__name__}")

# Sample data (wire up to Firestore later)
TODAYS_TASKS = [
    {"time": "8:00 am Daily", "task": "Feed Bella"},
    {"time": "12:00 pm Daily", "task": "Walk Max"},
    {"time": "10:00am, June 13", "task": "Vet Appointment for Bella"},
]

UPCOMING_TASKS = []

# colors used for the task pills
pill_colors = ["#6C5CE7", "#F05648"]

black = "#000000"
white = "#FFFFFF"
orange = "#F5821F"
nav_blue = "#0B4FB0"

NAV_SHRINK_SCALE = 0.6
NAV_HOVER_SCALE = 1.1

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

    pill_nav_routes = ["/homepage", "/taskboard", "/account_profile"]

    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Taskboard",
                size=28,
                weight=ft.FontWeight.W_800,
                color=black,
            ),
        ],
    )

    appbar = ft.Container(
        padding=ft.Padding.only(left=8, right=20, top=16, bottom=8),
        bgcolor=white,
        content=header_row,
    )

    def task_pill(label, index):
        color = "#0B4FB0"
        return ft.Container(
            margin=ft.Margin.only(top=6, bottom=6),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border_radius=30,
            bgcolor=color,
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        label,
                        color=white,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        expand=True,
                    ),
                ],
            ),
        )

    def task_label(item):
        return f"{item['time']} - {item['task']}"

    today_pills = ft.Column(
        spacing=0,
        controls=[task_pill(task_label(t), i) for i, t in enumerate(TODAYS_TASKS)],
    )

    upcoming_pills = ft.Column(
        spacing=0,
        controls=(
            [task_pill(task_label(t), i) for i, t in enumerate(UPCOMING_TASKS)]
            if UPCOMING_TASKS
            else [
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(vertical=20),
                    content=ft.Text(
                        "No upcoming tasks",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.BLACK,
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

    def section_box(content_column, min_height=None):
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

    add_task_button = ft.Container(
        content=ft.Column(
            controls=[
                ft.Button(
                    content=ft.Row(
                        spacing=6,
                        tight=True,
                        controls=[
                            ft.Icon(ft.Icons.ADD, color=white, size=18),
                            ft.Text("Add Task", color=white, weight=ft.FontWeight.W_700),
                        ],
                    ),
                    bgcolor="#0D6EFD",
                    on_click=go_to(page, "/taskboard_input"),
                ),
            ],
        ),
        alignment=ft.Alignment.CENTER,
        margin=ft.Margin.only(top=20),
    )

    # ---------------- Floating nav bar ----------------
    nav_state = {"resting_scale": 1.0, "hovering": False}
    # Taskboard is index 1 in DESTINATIONS, so it starts active since we're on this page.
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
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        on_scroll=handle_content_scroll,
        controls=[
            appbar,
            todays_task_section,
            upcoming_task_section,
            add_task_button,
            ft.Container(height=100),
        ],
    )

    return ft.View(
        route="/taskboard",
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
    page.title = "PawPlan"
    page.window.width = 430
    page.window.height = 900
    page.views.append(taskboard_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(_standalone_main)