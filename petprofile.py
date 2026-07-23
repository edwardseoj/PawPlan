import flet as ft
from typing import List, Dict, Callable, Optional
from dataclasses import dataclass
from enum import Enum


class TabType(Enum):
    REMINDERS = 0
    VET_RECORDS = 1


@dataclass
class Reminder:
    title: str
    date: str
    location: str
    checked: bool = False


@dataclass
class VetRecord:
    title: str
    description: str
    doctor: str


class PetProfileApp:
    def __init__(self):
        # Theme colors
        self.colors = {
            "primary": "#0D6EFD",
            "primary_dark": "#0B4FB0",
            "primary_light": "#1E6FC4",
            "secondary": "#ff751f",
            "white": "#FFFFFF",
            "white38": "#FFFFFF66",
            "soft_border": "#DDE3EE",
            "text_primary": "#000000",
            "text_secondary": "#666666",
        }

        # Data
        self.reminders: List[Reminder] = [
            Reminder("Vet Check-up", "August 15, 2026 at 10:00 AM", "Lebron Veterinary Hospital"),
            Reminder("Vaccine Booster", "Aug 18, 2026 at 2:30 PM", "Lebron Veterinary Hospital"),
            Reminder("Grooming Session", "Aug 25, 2026 at 9:00 AM", "Jalen & Wemby Grooming"),
        ]

        self.vet_records: List[VetRecord] = [
            VetRecord("Checkup - July 2026", "Bill Gates Microchips", "Dr. Johnny Sins"),
            VetRecord("Dental Cleaning - June 2026", "Teeth cleaned", "Dr. Michael Hacksyon"),
            VetRecord("Rabies Vaccination - May 2026", "Rabies shot administered", "Dr. Robin Da Bank"),
        ]

        self.selected_tab = TabType.REMINDERS
        self.tab_content_container = None
        self.tab_buttons = {}

    def build(self, page: ft.Page):
        page.title = "PawPlan"
        page.bgcolor = self.colors["white"]
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.scroll = None
        page.padding = 0

        # Build UI
        page.add(
            ft.Column(
                spacing=0,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self._build_main_content(),
                    self._build_bottom_nav(),
                ],
            )
        )

    def _build_main_content(self):
        return ft.Container(
            expand=True,
            margin=ft.Margin.all(0),
            padding=ft.Padding.all(0),
            content=ft.Column(
                controls=[
                    self._build_title(),
                    self._build_profile_image(),
                    self._build_tab_buttons(),
                    self._build_tab_content(),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
                tight=True,
                expand=True,
            ),
        )

    def _build_title(self):
        return ft.Container(
            expand=True,
            bgcolor=self.colors["secondary"],
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.only(left=16, right=16, top=10),
            content=ft.Text(
                "Pet Profile",
                size=22,
                weight=ft.FontWeight.W_700,
                color=self.colors["white"],
            ),
        )

    def _build_profile_image(self):
        return ft.Container(
            bgcolor=self.colors["primary_dark"],
            expand=True,
            alignment=ft.Alignment.CENTER,
            margin=ft.Margin.all(0),
            padding=ft.Padding.all(0),
            content=ft.Row(
                controls=[
                    ft.Image(
                        src="https://example.com/this-image-does-not-exist.png",
                        width=200,
                        height=200,
                        error_content=ft.Container(
                            content=ft.Icon(ft.Icons.BROKEN_IMAGE, size=200, color=ft.Colors.GREY_400),
                            alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.GREY_200,
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def _build_tab_buttons(self):
        # Create button references
        reminders_btn = ft.Container(
            content=ft.Text("Reminders", color=ft.Colors.WHITE, weight=ft.FontWeight.W_700),
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            border_radius=20,
            bgcolor=self.colors["primary_light"],
        )

        vet_records_btn = ft.Container(
            content=ft.Text("Vet Records", color=ft.Colors.WHITE, weight=ft.FontWeight.W_700),
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            border_radius=20,
            bgcolor="transparent",
        )

        self.tab_buttons = {
            TabType.REMINDERS: reminders_btn,
            TabType.VET_RECORDS: vet_records_btn,
        }

        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            bgcolor=self.colors["primary_dark"],
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.GestureDetector(
                        content=reminders_btn,
                        on_tap=self._on_tab_click(TabType.REMINDERS),
                    ),
                    ft.GestureDetector(
                        content=vet_records_btn,
                        on_tap=self._on_tab_click(TabType.VET_RECORDS),
                    ),
                ],
            ),
        )

    def _build_tab_content(self):
        self.tab_content_container = ft.Container(
            expand=True,
            bgcolor=self.colors["white"],
            content=self._build_reminders_content(),
        )
        return self.tab_content_container

    def _on_tab_click(self, tab_type: TabType):
        def handler(e):
            self.selected_tab = tab_type

            # Update button styles
            for tab, button in self.tab_buttons.items():
                button.bgcolor = self.colors["primary_light"] if tab == tab_type else "transparent"

            # Update content
            if tab_type == TabType.REMINDERS:
                self.tab_content_container.content = self._build_reminders_content()
            else:
                self.tab_content_container.content = self._build_vet_records_content()

            self.tab_content_container.page.update()

        return handler

    def _build_reminders_content(self):
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor=self.colors["white"],
            padding=ft.Padding.all(20),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=400,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            controls=[
                                self._create_reminder_card(reminder, index)
                                for index, reminder in enumerate(self.reminders)
                            ],
                            spacing=12,
                        ),
                    ),
                ],
                spacing=15,
            ),
        )

    def _build_vet_records_content(self):
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor=self.colors["white"],
            padding=ft.Padding.all(20),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=400,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            controls=[
                                self._create_vet_record_card(record)
                                for record in self.vet_records
                            ],
                            spacing=12,
                        ),
                    ),
                ],
                spacing=15,
            ),
        )

    def _create_bordered_card(self, content):
        """Helper function to create bordered card"""
        return ft.Container(
            border=ft.Border.all(2, self.colors["primary"]),
            border_radius=10,
            bgcolor="transparent",
            padding=15,
            content=content,
        )

    def _create_reminder_card(self, reminder: Reminder, index: int):
        """Create a reminder card with checkbox"""
        checkbox_container = ft.Container(
            width=24,
            height=24,
            border=ft.Border.all(2, self.colors["primary"]),
            border_radius=6,
            bgcolor="transparent",
            content=ft.Icon(ft.Icons.CHECK, size=16, color=self.colors["primary"]) if reminder.checked else None,
            alignment=ft.Alignment.CENTER,
        )

        def toggle_checkbox(e):
            reminder.checked = not reminder.checked
            checkbox_container.content = (
                ft.Icon(ft.Icons.CHECK, size=16, color=self.colors["primary"])
                if reminder.checked else None
            )
            self.tab_content_container.page.update()

        return self._create_bordered_card(
            ft.Row(
                controls=[
                    ft.GestureDetector(
                        content=checkbox_container,
                        on_tap=toggle_checkbox,
                    ),
                    ft.Column(
                        spacing=3,
                        expand=True,
                        controls=[
                            ft.Text(reminder.title, size=16, weight=ft.FontWeight.W_600,
                                    color=self.colors["text_primary"]),
                            ft.Text(reminder.date, size=13, color=self.colors["text_secondary"]),
                            ft.Text(reminder.location, size=13, color=self.colors["text_secondary"]),
                        ],
                    ),
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def _create_vet_record_card(self, record: VetRecord):
        """Create a vet record card"""
        return self._create_bordered_card(
            ft.Column(
                spacing=3,
                controls=[
                    ft.Text(record.title, size=16, weight=ft.FontWeight.W_600, color=self.colors["text_primary"]),
                    ft.Text(record.description, size=13, color=self.colors["text_secondary"]),
                    ft.Text(record.doctor, size=13, color=self.colors["text_secondary"]),
                ],
            )
        )

    def _build_bottom_nav(self):
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=20, vertical=20),
            bgcolor=self.colors["primary_dark"],
            border_radius=ft.BorderRadius.only(top_left=20, top_right=20),
            margin=ft.Margin.all(0),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    self._create_nav_button("Home"),
                    self._create_nav_button("Calendar"),
                    self._create_nav_button("Profile"),
                ],
            ),
        )

    def _create_nav_button(self, label: str):
        """Create a navigation button with placeholder action"""
        return ft.TextButton(
            label,
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
            on_click=lambda e: print(f"Navigated to {label}"),
        )


def main(page: ft.Page):
    app = PetProfileApp()
    app.build(page)


if __name__ == "__main__":
    ft.run(main)