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
#header
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

#page title
    title = ft.Container(
        expand=True,
        bgcolor="#ff751f",
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.only(left=16, right=16, top=10),
        content=ft.Text(
            "Pet Profile",
            size=22,
            weight=ft.FontWeight.W_700,
            color="White",
        ),
    )

# Your profile container with no margins
    profile_cont = ft.Container(
        bgcolor="#0B4FB0",
        expand=True,
        alignment=ft.Alignment.CENTER,
        margin=ft.Margin.all(0),
        padding=ft.Padding.all(0),
        content=ft.Row(
            controls=[
                ft.Image(
                    src="https://example.com/this-image-does-not-exist.png",
                    width=200,
                    height=200,
                    error_content=ft.Container(
                        content=ft.Icon(ft.Icons.BROKEN_IMAGE, size=200, color=ft.Colors.GREY_400),
                        alignment=ft.Alignment.CENTER,
                        bgcolor=ft.Colors.GREY_200,
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Bottom nav with no margins
    bottom_nav = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=20),
        bgcolor="#0B4FB0",
        border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
        margin=ft.Margin.all(0),  # Remove any margins
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.TextButton(
                    "Home", style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=lambda e: None
                ),
                ft.TextButton(
                    "Calendar",
                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                    on_click=lambda e: None,
                ),
                ft.TextButton(
                    "Profile",
                    style=ft.ButtonStyle(color=ft.Colors.WHITE),
                    on_click=lambda e: None,
                ),
            ],
        ),
    )

# Main layout
    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(
                    expand=True,
                    margin=ft.Margin.all(0),
                    padding=ft.Padding.all(0),
                    content=ft.Column(
                        controls=[
                            title,
                            profile_cont,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,  # Remove spacing between title and profile_cont
                        tight=True,  # Minimize spacing
                    ),
                ),
                bottom_nav,
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
