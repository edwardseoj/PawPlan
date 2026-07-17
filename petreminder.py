import flet as ft



def main(page: ft.Page):
    page.title = "PawPlan"
    page.bgcolor = "#FFFFFF"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = None

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
        margin=ft.Margin.only(left=16, right=16, top=10),
        content=ft.Text(
            "Today's Tasks",
            size=22,
            weight=ft.FontWeight.W_700,
            color="Black",
        ),
    )

    def create_alarm(e):

        def delete_alarm(e):
            alarm_list_layout.controls.remove(alarm_unit)
            page.update()

        alarm_unit = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=10, bottom=10),
            border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
            padding=15,
            width=float("inf"),
            content=ft.Text("New Reminder")
        )
        alarm_list_layout.controls.append(alarm_unit)
        page.update()

    alarm_list_layout = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

#reminder container
    alarm_cont = ft.Container(
        margin=ft.Margin.only(top=15, bottom=5),
        expand=True,
        border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
        border_radius=10,
        content=alarm_list_layout  # Inject the list layout here
    )

#addbutton
    add_button =  ft.Container(
        margin=ft.Margin.only(top=5,bottom=20),
        align=ft.Alignment.CENTER,
        content=ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color = "white",
            bgcolor="#0B4FB0",
            icon_size=24,
            tooltip="Add reminder",
            on_click=create_alarm,
        )
    )

#navbar
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
                appbar,
                title,
                alarm_cont,
                add_button,
                bottom_nav,
            ],
        )
    )

    page.window.width= 430
    page.window.height= 900


if __name__ == "__main__":
    ft.run(main)
