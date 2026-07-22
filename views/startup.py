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
    async def on_login(e: ft.LoginEvent):
        if e.error:
            print("Login error:", e.error)
            return
        # debugging
        if(page.auth != None):
            print("Logged in as:", page.auth.user["email"])
            await page.push_route("/homepage")

    return on_login


# STARTUP PAGE ("/")
def startup_view(page: ft.Page) -> ft.View:
    async def login_click(e):
        await page.login(provider)


    # content variables
    # paw_text = ft.Text("Paw", size=32, weight=ft.FontWeight.BOLD)
    # plan_text = ft.Text("Plan", size=32, weight=ft.FontWeight.BOLD)
    # title_row = ft.Row([paw_text, plan_text], alignment=ft.MainAxisAlignment.CENTER)
    #
    # login_btn = ft.Button("Login", on_click=go_to(page, "/login"))
    # signup_btn = ft.Button("Sign Up", on_click=go_to(page, "/register"))
    # button_row = ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    #
    # divider = ft.Column(

    # ---------- Logo: paw icon in a cyan rounded square + "PawPlan" wordmark ----------

    paw_icon = ft.Image(
        src="pawplan_icon.png",
        height=130,
        width=130,
        fit=ft.BoxFit.CONTAIN,
    )


    wordmark = ft.Row(
        [
            ft.Text("Paw", size=38, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
            ft.Text("Plan", size=38, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
        ],
        spacing=0,
    )
    wordmark = ft.Container(
        content = wordmark,
        padding = ft.Padding.only(right = 40),
    )

    logo_row = ft.Row(
        [paw_icon, wordmark],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=1,
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
            side = {ft.ControlState.DEFAULT: ft.BorderSide(2, "#000000")},
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
            side = {ft.ControlState.DEFAULT: ft.BorderSide(2, "#000000")},
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
    # Swap the ft.Text below for a ft.Image(src="google_logo.png", ...) if you
    # add a real Google "G" asset to your app's /assets folder.

    google_logo = ft.Container(
        height = 20,
        width = 20,
        content = ft.Image(
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/3840px-Google_%22G%22_logo.svg.png",
            height = 18,
            width = 18,
            fit = ft.BoxFit.CONTAIN,
        ),
    )

    google_btn = ft.OutlinedButton(
        content=ft.Stack(
            [
                ft.Container(
                    content= google_logo,
                    alignment=ft.Alignment.CENTER_LEFT,
                    padding=ft.Padding.only(left=15),
                ),
                ft.Container(
                    content=ft.Text("Sign in with Google", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    alignment = ft.Alignment.CENTER,
                    padding = ft.Padding.only(left = 25),
                ),
            ],
            width = 280,
            height = 55,
        ),
        width=280,
        height=55,
        on_click=login_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side={ft.ControlState.DEFAULT: ft.BorderSide(1, "#000000")},
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