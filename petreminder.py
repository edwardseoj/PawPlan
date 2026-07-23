import flet as ft


def main(page: ft.Page):
    page.title = "PawPlan"
    page.bgcolor = "#FFFFFF"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = None
    page.padding = 0

    primary = "#0D6EFD"
    soft_border = "#DDE3EE"
    white = "#FFFFFF"
    white38 = "#FFFFFF66"

    # page title
    title = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=10),
        align=ft.Alignment.CENTER,
        content=ft.Text(
            "Reminders",
            size=22,
            weight=ft.FontWeight.W_700,
            color="Black",
        ),
    )

    def create_alarm(e):
        def delete_alarm(e):
            alarm_list_layout.controls.remove(alarm_unit)
            page.update()

    # main alarm container
        alarm_unit = ft.Container(
            margin=ft.Margin.all(10),
            border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
            padding=10,
            border_radius=10,
            width=float("inf"),
            content=ft.Row(
                controls=[
                    #container subcont
                    ft.Container(
                        expand=3,
                        content=ft.Column(
                            controls=[
                                ft.Checkbox(
                                    value=False,
                                    on_change=lambda e: toggle_checkbox(e),
                                    fill_color={
                                        ft.ControlState.PRESSED: ft.Colors.BLUE,
                                        ft.ControlState.SELECTED: ft.Colors.BLUE,
                                    },
                                    check_color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    # placeholder time
                                    "8:00 AM",
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=2,
                        ),
                        align=ft.Alignment.CENTER,
                        border_radius=8,
                        padding=5,
                    ),
                    ft.Container(
                        expand=7,
                        content=ft.Column(
                            controls=[
                                #top portion
                                ft.Container(
                                    expand=1,
                                    content=ft.Row(
                                        controls=[
                                            ft.Text(
                                                "Reminder",
                                                size=16,
                                                weight=ft.FontWeight.W_600,
                                                color="Black",
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.DELETE_OUTLINE,
                                                icon_size=20,
                                                on_click=delete_alarm,
                                                tooltip="Delete",
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    padding=ft.Padding.only(
                                        left=10, right=5, top=5, bottom=5
                                    ),
                                ),
                                ft.Divider(height=1, color=ft.Colors.GREY_300),
                                #bottom portion
                                ft.Container(
                                    expand=1,
                                    content=ft.Row(
                                        controls=[
                                            ft.Text(
                                                "Repeat: Daily",
                                                size=12,
                                                color=ft.Colors.GREY_600,
                                            ),
                                            ft.Text(
                                                "On",
                                                size=12,
                                                color=ft.Colors.GREEN,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    padding=ft.Padding.only(
                                        left=10, right=10, top=5, bottom=5
                                    ),
                                ),
                            ],
                            spacing=0,
                            expand=True,
                        ),
                    ),
                ],
                spacing=8,
                expand=True,
            ),
        )
        alarm_list_layout.controls.append(alarm_unit)
        page.update()


    def toggle_checkbox(e):
        e.control.value = not e.control.value
        e.control.update()

    alarm_list_layout = ft.Column(
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    # reminder container
    alarm_cont = ft.Container(
        margin=ft.Margin.only(top=15, bottom=5, left=16, right=16),
        expand=True,
        border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
        border_radius=10,
        content=alarm_list_layout,
    )

    # add button
    add_button = ft.Container(
        margin=ft.Margin.only(top=5, bottom=20),
        align=ft.Alignment.CENTER,
        content=ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="white",
            bgcolor="#0B4FB0",
            icon_size=24,
            tooltip="Add reminder",
            on_click=create_alarm,
        ),
    )

    # navbar
    bottom_nav = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=20),
        bgcolor="#0B4FB0",
        border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.TextButton(
                    "Home", style=ft.ButtonStyle(color=white), on_click=lambda e: None
                ),
                ft.TextButton(
                    "Calendar",
                    style=ft.ButtonStyle(color=white),
                    on_click=lambda e: None,
                ),
                ft.TextButton(
                    "Profile",
                    style=ft.ButtonStyle(color=white),
                    on_click=lambda e: None,
                ),
            ],
        ),
    )

    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                title,
                alarm_cont,
                add_button,
                bottom_nav,
            ],
        )
    )

    page.window.width = 430
    page.window.height = 900


if __name__ == "__main__":
    ft.run(main)