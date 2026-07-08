import flet as ft
from views.loginregister import startup_view, login_view, register_view, make_on_login
from views.homepage import homepage_view
from views.petprofile_input import petprofile_input_view\

# logger setup
from utility.logging_config import setup_logging
setup_logging()

def main(page: ft.Page):
    page.title = "PawPlan"
    page.on_login = make_on_login(page)

    def route_change(e):
        page.views.clear()

        # loginregister
        if page.route == "/":
            page.views.append(startup_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))

        elif page.route == "/homepage":
            page.views.append(homepage_view(page))

        elif page.route == "/petprofile":
            page.views.append(petprofile_input_view(page))

        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)


ft.run(main, port=8550, view=ft.AppView.WEB_BROWSER)