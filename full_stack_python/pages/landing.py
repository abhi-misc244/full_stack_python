import reflex as rx 

from .. import navigation


def landing_component() -> rx.Component:
    return rx.vstack(
            # rx.theme_panel(default_open=True),
            rx.heading("Welcome to Abhishek's Website", size="9"),
            rx.link(
                rx.button("About us", color_scheme='gray'), 
                href=navigation.routes.ABOUT_US_ROUTE
            ),
            rx.divider(),
            rx.heading("Recent Projects", size="5"),
            spacing="5",
            justify="center",
            align="center",
            # text_align="center",
            min_height="85vh",
            id='my-child'
        )