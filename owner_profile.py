import flet as ft


def account_profile_view(page: ft.Page) -> ft.View:
    primary = "#0D6EFD"
    white = "#FFFFFF"

    # App bar
    appbar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        bgcolor=white,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("PawPlan", size=20, weight=ft.FontWeight.W_700, color="#000000"),
            ]
        ),
    )

    # Header
    header = ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        bgcolor=primary,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    "Account Profile",
                    color=white,
                    size=18,
                    weight=ft.FontWeight.W_700,
                ),
                ft.Button(
                    "Edit",
                    bgcolor=white,
                    color=primary,
                    on_click=lambda e: None,
                ),
            ],
        ),
    )

    # Profile details
    profile_details = ft.Container(
        margin=ft.Margin.symmetric(horizontal=16, vertical=12),
        padding=ft.Padding.all(12),
        bgcolor=white,
        border_radius=12,
        border=ft.Border.all(1, "#DDE3EE"),
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("John Doe", size=22, weight=ft.FontWeight.W_700),
                ft.Text("Username: johndoe12", size=16),
                ft.Text("Age: 21", size=16),
                ft.Text("Gender: Male", size=16),
                ft.Text("Pets:", size=16, weight=ft.FontWeight.W_600),
                ft.Text("Pet 1: Bella", size=14),
                ft.Text("Pet 2: Max", size=14),
            ],
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
                    "Home", style=ft.ButtonStyle(color=white), on_click=lambda e: page.go("/homepage")
                ),
                ft.TextButton(
                    "Calendar", style=ft.ButtonStyle(color=white), on_click=lambda e: None
                ),
                ft.TextButton(
                    "Profile", style=ft.ButtonStyle(color=white), on_click=lambda e: page.go("/account_profile")
                ),
            ],
        ),
    )

    return ft.View(
        route="/account_profile",
        bgcolor=white,
        scroll=None,
        padding=0,
        spacing=0,
        controls=[
            ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    appbar,
                    header,
                    profile_details,
                    ft.Container(expand=True),
                    bottom_nav,
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
    ft.run(_standalone_main)
