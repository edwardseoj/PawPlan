    import email

import flet as ft
# config
import pyrebase
from certifi import contents
from flet.controls.core import placeholder

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)



def main(page: ft.Page):
    page.title = "PawPlan"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    paw_text = ft.Text("Paw", size=32, weight=ft.FontWeight.BOLD)
    plan_text = ft.Text("Plan", size=32, weight=ft.FontWeight.BOLD)
    title_row = ft.Row([paw_text, plan_text], alignment=ft.MainAxisAlignment.CENTER)

    login_btn = ft.Container(
        content=ft.ElevatedButton("Login"),
        width=200,
        height=50
    )
    signup_btn = ft.Container(
        content=ft.ElevatedButton("Sign Up"),
        width=200,
        height=50
    )
    button_row = ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    divider = ft.Column([
        ft.Divider(thickness=1),
        ft.Text("Or Continue with"),
        ft.Divider(thickness=1)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # page popup
    def close_google_dialog(e):
        page.close_dialog()

    google_dlg = ft.AlertDialog(
        title=ft.Text("Google Sign In"),
        content=ft.Column(
          controls=[
            ft.CupertinoTextField(
                placeholder_text="email",
            ),
            ft.CupertinoTextField(
                placeholder_text="password",
                password=True,
                can_reveal_password=True ),
          ],
        ),
        actions=[ft.TextButton("OK", on_click=lambda e: page.pop_dialog())],
    )

    google_btn = ft.Container(
        content=ft.Button("Sign in with Google", on_click=lambda e: page.show_dialog(google_dlg)),
        width=250,
        height=50
    )




    page.add(
        ft.Column([
            title_row,
            ft.Container(height=20),
            button_row,
            ft.Container(height=20),
            divider,
            ft.Container(height=20),
            google_btn
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
