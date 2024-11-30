import reflex as rx 

def dashboard_component() -> rx.Component:
    return rx.box(
        rx.heading("Welcome back", size='2'),
        rx.divider(margin_top='1em', margin_bottom='1em'),
        min_height="85vh",
    )