import flet as ft
import logging
logger = logging.getLogger(__name__)

# firestore setup
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("pawplan_account.json")
db = firestore.client(database_id="pawplan")

# change this part later
current_user_id = "John Doe"

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


    # firestore code
    pets_ref = db.collection("users").document(current_user_id).collection("details").document("pets")

    # normla functions can't call asynch functions
    async def add_pet(e):
        pets_ref.set({
            "pets": firestore.ArrayUnion([{
                "name": pet_name.value,
                "type": pet_type.value,
                "age": pet_age.value,
                "breed": pet_breed.value
            }])
        }, merge=True)


        await go_homepage(e)

    # change this later
    submit_btn = ft.Button("Save Profile", on_click=add_pet)



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

