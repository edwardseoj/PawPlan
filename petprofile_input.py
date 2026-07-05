import flet as ft

def main(page: ft.Page):
    page.title = "Pet Profile"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    pet_name = ft.TextField(label="Pet Name", width=300, text_align=ft.TextAlign.CENTER)
    pet_Type = ft.Dropdown(
        label = "Pet Type",
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Yellow"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("White"),
        ],
        width=300
    )
    pet_age = ft.TextField(label="Age", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)
    pet_breed = ft.TextField(label="Breed", width=300, text_align=ft.TextAlign.CENTER)

    def submit_profile(e):
        page.dialog = ft.AlertDialog(
            title = ft.Text("Pet Profile Saved"),
            content=ft.Text(
                f"name: {pet_name.value}\n"
                f"Type: {pet_Type.value}\n"
                f"Age: {pet_age.value}\n"
                f"Breed: {pet_breed.value}"

            ),
            actions = [ft.TextButton("OK", on_click=lambda e: page.dialog.close())],
        )
        page.dialog.open = True
        page.update()

    submit_btn = ft.ElevatedButton("Save Profile", on_click=submit_profile)

    page.add(
        ft.Column(
            controls=[pet_name, pet_Type, pet_age, pet_breed, submit_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
ft.app(target=main)
