import calendar
import datetime

import flet as ft

# logger import
# use in push.route to see route changes
# will need to filter things though
# import logging


# logger = logging.getLogger(__name__)

# firestore setup
import firebase_admin
from firebase_admin import credentials, firestore

from utility.navigation import go_to

cred = credentials.Certificate("./pawplan_account.json")
firebase_admin.initialize_app(cred)
db = firestore.client(database_id="pawplan")


# Sample based on Mock Screens (will be updated later on)
TODAYS_TASKS = [
    {"time": "8:00 AM", "task": "Feed Bella"},
    {"time": "12:00 PM", "task": "Walk Max"},
    {"time": "6:00 PM", "task": "Give Bella Medication"},
]

UPCOMING_EVENT = "Upcoming Vet Visit for Bella - June 15"

DESTINATIONS = [
    ft.NavigationBarDestination(
        icon =  ft.Icons.WIDGETS_OUTLINED,
        selected_icon = ft.Icons.HOUSE,
        label = "Home"
    ),
    ft.NavigationBarDestination(
        icon = ft.Icons.WIDGETS_OUTLINED,
        selected_icon = ft.Icons.CALENDAR_MONTH,
        label = "Calendar"
    ),
    ft.NavigationBarDestination(
        icon = ft.Icons.WIDGETS_OUTLINED,
        selected_icon = ft.Icons.PERSON,
        label = "Profile"
    ),
]

LOGO_SIZE = 70

NAV_SHRINK_SCALE = 0.6



