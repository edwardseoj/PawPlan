import os
import flet as ft
import logging
from flet.auth.providers import GoogleOAuthProvider

# note that this one would not work in the build app
# find an alternative
from dotenv import load_dotenv
from utility.navigation import go_to

logger = logging.getLogger(f"pawplan.{__name__}")

# get values from .env
load_dotenv()
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
    async def on_login(e: ft.LoginEvent):
        if e.error:
            logger.error("Login error: %s", e.error)
            return
        # debugging
        if(page.auth != None):
            logger.info("Logged in as: %s", page.auth.user["email"])
            await page.push_route("/homepage")

    return on_login





# STARTUP PAGE ("/")
def startup_view(page: ft.Page) -> ft.View:
    async def login_click(e):
        await page.login(provider)


    # ---------- Logo: paw icon in a cyan rounded square + "PawPlan" wordmark ----------
    paw_icon = ft.Container(
        content=ft.Icon(ft.Icons.PETS, size=48, color=ft.Colors.BLACK),
        width=90,
        height=90,
        bgcolor=ft.Colors.CYAN_200,
        border_radius=20,
        alignment=ft.Alignment.CENTER,
    )
    wordmark = ft.Row(
        [
            ft.Text("Paw", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
            ft.Text("Plan", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
        ],
        spacing=0,
    )
    logo_row = ft.Row(
        [paw_icon, wordmark],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )

    # ---------- Login / Sign Up buttons ----------
    login_btn = ft.Button(
        "Login",
        width=140,
        height=55,
        on_click=go_to(page, "/login"),
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_900,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
        ),
    )
    signup_btn = ft.Button(
        "Sign Up",
        width=140,
        height=55,
        on_click=go_to(page, "/register"),
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_500,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
        ),
    )
    button_row = ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # ---------- "Or Continue with" divider ----------
    divider = ft.Row(
        [
            ft.Container(content=ft.Divider(thickness=1), expand=True),
            ft.Text("Or Continue with", size=14, color=ft.Colors.GREY_600),
            ft.Container(content=ft.Divider(thickness=1), expand=True),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ---------- Google sign-in button ----------
    # Using a styled "G" instead of a remote image so this still renders offline.
    # Swap the ft.Text below for an ft.Image(src="google_logo.png", ...) if you
    # add a real Google "G" asset to your app's /assets folder.
    google_g = ft.Text("G", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
    google_btn = ft.OutlinedButton(
        content=ft.Row(
            [
                google_g,
                ft.Text("Sign in with Google", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        width=280,
        height=55,
        on_click=login_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.Colors.BLACK26),
            bgcolor=ft.Colors.WHITE,
        ),
    )

    # ---------- Bottom accent bars (blue over orange) ----------
    bottom_bars = ft.Column(
        [
            ft.Container(height=25, bgcolor=ft.Colors.BLUE_900, expand=True),
            ft.Container(height=25, bgcolor=ft.Colors.ORANGE, expand=True),
        ],
        spacing=0,
    )

    # call content
    return ft.View(
        route="/",
        bgcolor=ft.Colors.WHITE,
        padding=0,
        controls=[
            ft.Column(
                [
                    ft.Container(height=80),
                    logo_row,
                    ft.Container(height=40),
                    button_row,
                    ft.Container(height=30),
                    ft.Container(content=divider, width=340),
                    ft.Container(height=30),
                    google_btn,
                    ft.Container(expand=True),  # pushes the bottom bars down
                    bottom_bars,
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=0,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
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