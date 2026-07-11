import flet as ft


def main(page: ft.Page):
    page.title = "PawPlan"
    page.bgcolor = "#FFFFFF"
    page.scroll = None

    primary = "#0D6EFD"
    soft_border = "#DDE3EE"
    white = "#FFFFFF"
    white38 = "#FFFFFF66"

    appbar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#FFFFFF",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("PawPlan", size=20, weight=ft.FontWeight.W_700, color="#000000"),
            ]
        ),
    )


    tasks = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=10),
        content=ft.Text(
            "Today's Tasks",
            size=22,
            weight=ft.FontWeight.W_700,
            color="Black",
        ),
    )

    bottom_nav = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
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
            controls=[
                appbar,
                tasks,
                ft.Container(expand=True),
                bottom_nav,
            ],
        )
    )

    page.window.width= 430
    page.window.height= 900


if __name__ == "__main__":
    ft.run(main)