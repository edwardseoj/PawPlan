import logging
import flet as ft
import time

logger = logging.getLogger(__name__)

# for push route with no extra conditions
def go_to(page: ft.Page, route: str, on_after=None):
    async def handler(e):
        try:
            t0 = time.perf_counter()
            await page.push_route(route)
            t1 = time.perf_counter()
            logger.debug(f"push_route to {route!r} took {t1-t0:.4f}s")
        except Exception as ex:
            logger.error(f"Navigation to {route} failed: {ex}")
        if on_after:
            try:
                on_after(e)
            except Exception as ex:
                logger.exception("on_after callback failed: %s", ex)
    return handler