def homepage_view(page: ft.Page) -> ft.View:

    # def view_reminder(pet_name):
    #     def handler(e):
    #         logger.info(f"View reminder clicked for {pet_name}")
    #     return handler

    # no navigation here yet
    def go_settings(e):
        # logger.info("Settings nav clicked")
        print("Settings nav clicked")

    nav_routes = ["/homepage", "/calendar", "/account_profile"]

    primary = "#0D6EFD"
    header_blue = "#1450B4"
    orange = "#F5821F"
    soft_border = "#DDE3EE"
    white = "#FFFFFF"
    black = "#000000"
    green = "#4CAF50"
    nav_blue = "#0B4FB0"
    calendar_header_blue = "#2F6FCB"
    weekend_blue = "#3B6FD6"


    appbar = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
        bgcolor=white,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[

                        ft.Container(
                            width=LOGO_SIZE,
                            height=LOGO_SIZE,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Image(
                                src="pawplan_icon.png",
                                width=LOGO_SIZE,
                                height=LOGO_SIZE,
                                fit=ft.BoxFit.CONTAIN,
                            ),
                        ),

                        ft.Row(
                            spacing=2,
                            controls=[
                                ft.Text("Paw", size=22, weight=ft.FontWeight.W_800, color=orange),
                                ft.Text("Plan", size=22, weight=ft.FontWeight.W_800, color="#0B2E6B"),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.NOTIFICATIONS_NONE, color=black, size=26),
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color=black,
                            items=[
                                ft.PopupMenuItem(
                                    content = ft.Text("Settings"),
                                    icon=ft.Icons.SETTINGS_OUTLINED,
                                    on_click=go_settings,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


    appbar_divider = ft.Container(height=5, bgcolor=orange)



    # pet list
    # make dynamic later


    # firestore code
    current_user_id = "John Doe"
    pets_ref = db.collection("users").document(current_user_id).collection("details").document("pets")

    # get data
    doc = pets_ref.get()
    if doc.exists:
        data = doc.to_dict()
        pet_list = data.get("pets", [])
        print(pet_list)
    else:
        print("No such document!")



    def pet_card(index):
        # get the name per index
        pet_name = pet_list[index]["name"]

        return ft.Container(
            width=110,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[

                    ft.Text(pet_name, color=white, size=15, weight=ft.FontWeight.W_700),
                    ft.Container(
                        width=90,
                        height=90,
                        bgcolor="#F1D9B0",
                        border_radius=10,
                        border=ft.Border.all(2, white),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(ft.Icons.PETS, size=40, color="#8A6A3B"),
                    ),
                    ft.Button(
                        content=ft.Text("View Reminder", size=8, color=white),
                        bgcolor=green,
                        # on_click=view_reminder(pet["name"]),
                    ),
                ],
            ),
        )

    header = ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=16),
        bgcolor=header_blue,
        content=ft.Column(
            spacing=16,
            controls=[

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Hello, John",
                            color=white,
                            size=24,
                            weight=ft.FontWeight.W_800,
                        ),
                        ft.Button(
                            content=ft.Row(
                                spacing=6,
                                tight=True,
                                controls=[
                                    ft.Text("Add Pet", color=primary, weight=ft.FontWeight.W_700),
                                    ft.Icon(ft.Icons.ARROW_CIRCLE_RIGHT, color=primary, size=18),
                                ],
                            ),
                            bgcolor=white,
                            on_click=go_to(page, "/petprofile"),
                        ),
                    ],
                ),
                ft.Row(
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO,

                    # pet_card gets added per pet in the pet_list
                    controls=[pet_card(index) for index, pet in enumerate(pet_list)],
                ),
            ],
        ),
    )

    # Added Calendar (should have backend functions for vet scheduled visits)
    today = datetime.date.today()
    calendar_year, calendar_month = today.year, today.month
    calendar.setfirstweekday(calendar.SUNDAY)
    weeks = calendar.monthcalendar(calendar_year, calendar_month)
    month_label = f"{calendar.month_name[calendar_month].upper()} {calendar_year}"

    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

    def day_cell(day, col_index):
        weekend = col_index == 0 or col_index == 6
        todays = day == today.day
        text_color = weekend_blue if weekend else "#1F2937"
        if day == 0:
            return ft.Container(expand=1, height=30)
        return ft.Container(
            expand=1,
            height=30,
            border_radius=6,
            bgcolor=primary if todays else None,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                str(day),
                size=11,
                color=white if todays else text_color,
                weight=ft.FontWeight.W_700 if todays else ft.FontWeight.W_400,
            ),
        )

    calendar_rows = [
        ft.Row(
            spacing=2,
            controls=[day_cell(d, i) for i, d in enumerate(week)],
        )
        for week in weeks
    ]

    calendar_widget = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=14),
        bgcolor=white,
        border_radius=10,
        border=ft.Border.all(1, soft_border),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Column(
            spacing=6,
            controls=[

                ft.Container(
                    padding=ft.Padding.symmetric(vertical=8),
                    bgcolor=calendar_header_blue,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        month_label, size=12, weight=ft.FontWeight.W_700, color=white
                    ),
                ),

                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=8),
                    content=ft.Row(
                        spacing=2,
                        controls=[
                            ft.Container(
                                expand=1,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text(
                                    label, size=9, weight=ft.FontWeight.W_700, color="#6B7280"
                                ),
                            )
                            for label in weekday_labels
                        ],
                    ),
                ),
                ft.Container(

                    padding=ft.Padding.only(left=8, right=8, bottom=10),
                    content=ft.Column(spacing=4, controls=calendar_rows),
                ),
            ],
        ),
    )





    # Today's Tasks (for backends this needs to be connected to reminder page)

    def task_row(item):
        return ft.Container(
            border=ft.Border.all(1, soft_border),
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            content=ft.Text(
                f"{item['time']} - {item['task']}",
                size=15,
                weight=ft.FontWeight.W_600,
                color=black,
            ),
        )


    tasks_section = ft.Container(
        margin=ft.Margin.only(left=16, right=16, top=16),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text(
                    "Today's Task",
                    size=20,
                    weight=ft.FontWeight.W_700,
                    color=black,
                ),

                *[task_row(item) for item in TODAYS_TASKS],
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=14, vertical=12),
                    border=ft.Border.all(1, soft_border),
                    border_radius=8,
                    content=ft.Text(
                        UPCOMING_EVENT,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=black,
                    ),
                ),
            ],
        ),
    )

    # Navigation Bar (turned into a pill)

    def pill_destination(index, label, icon):
        async def handle_nav_click(e):
            print(nav_routes[index])
            str = nav_routes[index]
            await page.push_route(str)
            restore_nav(e)

        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border_radius=20,
            on_click=handle_nav_click,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing = 2,
                tight=True,
                controls=[
                    ft.Icon(icon, color=white, size=20),
                    ft.Text(label, size=11, color=white, weight=ft.FontWeight.W_600),
                ],
            ),
        )

    floating_nav = ft.Container(
        bgcolor=nav_blue,
        border_radius=32,
        padding=ft.Padding.symmetric(horizontal=18, vertical=10),
        scale=1.0,
        animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        shadow=ft.BoxShadow(
            blur_radius=16,
            spread_radius=1,
            color="#00000055",
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            tight=True,
            controls=[
                pill_destination(i, dest.label, dest.selected_icon)

                for i, dest in enumerate(DESTINATIONS)
            ],
        ),
    )

    def shrink_nav():
        if floating_nav.scale != NAV_SHRINK_SCALE:
            floating_nav.scale = NAV_SHRINK_SCALE
            floating_nav.update()

    def restore_nav(e=None):
        if floating_nav.scale != 1.0:
            floating_nav.scale = 1.0
            floating_nav.update()

    floating_nav.on_click = restore_nav

    def handle_content_scroll(e: ft.OnScrollEvent):
        if e.event_type == ft.ScrollType.USER:
            shrink_nav()

    main_content = ft.Column(
        spacing = 0,
        expand = True,
        scroll = ft.ScrollMode.AUTO,
        on_scroll = handle_content_scroll,

        controls = [
            appbar,
            appbar_divider,
            header,
            calendar_widget,
            tasks_section,
            ft.Container(height=100),
        ],
    )

    return ft.View(
        route="/homepage",
        bgcolor="#FFFFFF",
        padding=0,
        spacing=0,
        controls=[
            ft.Stack(
                expand = True,
                controls = [
                    main_content,
                    ft.Container(
                        align = ft.Alignment.BOTTOM_CENTER,
                        expand = True,
                        content = floating_nav,
                        padding = ft.Padding.only(bottom = 20),
                    ),

                ],
            )
        ],
    )


def _standalone_main(page: ft.Page):
    # Lets you run `python homepage.py` on its own to preview this screen
    page.title = "PawPlan"
    page.window.width = 430
    page.window.height = 900
    page.views.append(homepage_view(page))
    page.update()


if __name__ == "__main__":
    ft.run(_standalone_main, assets_dir="assets")