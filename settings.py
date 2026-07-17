import flet as ft
from flet import NavigationBar


def settings_view(page: ft.Page) -> ft.View:
    primary = "#0D6EFD"
    soft_border = "#DDE3EE"
    white = "#FFFFFF"
    white38 = "#FFFFFF66"

    #TODO: add back button
    appbar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#8C52FF",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Settings", size=20, weight=ft.FontWeight.W_700, color="#FFFFFF"),
            ]
        ),
    )

    #settings buttons
    settings = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        bgcolor=white,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.TextButton(
                    "Change Name"
                ),
                ft.TextButton(
                    "Change Username"
                ),
                ft.TextButton(
                    "Change Password"
                ),
                ft.TextButton(
                    "Change Appearance"
                )
            ],
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

#TODO: implement
# replacement nav bar
    # page.navigation_bar = ft.NavigationBar(
    #     destinations=[
    #         ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Home"),
    #         ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Calendar"),
    #         ft.NavigationBarDestination(
    #             icon=ft.Icons.BOOKMARK_BORDER,
    #             selected_icon=ft.Icons.BOOKMARK,
    #             label="Profile",
    #         ),
    #     ]
    # )

    return ft.View(
        route="/homepage",
        bgcolor="#FFFFFF",
        scroll=None,
        padding=0,
        spacing=0,
        controls=[
            ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    appbar,
                    settings,
                    ft.Container(expand=True),
                    #NavigationBar()
                    bottom_nav,
                ],
            )
        ],
    )

def _standalone_main(page: ft.Page):
    # Lets you run `python homepage.py` on its own to preview this screen
    page.title = "PawPlan"
    page.window.width = 430
    page.window.height = 900
    page.views.append(settings_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(_standalone_main)