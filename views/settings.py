import flet as ft

import logging
logger = logging.getLogger(f"pawplan.{__name__}")



primary = "#0D6EFD"
black = "#000000"
white = "#FFFFFF"
soft_border = "#DDE3EE"
header_blue = "#1450B4"



SETTINGS_OPTIONS = [
    "Change Username",
    "Change Email",
    "Change Password",
    "Change Appearance"
]


def settings_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    # async def go_back(e: ft.ViewPopEvent):
    #     logger.debug("Back to homepage clicked")
    #     try:
    #         if e.view is not None:
    #             print("View pop:", e.view)
    #             page.views.remove(e.view)
    #             top_view = page.views[-1]
    #             await page.push_route(top_view.route)
    #             logger.debug("Route popped")
    #         else:
    #             logger.debug("Route stuck")
    #         # await page.pop_route()
    #     except Exception as ex:
    #         logger.error(f"Error occurred: {ex}")
    async def go_back(e):
        logger.debug("Going back")
        await page.push_route("/homepage")


    def setting_option_tapped(label):
        def handler(e):
            logger.debug("Setting option tapped clicked")
        return handler



    #APPBAR
    appbar = ft.Container(
        padding = ft.Padding.symmetric(horizontal=16, vertical=16),
        bgcolor = header_blue,
        content=ft.Row(
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon = ft.Icons.ARROW_BACK,
                    icon_color = white,
                    on_click = go_back,
                ),

                ft.Text(
                    "Settings",
                    color = white,
                    size = 25,
                    weight = ft.FontWeight.W_800,
                )
            ]
        ),
    )

    def toggle_appearance(e):
            if e.control.value:  # ON
                logger.debug("Dark mode enabled")
                page.theme_mode = ft.ThemeMode.DARK
            else:  # OFF
                logger.debug("Light mode enabled")
                page.theme_mode = ft.ThemeMode.LIGHT
            page.update()

    def setting_row(label):
        if label ==  "Change Appearance":
            trailing = ft.Switch(
                value = page.theme_mode == ft.ThemeMode.DARK,
                active_color = primary,
                on_change = toggle_appearance,
            )
        else:
            trailing = ft.Icon(ft.Icons.CHEVRON_RIGHT, color = "#9CA3AF", size = 20)


        return ft.Container(
            border = ft.Border.all(1, soft_border),
            border_radius = 8,
            padding = ft.Padding.symmetric(horizontal=14, vertical=16),

            on_click = None if label == "Change Appearance" else setting_option_tapped(label),
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Text(
                        label,
                        size = 15,
                        weight = ft.FontWeight.W_400,
                        color = ft.Colors.ON_SURFACE,
                    ),
                    trailing,
                ],
            ),
        )

    settings_list = ft.Container(
        margin = ft.Margin.only(left = 16,
                                right = 16,
                                top = 16
        ),

        content = ft.Column(
            spacing = 10,
            controls = [
                setting_row(label) for label in SETTINGS_OPTIONS
            ],
        ),
    )



    main_content = ft.Column(
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            appbar,
            settings_list,
            ft.Container(height=100),
        ],
    )

    return ft.View(
        route="/settings",
        bgcolor=None,
        padding=0,
        spacing=0,
        controls=[
            main_content
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