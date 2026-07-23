import logging
import flet as ft

logger = logging.getLogger(__name__)

# for push route with no extra conditions
def go_to(page: ft.Page, route: str, on_after=None):
    async def handler(e):
        try:
            await page.push_route(route)
        except Exception as ex:
            logger.error(f"Navigation to {route} failed: {ex}")
        if on_after:
            on_after(e)
    return handler