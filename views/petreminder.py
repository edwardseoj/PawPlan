import flet as ft
import logging

from google.cloud.firestore_v1 import FieldFilter
from model.firebase_setup import db
from model.firestore_auth import get_uid

logger = logging.getLogger(__name__)
# === COPILOT NOTE ===
# Changed by Copilot: Reminder list is loaded asynchronously in a
# background thread so the view renders immediately. This prevents
# blocking during navigation when Firestore I/O is performed.
# === END NOTE ===


def petreminder_view(page: ft.Page) -> ft.View:

    primary = "#0D6EFD"
    soft_border = "#DDE3EE"
    white = "#FFFFFF"
    white38 = "#FFFFFF66"


    async def go_home(e):
        logger.info("Home nav clicked")
        try:
            await page.push_route("/homepage")
            logger.info("Route pushed")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

    async def go_calendar(e):
        logger.info("Calendar nav clicked")
        try:
            await page.push_route("/calendar")
            logger.info("Route pushed")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

    async def go_profile(e):
        logger.info("Profile nav clicked")
        try:
            await page.push_route("/profile")
            logger.info("Route pushed")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

    # header
    appbar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#FFFFFF",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("PawPlan", size=20, weight=ft.FontWeight.W_700, color="#000000"),
            ]
        ),
    )

    # page title
    title = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=10),
        content=ft.Text(
            "Today's Tasks",
            size=22,
            weight=ft.FontWeight.W_700,
            color="Black",
        ),
    )

    def create_alarm(e):

        def delete_alarm(e):
            alarm_list_layout.controls.remove(alarm_unit)
            page.update()

        alarm_unit = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=10, bottom=10),
            border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
            padding=15,
            width=float("inf"),
            content=ft.Text("New Reminder")
        )
        alarm_list_layout.controls.append(alarm_unit)
        page.update()


    import threading

    # temporary code
    # change all later
    pet_name = "ben" # temporary, change later
    reminder_list = []

    def create_reminder_control(reminder_name):
        def delete_alarm(e):
            alarm_list_layout.controls.remove(alarm_unit)
            page.update()

        alarm_unit = ft.Container(
            margin=ft.Margin.only(left=20, right=20, top=10, bottom=10),
            border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
            padding=15,
            width=float("inf"),
            content=ft.Text(reminder_name)
        )
        return alarm_unit

    alarm_list_layout = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        controls=[ft.Text("Loading reminders...")]
    )

    def _fetch_reminders():
        try:
            current_user_id = get_uid()  # Get the current user's email
            reminder_ref = (
                db.collection("users").document(current_user_id).collection("details").document("pets").collection("reminders").
                where(filter=FieldFilter("pet", "==", pet_name))
                .stream()
            )
            reminders = []
            for reminder in reminder_ref:
                data = reminder.to_dict()
                reminders.append(data.get("name", ""))

            reminder_list[:] = reminders
            if reminders:
                alarm_list_layout.controls[:] = [create_reminder_control(r) for r in reminders]
            else:
                alarm_list_layout.controls[:] = [ft.Text("No reminders")]
            page.update()
        except Exception as ex:
            logger.exception("Failed fetching reminders: %s", ex)
            alarm_list_layout.controls[:] = [ft.Text("Failed to load reminders")]
            page.update()

    threading.Thread(target=_fetch_reminders, daemon=True).start()


    # reminder container
    alarm_cont = ft.Container(
        margin=ft.Margin.only(top=15, bottom=5),
        expand=True,
        border=ft.Border.all(width=2.5, color=ft.Colors.GREY_400),
        border_radius=10,
        content=alarm_list_layout  # Inject the list layout here
    )

    # add button
    add_button = ft.Container(
        margin=ft.Margin.only(top=5, bottom=20),
        align=ft.Alignment.CENTER,
        content=ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="white",
            bgcolor="#0B4FB0",
            icon_size=24,
            tooltip="Add reminder",
            on_click=create_alarm,
        )
    )

    # navbar
    bottom_nav = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=20),
        bgcolor="#0B4FB0",
        border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.TextButton(
                    "Home", style=ft.ButtonStyle(color=white), on_click=go_home
                ),
                ft.TextButton(
                    "Calendar",
                    style=ft.ButtonStyle(color=white),
                    on_click=go_calendar,
                ),
                ft.TextButton(
                    "Profile",
                    style=ft.ButtonStyle(color=white),
                    on_click=go_profile,
                ),
            ],
        ),
    )

    return ft.View(
        route="/petreminder",
        controls=[
            ft.Column(
                spacing=0,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    appbar,
                    title,
                    alarm_cont,
                    add_button,
                    bottom_nav,
                ],
            )
        ],
    )