import reflex as rx

def project_not_found() -> rx.Component:
    return rx.hstack(
            rx.heading("Project Not Found"),spacing="5",
            align="center",
            min_height="85vh")