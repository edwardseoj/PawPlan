import os
import flet as ft
from flet.auth.providers import GoogleOAuthProvider

# note that this one would not work in the build app
# find an alternative
from dotenv import load_dotenv

from utility.navigation import go_to

load_dotenv()

# get values from .env
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

# error checking
if not client_id or not client_secret:
    raise ValueError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env file")


# auth code
provider = GoogleOAuthProvider(
    client_id=client_id,
    client_secret=client_secret,
    redirect_url="http://localhost:8550/oauth_callback",
)


def make_on_login(page: ft.Page):
    def on_login(e: ft.LoginEvent):
        if e.error:
            print("Login error:", e.error)
            return
        print("Logged in as:", page.auth.user["email"])
    return on_login


# STARTUP PAGE ("/")
def startup_view(page: ft.Page) -> ft.View:
    async def login_click(e):
        await page.login(provider)

    async def go_login(e):
        await page.push_route("/login")

    async def go_register(e):
        await page.push_route("/register")

    # content variables
    paw_text = ft.Text("Paw", size=32, weight=ft.FontWeight.BOLD)
    plan_text = ft.Text("Plan", size=32, weight=ft.FontWeight.BOLD)
    title_row = ft.Row([paw_text, plan_text], alignment=ft.MainAxisAlignment.CENTER)

    login_btn = ft.Button("Login", on_click=go_login)
    signup_btn = ft.Button("Sign Up", on_click=go_register)
    button_row = ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    divider = ft.Column(
        [
            ft.Divider(thickness=1),
            ft.Text("Or Continue with"),
            ft.Divider(thickness=1),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    google_btn = ft.Button("Sign in with Google", width=250, on_click=login_click)

    # call content
    return ft.View(
        route="/",
        controls=[
            ft.Column(
                [
                    title_row,
                    ft.Container(height=20),
                    button_row,
                    ft.Container(height=20),
                    divider,
                    ft.Container(height=20),
                    google_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# LOGIN SCREEN ("/login")
def login_view(page: ft.Page) -> ft.View:

    # content variables
    back_btn = ft.TextButton("Back", on_click=go_to(page, "/"))
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, width=300)
    login_btn = ft.Button("Log In", width=150, on_click=go_to(page, "/homepage"))
    register_link = ft.TextButton("Not registered yet?", on_click=go_to(page, "/register"))

    # call content
    return ft.View(
        route="/login",
        controls=[
            ft.Column(
                [
                    ft.Row([back_btn], alignment=ft.MainAxisAlignment.START),
                    ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
                    username,
                    password,
                    register_link,
                    login_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# REGISTER SCREEN ("/register")
def register_view(page: ft.Page) -> ft.View:
    async def go_root(e):
        await page.push_route("/")

    async def go_login(e):
        await page.push_route("/login")

    async def do_register(e):
        await page.push_route("/homepage")

    # content variables
    back_btn = ft.TextButton("Back", on_click=go_root)
    username = ft.TextField(label="Username", width=300)
    fullname = ft.TextField(label="Full Name", width=300)
    gender = ft.Row(
        [
            ft.Row([back_btn], alignment=ft.MainAxisAlignment.START),
            ft.Text("Gender:"),
            ft.Button("Male", width=80),
            ft.Button("Female", width=80),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    dob = ft.Row(
        [
            ft.TextField(label="MM", width=70),
            ft.TextField(label="DD", width=70),
            ft.TextField(label="YYYY", width=100),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    password = ft.TextField(label="Password", password=True, width=300)
    create_btn = ft.Button("Create Account", width=180, on_click=do_register)
    back_to_login_btn = ft.TextButton("Back to Login", on_click=go_login)

    # call content
    return ft.View(
        route="/register",
        controls=[
            ft.Column(
                [
                    ft.Text("Register", size=24, weight=ft.FontWeight.BOLD),
                    username,
                    fullname,
                    gender,
                    ft.Text("Date of birth:"),
                    dob,
                    password,
                    create_btn,
                    back_to_login_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
