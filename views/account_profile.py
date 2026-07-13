import flet as ft

from utility.navigation import go_to


def account_profile_view(page: ft.Page) -> ft.View:

    primary = "#0D6EFD"
    white = "#FFFFFF"
    black = "#000000"

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

    owner_profile = ft.Container(
        width = 280,
        padding = ft.Padding.all(20),
        bgcolor=white,
        border_radius=12,
        border = ft.Border.all(1, "#DDE3EE"),
        content = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Juan Dela Cruz",
                    size = 40,
                    weight=ft.FontWeight.W_700,
                    color = black,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text (
                    "Username: @juan_dcruz",
                    size = 20,
                    weight=ft.FontWeight.W_700,
                    color = black,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text (
                    "Age: 20",
                    size = 20,
                    weight=ft.FontWeight.W_700,
                    color = black,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text (
                    "Gender: Male",
                    size = 20,
                    weight=ft.FontWeight.W_700,
                    color = black,
                    text_align=ft.TextAlign.CENTER,
                )
            ]
        )

    )



    profile_details = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=140, bottom=16),
        bgcolor=white,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[owner_profile],
        )
    )



    bottom_nav = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#0B4FB0",
        border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.TextButton(
                    "Home", style=ft.ButtonStyle(color=white), on_click=go_to(page, "/homepage")
                ),
                ft.TextButton(
                    "Calendar",
                    style=ft.ButtonStyle(color=white),
                    on_click=lambda e: None,
                ),
                ft.TextButton(
                    "Profile",
                    style=ft.ButtonStyle(color=white),
                    on_click=go_to(page, "/account_profile"),
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


# def _standalone_main(page: ft.Page):
#     page.title = "Account Profile"
#     page.window.width = 430
#     page.window.height = 900
#     page.views.append(account_profile_view(page))
#     page.update()
#
#
# if __name__ == "__main__":
#     ft.run(_standalone_main, port=8550, view=ft.AppView.WEB_BROWSER)
