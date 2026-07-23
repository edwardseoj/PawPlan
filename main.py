import flet as ft
import time

# logger setup
from utility.logging_config import setup_logging
from views.petreminder import petreminder_view
from views.settings import settings_view

setup_logging()
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from views.account_profile import account_profile_view
from views.startup import startup_view, make_on_login
from views.login import login_view
from views.register import register_view
from views.homepage import homepage_view
from views.petprofile_input import petprofile_input_view


def main(page: ft.Page):
    page.title = "PawPlan"
    page.window.height = 900
    page.window.width = 430
    page.window.resizable = False
    page.on_login = make_on_login(page)

    # originally a big chunk of elifs
    # add here new routes
    ROUTES = {
        "/": startup_view,
        "/login": login_view,
        "/register": register_view,
        "/homepage": homepage_view,
        "/petprofile": petprofile_input_view,
        "/account_profile": account_profile_view,
        "/petreminder": petreminder_view,
        "/settings": settings_view
    }

    def route_change(e):
        start_total = time.perf_counter()
        page.views.clear()
        view_builder = ROUTES.get(page.route)

        if view_builder is None:
            view_builder = ROUTES["/homepage"] # default route

        build_start = time.perf_counter()
        page.views.append(view_builder(page))
        build_end = time.perf_counter()

        update_start = time.perf_counter()
        page.update()
        update_end = time.perf_counter()

        total_end = time.perf_counter()
        logger.debug(f"Route change to {page.route!r}: build={build_end-build_start:.4f}s update={update_end-update_start:.4f}s total={total_end-start_total:.4f}s")

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
            if page.views:
                top_view = page.views[-1]
                t0 = time.perf_counter()
                await page.push_route(top_view.route)
                t1 = time.perf_counter()
                logger.debug(f"push_route to {top_view.route!r} took {t1-t0:.4f}s (view_pop)")
            else:
                t0 = time.perf_counter()
                await page.push_route("/homepage")
                t1 = time.perf_counter()
                logger.debug(f"push_route to '/homepage' took {t1-t0:.4f}s (view_pop)")
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(None)


ft.run(main, port=8550, view=ft.AppView.WEB_BROWSER)