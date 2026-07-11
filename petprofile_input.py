import flet as ft

import logging
logger = logging.getLogger(__name__)

primary = "#0D6EFD"
header_blue = "#1450B4"
white = "#FFFFFF"
black = "#000000"
soft_border = "#DDE3EE"


def petprofile_input_view(page: ft.Page) -> ft.View:
    async def go_back(e):
        logger.info("Back to homepage clicked")
        try:
            await page.pop_route()
            logger.info("Route popped")
        except Exception as ex:
            logger.error(f"Error occurred: {ex}")

    # content variables
    pet_name = ft.TextField(label="Pet Name", width=300, text_align=ft.TextAlign.CENTER)
    pet_type = ft.Dropdown(
        label="Pet Type",
        options=[
            ft.dropdown.Option("Dog"),
            ft.dropdown.Option("Cat"),
        ],
        width=300,
    )
    pet_age = ft.TextField(
        label="Age",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
    )
    pet_breed = ft.TextField(label="Breed", width=300, text_align=ft.TextAlign.CENTER)

    def close_confirm_dialog(e):
        logger.info("Pet profile confirmation dismissed")
        page.pop_dialog()

    def submit_profile(e):
        logger.info(
            "Submitting pet profile: "
            f"name={pet_name.value}, type={pet_type.value}, "
            f"age={pet_age.value}, breed={pet_breed.value}"
        )
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Pet Profile Saved"),
            content=ft.Text(
                f"Name: {pet_name.value}\n"
                f"Type: {pet_type.value}\n"
                f"Age: {pet_age.value}\n"
                f"Breed: {pet_breed.value}"
            ),
            actions=[ft.TextButton("OK", on_click=close_confirm_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(confirm_dialog)

    submit_btn = ft.Button(
        content=ft.Text("Save Profile", color=white, weight=ft.FontWeight.W_700),
        bgcolor=primary,
        on_click=submit_profile,
    )

    header = ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=16),
        bgcolor=header_blue,
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=white,
                    on_click=go_back,
                ),
                ft.Text(
                    "Add New Pet",
                    color=white,
                    size=22,
                    weight=ft.FontWeight.W_800,
                ),
            ],
        ),
    )

    form = ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=24),
        content=ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                pet_name,
                pet_type,
                pet_age,
                pet_breed,
                ft.Container(height=10),
                submit_btn,
            ],
        ),
    )

    return ft.View(
        route="/petprofile",
        bgcolor=white,
        padding=0,
        spacing=0,
        controls=[
            ft.Column(
                spacing=0,
                controls=[
                    header,
                    form,
                ],
            )
        ],
    )


def _standalone_main(page: ft.Page):
    # Lets you run `python petprofile_input.py` on its own to preview this screen
    page.title = "PawPlan"
    page.window.width = 430
    page.window.height = 900
    page.views.append(petprofile_input_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(_standalone_main)