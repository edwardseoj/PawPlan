import flet as ft
import logging
logger = logging.getLogger(__name__)

def petprofile_input_view(page: ft.Page) -> ft.View:
    async def go_homepage(e):
        logger.info("Go to pet profile clicked")
        try:
            await page.push_route("/homepage")
            logger.info("Route pushed")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

    # content variables
    pet_name = ft.TextField(label="Pet Name", width=300)
    pet_type = ft.Dropdown(
        label = "Pet Type",
        options=[
            ft.dropdown.Option("Dog"),
            ft.dropdown.Option("Cat"),
        ],
        width=300
    )
    pet_age = ft.TextField(label="Age", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)
    pet_breed = ft.TextField(label="Breed", width=300, text_align=ft.TextAlign.CENTER)
    submit_btn = ft.Button("Save Profile", on_click=go_homepage)


    return ft.View(
        # call here the contents
        route="/petprofile",
        controls=[
            ft.Column(

                controls=[
                    ft.Container(pet_name),
                    ft.Container(height=20),
                    ft.Container(pet_type),
                    ft.Container(height=20),
                    ft.Container(pet_age),
                    ft.Container(height=20),
                    ft.Container(pet_breed),
                    ft.Container(height=20),
                    ft.Container(submit_btn),
                ],

                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

# # to try running it as itself
# def _standalone_main(page: ft.Page):
#     page.title = "PawPlan"
#     page.window.width = 430
#     page.window.height = 900
#     page.views.append(petprofile_input_view(page))
#     page.update()
#
# if __name__ == "__main__":
#     ft.run(_standalone_main)
#
# def main(page: ft.Page):
#     page.title = "Pet Profile"
#     page.horizontal_alignment = ft.MainAxisAlignment.CENTER
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#
#     pet_name = ft.TextField(label="Pet Name", width=300, text_align=ft.TextAlign.CENTER)
#     pet_Type = ft.Dropdown(
#         label = "Pet Type",
#         options=[
#             ft.dropdown.Option("Dog"),
#             ft.dropdown.Option("Cat"),
#         ],
#         width=300
#     )
#     pet_age = ft.TextField(label="Age", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)
#     pet_breed = ft.TextField(label="Breed", width=300, text_align=ft.TextAlign.CENTER)
#
#     # alert dialog popup
#     def submit_profile(e):
#         page.dialog = ft.AlertDialog(
#             title = ft.Text("Pet Profile Saved"),
#             content=ft.Text(
#                 f"name: {pet_name.value}\n"
#                 f"Type: {pet_Type.value}\n"
#                 f"Age: {pet_age.value}\n"
#                 f"Breed: {pet_breed.value}"
#
#             ),
#             actions = [ft.TextButton("OK", on_click=lambda e: page.dialog.close())],
#         )
#         page.dialog.open = True
#         page.update()
#
#     # button that calls alert dialog
#     submit_btn = ft.ElevatedButton("Save Profile", on_click=submit_profile)
#
#     # call variables
#     page.add(
#         ft.Column(
#             controls=[pet_name, pet_Type, pet_age, pet_breed, submit_btn],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         )
#     )
#
# # comment this out later
# ft.app(target=main)
